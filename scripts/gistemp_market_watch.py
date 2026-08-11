#!/usr/bin/env python3
"""Snapshot a full Polymarket GISTEMP ladder at production-quality L2 depth.

The output is append-only JSONL. Each record contains one Gamma event snapshot,
all YES/NO order books fetched in one CLOB batch, and deterministic full-ladder
basket economics at executable depth.

No third-party dependencies.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

GAMMA_BASE = "https://gamma-api.polymarket.com"
CLOB_BOOKS_URL = "https://clob.polymarket.com/books"
USER_AGENT = "polymarket-weather-gistemp-market-watch/1.0"
DEFAULT_FEE_RATE = 0.05


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


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
        if isinstance(decoded, list):
            return decoded
        return [decoded]
    return [value]


def request_json(url: str, *, data: Any = None, timeout: float = 30.0) -> Any:
    headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}
    body = None
    method = "GET"
    if data is not None:
        body = json.dumps(data, separators=(",", ":")).encode("utf-8")
        headers["Content-Type"] = "application/json"
        method = "POST"
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return json.load(response)


def market_label(market: dict[str, Any]) -> str:
    for key in ("groupItemTitle", "question", "slug"):
        value = market.get(key)
        if value:
            return str(value)
    return str(market.get("id", "unknown"))


def token_rows(event: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for market in event.get("markets") or []:
        outcomes = [str(x) for x in parse_jsonish(market.get("outcomes"))]
        tokens = [str(x) for x in parse_jsonish(market.get("clobTokenIds"))]
        if len(outcomes) != len(tokens) or not tokens:
            continue
        label = market_label(market)
        for outcome, token_id in zip(outcomes, tokens):
            rows.append(
                {
                    "event_id": event.get("id"),
                    "event_slug": event.get("slug"),
                    "event_title": event.get("title"),
                    "market_id": market.get("id"),
                    "condition_id": market.get("conditionId") or market.get("condition_id"),
                    "market_slug": market.get("slug"),
                    "bucket": label,
                    "outcome": outcome,
                    "token_id": token_id,
                    "fees_enabled": market.get("feesEnabled"),
                    "neg_risk": market.get("negRisk"),
                }
            )
    return rows


def decimal_levels(levels: Iterable[dict[str, Any]]) -> list[tuple[float, float]]:
    out: list[tuple[float, float]] = []
    for level in levels:
        try:
            p = float(level["price"])
            s = float(level["size"])
        except (KeyError, TypeError, ValueError):
            continue
        if p >= 0 and s > 0:
            out.append((p, s))
    return out


def fee_per_share(price: float, fee_rate: float) -> float:
    return fee_rate * price * (1.0 - price)


def buy_cost_for_qty(
    asks: list[tuple[float, float]], qty: float, *, fee_rate: float
) -> tuple[float, float] | None:
    if qty <= 0:
        return (0.0, 0.0)
    remaining = qty
    raw_cost = 0.0
    fee = 0.0
    for price, size in asks:
        take = min(remaining, size)
        raw_cost += take * price
        fee += take * fee_per_share(price, fee_rate)
        remaining -= take
        if remaining <= 1e-12:
            return raw_cost, fee
    return None


def common_qty_breakpoints(ask_books: list[list[tuple[float, float]]]) -> list[float]:
    if not ask_books or any(not book for book in ask_books):
        return []
    cumulative_sets: list[list[float]] = []
    for book in ask_books:
        total = 0.0
        cums: list[float] = []
        for _, size in book:
            total += size
            cums.append(total)
        cumulative_sets.append(cums)
    max_common = min(cums[-1] for cums in cumulative_sets)
    candidates = {max_common}
    for cums in cumulative_sets:
        for qty in cums:
            if 0 < qty <= max_common:
                candidates.add(qty)
    return sorted(candidates)


def basket_curve(
    ask_books: list[list[tuple[float, float]]],
    *,
    payout_per_complete_set: float,
    fee_rate: float,
    max_points: int = 80,
) -> list[dict[str, float]]:
    points = common_qty_breakpoints(ask_books)
    if len(points) > max_points:
        points = sorted(set(points[: max_points - 1] + [points[-1]]))

    curve: list[dict[str, float]] = []
    for qty in points:
        raw = 0.0
        fees = 0.0
        valid = True
        for book in ask_books:
            result = buy_cost_for_qty(book, qty, fee_rate=fee_rate)
            if result is None:
                valid = False
                break
            raw_leg, fee_leg = result
            raw += raw_leg
            fees += fee_leg
        if not valid:
            continue
        deterministic_value = payout_per_complete_set * qty
        all_in = raw + fees
        curve.append(
            {
                "qty_each_leg": qty,
                "raw_cost": raw,
                "taker_fees": fees,
                "all_in_cost": all_in,
                "deterministic_value": deterministic_value,
                "net_edge_dollars": deterministic_value - all_in,
                "net_edge_per_complete_set": (deterministic_value - all_in) / qty,
            }
        )
    return curve


def normalize_book(book: dict[str, Any], token_meta: dict[str, Any]) -> dict[str, Any]:
    bids = decimal_levels(book.get("bids") or [])
    asks = decimal_levels(book.get("asks") or [])
    bids.sort(key=lambda x: x[0], reverse=True)
    asks.sort(key=lambda x: x[0])
    return {
        **token_meta,
        "book_market": book.get("market"),
        "book_timestamp": book.get("timestamp"),
        "book_hash": book.get("hash"),
        "tick_size": book.get("tick_size"),
        "min_order_size": book.get("min_order_size"),
        "book_neg_risk": book.get("neg_risk"),
        "last_trade_price": book.get("last_trade_price"),
        "best_bid": bids[0][0] if bids else None,
        "best_ask": asks[0][0] if asks else None,
        "bids": [{"price": p, "size": s} for p, s in bids],
        "asks": [{"price": p, "size": s} for p, s in asks],
    }


def event_fee_bips(event: dict[str, Any]) -> float | None:
    for key in ("negRiskFeeBips", "neg_risk_fee_bips"):
        value = event.get(key)
        if value is not None:
            try:
                return float(value)
            except (TypeError, ValueError):
                pass
    markets = event.get("markets") or []
    vals = []
    for market in markets:
        value = market.get("negRiskFeeBips")
        if value is not None:
            try:
                vals.append(float(value))
            except (TypeError, ValueError):
                pass
    return vals[0] if vals and all(abs(v - vals[0]) < 1e-9 for v in vals) else None


def append_jsonl(path: Path, record: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, sort_keys=True, separators=(",", ":")))
        f.write("\n")


def snapshot(event_slug: str, *, timeout: float, fee_rate: float) -> dict[str, Any]:
    received_start = now_iso()
    event_url = f"{GAMMA_BASE}/events/slug/{urllib.parse.quote(event_slug, safe='')}"
    event = request_json(event_url, timeout=timeout)
    rows = token_rows(event)
    if not rows:
        raise RuntimeError("event contains no parseable CLOB token IDs")
    if len(rows) > 15:
        raise RuntimeError(
            f"event has {len(rows)} tokens; split batching is required above CLOB's 15-book limit"
        )

    books_raw = request_json(
        CLOB_BOOKS_URL,
        data=[{"token_id": row["token_id"]} for row in rows],
        timeout=timeout,
    )
    by_asset = {str(book.get("asset_id")): book for book in books_raw}
    books = [normalize_book(by_asset.get(row["token_id"], {}), row) for row in rows]

    yes_books = []
    no_books = []
    for row in books:
        asks = [(x["price"], x["size"]) for x in row["asks"]]
        outcome = row["outcome"].strip().lower()
        if outcome == "yes":
            yes_books.append(asks)
        elif outcome == "no":
            no_books.append(asks)

    market_count = len(event.get("markets") or [])
    fee_bips = event_fee_bips(event)
    lam = None if fee_bips is None else 1.0 - fee_bips / 10_000.0

    economics: dict[str, Any] = {
        "assumed_taker_fee_rate": fee_rate,
        "market_count": market_count,
        "neg_risk_fee_bips": fee_bips,
    }
    if len(yes_books) == market_count and market_count > 0:
        economics["full_yes_basket"] = basket_curve(
            yes_books,
            payout_per_complete_set=1.0,
            fee_rate=fee_rate,
        )
    if len(no_books) == market_count and market_count > 1 and lam is not None:
        economics["full_no_conversion"] = basket_curve(
            no_books,
            payout_per_complete_set=lam * (market_count - 1),
            fee_rate=fee_rate,
        )

    metadata_keys = (
        "id",
        "slug",
        "title",
        "active",
        "closed",
        "liquidity",
        "volume",
        "openInterest",
        "startDate",
        "endDate",
        "negRisk",
        "negRiskMarketID",
        "negRiskFeeBips",
        "resolutionSource",
    )
    return {
        "snapshot_started_at": received_start,
        "snapshot_finished_at": now_iso(),
        "event": {key: event.get(key) for key in metadata_keys if key in event},
        "books": books,
        "economics": economics,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Capture full GISTEMP event L2 and deterministic ladder economics."
    )
    parser.add_argument("--event-slug", required=True)
    parser.add_argument("--out", type=Path, default=Path("data/gistemp-market/books.jsonl"))
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument(
        "--taker-fee-rate",
        type=float,
        default=DEFAULT_FEE_RATE,
        help="current Weather fee rate; use 0 for fee-free historical replay",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        record = snapshot(
            args.event_slug,
            timeout=args.timeout,
            fee_rate=args.taker_fee_rate,
        )
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError, RuntimeError) as exc:
        print(f"snapshot failed: {exc}", file=sys.stderr)
        return 1

    append_jsonl(args.out, record)
    books = record["books"]
    print(
        f"captured {len(books)} token books for {record['event'].get('title', args.event_slug)} "
        f"at {record['snapshot_finished_at']}"
    )
    for row in books:
        print(
            f"{row['bucket']} {row['outcome']}: "
            f"bid={row['best_bid']} ask={row['best_ask']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
