# Final hypothesis readiness matrix — 2026-08-13

## Executive verdict

The Weather research portfolio is sufficiently mature that broad discovery should stop being a prerequisite for implementation work.

The remaining research is **lane-specific finalization**: resolve the smallest uncertainty that can still reverse the profitability conclusion.

Current ranking by closeness to implementation-quality evidence:

1. **T+0 resolver/source repricing** — closest; live synchronized evidence already exists.
2. **Market-opening price discovery** — easiest new lane to observe prospectively every day.
3. **AIFS early-revision timing** — easy to log prospectively and reusable across many temperature markets, but source-field limitations are now explicit.
4. **Snowfall brackets** — strongest demonstrated new-family capacity; needs one strict historical resolver-CDF reconstruction and future full-distribution capture.
5. **Mt. Washington wind thresholds** — cleanest structural math; active August market is useful for source/F6 research but currently very low capacity.
6. **Spatial one-report-ahead nowcast** — enhancement after exact-station source advantages are exhausted.

This order distinguishes **readiness** from ultimate capacity. Snowfall may ultimately have much larger dollar capacity than opening or AIFS, but it is less immediately observable in August.

---

## 1. Readiness matrix

| Lane | Strongest evidence already present | Remaining research blocker | Can measure now? | Main falsifier |
|---|---|---|---:|---|
| T+0 resolver/source | live source-to-book lag + historical replications | fastest trustworthy source and resolver basis | **yes** | market reprices before source arrives / no stale depth |
| Market opening | recurring creation schedule + pre-existing forecast information | first executable book vs frozen pre-list q | **yes** | books efficient immediately / apparent errors only UI artifacts |
| AIFS timing | official AIFS-vs-IFS dissemination asymmetry | exact first-seen lead + value of 6-hour instantaneous fields | **yes** | no incremental information after market conditioning |
| Snow brackets | ~$1.448M NYC case + WPC probability products | point-in-time WPC->Central Park CDF + price alignment | historical now; full live when snow recurs | resolver basis too wide / market already prices revisions |
| Mt Washington | exact nested-threshold math + active resolver source | live summit -> F6 basis + meaningful threshold depth | **yes** | live source unreliable vs F6 / no economic depth |
| Spatial nowcast | physical mechanism + existing T+0 cases | incremental next-report skill beyond direct source/market | yes | no incremental Brier/log-loss improvement |

---

## 2. T+0: research is no longer the main blocker

Files:

- `research/live-nyc-source-book-latency-2026-08-12.md`
- `research/us-t0-feed-priority-2026-08-12.md`
- `research/t0-finalization-research-2026-08-13.md`

Already known:

- an actual source-first-seen to CLOB lag was observed live;
- historical markout replications include positive and negative controls;
- hard-elimination and soft-survival states are mathematically defined;
- several exact-station international precursor feeds have been identified.

The highest-value remaining research is a **source race**, especially for U.S. stations:

`MADIS OMO/LDM vs AWC vs NOAA TXT vs market repricing`.

For a chosen resolver/source pair, research is effectively complete once:

- first-seen latency is measured;
- source-to-contract resolver basis is stable enough around bucket boundaries;
- repeated post-source stale capacity exists.

Do not delay the entire project for a universal city/source solution. Source quality can be ranked per city.

---

## 3. Market opening: best immediate second dry-research lane

Files:

- `research/market-opening-efficiency.md`
- `research/market-opening-profit-thesis-deep-dive-2026-08-13.md`
- `research/market-opening-hypothesis-finalization-2026-08-13.md`

The research question is unusually cheap because `q_pre` can be computed before listing and frozen.

The only decisive evidence missing is:

`frozen pre-list q -> first executable L2 -> convergence path`

with post-list weather releases timestamped separately.

This lane should not require new meteorological research. If first books are already efficient, reject quickly. If not, the recurring daily listing schedule makes the finding highly reusable.

One unresolved API detail is whether Polymarket's `new_market` WebSocket event can be used as an unscoped global discovery feed; current docs show `new_market` but also show subscriptions initialized with known asset IDs. Treat global discovery behavior as unverified. Narrow keyset event/market discovery is a robust research fallback.

---

## 4. AIFS: timing advantage is real in distribution policy; direct-max signal is not

Files:

- `research/aifs-public-timing-profit-thesis-2026-08-13.md`
- `research/aifs-hypothesis-finalization-2026-08-13.md`

The main correction from deeper research is important:

- open AIFS is distributed as forecasts are produced;
- open IFS is distributed after the real-time dissemination schedule;
- but the current free AIFS open subset provides 6-hourly instantaneous 2m temperature rather than the IFS open extrema fields.

Therefore the exact final test is:

`actual AIFS field first_seen -> station-calibrated q revision -> market response -> later IFS/consensus revision`.

AIFS is worth keeping if it predicts later resolver/consensus movement **after conditioning on current Polymarket prices**.

