#!/usr/bin/env python3
"""Enrich raw V2 wallet OrderFilled JSONL with official Polymarket metadata.

Input is the JSONL emitted by sqd_v2_wallet_orders.py. For each unique token:

1. CLOB /markets-by-token resolves condition + canonical Yes/No token IDs.
2. Gamma /markets?condition_ids=... resolves human market/event metadata.
3. CLOB /clob-markets/{condition_id} resolves current CLOB token labels and
   fee/tick parameters.

The three token-side representations are cross-checked. Raw trade fields are
never modified; metadata is added under the top-level ``market`` key.

No third-party dependencies.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Iterable

CLOB_BASE = "https://clob.polymarket.com"
GAMMA_BASE = "https://gamma-api.polymarket.com"
USER_AGENT = "polymarket-weather-enrich-v2-wallet-orders/1.0"


def request_json(url: str, *, timeout: float, retries: int = 5) -> Any:
    req = urllib.request.Request(
        url,
        headers={"Accept": "application/json", "User-Agent": USER_AGENT},
        method="GET",
    )
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                return json.load(response)
        except urllib.error.HTTPError as exc:
            if exc.code not in (429, 500, 502, 503, 504) or attempt >= retries:
                detail = exc.read().decode("utf-8", errors="replace")
                raise RuntimeError(f"HTTP {exc.code} for {url}: {detail[:500]}") from exc
            retry_after = exc.headers.get("Retry-After")
            try:
                delay = float(retry_after) if retry_after else min(2**attempt, 10)
            except ValueError:
                delay = min(2**attempt, 10)
            time.sleep(delay)
        except urllib.error.URLError:
            if attempt >= retries:
                raise
            time.sleep(min(2**attempt, 10))
    raise RuntimeError(f"unreachable retry loop for {url}")


def parse_jsonish(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    if isinstance(value, str):
        value = value.strip()
        if not value:
            return []
        try:
            decoded = json.loads(value)
        except json.JSONDecodeError:
            return [value]
        return decoded if isinstance(decoded, list) else [decoded]
    return [value]


def compact_event(event: dict[str, Any]) -> dict[str, Any]:
    tags = event.get("tags") or []
    return {
        "id": event.get("id"),
        "slug": event.get("slug"),
        "title": event.get("title"),
        "category": event.get("category"),
        "subcategory": event.get("subcategory"),
        "resolution_source": event.get("resolutionSource"),
        "start_date": event.get("startDate"),
        "end_date": event.get("endDate"),
        "neg_risk": event.get("negRisk"),
        "neg_risk_market_id": event.get("negRiskMarketID"),
        "neg_risk_fee_bips": event.get("negRiskFeeBips"),
        "enable_neg_risk": event.get("enableNegRisk"),
        "series_slug": event.get("seriesSlug"),
        "tags": [
            {
                "id": tag.get("id"),
                "label": tag.get("label"),
                "slug": tag.get("slug"),
            }
            for tag in tags
            if isinstance(tag, dict)
        ],
    }


def weather_evidence(market: dict[str, Any], event: dict[str, Any] | None) -> list[str]:
    evidence: list[str] = []
    values = [
        ("market.category", market.get("category")),
        ("event.category", event.get("category") if event else None),
        ("event.subcategory", event.get("subcategory") if event else None),
        ("event.seriesSlug", event.get("seriesSlug") if event else None),
    ]
    for label, value in values:
        if value and "weather" in str(value).lower():
            evidence.append(f"{label}={value}")
    if event:
        for tag in event.get("tags") or []:
            if not isinstance(tag, dict):
                continue
            label = str(tag.get("label") or "")
            slug = str(tag.get("slug") or "")
            if "weather" in label.lower() or "weather" in slug.lower():
                evidence.append(f"event.tag={slug or label}")
    return evidence


def select_gamma_market(markets: Any, condition_id: str) -> dict[str, Any]:
    if not isinstance(markets, list):
        raise RuntimeError(f"Gamma response is not a list for {condition_id}")
    exact = [
        market
        for market in markets
        if isinstance(market, dict)
        and str(market.get("conditionId") or "").lower() == condition_id.lower()
    ]
    if len(exact) != 1:
        raise RuntimeError(
            f"Gamma condition lookup {condition_id} returned {len(exact)} exact matches"
        )
    return exact[0]


def clob_outcomes(clob_market: dict[str, Any]) -> dict[str, str]:
    out: dict[str, str] = {}
    for item in clob_market.get("t") or []:
        if not isinstance(item, dict):
            continue
        token_id = item.get("t")
        outcome = item.get("o")
        if token_id is not None and outcome is not None:
            out[str(token_id)] = str(outcome)
    return out


def gamma_token_outcome(market: dict[str, Any], token_id: str) -> str | None:
    tokens = [str(x) for x in parse_jsonish(market.get("clobTokenIds"))]
    outcomes = [str(x) for x in parse_jsonish(market.get("outcomes"))]
    if len(tokens) != len(outcomes):
        return None
    for token, outcome in zip(tokens, outcomes):
        if token == token_id:
            return outcome
    return None


def resolve_token(token_id: str, *, timeout: float) -> dict[str, Any]:
    parent = request_json(
        f"{CLOB_BASE}/markets-by-token/{urllib.parse.quote(token_id, safe='')}",
        timeout=timeout,
    )
    if not isinstance(parent, dict):
        raise RuntimeError(f"unexpected markets-by-token response for {token_id}")

    condition_id = str(parent.get("condition_id") or "")
    primary = str(parent.get("primary_token_id") or "")
    secondary = str(parent.get("secondary_token_id") or "")
    if not condition_id or not primary or not secondary:
        raise RuntimeError(f"incomplete markets-by-token response for {token_id}: {parent!r}")
    if token_id == primary:
        canonical_outcome = "Yes"
    elif token_id == secondary:
        canonical_outcome = "No"
    else:
        raise RuntimeError(
            f"token {token_id} is neither primary nor secondary for condition {condition_id}"
        )

    query = urllib.parse.urlencode({"condition_ids": condition_id})
    gamma_market = select_gamma_market(
        request_json(f"{GAMMA_BASE}/markets?{query}", timeout=timeout), condition_id
    )
    clob_market = request_json(
        f"{CLOB_BASE}/clob-markets/{urllib.parse.quote(condition_id, safe='')}",
        timeout=timeout,
    )
    if not isinstance(clob_market, dict):
        raise RuntimeError(f"unexpected CLOB market response for {condition_id}")

    gamma_outcome = gamma_token_outcome(gamma_market, token_id)
    clob_outcome = clob_outcomes(clob_market).get(token_id)
    side_checks = {
        "markets_by_token": canonical_outcome,
        "gamma": gamma_outcome,
        "clob_market": clob_outcome,
    }
    known_outcomes = [value.lower() for value in side_checks.values() if value]
    side_consistent = bool(known_outcomes) and len(set(known_outcomes)) == 1

    events = [x for x in (gamma_market.get("events") or []) if isinstance(x, dict)]
    event = events[0] if len(events) == 1 else None
    event_summary = compact_event(event) if event else None
    weather_match = weather_evidence(gamma_market, event)

    return {
        "condition_id": condition_id,
        "token_outcome": canonical_outcome,
        "token_side_checks": side_checks,
        "token_side_consistent": side_consistent,
        "primary_yes_token_id": primary,
        "secondary_no_token_id": secondary,
        "market_id": gamma_market.get("id"),
        "market_slug": gamma_market.get("slug"),
        "question": gamma_market.get("question"),
        "bucket_label": gamma_market.get("groupItemTitle") or gamma_market.get("question"),
        "group_item_threshold": gamma_market.get("groupItemThreshold"),
        "market_category": gamma_market.get("category"),
        "resolution_source": gamma_market.get("resolutionSource"),
        "start_date": gamma_market.get("startDate"),
        "end_date": gamma_market.get("endDate"),
        "active": gamma_market.get("active"),
        "closed": gamma_market.get("closed"),
        "fees_enabled": gamma_market.get("feesEnabled"),
        "gamma_fee_schedule": gamma_market.get("feeSchedule"),
        "market_description": gamma_market.get("description"),
        "event_count": len(events),
        "event": event_summary,
        "weather_evidence": weather_match,
        "is_weather_metadata_match": bool(weather_match),
        "clob_min_order_size": clob_market.get("mos"),
        "clob_min_tick_size": clob_market.get("mts"),
        "clob_maker_base_fee_bips": clob_market.get("mbf"),
        "clob_taker_base_fee_bips": clob_market.get("tbf"),
        "clob_fee_details": clob_market.get("fd"),
        "clob_rewards": clob_market.get("r"),
        "clob_taker_order_delay_enabled": clob_market.get("itode"),
        "clob_min_order_age_seconds": clob_market.get("oas"),
    }


def load_cache(path: Path | None) -> dict[str, dict[str, Any]]:
    if path is None or not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"cache is not a JSON object: {path}")
    return {str(k): v for k, v in data.items() if isinstance(v, dict)}


def save_cache(path: Path | None, cache: dict[str, dict[str, Any]]) -> None:
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as handle:
        json.dump(cache, handle, separators=(",", ":"), sort_keys=True)
        handle.write("\n")
    tmp.replace(path)


def iter_jsonl(handle: Iterable[str]) -> Iterable[dict[str, Any]]:
    for line_number, raw in enumerate(handle, start=1):
        raw = raw.strip()
        if not raw:
            continue
        try:
            row = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid JSON on input line {line_number}: {exc}") from exc
        if not isinstance(row, dict):
            raise ValueError(f"input line {line_number} is not a JSON object")
        yield row


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Enrich SQD Polymarket V2 wallet-order JSONL with official market metadata."
    )
    parser.add_argument("input", nargs="?", type=Path, help="raw JSONL; defaults to stdin")
    parser.add_argument("--output", type=Path, help="enriched JSONL; defaults to stdout")
    parser.add_argument(
        "--cache",
        type=Path,
        default=Path("data/token_metadata_cache.json"),
        help="persistent token metadata cache",
    )
    parser.add_argument("--timeout", type=float, default=30.0, help="HTTP timeout seconds")
    parser.add_argument(
        "--fail-fast",
        action="store_true",
        help="abort on metadata lookup failure instead of preserving row with enrichment_error",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_handle = args.input.open("r", encoding="utf-8") if args.input else sys.stdin
    output_handle = args.output.open("w", encoding="utf-8") if args.output else sys.stdout
    cache = load_cache(args.cache)
    cache_dirty = False
    count = 0
    failures = 0

    try:
        for row in iter_jsonl(input_handle):
            token_id = str(row.get("token_id") or "")
            if not token_id:
                raise ValueError("input row missing token_id")

            metadata = cache.get(token_id)
            enrichment_error = None
            if metadata is None:
                try:
                    metadata = resolve_token(token_id, timeout=args.timeout)
                    cache[token_id] = metadata
                    cache_dirty = True
                except (RuntimeError, urllib.error.URLError) as exc:
                    if args.fail_fast:
                        raise
                    failures += 1
                    enrichment_error = str(exc)

            enriched = dict(row)
            if metadata is not None:
                enriched["market"] = metadata
                if not metadata.get("token_side_consistent"):
                    enriched["metadata_integrity_error"] = "token outcome mappings disagree"
            if enrichment_error:
                enriched["enrichment_error"] = enrichment_error

            output_handle.write(json.dumps(enriched, separators=(",", ":"), sort_keys=True) + "\n")
            count += 1

        if cache_dirty:
            save_cache(args.cache, cache)
        print(
            f"rows={count} unique_tokens_cached={len(cache)} enrichment_failures={failures}",
            file=sys.stderr,
        )
        return 0
    except (OSError, ValueError, RuntimeError, urllib.error.URLError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    finally:
        if args.input:
            input_handle.close()
        if args.output:
            output_handle.close()


if __name__ == "__main__":
    raise SystemExit(main())
