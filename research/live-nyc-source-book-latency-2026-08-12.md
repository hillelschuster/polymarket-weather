# Live NYC source → book latency — 2026-08-12

## Verdict

KLGA `16:51Z` precise METAR (82.94°F) first appeared on the polled NOAA station TXT at **2026-08-12T16:54:31.136858+00:00**. NOAA `Last-Modified` was **Wed, 12 Aug 2026 16:54:29 GMT**. The prior visible file was the `15:51Z` 80.96°F report.

The public station-file route therefore exposed the new report **211.1 seconds / 3m31.1s after the nominal 16:51:00 observation time**. The file's own `Last-Modified` was 209 seconds / 3m29s after nominal observation time.

The profitable clock is not observation time. It is:

`source_first_seen → executable market reprice`.

## Exact first book changes after source first-seen

| Bucket | Book at source first-seen | First bid change | First ask change | +60s book | +300s book | Mid Δ +60s | Mid Δ +300s |
|---|---|---|---|---|---|---:|---:|
| 80-81°F | NA / 0.001 | none | none | NA / 0.001 | NA / 0.001 | NA | NA |
| 84-85°F | 0.060 / 0.120 | 0.3s → 0.070 | 26.6s → 0.130 | 0.080 / 0.130 | 0.080 / 0.130 | +0.015 | +0.015 |
| 86-87°F | 0.470 / 0.530 | 22.6s → 0.480 | 26.6s → 0.500 | 0.410 / 0.500 | 0.420 / 0.500 | -0.045 | -0.040 |
| 88-89°F | 0.360 / 0.430 | 26.6s → 0.370 | 24.6s → 0.420 | 0.390 / 0.440 | 0.390 / 0.420 | +0.020 | +0.010 |
| 82-83°F | 0.001 / 0.004 | none | none | 0.001 / 0.004 | 0.001 / 0.004 | +0.000 | +0.000 |

The central ladder therefore retained stale/old top-of-book levels for roughly **20–27 seconds** on several economically relevant sides after this public feed first exposed the new report. The 84–85 bid reacted almost immediately, so the lag is not uniform across buckets or sides.

## Trade prints around source first-seen

The default market tape showed a **7-share 86–87°F YES BUY at 0.53** about **20.9 seconds after source first-seen**.

A separate `takerOnly=false` reconstruction of the complementary token showed the same timestamp/market with **2 + 5 = 7 shares of 86–87°F NO at 0.47**, transaction:

`0xcf47d6cb1e28b5dcf961fbd64702a362d191dc45240794c803a758adaf4703a4`

The complementary prices sum to exactly `$1.00`, consistent with Polymarket's complete-set matching path.

NO historical marks then moved:

- fill: **0.470** at `+20.9s`;
- **0.555** at `+38.9s`;
- **0.540** at `+98.9s`;
- **0.545** at `+155.9s`.

Thus the 47¢ NO leg had a **+8.5¢/share** market markout roughly 18 seconds after the fill, or **+$0.595 on 7 shares / +18.1% on 47¢ cash per share** before any maker rebate.

Because the ordinary market tape used the Data API's default taker-only behavior while the complementary NO records appeared when `takerOnly=false`, the observed structure is **consistent with YES as the active/taker side and NO as passive complementary liquidity**. Treat that role attribution as a strong API-level inference until the transaction's OrderFilled logs are separately decoded on-chain.

## What was and was not directly crossable

### Hard elimination: no money left

The report moved KLGA from 80.96°F to 82.94°F, mechanically eliminating the 80–81°F final bucket under the running observed maximum. But 80–81 YES was already at the floor before source first-seen. There was essentially no fresh capital to capture from that elimination.

This is an important negative control: **physical certainty does not imply alpha if price already reflects it.**

### Central-ladder midpoint movement: real, but spreads matter

A fresh long-YES taker trade was not obviously profitable from the captured top-of-book:

- 84–85 started around `0.060 / 0.120`; its later bid was only ~0.080;
- 88–89 started around `0.360 / 0.430`; its later bid was only ~0.390;
- 86–87 moved downward, so the profitable directional side was complementary NO rather than buying YES.

The wide spreads absorb much of the midpoint reaction. This specific live event therefore supports **maker/skew/cancel economics more strongly than indiscriminate taker crossing**.

## Profitability interpretation

The live result changes the implementation priority in a precise way:

1. **There is real post-source-arrival market latency.** Multiple central-ladder sides did not update for ~20–27 seconds after the measured public source first-seen clock.
2. **The cheap NOAA station TXT is itself late.** It exposed the 16:51 report ~3.5 minutes after nominal observation time. Faster weather dissemination has more expected value than shaving milliseconds from a 2-second book poller.
3. **Maker routing looks especially attractive.** The observed complementary 47¢ NO fill had very strong immediate positive markout while a 53¢ YES taker crossed it.
4. **Taker mode must remain price-selective.** The captured YES spreads were wide enough that a correct directional update did not automatically yield positive executable markout.
5. **Future live captures must record both YES and NO books.** Capturing only YES books is insufficient for exact short/complementary execution economics on binary markets.

## Feed priority

The next US source test should be:

1. shortened **5-minute ASOS** observations as an earlier temperature-state feed;
2. if market participants are still faster, **MADIS OMO / one-minute ASOS via LDM or another continuous distribution path**;
3. synchronized against the public Polymarket **market WebSocket**, not REST polling, once the weather source is fast enough to matter.

The ordinary NOAA station TXT remains useful as a free verification/baseline route, but it should not be assumed to be the production trigger.

## Required three-clock accounting

Every future T+0 event must store separately:

1. `observation_valid_time` — timestamp inside the weather report;
2. `source_first_seen_time` — when the bot's actual feed exposed the information;
3. `market_reprice_time` — when executable prices/depth changed.

Only `(3 - 2)` is monetizable by that source. Using `(3 - 1)` can overstate live alpha by minutes.
