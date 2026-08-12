#!/usr/bin/env python3
"""Backfill public Polymarket user activity without silently hitting offset caps.

The Data API /activity endpoint is public and human-enriched. It includes TRADE,
SPLIT, MERGE, REDEEM, REWARD, CONVERSION, MAKER_REBATE and REFERRAL_REWARD.
The endpoint caps offset at 10,000, so this collector recursively splits the
requested Unix-time interval whenever a window fills the last safe page.

For exact V2 maker/taker role and logged platform fees, join TRADE rows to the
SQD OrderFilled collector by transaction hash/token/time. This script is the
fast human-readable activity layer, not a substitute for the onchain ledger.

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
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Iterator

DATA_API = "https://data-api.polymarket.com/activity"
USER_AGENT = "polymarket-weather-user-activity/1.0"
PAGE_SIZE = 500
MAX_OFFSET = 10_000
LAST_SAFE_OFFSET = 9_500
ALL_TYPES = (
    "TRADE",
    "SPLIT",
    "MERGE",
    "REDEEM",
    "REWARD",
    "CONVERSION",
    "MAKER_REBATE",
    "REFERRAL_REWARD",
)


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


def parse_time(value: str) -> int:
    value = value.strip()
    if value.isdigit():
        return int(value)
    normalized = value.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            f"invalid time {value!r}; use Unix seconds or ISO-8601"
        ) from exc
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return int(parsed.timestamp())


def utc_iso(timestamp: int) -> str:
    return datetime.fromtimestamp(timestamp, tz=timezone.utc).isoformat().replace("+00:00", "Z")


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


def activity_page(
    user: str,
    *,
    start: int,
    end: int,
    offset: int,
    activity_types: tuple[str, ...],
    timeout: float,
) -> list[dict[str, Any]]:
    params: list[tuple[str, str]] = [
        ("user", user),
        ("start", str(start)),
        ("end", str(end)),
        ("limit", str(PAGE_SIZE)),
        ("offset", str(offset)),
        ("sortBy", "TIMESTAMP"),
        ("sortDirection", "ASC"),
    ]
    if activity_types:
        params.append(("type", ",".join(activity_types)))
    url = DATA_API + "?" + urllib.parse.urlencode(params)
    payload = request_json(url, timeout=timeout)
    if not isinstance(payload, list):
        raise RuntimeError(
            f"unexpected activity response for {start}..{end} offset={offset}: "
            f"{type(payload).__name__}"
        )
    rows: list[dict[str, Any]] = []
    for item in payload:
        if not isinstance(item, dict):
            raise RuntimeError(f"unexpected activity row: {item!r}")
        rows.append(item)
    return rows


def window_is_saturated(
    user: str,
    *,
    start: int,
    end: int,
    activity_types: tuple[str, ...],
    timeout: float,
) -> bool:
    page = activity_page(
        user,
        start=start,
        end=end,
        offset=LAST_SAFE_OFFSET,
        activity_types=activity_types,
        timeout=timeout,
    )
    return len(page) == PAGE_SIZE


def iter_window(
    user: str,
    *,
    start: int,
    end: int,
    activity_types: tuple[str, ...],
    timeout: float,
) -> Iterator[dict[str, Any]]:
    if end < start:
        return

    if window_is_saturated(
        user,
        start=start,
        end=end,
        activity_types=activity_types,
        timeout=timeout,
    ):
        if start == end:
            raise RuntimeError(
                f"activity exceeds {MAX_OFFSET} rows within Unix second {start}; "
                "use the SQD V2 collector for lossless reconstruction"
            )
        midpoint = start + (end - start) // 2
        yield from iter_window(
            user,
            start=start,
            end=midpoint,
            activity_types=activity_types,
            timeout=timeout,
        )
        yield from iter_window(
            user,
            start=midpoint + 1,
            end=end,
            activity_types=activity_types,
            timeout=timeout,
        )
        return

    offset = 0
    while offset <= LAST_SAFE_OFFSET:
        page = activity_page(
            user,
            start=start,
            end=end,
            offset=offset,
            activity_types=activity_types,
            timeout=timeout,
        )
        for row in page:
            enriched = dict(row)
            timestamp = enriched.get("timestamp")
            if timestamp is not None:
                try:
                    enriched["timestamp_utc"] = utc_iso(int(timestamp))
                except (TypeError, ValueError, OSError):
                    pass
            yield enriched
        if len(page) < PAGE_SIZE:
            break
        offset += PAGE_SIZE


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Backfill public Polymarket user activity with automatic time-window splitting."
    )
    parser.add_argument("user", help="Polymarket proxy/profile wallet address")
    parser.add_argument("--start", required=True, type=parse_time, help="Unix seconds or ISO-8601")
    parser.add_argument("--end", required=True, type=parse_time, help="Unix seconds or ISO-8601")
    parser.add_argument(
        "--type",
        dest="activity_types",
        action="append",
        choices=ALL_TYPES,
        help="activity type; repeat as needed; default is all types",
    )
    parser.add_argument("--output", type=Path, help="JSONL output; defaults to stdout")
    parser.add_argument("--timeout", type=float, default=30.0)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        user = normalize_address(args.user)
        if args.end < args.start:
            raise ValueError("--end is before --start")
        activity_types = tuple(args.activity_types or ())

        out = args.output.open("w", encoding="utf-8") if args.output else sys.stdout
        count = 0
        try:
            for row in iter_window(
                user,
                start=args.start,
                end=args.end,
                activity_types=activity_types,
                timeout=args.timeout,
            ):
                out.write(json.dumps(row, separators=(",", ":"), sort_keys=True) + "\n")
                count += 1
        finally:
            if args.output:
                out.close()

        print(
            f"user={user} start={args.start} end={args.end} rows={count} "
            f"types={','.join(activity_types) if activity_types else 'ALL'}",
            file=sys.stderr,
        )
        return 0
    except (OSError, ValueError, RuntimeError, urllib.error.URLError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
