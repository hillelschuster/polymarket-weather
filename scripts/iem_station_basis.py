#!/usr/bin/env python3
"""Measure daily-high basis between a Polymarket resolver station and comparator.

Fetches IEM computed daily summaries for two ASOS/AWOS stations in one request,
pairs days with complete maxima, converts Fahrenheit to Celsius, and emits
per-day JSONL plus a compact month/regime summary to stderr or --summary.

Use this to quantify city-label / resolver-location basis (e.g. RKSI vs RKSS).
IEM daily summaries are research observations, not automatically the exact
contract settlement source; final event reconstruction must follow the market's
named resolver and civil-day rules.

No third-party dependencies.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import math
import statistics
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path
from typing import Any, Iterable

IEM_DAILY = "https://mesonet.agron.iastate.edu/cgi-bin/request/daily.py"
USER_AGENT = "polymarket-weather-iem-station-basis/1.0"
VARS = ("max_temp_f", "avg_wind_speed_kts", "avg_wind_drct")


def parse_date(value: str) -> date:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as exc:
        raise argparse.ArgumentTypeError("dates must be YYYY-MM-DD") from exc


def request_text(url: str, *, timeout: float, retries: int = 5) -> str:
    req = urllib.request.Request(
        url,
        headers={"Accept": "text/csv,text/plain,*/*", "User-Agent": USER_AGENT},
        method="GET",
    )
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                return response.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            if exc.code not in (429, 500, 502, 503, 504) or attempt >= retries:
                detail = exc.read().decode("utf-8", errors="replace")
                raise RuntimeError(f"IEM HTTP {exc.code}: {detail[:500]}") from exc
            time.sleep(min(2**attempt, 10))
        except urllib.error.URLError:
            if attempt >= retries:
                raise
            time.sleep(min(2**attempt, 10))
    raise RuntimeError("unreachable retry loop")


def maybe_float(value: Any) -> float | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text or text.lower() in {"none", "null", "nan", "m"}:
        return None
    try:
        x = float(text)
    except ValueError:
        return None
    return x if math.isfinite(x) else None


def f_to_c(value: float) -> float:
    return (value - 32.0) * 5.0 / 9.0


def fetch_daily(
    network: str,
    stations: tuple[str, str],
    start: date,
    end: date,
    *,
    timeout: float,
) -> list[dict[str, str]]:
    params = [
        ("sts", start.isoformat()),
        ("ets", end.isoformat()),
        ("network", network),
        ("stations", ",".join(stations)),
        ("var", ",".join(VARS)),
        ("na", "blank"),
        ("format", "csv"),
    ]
    text = request_text(IEM_DAILY + "?" + urllib.parse.urlencode(params), timeout=timeout)
    if text.startswith("ERROR:"):
        raise RuntimeError(text.strip())
    return list(csv.DictReader(io.StringIO(text)))


def wind_sector(degrees: float | None) -> str | None:
    if degrees is None:
        return None
    names = ("N", "NE", "E", "SE", "S", "SW", "W", "NW")
    return names[int(((degrees % 360.0) + 22.5) // 45.0) % 8]


def percentile(values: list[float], q: float) -> float | None:
    if not values:
        return None
    xs = sorted(values)
    if len(xs) == 1:
        return xs[0]
    pos = (len(xs) - 1) * q
    lo = math.floor(pos)
    hi = math.ceil(pos)
    if lo == hi:
        return xs[lo]
    return xs[lo] * (hi - pos) + xs[hi] * (pos - lo)


def summarize(values: list[float]) -> dict[str, Any]:
    if not values:
        return {"n": 0}
    return {
        "n": len(values),
        "mean_basis_c": statistics.fmean(values),
        "median_basis_c": statistics.median(values),
        "p10_basis_c": percentile(values, 0.10),
        "p25_basis_c": percentile(values, 0.25),
        "p75_basis_c": percentile(values, 0.75),
        "p90_basis_c": percentile(values, 0.90),
        "min_basis_c": min(values),
        "max_basis_c": max(values),
        "p_resolver_le_minus_1c": sum(x <= -1.0 + 1e-9 for x in values) / len(values),
        "p_resolver_le_minus_2c": sum(x <= -2.0 + 1e-9 for x in values) / len(values),
        "p_resolver_le_minus_3c": sum(x <= -3.0 + 1e-9 for x in values) / len(values),
        "p_resolver_le_minus_4c": sum(x <= -4.0 + 1e-9 for x in values) / len(values),
        "p_resolver_warmer": sum(x > 0.0 + 1e-9 for x in values) / len(values),
    }


def pair_rows(
    raw: Iterable[dict[str, str]], resolver: str, comparator: str
) -> list[dict[str, Any]]:
    by_day: dict[str, dict[str, dict[str, str]]] = defaultdict(dict)
    for row in raw:
        station = str(row.get("station") or "").upper()
        day = str(row.get("day") or "")[:10]
        if station and day:
            by_day[day][station] = row

    out: list[dict[str, Any]] = []
    for day in sorted(by_day):
        a = by_day[day].get(resolver)
        b = by_day[day].get(comparator)
        if not a or not b:
            continue
        a_f = maybe_float(a.get("max_temp_f"))
        b_f = maybe_float(b.get("max_temp_f"))
        if a_f is None or b_f is None:
            continue
        a_c = f_to_c(a_f)
        b_c = f_to_c(b_f)
        wind_dir = maybe_float(a.get("avg_wind_drct"))
        out.append(
            {
                "date": day,
                "month": day[:7],
                "resolver_station": resolver,
                "comparator_station": comparator,
                "resolver_max_f": a_f,
                "comparator_max_f": b_f,
                "resolver_max_c": a_c,
                "comparator_max_c": b_c,
                "basis_c": a_c - b_c,
                "resolver_avg_wind_drct": wind_dir,
                "resolver_avg_wind_sector": wind_sector(wind_dir),
                "resolver_avg_wind_speed_kts": maybe_float(a.get("avg_wind_speed_kts")),
            }
        )
    return out


def build_summary(rows: list[dict[str, Any]], *, network: str) -> dict[str, Any]:
    by_month: dict[str, list[float]] = defaultdict(list)
    by_wind: dict[str, list[float]] = defaultdict(list)
    for row in rows:
        basis = float(row["basis_c"])
        by_month[str(row["month"])].append(basis)
        sector = row.get("resolver_avg_wind_sector")
        if sector:
            by_wind[str(sector)].append(basis)
    return {
        "network": network,
        "resolver_station": rows[0]["resolver_station"] if rows else None,
        "comparator_station": rows[0]["comparator_station"] if rows else None,
        "overall": summarize([float(row["basis_c"]) for row in rows]),
        "by_month": {month: summarize(vals) for month, vals in sorted(by_month.items())},
        "by_resolver_wind_sector": {
            sector: summarize(vals) for sector, vals in sorted(by_wind.items())
        },
        "caveat": (
            "IEM computed daily summaries are a research proxy. Contract settlement must be "
            "reconstructed from the exact named resolver/source and its day/rounding rules."
        ),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Measure resolver/comparator daily-high basis from IEM.")
    parser.add_argument("--network", required=True, help="IEM network, e.g. KR__ASOS")
    parser.add_argument("--resolver", required=True, help="resolver station, e.g. RKSI")
    parser.add_argument("--comparator", required=True, help="comparison station, e.g. RKSS")
    parser.add_argument("--start", required=True, type=parse_date)
    parser.add_argument("--end", required=True, type=parse_date)
    parser.add_argument("--output", type=Path, help="per-day JSONL; defaults to stdout")
    parser.add_argument("--summary", type=Path, help="summary JSON; defaults to stderr")
    parser.add_argument("--timeout", type=float, default=30.0)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if args.end < args.start:
            raise ValueError("--end is before --start")
        resolver = args.resolver.upper()
        comparator = args.comparator.upper()
        if resolver == comparator:
            raise ValueError("resolver and comparator must differ")

        raw = fetch_daily(
            args.network,
            (resolver, comparator),
            args.start,
            args.end,
            timeout=args.timeout,
        )
        rows = pair_rows(raw, resolver, comparator)
        summary = build_summary(rows, network=args.network)

        out = args.output.open("w", encoding="utf-8") if args.output else sys.stdout
        try:
            for row in rows:
                out.write(json.dumps(row, separators=(",", ":"), sort_keys=True) + "\n")
        finally:
            if args.output:
                out.close()

        summary_text = json.dumps(summary, indent=2, sort_keys=True)
        if args.summary:
            args.summary.parent.mkdir(parents=True, exist_ok=True)
            args.summary.write_text(summary_text + "\n", encoding="utf-8")
        else:
            print(summary_text, file=sys.stderr)
        return 0
    except (OSError, ValueError, RuntimeError, urllib.error.URLError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
