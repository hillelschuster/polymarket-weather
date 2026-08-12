#!/usr/bin/env python3
"""Backfill one wallet's canonical Polymarket V2 OrderFilled rows from SQD.

The key filter is OrderFilled.topic2 == wallet. In Polymarket CTF Exchange V2,
topic2 is the owner/maker field of the order being reported for both passive
maker orders and the active takerOrder rollup. This yields the wallet's own
order fills without summing same-transaction counterparty legs.

Output is append-free JSONL: one decoded OrderFilled row per line.

No third-party dependencies.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from decimal import Decimal, getcontext
from pathlib import Path
from typing import Any, Iterable

PORTAL_BASE = "https://portal.sqd.dev/datasets/polygon-mainnet"
FINALIZED_STREAM_URL = f"{PORTAL_BASE}/finalized-stream"
FINALIZED_HEAD_URL = f"{PORTAL_BASE}/finalized-head"

CTF_EXCHANGE_V2 = "0xe111180000d2663c0091e4f400237545b87b996b"
NEG_RISK_CTF_EXCHANGE_V2 = "0xe2222d279d744050d28e00520010520000310f59"
EXCHANGES = (CTF_EXCHANGE_V2, NEG_RISK_CTF_EXCHANGE_V2)

ORDER_FILLED_TOPIC = (
    "0xd543adfd945773f1a62f74f0ee55a5e3b9b1a28262980ba90b1a89f2ea84d8ee"
)

# Conservative V2-era start. Override on CLI when a narrower range is known.
DEFAULT_FROM_BLOCK = 84_902_353
DEFAULT_CHUNK_BLOCKS = 500_000
AMOUNT_SCALE = Decimal(1_000_000)
ZERO_BYTES32 = "0x" + "00" * 32
USER_AGENT = "polymarket-weather-sqd-v2-wallet-orders/1.0"

getcontext().prec = 50


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


def address_topic(address: str) -> str:
    return "0x" + "0" * 24 + normalize_address(address)[2:]


def topic_address(topic: str) -> str:
    topic = topic.lower()
    if not topic.startswith("0x") or len(topic) != 66:
        raise ValueError(f"invalid address topic: {topic!r}")
    return "0x" + topic[-40:]


def decimal_text(value: Decimal, places: int = 12) -> str:
    text = f"{value:.{places}f}".rstrip("0").rstrip(".")
    return text or "0"


def utc_iso(timestamp: int) -> str:
    return datetime.fromtimestamp(timestamp, tz=timezone.utc).isoformat().replace("+00:00", "Z")


def request_json(url: str, *, timeout: float = 30.0) -> Any:
    req = urllib.request.Request(
        url,
        headers={"Accept": "application/json", "User-Agent": USER_AGENT},
        method="GET",
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return json.load(response)


def finalized_head(timeout: float) -> int:
    payload = request_json(FINALIZED_HEAD_URL, timeout=timeout)
    if not isinstance(payload, dict) or "number" not in payload:
        raise RuntimeError(f"unexpected finalized-head response: {payload!r}")
    return int(payload["number"])


def stream_request(
    payload: dict[str, Any], *, timeout: float, retries: int = 5
) -> urllib.response.addinfourl | None:
    body = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    req = urllib.request.Request(
        FINALIZED_STREAM_URL,
        data=body,
        headers={
            "Accept": "application/x-ndjson, application/json",
            "Content-Type": "application/json",
            "User-Agent": USER_AGENT,
        },
        method="POST",
    )

    for attempt in range(retries + 1):
        try:
            response = urllib.request.urlopen(req, timeout=timeout)
            if response.status == 204:
                response.close()
                return None
            return response
        except urllib.error.HTTPError as exc:
            if exc.code not in (429, 500, 503) or attempt >= retries:
                detail = exc.read().decode("utf-8", errors="replace")
                raise RuntimeError(
                    f"SQD HTTP {exc.code}: {detail[:1000]}"
                ) from exc
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
    return None


def iter_response_blocks(response: Iterable[bytes]) -> Iterable[dict[str, Any]]:
    for raw_line in response:
        line = raw_line.decode("utf-8").strip()
        if not line:
            continue
        item = json.loads(line)
        if isinstance(item, list):
            for block in item:
                if isinstance(block, dict):
                    yield block
        elif isinstance(item, dict):
            yield item
        else:
            raise RuntimeError(f"unexpected SQD NDJSON item: {type(item).__name__}")


def split_words(data: str, expected: int = 7) -> list[str]:
    if not data.startswith("0x"):
        raise ValueError("log data is not 0x-prefixed")
    raw = data[2:]
    if len(raw) != expected * 64:
        raise ValueError(
            f"unexpected OrderFilled data length: {len(raw)} hex chars, expected {expected * 64}"
        )
    return [raw[i : i + 64] for i in range(0, len(raw), 64)]


def decode_order_filled(block: dict[str, Any], log: dict[str, Any], wallet: str) -> dict[str, Any]:
    topics = [str(x).lower() for x in log.get("topics") or []]
    if len(topics) != 4:
        raise ValueError(f"OrderFilled expected 4 topics, got {len(topics)}")
    if topics[0] != ORDER_FILLED_TOPIC:
        raise ValueError(f"unexpected topic0: {topics[0]}")

    order_hash = topics[1]
    order_owner = topic_address(topics[2])
    taker_field = topic_address(topics[3])
    if order_owner != wallet:
        raise ValueError(f"SQD returned non-target owner {order_owner} for {wallet}")

    words = split_words(str(log["data"]).lower())
    side_code = int(words[0], 16)
    if side_code not in (0, 1):
        raise ValueError(f"unknown Side value: {side_code}")
    side = "BUY" if side_code == 0 else "SELL"

    token_id = int(words[1], 16)
    maker_amount_raw = int(words[2], 16)
    taker_amount_raw = int(words[3], 16)
    logged_fee_raw = int(words[4], 16)
    builder = "0x" + words[5]
    metadata = "0x" + words[6]

    maker_amount = Decimal(maker_amount_raw) / AMOUNT_SCALE
    taker_amount = Decimal(taker_amount_raw) / AMOUNT_SCALE
    logged_fee = Decimal(logged_fee_raw) / AMOUNT_SCALE

    if side == "BUY":
        shares = taker_amount
        cash_before_fee = maker_amount
        cash_after_logged_fee = maker_amount + logged_fee
    else:
        shares = maker_amount
        cash_before_fee = taker_amount
        cash_after_logged_fee = taker_amount - logged_fee

    if shares <= 0:
        raise ValueError("OrderFilled has non-positive share quantity")

    raw_price = cash_before_fee / shares
    logged_fee_adjusted_price = cash_after_logged_fee / shares
    fee_per_share = logged_fee / shares

    exchange = normalize_address(str(log["address"]))
    role = "AGGRESSIVE" if taker_field == exchange else "PASSIVE"

    header = block.get("header") or {}
    timestamp = int(header["timestamp"])

    return {
        "timestamp": timestamp,
        "timestamp_utc": utc_iso(timestamp),
        "block_number": int(header["number"]),
        "transaction_hash": str(log["transactionHash"]).lower(),
        "log_index": int(log["logIndex"]),
        "exchange": exchange,
        "order_hash": order_hash,
        "wallet": wallet,
        "role": role,
        "side": side,
        "token_id": str(token_id),
        "maker_amount_raw": str(maker_amount_raw),
        "taker_amount_raw": str(taker_amount_raw),
        "logged_fee_raw": str(logged_fee_raw),
        "maker_amount": decimal_text(maker_amount, 6),
        "taker_amount": decimal_text(taker_amount, 6),
        "shares": decimal_text(shares, 6),
        "cash_before_logged_fee": decimal_text(cash_before_fee, 6),
        "logged_fee": decimal_text(logged_fee, 6),
        "cash_after_logged_fee": decimal_text(cash_after_logged_fee, 6),
        "raw_price": decimal_text(raw_price),
        "logged_fee_per_share": decimal_text(fee_per_share),
        "logged_fee_adjusted_price": decimal_text(logged_fee_adjusted_price),
        "counterparty_or_exchange": taker_field,
        "builder": builder,
        "builder_fee_requires_lookup": builder != ZERO_BYTES32,
        "metadata": metadata,
    }


def query_payload(wallet: str, from_block: int, to_block: int) -> dict[str, Any]:
    return {
        "type": "evm",
        "fromBlock": from_block,
        "toBlock": to_block,
        "fields": {
            "block": {"number": True, "timestamp": True},
            "log": {
                "address": True,
                "topics": True,
                "data": True,
                "transactionHash": True,
                "logIndex": True,
            },
        },
        "logs": [
            {
                "address": list(EXCHANGES),
                "topic0": [ORDER_FILLED_TOPIC],
                "topic2": [address_topic(wallet)],
            }
        ],
    }


def backfill(
    wallet: str,
    *,
    from_block: int,
    to_block: int,
    chunk_blocks: int,
    timeout: float,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    cursor = from_block

    while cursor <= to_block:
        chunk_end = min(to_block, cursor + chunk_blocks - 1)
        payload = query_payload(wallet, cursor, chunk_end)
        response = stream_request(payload, timeout=timeout)
        if response is None:
            cursor = chunk_end + 1
            continue

        max_returned_block: int | None = None
        saw_block = False
        try:
            for block in iter_response_blocks(response):
                saw_block = True
                header = block.get("header") or {}
                block_number = int(header["number"])
                max_returned_block = (
                    block_number
                    if max_returned_block is None
                    else max(max_returned_block, block_number)
                )
                for log in block.get("logs") or []:
                    rows.append(decode_order_filled(block, log, wallet))
        finally:
            response.close()

        if not saw_block:
            # SQD documents that an empty bounded response can mean every block
            # in the requested range was skipped by the filters.
            cursor = chunk_end + 1
        elif max_returned_block is not None:
            # A response may stop before toBlock at a worker boundary. Resuming
            # after the last returned block is conservative and never skips a
            # matching row; it can only re-scan a no-match tail.
            cursor = max_returned_block + 1
        else:
            raise RuntimeError("SQD response contained blocks without block numbers")

    rows.sort(key=lambda row: (row["block_number"], row["log_index"]))
    return rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Backfill canonical Polymarket V2 OrderFilled rows for one wallet via SQD Portal."
    )
    parser.add_argument("wallet", help="0x-prefixed Polygon wallet/proxy address")
    parser.add_argument(
        "--from-block",
        type=int,
        default=DEFAULT_FROM_BLOCK,
        help=f"inclusive start block (default: {DEFAULT_FROM_BLOCK})",
    )
    parser.add_argument(
        "--to-block",
        type=int,
        help="inclusive end block; defaults to SQD's latest finalized Polygon block",
    )
    parser.add_argument(
        "--chunk-blocks",
        type=int,
        default=DEFAULT_CHUNK_BLOCKS,
        help=f"bounded query size (default: {DEFAULT_CHUNK_BLOCKS})",
    )
    parser.add_argument("--timeout", type=float, default=60.0, help="HTTP timeout seconds")
    parser.add_argument(
        "--output",
        type=Path,
        help="JSONL output path; defaults to stdout",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        wallet = normalize_address(args.wallet)
        if args.from_block < 0:
            raise ValueError("--from-block must be >= 0")
        if args.chunk_blocks <= 0:
            raise ValueError("--chunk-blocks must be > 0")
        to_block = args.to_block if args.to_block is not None else finalized_head(args.timeout)
        if to_block < args.from_block:
            raise ValueError("--to-block is before --from-block")

        rows = backfill(
            wallet,
            from_block=args.from_block,
            to_block=to_block,
            chunk_blocks=args.chunk_blocks,
            timeout=args.timeout,
        )

        out = args.output.open("w", encoding="utf-8") if args.output else sys.stdout
        try:
            for row in rows:
                out.write(json.dumps(row, separators=(",", ":"), sort_keys=True) + "\n")
        finally:
            if args.output:
                out.close()

        print(
            f"wallet={wallet} rows={len(rows)} blocks={args.from_block}-{to_block}",
            file=sys.stderr,
        )
        return 0
    except (OSError, ValueError, RuntimeError, urllib.error.URLError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
