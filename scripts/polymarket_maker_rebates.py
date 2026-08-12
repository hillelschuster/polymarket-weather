#!/usr/bin/env python3
"""Collect actual Polymarket maker rebate cashflows by date.

Uses the public unauthenticated CLOB endpoint:
    GET /rebates/current?date=YYYY-MM-DD&maker_address=0x...

The endpoint returns one row per rebated condition for that maker/date. Output
is JSONL so it can be joined directly to enriched wallet fills by condition_id
and date. No rebate formula is estimated here; these are actual reported USDC
rebate amounts.

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
from datetime import date, datetime, timedelta
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Iterable

CLOB_BASE = "https://clob.polymarket.com"
USER_AGENT = "polymarket-weather-maker-rebates/1.0"


def normalize_address(value: str) -> str:
    value = value.strip().lower()
    if not value.startswith("0x"):
        value = "0x" + value
    if len(value) != 42:
        raise ValueError(f"invalid EVM address: {value!r}")
    try:
        int(value[2:], 16)
    except ValueError as exc:
        raise ValueError(f"invalid EVM address: {value!r}") from exc
    return value


def parse_date(value: str) -> date:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"invalid date {value!r}; expected YYYY-MM-DD") from exc


def daterange(start: date, end: date) -> Iterable[date]:
    current = start
    while current <= end:
        yield current
        current += timedelta(days=1)


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


def fetch_day(maker: str, day: date, *, timeout: float) -> list[dict[str, Any]]:
    query = urllib.parse.urlencode(
        {"date": day.isoformat(), "maker_address": maker}
    )
    payload = request_json(f"{CLOB_BASE}/rebates/current?{query}", timeout=timeout)
    if not isinstance(payload, list):
        raise RuntimeError(f"unexpected rebate response for {day}: {type(payload).__name__}")

    rows: list[dict[str, Any]] = []
    for raw in payload:
        if not isinstance(raw, dict):
            raise RuntimeError(f"unexpected rebate row for {day}: {raw!r}")
        row = {
            "date": str(raw.get("date") or day.isoformat()),
            "condition_id": str(raw.get("condition_id") or "").lower(),
            "asset_address": str(raw.get("asset_address") or "").lower(),
            "maker_address": str(raw.get("maker_address") or maker).lower(),
            "rebated_fees_usdc": str(raw.get("rebated_fees_usdc") or "0"),
        }
        if row["maker_address"] != maker:
            raise RuntimeError(
                f"endpoint returned maker {row['maker_address']} while querying {maker}"
            )
        if not row["condition_id"]:
            raise RuntimeError(f"rebate row missing condition_id: {raw!r}")
        try:
            Decimal(row["rebated_fees_usdc"])
        except InvalidOperation as exc:
            raise RuntimeError(f"invalid rebate amount: {raw!r}") from exc
        rows.append(row)
    return rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Collect actual public Polymarket maker rebate USDC cashflows by date."
    )
    parser.add_argument("maker", help="maker/proxy 0x address")
    parser.add_argument("--start-date", required=True, type=parse_date)
    parser.add_argument("--end-date", type=parse_date, help="inclusive; defaults to start date")
    parser.add_argument(
        "--condition-id",
        action="append",
        default=[],
        help="optional condition filter; repeat to keep multiple conditions",
    )
    parser.add_argument("--output", type=Path, help="JSONL output; defaults to stdout")
    parser.add_argument("--timeout", type=float, default=30.0)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        maker = normalize_address(args.maker)
        start = args.start_date
        end = args.end_date or start
        if end < start:
            raise ValueError("--end-date is before --start-date")
        condition_filter = {value.lower() for value in args.condition_id}

        out = args.output.open("w", encoding="utf-8") if args.output else sys.stdout
        count = 0
        total = Decimal("0")
        try:
            for day in daterange(start, end):
                for row in fetch_day(maker, day, timeout=args.timeout):
                    if condition_filter and row["condition_id"] not in condition_filter:
                        continue
                    out.write(json.dumps(row, separators=(",", ":"), sort_keys=True) + "\n")
                    count += 1
                    total += Decimal(row["rebated_fees_usdc"])
        finally:
            if args.output:
                out.close()

        print(
            f"maker={maker} dates={start.isoformat()}..{end.isoformat()} "
            f"rows={count} rebates_usdc={total}",
            file=sys.stderr,
        )
        return 0
    except (OSError, ValueError, RuntimeError, urllib.error.URLError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
