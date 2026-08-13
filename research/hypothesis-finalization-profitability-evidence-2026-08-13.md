# Hypothesis finalization — profitability evidence still required

Snapshot: **2026-08-13**

## Verdict

Broad Weather hypothesis generation is no longer the highest-value research activity.

The project is much closer to implementation if research now answers a short list of unresolved economic questions for the strongest lanes:

1. **T+0 resolver/source repricing** — already has live synchronized evidence; finalize source quality, basis and repeatability.
2. **Snowfall bracket probability** — strongest new-family capacity; finalize point-in-time resolver calibration and historical market response.
3. **ECMWF AIFS timing** — potentially reusable information lead; finalize exact public availability and incremental predictive value.
4. **Weather market opening** — cheap recurring hypothesis; finalize first-book price discovery and convergence.
5. **Mt. Washington wind thresholds** — clean structural math; finalize live-source-to-F6 basis and threshold-market coherence.

Spatial one-report-ahead nowcasting remains useful, but it is an enhancement after exact-station source work rather than a precondition for first implementation.

---

## 1. Common evidence ladder

Every thesis should pass the same sequence.

### A. Information exists point-in-time

Record separately:

- physical/valid time;
- source publication time if supplied by provider;
- local source first-seen time;
- market timestamp.

A thesis based on information that was not actually available yet is invalid regardless of backtest PnL.

### B. Information changes resolver probability

Let `q_before` and `q_after` be resolver-calibrated probability vectors before and after a source update.

The information must improve prediction of the exact contractual resolver object, not generic weather.

Useful evaluation:

- log loss;
- Brier score;
- calibration curves;
- PIT diagnostics for continuous distributions;
- error by bucket boundary;
- conditional results by city/regime/horizon.

### C. Market incorporates the same information later or incompletely

Measure:

`lead = market_material_reprice_time - source_first_seen_time`.

Positive lead is necessary for a pure latency thesis.

For slower valuation theses, measure whether the market's probability error relative to the resolver model shrinks after the information update.

### D. Economic magnitude is material

Do not rank research by percentage move alone.

For each opportunity preserve:

- size of probability revision;
- available market depth around the relevant time;
- spread;
- applicable fee schedule;
- duration of the discrepancy;
- later markout;
- eventual settlement outcome.

The comparison statistic should ultimately be expected net dollars per opportunity and expected opportunity frequency.

### E. Result is not one-event dependent

Track contribution of the largest event to cumulative evidence.

A promising rare-event family can still be valuable, but its expected opportunity frequency must be explicit rather than hidden inside one spectacular example.

---

## 2. Finalization criterion

A research lane is sufficiently specified for a dry implementation when all of the following are known:

- exact resolver object and rule cutoff;
- exact source or source ensemble;
- source first-seen timestamp can be recorded;
- deterministic mapping from current information to a probability vector or threshold probability;
- market token outcomes are explicitly mapped;
- relevant market state can be recorded point-in-time;
- historical/live evidence shows the probability information is not always incorporated immediately;
- the remaining unknown is primarily real fill/execution behavior rather than basic signal definition.

There is no requirement for an arbitrary number of days. Evidence should advance sequentially as the remaining uncertainty changes from signal validity to market response to live execution.

---

## 3. Cross-lane ranking metric

Use a common research value measure:

`LaneValue ~ opportunity_frequency * expected_net_dollars_per_opportunity * scalable_capacity`.

Keep distinct:

- forecast accuracy;
- information lead;
- market inefficiency magnitude;
- fillable capacity.

A very accurate signal with no market delay has little trading value. A huge percentage edge with $3 of depth may be inferior to a smaller repeated edge with thousands of dollars of depth.

---

## 4. Current Polymarket economics relevant to research

Current official Polymarket documentation states that Weather uses a taker fee rate of `0.05` in:

`fee = shares * feeRate * p * (1-p)`

while makers pay zero platform trading fee and the Weather maker rebate allocation is 25% of eligible taker fees.

Official sources:

- https://docs.polymarket.com/trading/fees
- https://docs.polymarket.com/market-makers/maker-rebates

Therefore historical research should preserve maker/taker attribution whenever possible and avoid treating gross price movement as net edge.

Polymarket also exposes realized maker rebate information by market/date/address, which means live research can later measure rather than assume rebate contribution:

- https://docs.polymarket.com/api-reference/rebates/get-current-rebated-fees-for-a-maker

---

## 5. Current data infrastructure relevant to finalization

Official Polymarket APIs currently expose:

- real-time market book and price updates over WebSocket;
- market lifecycle events including `new_market` when custom features are enabled;
- historical price data and batch price history;
- stable keyset market/event pagination;
- per-market fee/tick metadata.

Sources:

- https://docs.polymarket.com/market-data/realtime-data
- https://docs.polymarket.com/api-reference/markets/get-batch-prices-history
- https://docs.polymarket.com/api-reference/markets/list-markets-keyset-pagination
- https://docs.polymarket.com/api-reference/events/list-events-keyset-pagination

One important documentation ambiguity remains for market opening research: the market-stream examples require known token IDs even when `new_market` custom events are enabled. Therefore do not assume `new_market` is a global discovery stream until verified experimentally. The robust research fallback is narrow Weather discovery using keyset/tag/date filters.

---

## 6. Priority conclusion

Research effort should now be allocated to the **remaining unknown with the largest effect on expected dollars**, not evenly across all ideas.

Current order:

1. T+0 fast resolver source arrival and basis;
2. snowfall point-in-time reconstruction;
3. AIFS first-seen and incremental resolver signal;
4. prospective market-opening capture;
5. Mt. Washington source/F6 and threshold coherence.

The next files in this research pass specify the decisive measurements for each of these lanes.