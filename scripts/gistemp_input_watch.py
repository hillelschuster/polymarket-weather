#!/usr/bin/env python3
"""Point-in-time archiver for GISTEMP resolver inputs.

Archives changed upstream files with receipt timestamps and SHA256 hashes so a
later replay can reproduce exactly what was publicly available before NASA's
monthly GISTEMP release.

No third-party dependencies.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_GHCN_URL = (
    "https://www.ncei.noaa.gov/pub/data/ghcn/v4/"
    "ghcnm.tavg.latest.qcf.tar.gz"
)
DEFAULT_ERSST_TEMPLATE = (
    "https://www.ncei.noaa.gov/pub/data/cmb/ersst/v5/netcdf/"
    "ersst.v5.{yyyymm}.nc"
)
DEFAULT_NASA_OUTPUT_URL = (
    "https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.csv"
)
USER_AGENT = "polymarket-weather-gistemp-watch/1.0"
CHUNK = 1024 * 1024


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def iso_z(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def stamp(dt: datetime) -> str:
    return dt.strftime("%Y%m%dT%H%M%SZ")


def parse_month(value: str) -> str:
    if not re.fullmatch(r"\d{4}-\d{2}", value):
        raise argparse.ArgumentTypeError("month must be YYYY-MM")
    year, month = map(int, value.split("-"))
    if not 1 <= month <= 12:
        raise argparse.ArgumentTypeError("month must be YYYY-MM")
    return f"{year:04d}-{month:02d}"


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"version": 1, "sources": {}}
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError(f"invalid state file: {path}")
    data.setdefault("version", 1)
    data.setdefault("sources", {})
    return data


def atomic_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=True)
        f.write("\n")
    os.replace(tmp, path)


def append_jsonl(path: Path, record: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, sort_keys=True, separators=(",", ":")))
        f.write("\n")


def safe_name(url: str) -> str:
    tail = url.rstrip("/").split("/")[-1] or "download"
    return re.sub(r"[^A-Za-z0-9._-]+", "_", tail)


def download_one(
    *,
    name: str,
    url: str,
    archive_dir: Path,
    state: dict[str, Any],
    log_path: Path,
    timeout: float,
) -> dict[str, Any]:
    requested_at = utc_now()
    previous = state["sources"].get(name, {})

    headers = {"User-Agent": USER_AGENT, "Accept": "*/*"}
    if previous.get("etag"):
        headers["If-None-Match"] = str(previous["etag"])
    if previous.get("last_modified"):
        headers["If-Modified-Since"] = str(previous["last_modified"])

    req = urllib.request.Request(url, headers=headers, method="GET")
    record: dict[str, Any] = {
        "source": name,
        "url": url,
        "requested_at": iso_z(requested_at),
    }

    tmp_path: Path | None = None
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            received_at = utc_now()
            status = getattr(response, "status", 200)
            record.update(
                {
                    "status": int(status),
                    "received_at": iso_z(received_at),
                    "etag": response.headers.get("ETag"),
                    "last_modified": response.headers.get("Last-Modified"),
                    "content_length_header": response.headers.get("Content-Length"),
                }
            )

            archive_dir.mkdir(parents=True, exist_ok=True)
            fd, tmp_raw = tempfile.mkstemp(prefix=f".{name}.", dir=archive_dir)
            os.close(fd)
            tmp_path = Path(tmp_raw)

            h = hashlib.sha256()
            size = 0
            with tmp_path.open("wb") as out:
                while True:
                    chunk = response.read(CHUNK)
                    if not chunk:
                        break
                    out.write(chunk)
                    h.update(chunk)
                    size += len(chunk)

            digest = h.hexdigest()
            record["bytes"] = size
            record["sha256"] = digest

            changed = digest != previous.get("sha256")
            record["changed"] = changed

            if changed:
                filename = (
                    f"{stamp(received_at)}_{name}_{digest[:12]}_{safe_name(url)}"
                )
                final_path = archive_dir / filename
                shutil.move(str(tmp_path), final_path)
                tmp_path = None
                record["archive_path"] = str(final_path)
            else:
                record["archive_path"] = previous.get("archive_path")
                tmp_path.unlink(missing_ok=True)
                tmp_path = None

            state["sources"][name] = {
                "url": url,
                "last_checked": iso_z(received_at),
                "etag": record.get("etag"),
                "last_modified": record.get("last_modified"),
                "bytes": size,
                "sha256": digest,
                "archive_path": record.get("archive_path"),
            }

    except urllib.error.HTTPError as exc:
        received_at = utc_now()
        if exc.code == 304:
            record.update(
                {
                    "status": 304,
                    "received_at": iso_z(received_at),
                    "changed": False,
                    "sha256": previous.get("sha256"),
                    "archive_path": previous.get("archive_path"),
                }
            )
            previous["last_checked"] = iso_z(received_at)
            state["sources"][name] = previous
        else:
            record.update(
                {
                    "status": exc.code,
                    "received_at": iso_z(received_at),
                    "changed": False,
                    "error": str(exc),
                }
            )
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        record.update(
            {
                "status": "error",
                "received_at": iso_z(utc_now()),
                "changed": False,
                "error": str(exc),
            }
        )
    finally:
        if tmp_path is not None:
            tmp_path.unlink(missing_ok=True)
        append_jsonl(log_path, record)

    return record


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Archive point-in-time GISTEMP upstream inputs and NASA output."
    )
    p.add_argument("--month", required=True, type=parse_month, help="target month YYYY-MM")
    p.add_argument(
        "--archive-dir",
        type=Path,
        default=Path("data/gistemp-inputs"),
        help="directory for archived binary snapshots",
    )
    p.add_argument("--state", type=Path, default=None, help="state JSON path")
    p.add_argument("--log", type=Path, default=None, help="append-only JSONL log path")
    p.add_argument("--timeout", type=float, default=90.0)
    p.add_argument("--ghcn-url", default=DEFAULT_GHCN_URL)
    p.add_argument("--ersst-url", default=None)
    p.add_argument("--nasa-output-url", default=DEFAULT_NASA_OUTPUT_URL)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    month = args.month
    yyyymm = month.replace("-", "")

    archive_dir: Path = args.archive_dir
    state_path = args.state or archive_dir / "state.json"
    log_path = args.log or archive_dir / "checks.jsonl"
    ersst_url = args.ersst_url or DEFAULT_ERSST_TEMPLATE.format(yyyymm=yyyymm)

    state = load_json(state_path)
    state["target_month"] = month

    specs = [
        ("ghcn_qcf", args.ghcn_url),
        (f"ersst_{yyyymm}", ersst_url),
        ("nasa_loti", args.nasa_output_url),
    ]

    results = []
    for name, url in specs:
        result = download_one(
            name=name,
            url=url,
            archive_dir=archive_dir,
            state=state,
            log_path=log_path,
            timeout=args.timeout,
        )
        results.append(result)
        atomic_json(state_path, state)

    for r in results:
        if r.get("status") in (200, 304):
            flag = "CHANGED" if r.get("changed") else "unchanged"
            digest = (r.get("sha256") or "")[:12]
            print(f"{r['source']}: {flag} status={r['status']} sha256={digest}")
        else:
            print(
                f"{r['source']}: unavailable status={r.get('status')} "
                f"error={r.get('error', '')}",
                file=sys.stderr,
            )

    # Missing ERSST before its monthly publication is expected; network failures are not.
    hard_errors = [r for r in results if r.get("status") == "error"]
    return 1 if hard_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
