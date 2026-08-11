# GISTEMP first-release labels from resolved Polymarket contracts

Snapshot: **2026-08-11**

Purpose: create settlement-faithful historical labels for the GISTEMP strategy **without contaminating them with NASA's later revisions**.

Polymarket resolves these markets on the value NASA first publishes for the target month and explicitly ignores later revisions. Therefore the resolved Polymarket winning bracket is itself the correct historical trading label.

This is enough for the first backtest. We do not need an exact hundredth-degree historical vintage to ask whether a pre-release model would have bought the contract that paid $1.

---

# 1. Why use Polymarket outcomes as labels

NASA GISTEMP history is revised when late station reports or corrections arrive. NASA has documented revisions as large as **0.05°C**, which equals one modern Polymarket bracket width.

If we backtest against today's revised NASA table, we can label the actual settled contract as "wrong" even though it was correct under the market's rules.

For every historical month use:

`label = resolved Polymarket winning outcome`.

Only later, if useful, recover the exact first-published hundredth for residual calibration.

---

# 2. Verified resolved label set

The bracket scheme changed over time. Preserve the **actual listed brackets** per contract rather than normalizing old months into a modern grid.

| Month | Winning first-release bracket | Event volume | Contract structure / notes |
|---|---|---:|---|
| Sep 2024 | **1.23–1.28°C** | ~$2.5M | 6 outcomes; old 0.06-ish bracket scheme |
| Oct 2024 | **1.29–1.34°C** | **$863.5k** | 6 outcomes |
| Nov 2024 | **1.30–1.34°C** | **$2.554M** | 6 outcomes |
| Dec 2024 | **1.25–1.29°C** | **$2.546M** | 5 outcomes |
| Jan 2025 | **>1.34°C** | **~$4.93M** | very high-volume full ladder |
| Feb 2025 | **1.25–1.29°C** | **~$3.74M** | full ladder |
| Mar 2025 | **1.32–1.36°C** | **~$2.87M** | contract-specific bins |
| May 2025 | **1.05–1.09°C** | **~$366k** | full ladder |
| Jun 2025 | **1.00–1.04°C** | **~$419k** | full ladder |
| Jul 2025 | **1.00–1.04°C** | **$2.042M** | bins `<0.90`, .90-.94, .95-.99, 1.00-1.04, 1.05-1.10, >1.10 |
| Aug 2025 | **>1.10°C** | **$647.6k** | same older coarse upper-tail structure |
| Sep 2025 | **>1.19°C** | **$2.415M** | bins `<1.00` through `>1.19` |
| Oct 2025 | **1.20–1.24°C** | **~$321.6k** | use the full exact-ladder event, not the separate coarse lower-strike event |
| Nov 2025 | **1.20–1.24°C** | **$977.6k** | modern 0.05°C ladder |
| Dec 2025 | **1.05–1.09°C** | **$719.7k** | modern ladder |
| Jan 2026 | **1.05–1.09°C** | **$1.054M** | modern ladder |
| Feb 2026 | **1.20–1.24°C** | **~$221k** | modern ladder |
| Mar 2026 | **1.25–1.29°C** | **$431.7k** | modern ladder |
| Apr 2026 | **1.15–1.19°C** | **$383.6k** | modern ladder |
| May 2026 | **1.10–1.14°C** | **$201.8k** | modern ladder |
| Jun 2026 | **1.15–1.19°C** | **~$88.6k** | modern ladder |

The exact event volumes can differ slightly across crawls as Polymarket indexing settles; preserve the winning bracket as the primary label and treat volume as dated capacity evidence.

---

# 3. Primary Polymarket event sources

Representative event URLs:

- Sep 2024: https://polymarket.com/event/september-2024-temperature-increase-c
- Oct 2024: https://polymarket.com/event/october-2024-temperature-increase-c
- Nov 2024: https://polymarket.com/event/november-2024-temperature-increase-c
- Dec 2024: https://polymarket.com/event/december-2024-temperature-increase-c
- Jul 2025: https://polymarket.com/event/july-2025-temperature-increase-c-513
- Aug 2025: https://polymarket.com/event/july-2025-temperature-increase-c-394
- Sep 2025: https://polymarket.com/event/september-2025-temperature-increase-c
- Nov 2025: https://polymarket.com/event/november-2025-temperature-increase-c
- Dec 2025: https://polymarket.com/event/december-2025-temperature-increase-c
- Jan 2026: https://polymarket.com/event/january-2026-temperature-increase-c
- Mar 2026: https://polymarket.com/event/march-2026-temperature-increase-c
- Apr 2026: https://polymarket.com/event/april-2026-temperature-increase-c
- May 2026: https://polymarket.com/event/may-2026-temperature-increase-c

For months with multiple related Polymarket events, use the **full mutually exclusive bracket ladder** where possible. Do not mix it with separate binary/coarse threshold markets as if they were the same label set.

