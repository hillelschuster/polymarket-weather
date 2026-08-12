# Live NYC source → book latency — 2026-08-12

## Verdict

KLGA `16:51Z` precise METAR (82.94°F) first appeared on the polled NOAA station TXT at **2026-08-12T16:54:31.136858+00:00**. NOAA `Last-Modified` was **Wed, 12 Aug 2026 16:54:29 GMT**. The prior visible file was the `15:51Z` 80.96°F report.

The public feed therefore crossed the 80–81°F → 82–83°F observed-state boundary about **3m40s after nominal observation time** (first-seen clock), but the relevant question is what the CLOB still offered *after first seen*.

## Exact first book changes after source first-seen

| Bucket | Book at source first-seen | First bid change | First ask change | +60s book | +300s book | Mid Δ +60s | Mid Δ +300s |
|---|---|---|---|---|---|---:|---:|
| 80-81°F | NA / 0.001 | none | none | NA / 0.001 | NA / 0.001 | NA | NA |
| 84-85°F | 0.060 / 0.120 | 0.3s → 0.070 | 26.6s → 0.130 | 0.080 / 0.130 | 0.080 / 0.130 | +0.015 | +0.015 |
| 86-87°F | 0.470 / 0.530 | 22.6s → 0.480 | 26.6s → 0.500 | 0.410 / 0.500 | 0.420 / 0.500 | -0.045 | -0.040 |
| 88-89°F | 0.360 / 0.430 | 26.6s → 0.370 | 24.6s → 0.420 | 0.390 / 0.440 | 0.390 / 0.420 | +0.020 | +0.010 |
| 82-83°F | 0.001 / 0.004 | none | none | 0.001 / 0.004 | 0.001 / 0.004 | +0.000 | +0.000 |

## Trade prints from -30s to +300s around source first-seen

| Relative sec | Bucket/token label | Side | Qty | Price |
|---:|---|---|---:|---:|
| -4.1 | No | BUY | 130.60 | 0.9571 |
| +20.9 | 86-87°F | BUY | 7.00 | 0.5300 |
| +127.9 | 92-93°F | SELL | 57.00 | 0.0040 |
| +151.9 | 92-93°F | BUY | 72.21 | 0.0050 |
| +296.9 | 90-91°F | SELL | 300.00 | 0.0401 |
| +298.9 | 90-91°F | BUY | 17.50 | 0.0534 |

## Economic reading

- **Hard elimination was not monetizable here:** 80–81°F was already at the floor before the report. This is a valid negative control against assuming every physical threshold crossing creates PnL.

- **There was a genuine post-arrival repricing window in the central ladder.** The source-first-seen book remained unchanged for roughly the first 10 seconds in the coarse report, while material bid/ask changes appeared later. Exact first-change latency is shown above from 2-second snapshots.

- **Spread is the immediate economic filter.** A midpoint reaction is not automatically taker alpha. For upward moves, compare initial ask to subsequent executable bid; for downward moves, the capture omitted complementary NO books, so unrestricted fresh short entry cannot be claimed. The strongest immediate value of the information can therefore be stale-maker cancellation/inventory skew even when taker spread is too wide.

- The live correction is durable: `observation_valid_time`, `source_first_seen_time`, and `market_reprice_time` must be separate clocks. Only market-reprice minus source-first-seen is monetizable by that source.

## Next profitability action

Do not optimize the exchange client before the weather feed. Test a faster US observation route (5-minute ASOS stream and, if needed, MADIS OMO/LDM) against the same synchronized CLOB WebSocket. The ordinary NOAA station TXT is now a measured baseline, not an assumed production trigger.