This can be logged prospectively immediately and should not block T+0 work.

---

## 5. Snowfall: highest-capacity new thesis needs one rigorous reconstruction

Files:

- `research/snowfall-cumulative-state-alpha.md`
- `research/snowfall-bracket-profit-thesis-deep-dive-2026-08-13.md`
- `research/snowfall-hypothesis-finalization-2026-08-13.md`

The January 24–26 Central Park bracket event's ~$1.448M total volume makes it the most important new-family historical study.

The missing evidence is not another source list. It is one strict point-in-time timeline containing:

- WPC probability vintages actually available at the time;
- Central Park resolver calibration;
- `A_t + U_t + R_t` snowfall state;
- Polymarket price path through each forecast/observation/publication update;
- final resolver value.

Historical WPC winter-weather archives and GIS probability products make meaningful reconstruction feasible, although full historical current-style percentile/GRIB availability should not be assumed without verification.

If that reconstruction shows large fair-value revisions systematically preceding market movement, snow should become a major seasonal implementation lane when markets recur.

---

## 6. Mt. Washington: use August as a resolver laboratory

Files:

- `research/mt-washington-wind-data-semantics.md`
- `research/mt-washington-threshold-profit-thesis-2026-08-13.md`
- `research/mt-washington-hypothesis-finalization-2026-08-13.md`

The August 2026 market is active now but its indexed volume is only around a few hundred dollars, so it should not be treated as a capacity opportunity.

It is still valuable for research because it allows prospective measurement of:

`live summit gust -> nightly F6 -> final F6`

on the exact contractual source.

The nested-threshold identity remains exact:

for `K1 < K2`,

`YES(W>=K1) + NO(W>=K2)`

has fair value:

`1 + P(K1 <= W < K2)`.

Therefore the event is useful for studying whether market threshold states are coherent with one latent survival curve and whether live summit data reaches the contractual F6 state predictably.

If future higher-volume months recur, this research becomes immediately reusable.

---

## 7. Spatial nowcast should not block first deployment research

Files:

- `research/spatial-and-cross-market-propagation.md`
- `research/spatial-one-report-ahead-profit-thesis-2026-08-13.md`

This remains a potentially strong enhancement where the resolver station reports slowly.

But exact-station high-frequency sources dominate nearby-station inference whenever they exist and arrive early.

Only promote spatial features that improve next-resolver-report probability after conditioning on:

- resolver's own recent observations;
- direct fast source if available;
- forecast state;
- current market probability.

The value of spatial research is incremental crossing prediction, not complexity for its own sake.

---

## 8. Common missing metric: stale capacity after information

Across all fast-information lanes, the project should report the same object:

`C_tau(e)` = executable quantity still available at least `e` probability/value away from the post-information fair state at `tau` seconds/minutes after source first seen.

This is more useful than event volume.

Examples:

- T+0: stale depth after new station observation;
- AIFS: stale depth after early model revision;
- opening: initial depth away from frozen pre-list q;
- snowfall: stale depth after WPC/observed-snow update;
- wind: threshold depth after source/F6-relevant state update.

Together with event frequency, this lets research compare expected scalable dollars across unrelated Weather families.

---

## 9. Common missing metric: probability-model uncertainty

Every apparent q-price difference should carry a model uncertainty estimate.

Let model fair probability be `q_hat` with uncertainty interval/distribution.

The useful signal is not merely:

`q_hat - price`.

It is whether the economic discrepancy remains material relative to:

- calibration uncertainty;
- resolver-basis uncertainty;
- source-timing uncertainty;
- executable spread/fee/depth.

Hard-elimination T+0 states are attractive partly because model uncertainty collapses to near zero once resolver basis is trusted. Snowfall and AIFS need wider uncertainty margins.

---

## 10. What no longer needs to block implementation work

Do not wait for:

- a universal Weather model;
- every city/resolver source;
- complete historical L2 for every market;
- Rust migration;
- every new Weather family to be backtested;
- spatial nowcasting;
- a large generic database/research platform.

Those items may become useful later, but none is required to test the already-defined economic mechanisms.

The research portfolio now has enough specificity that the next unanswered questions are mainly **first-seen source quality, point-in-time fair probability, stale executable capacity, and live fill behavior**.

---

## 11. Research conclusion

The project is closest to real economic evidence by treating the hypotheses asymmetrically:

- **T+0:** finish the source/basis race and measure stale capacity;
- **Opening:** begin prospective first-book measurement immediately;
- **AIFS:** log exact first-seen revisions immediately;
- **Snow:** complete the January 2026 point-in-time reconstruction before next winter event;
- **Mt Washington:** use active August as a source/F6 structural laboratory;
- **Spatial:** add only after direct-source residual value is measured.

The common decision standard is no longer “is the weather forecast good?” It is:

> Does resolver-relevant information become available to us before enough of the executable market has incorporated it, with enough repeatable capacity to create meaningful expected net dollars?
