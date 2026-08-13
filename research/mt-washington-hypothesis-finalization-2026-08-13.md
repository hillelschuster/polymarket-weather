# Mt. Washington wind thresholds — hypothesis finalization

Snapshot: **2026-08-13**

## Verdict

Mt. Washington is the cleanest structural non-temperature Weather family, but current August 2026 market liquidity is still very small. The active August event is therefore most useful as a **live research instrument** for resolver/source mapping and threshold coherence, not yet as evidence of scalable capacity.

The July event demonstrated that this family can attract materially more volume; current August conditions let the project collect point-in-time evidence before a larger future event.

---

## 1. Contractual object and current active market

The August 2026 Polymarket event resolves from the highest whole-mph summit wind speed published by Mount Washington Observatory in its monthly F6 records, with revisions considered until the first following-month datapoint.

Official Polymarket event:

- https://polymarket.com/event/highest-mtpt-washington-wind-speed-in-august-20260727152349919

The indexed snapshot on August 13 showed only about `$252` total volume, so current capacity is negligible compared with the July event and with the large snowfall markets.

Mount Washington Observatory publishes:

- real-time summit conditions;
- 24-hour/current statistics;
- twice-daily Higher Summits Forecast;
- monthly F6 archives from 2005 onward.

Official sources:

- https://mountwashington.org/weather/
- https://mountwashington.org/weather/mount-washington-weather-archives/monthly-f6/

The archive page describes the F6 forms as raw daily weather summaries from the summit station.

---

## 2. Exact nested-threshold identity

Let `W` be the final monthly maximum gust and thresholds `K1 < K2`.

The events are nested:

`{W >= K2} subset {W >= K1}`.

Therefore:

`q(K1) >= q(K2)`.

More strongly, the portfolio:

`YES(W >= K1) + NO(W >= K2)`

has terminal payout:

- `$1` if `W < K1`;
- `$2` if `K1 <= W < K2`;
- `$1` if `W >= K2`.

Hence its fair value is:

`1 + P(K1 <= W < K2)`

or:

`1 + q(K1) - q(K2)`.

This identity is independent of any wind model.

Research should therefore preserve simultaneous threshold prices and test whether observed market states are coherent with a single latent distribution over `W`.

---

## 3. One latent CDF should price every threshold

Define monthly maximum CDF:

`F_W(w) = P(W <= w)`.

Then for threshold `K`:

`q_K = P(W >= K) = 1 - F_W(K-)`.

The full seven-threshold event can be represented by one monotone survival curve rather than seven independent binary models.

This makes calibration diagnostically strong: if market threshold prices cannot be fit by any plausible monotone survival curve after accounting for spreads, there is a structural inconsistency or display/liquidity artifact worth investigating.

---

## 4. Running maximum collapses lower-threshold uncertainty

Let `M_t` be the trusted running monthly maximum through time `t`.

For any threshold `K <= M_t`:

`P(W >= K) = 1`

provided the live source is known to map reliably into the contractual F6 record.

For uncrossed threshold `K > M_t`, only future gust opportunities matter.

A simple event-hazard form is:

`q_K(t) = 1 - product_j (1 - h_j(K))`

where `j` indexes remaining high-wind synoptic opportunities.

For small hazards:

`q_K ~= 1 - exp(-Lambda_K)`.

This is preferable to a normal distribution over monthly maximum because the maximum is driven by discrete frontal/cyclone/mountain-wave events.

---

## 5. The most important resolver-basis measurement

The contract resolves from F6, but the Observatory exposes current summit conditions earlier.

Research must estimate:

`P(F6_daily_or_monthly_max >= K | live summit source first showed >= K)`.

For every live threshold approach/crossing, record:

- raw current summit gust and timestamp;
- local first-seen timestamp;
- 24-hour summary if available;
- nightly F6 value after publication;
- final monthly F6 value;
- any pre-cutoff revision.

The current August market is useful precisely because this mapping can be observed prospectively even with little trading volume.

---

## 6. Historical distribution has unusually good source depth

Mount Washington Observatory provides F6 data from 2005 onward and broader long-term normals/extremes. Its archive states that August's record peak gust is 147 mph, set in 2020.

Official source:

- https://mountwashington.org/weather/mount-washington-weather-archives/

The Observatory also states that minute-resolution air-temperature data and long histories of other measurements can be requested, though most research data requests may involve a cost.

Official source:

- https://mountwashington.org/research/data-request/data-availability/

The high-value historical reconstruction is calendar-month specific:

- monthly maximum distribution;
- distribution of date of monthly maximum;
- threshold-cross frequency by date;
- probability of later higher maximum conditional on current running max;
- event type responsible for each extreme gust.

Do not use annual wind-extreme frequencies directly as August priors.

---

## 7. Forecast component should model discrete opportunities

The twice-daily Higher Summits Forecast is station/terrain specific and should be tested against broad numerical guidance.

For each forecast issue preserve:

- issue time;
- wind/gust range or language;
- strongest expected period;
- direction;
- relevant synoptic feature;
- realized next-48h F6 maximum.

Then estimate event-specific threshold hazards rather than a generic monthly mean.

One possible compact state is:

`Lambda_K = sum_j lambda_j * P(gust_j >= K | forecast_j)`.

The exact parameterization matters less than maintaining one coherent survival curve across all thresholds.

---

## 8. Current August market is a useful dry research control

The active August event currently combines:

- exact live resolver source;
- seven nested thresholds;
- low current volume;
- the remainder of the month still unresolved.

Because volume is so low, it should not be used to infer scalable profit. It can still answer:

1. whether live summit gusts map cleanly into nightly F6;
2. whether displayed/recorded threshold probabilities respect nesting after considering bid/ask data;
3. whether threshold crossings reach F6 before/after market adjustment;
4. how the Higher Summits Forecast changes the implied survival curve through time.

This is high-value preparation for a later higher-capacity month.

---

## 9. Falsification / downgrade criteria

Downgrade the thesis if:

1. live summit conditions frequently differ materially from later F6 maxima near market thresholds;
2. F6 revisions before cutoff make live crossing inference unreliable;
3. future threshold hazards cannot be calibrated with enough precision to distinguish adjacent 5-mph thresholds;
4. apparent threshold inconsistencies disappear when using actual executable bid/ask rather than displayed probabilities;
5. larger-volume July-like events do not recur;
6. the only structural violations occur at negligible depth.

---

## 10. Final research deliverable

The Mt. Washington hypothesis is finalized when the project has:

- a live-current-source to nightly-F6 basis table from the active August market;
- a historical August/month-specific threshold survival prior;
- a coherent one-CDF representation of all threshold probabilities;
- prospective market-state records around any new running-max/threshold event;
- evidence separating pure threshold identities from model-dependent interval value.

This can be gathered now even though current market capacity is low.