---

# 4. The label set is economically meaningful

This sample is not just scientifically diverse; it contains genuine capacity.

Several events traded **$2–5 million**:

- Sep 2024 ~2.5M;
- Nov 2024 2.55M;
- Dec 2024 2.55M;
- Jan 2025 ~4.93M;
- Feb 2025 ~3.74M;
- Mar 2025 ~2.87M;
- Jul 2025 2.04M;
- Sep 2025 2.42M.

A strategy capable of moving bracket probability materially before those markets converge has far higher dollar capacity than a typical single daily-temperature city event.

The lower 2026 volumes do not invalidate the family; they indicate that capacity varies substantially by month/market attention and must be measured at execution time.

---

# 5. Label variation is exactly what we need

The outcomes range from roughly **1.00°C** to **>1.34°C** across the sample.

That means the historical study includes:

- relatively cool anomaly months;
- very warm months;
- upper-tail outcomes;
- central-bin outcomes;
- several different contract grids.

A direct-replica / basis model that succeeds only in the very hottest regime will be obvious.

The correct evaluation is always contract-native:

`predicted continuous GISTEMP distribution`

`→ integrate probability over that month's actual listed brackets`

`→ compare with actual market asks`

`→ resolved paid bracket`.

Never force every month to use today's six bins.

---

# 6. Minimal historical target table

For each month store only:

`month`
`market_event_slug`
`market_open_time`
`NASA_scheduled_release_time`
`actual_bracket_edges`
`winning_bracket`
`event_volume`

Then add information snapshots:

`ERSST_available_time`
`ERA5T_available_time`
`GHCN_qcf_snapshot_time`
`replica_value`
`replica_distribution`
`market_prices_at_same_time`.

This is sufficient to answer the profit question.

---

# 7. First backtest does not need exact first-release hundredths

Suppose the model at D+5 predicts a continuous normal-like residual distribution centered at 1.17°C.

For an April-2026-style contract, compute:

`P(<1.10)`
`P(1.10–1.14)`
`P(1.15–1.19)`
`P(1.20–1.24)`
`P(1.25–1.29)`
`P(>1.29)`.

If the actual Polymarket winner is 1.15–1.19, that is enough to score log loss and trading PnL.

Exact original NASA value becomes valuable only when estimating the residual distribution more finely than the bracket width.

---

# 8. Historical price snapshots are the next important addition

The label tells us forecast accuracy. Making money requires the price at the same information time.

For each month sample the full ladder at economically meaningful stages:

1. month end;
2. ERSST-v5 first availability;
3. ERA5T full-month availability;
4. latest GHCN qcf update before NASA release;
5. 6h before release;
6. 1h before release.

Then calculate:

`EV_i(t) = P_replica(bucket_i | info_t) - executable_all_in_cost_i(t)`.

This tells us **when** the climate model becomes valuable enough to trade, not just whether it eventually predicts the winner.

---

# 9. Highest-value model comparison

Do not start with many climate indices.

Test four objects:

### A. Market only

Normalized Polymarket ladder.

### B. ERA5T basis

A simple historical mapping from ERA5T monthly global anomaly to first-release GISTEMP bracket probabilities.

### C. ERSST + land basis

Use early ERSST-v5 plus a simple land/reanalysis estimate.

### D. Direct NASA replica

Current GHCN qcf + ERSST-v5 through published GISTEMP code.

Expected ordering near release should be D > C/B if the upstream inputs are already sufficiently complete. Measure it rather than assume.

---

# 10. First-release revision uncertainty is itself a distribution

A direct replica run several days before NASA publication may differ from first publication because additional GHCN data arrives.

Let:

`delta(t) = G_NASA_first - G_replica_using_files_available_at_t`.

Across historical/live dry runs, estimate the empirical distribution of `delta` by days/hours before release.

Then:

`G_first_distribution(t) = G_replica(t) + empirical_delta_horizon`.

This is the entire uncertainty model.

If the standard residual near release is much less than the bracket width, the strategy becomes high confidence without sophisticated statistics.

---

# 11. Exact objective

For each information stage and historical contract:

1. build probability over the contract's listed brackets;
2. compare with contemporaneous market prices;
3. buy any expression with positive net EV at available depth;
4. measure dollar PnL and capital lock.

Rank stages by:

`expected dollars per month`.

The key discovery may be that D+5 has wider edge but lower certainty, while release morning has tiny uncertainty but only a small residual market mispricing. Whichever produces more executable dollars wins.

---

# Bottom line

Polymarket itself gives us a clean **20+ month settlement-faithful first-release label set** spanning multiple anomaly regimes and several million-dollar contracts.

That removes one of the hardest historical-data problems for the climate strategy.

The next decisive dataset is simply the **upstream input / market-price timeline** for those same months. If a tiny NASA-replica model consistently identifies the paid bracket before market prices converge, this is likely the highest-capacity weather edge in the project.