# T+0 threshold survival — reduce same-day temperature trading to the next integer

Snapshot: **2026-08-12**

Purpose: isolate the smallest T+0 probability problem implied by actual profitable Weather-specialist flow.

## Verdict

Once the named resolver airport has already reported the current whole-degree maximum bucket `k`, a same-day exact-high market often collapses from a full weather-distribution problem into a much simpler question:

> **Will the resolver cross into `k+1` before the local day is locked?**

For the current bucket, the fair value is approximately the survival probability of *no higher resolver print*, adjusted for source basis/revisions.

This is directly observed in a transaction between two profitable Weather specialists on **Wellington July 21, 2026**:

- active taker `balthazar` bought the **11°C YES** bucket at ~5.91¢ raw / ~6.19¢ all-in at **01:56:10 UTC = 13:56:10 local NZST**;
- official AviationWeather.gov station observations for `NZWN` were **52°F ≈ 11.1°C at 01:30 UTC** and again **52°F ≈ 11.1°C at 02:00 UTC**;
- at **02:30 UTC**, `NZWN` printed **54°F ≈ 12.2°C**, crossing the next whole-degree threshold only **34 minutes after the trade**;
- passive specialist `Poligarch` supplied part of the complementary liquidity at zero maker fee in the same exchange match.

The individual balthazar trade lost its 11°C thesis if Wunderground incorporated the later 12°C airport report in the resolver history, but that is not the main result. The trade identifies the exact probability object a specialist was willing to pay for during the local peak window.

The research target should therefore be a **next-degree hazard/survival model**, not a generic same-day forecasting stack.

---

# 1. Direct transaction evidence

Transaction:

`0xfde6e19660e6a98edd7328dfc68c2e4841e82b93bf7fc346c2827cc6cb5a3213`

Timestamp:

`2026-07-21 01:56:10 UTC`.

Local Wellington time in July is UTC+12:

`2026-07-21 13:56:10 NZST`.

Polymarket event:

**Highest temperature in Wellington on July 21?**

Resolver rule:

- Wellington Intl Airport Station;
- Wunderground `NZWN` daily history;
- whole degrees Celsius;
- revisions count until the first following-day datapoint appears.

Polymarket source:

https://polymarket.com/event/highest-temperature-in-wellington-on-july-21-2026

### Active taker

`OrdersMatched.takerOrderMaker`:

`0x5a218C7AD04135830a45c41AAed7294Df7809318`

Polymarket identifies this trader as **balthazar**, which appears in profitable Weather-leaderboard snapshots.

The transaction action identifies the trade as roughly:

- BUY **29.780165 11°C YES**;
- raw pUSD consideration ≈ **$1.759999**;
- raw price ≈ **5.91¢/share**;
- wallet pUSD transfer including fee ≈ **$1.842789**;
- implied fee ≈ **$0.082790**;
- all-in cost ≈ **6.188¢/share**.

Thus the taker fee consumed roughly **4.7% of raw cash notional** on this cheap-tail entry.

The important inference is that this was not a sub-point discrepancy. The trader needed to believe the 11°C bucket retained materially more than ~6.2% probability to justify crossing.

### Passive counterparty

Poligarch:

`0xb40e89677d59665d5188541ad860450a6e2a7cc9`

is a matched passive maker in the same transaction:

- fee = `0`;
- pUSD contribution ≈ `9.400590`;
- relevant complementary token amount ≈ `9.99`;
- effective price ≈ **94.1¢**.

Raw complementary prices sum to approximately `$1`, consistent with the CTF Exchange V2 two-BUY complete-set MINT matching path.

This transaction therefore directly links:

- an information-consuming Weather taker;
- a passive Weather liquidity specialist;
- the exact same T+0 threshold state.

---

# 2. Official airport state around the trade

NOAA AviationWeather.gov provides worldwide METAR observations and its indexed tabular archive for `NZWN` shows:

| UTC | Local NZST | Temperature |
|---|---|---:|
| 2026-07-21 01:00 | 13:00 | 52°F ≈ 11.1°C |
| **01:30** | **13:30** | **52°F ≈ 11.1°C** |
| **01:56 trade** | **13:56** | — |
| **02:00** | **14:00** | **52°F ≈ 11.1°C** |
| **02:30** | **14:30** | **54°F ≈ 12.2°C** |
| 03:00 | 15:00 | 52°F ≈ 11.1°C |
| 03:30 | 15:30 | 52°F ≈ 11.1°C |
| 04:00 | 16:00 | 52°F ≈ 11.1°C |

Official AviationWeather data/API documentation:

https://aviationweather.gov/data/api/

Indexed NZWN observation page:

https://aviationweather.gov/data/metar/?hours=24&ids=NZWN&tabular=1

This is a particularly informative path:

- 11°C had already been observed before the trade;
- the next routine observation after the trade was still in 11°C territory;
- the next integer threshold was crossed only at the subsequent half-hour report;
- the crossing was brief: later routine reports returned to ~11°C.

That is exactly the kind of extrema event where a faster 1-minute airport feed can outperform 30-minute METAR monitoring.

---

# 3. The probability object

Let:

`M_t` = highest resolver-equivalent temperature observed so far;

`k` = current whole-degree resolver bucket already reached;

`u_k` = minimum source-equivalent state that would make the resolver show `k+1` rather than `k`;

`T` = resolver cutoff / end of relevant local day.

Define the first-crossing time:

`tau = inf{s > t : resolver_equivalent_temp_s >= u_k}`.

Then the current-bucket fair probability is approximately:

`q_k(t) = P(tau > T | information available at t)`

provided:

- `k` is already guaranteed to have been printed by the resolver/source mapping;
- lower outcomes are no longer feasible;
- no source revision can erase the existing `k` maximum.

More generally, include resolver/source-basis uncertainty:

`q_k(t) = P(final_resolver_bucket = k | direct feed path, resolver path, forecasts, time)`.

This is a survival-analysis problem.

---

# 4. Why this is simpler than a full T+0 daily-max model

Before any meaningful daytime observation, we need a probability distribution over many final maxima.

After the station has already reached a near-modal bucket during the peak window:

- all lower maxima are impossible or nearly impossible;
- probability mass is concentrated in the current bucket and one/few higher buckets;
- the dominant question is whether enough additional heating occurs to cross the next integer;
- as time advances past climatological peak, the hazard of another whole degree falls rapidly.

That means the core signal can often be represented by one probability:

`P(next_degree_crossing before cutoff)`.

No large ML model is needed.

---

# 5. Minimal hazard model

At every direct observation time `t`, estimate:

`h(t, state) = P(cross k+1 before end | current state)`.

Then:

`q_current_bucket = 1 - h` approximately.

Useful state variables are deliberately small:

1. **distance to next resolver threshold** in 0.1°C/native source units;
2. current temperature;
3. running maximum;
4. 5/10/30-minute temperature slope;
5. local solar time / minutes from climatological peak;
6. cloud amount / shortwave radiation proxy if materially available;
7. wind direction/speed, especially marine/front regimes;
8. latest short-range forecast maximum remaining today;
9. source-specific rounding/basis to the resolver;
10. whether the current max was a one-minute spike or sustained across reports.

Start with an empirical nearest-neighbor/bin estimator, not a complex survival package:

`P(cross | station, month, local-time bin, threshold distance, recent slope)`.

Only add variables that improve out-of-sample fee-adjusted PnL.

---

# 6. Even simpler empirical estimator

For each historical station-day and every observation snapshot after the running maximum enters whole-degree bucket `k`, record:

`minutes_to_local_peak`
`minutes_to_end`
`current_temp - running_max`
`distance_to_next_degree`
`temp_change_10m`
`temp_change_30m`
`cloud/wind bins if available`
`eventually_crossed_next_degree ∈ {0,1}`.

For a new state, estimate:

`p_cross = mean(eventually_crossed_next_degree among comparable historical states)`.

Then:

`q_k = 1 - p_cross`.

This estimator is interpretable, point-in-time safe, and easy to validate city by city.

---

# 7. Source-frequency advantage

The Wellington case highlights the key microstructure problem.

Routine AviationWeather `NZWN` METAR observations are visible at roughly 30-minute intervals in the reconstructed path.

MetService separately documents a **1-Minute Observations API** for Wellington Airport:

- station `93110 / NZWN`;
- air temperature available;
- observation every minute;
- typical transmission/ingestion ~30–40 seconds after observation;
- roughly 60 days of API history;
- commercial access.

Official MetService source:

https://about.metservice.com/our-company/our-services/data-services/1-minute-observations-api/

If a 1-minute feed had shown the temperature rising through the eventual 12°C-equivalent threshold before the 02:30 METAR, a trader using it could:

- avoid buying stale 11°C YES;
- cancel 11°C maker bids before they are adversely selected;
- buy 12°C / sell 11°C before slower participants reprice.

This is precisely why high-frequency direct source data has value even when it is not itself the contractual resolver.

---

# 8. Crossing-hazard execution rule

For current bucket YES at ask `a`:

`all_in_cost = a + taker_fee(a)`.

Trade only if:

`1 - p_cross - resolver_basis_uncertainty > all_in_cost + required_margin`.

For an owned current-bucket YES at bid `b`:

`sell if net_bid(b) > 1 - p_cross`.

For the next bucket `k+1`:

its fair value is not exactly `p_cross` because crossing `k+1` can continue into `k+2`.

A compact ladder decomposition is:

`P(final=k) = 1 - P(cross k+1)`

`P(final=k+1) = P(cross k+1) - P(cross k+2)`

`P(final=k+2) = P(cross k+2) - P(cross k+3)`

and so on.

Near the end of the peak window, only one or two crossing hazards may matter materially.

---

# 9. Why cheap current-bucket YES can be attractive

Suppose the current station maximum is already 11°C and the market offers 11°C YES at 5.9¢ raw.

With the observed balthazar fee, break-even was roughly 6.19%.

The trade only needs:

`P(no 12°C+ resolver print) > 6.19%`

for positive settlement EV before any later exit opportunity.

That is a low probability hurdle in percentage terms, although calibration errors in extreme tails can be large.

This helps explain why sophisticated Weather traders may buy low-priced exact buckets that look almost dead to participants watching only the modal forecast: once the current bucket is already physically printed, its residual probability can be materially larger than a stale few-cent quote if the heating window is nearly exhausted.

The Wellington example happened to cross 12°C later. A statistically useful test requires all analogous trades, including winners and losers.

---

# 10. Expected alpha sources inside the hazard

The highest-value deviations between our crossing probability and market price are likely to occur when the market uses coarse state information.

### A. Hidden sub-METAR rise

1-minute direct feed rises toward the next threshold between routine 30-minute reports.

Market still prices from last visible whole-degree airport report.

### B. Hidden cooling after a transient maximum

Direct feed shows the peak has already passed and temperature is falling; market still overprices another degree.

### C. Source rounding discontinuity

A 0.1°C direct temperature is very close to the resolver's whole-degree boundary. Correct source-basis mapping moves a large amount of probability abruptly.

### D. Cloud/wind regime change

A cloud break, sea-breeze onset, front or wind shift materially changes the remaining heating hazard before slower numerical guidance updates.

### E. Current-bucket overreaction

Market sees a new maximum and prices the current integer as almost certain, ignoring a still-material chance of another degree.

The same model can trade both sides of these errors.

---

# 11. Best city candidates for this specific strategy

The broader source research now suggests this ranking for **threshold survival**, which differs somewhat from generic forecasting priority.

## Tier 1

### Seoul / Incheon `RKSI`

KMA AMOS:

- exact resolver airport;
- minute-by-minute temperature;
- 0.1°C precision;
- history back to ~2005.

This is the cleanest dataset for building the hazard model immediately.

### Hong Kong / HKG

HKO provides running max/min based on 1-minute means, updated around every 10 minutes. This directly exposes the path-dependent state.

### Singapore / Changi

NEA minute-scale station temperatures plus API history since 2016.

## Tier 2

### Wellington / `NZWN`

Excellent 1-minute source but commercial and only ~60d directly retained by the API.

### Paris

Météo-France 6-minute observations; exact event/source regime must be mapped because Polymarket changed Paris station behavior in 2026.

### Amsterdam / Schiphol

KNMI 10-minute observations plus push notification.

### Helsinki-Vantaa / `EFHK`

FMI 10-minute exact-airport observations with long archive.

### Munich / `EDDM`

DWD station 1262 München-Flughafen has 10-minute live and historical temperature archives.

---

# 12. Production-fidelity backtest

For each resolved event-day and every direct-source update during the useful T+0 window:

1. reconstruct the resolver-visible max using only information published by that moment;
2. reconstruct the faster direct-feed state;
3. estimate `p_cross` from training history available before the event;
4. save the synchronized Polymarket bid/ask ladder;
5. simulate actual taker depth and maker fills;
6. settle against the event's correct source/version.

Main outputs:

`city × local_hour × current_bucket_age × threshold_distance ->`

- Brier/log loss for crossing;
- calibration;
- market-implied crossing probability;
- average executable residual;
- taker PnL;
- maker markout;
- capacity;
- dollars per capital-hour.

The most important curve is:

`edge as function of minutes since current bucket first printed`.

If the market systematically underprices current-bucket survival as the peak window closes, that is a directly tradable repeated edge.

---

# 13. Smallest live logic

For each active same-day temperature event:

`new direct observation`

`-> update running max and next threshold distance`

`-> compute p_cross(next degree)`

`-> convert to coherent current/next-bucket probabilities`

`-> compare with live all-in executable prices`

`-> cancel stale maker quotes immediately`

`-> cross only clear positive-EV depth`

`-> otherwise quote passively around q`

This is significantly smaller than a generic multi-model weather platform.

---

# 14. What the Wellington transaction proves and does not prove

### Proven / directly observed

- balthazar was the active/taker user in the exchange match;
- it bought 11°C YES around 13:56 local at ~5.91¢ raw / ~6.19¢ all-in;
- the named airport's routine report was ~11.1°C before and immediately after the trade;
- the airport printed ~12.2°C 34 minutes later;
- Poligarch supplied passive complementary liquidity with fee zero;
- the contract resolves whole-degree Wunderground history for the same airport.

### Inference

The most natural economic interpretation is that balthazar was buying the probability that the current 11°C maximum would survive without a subsequent 12°C+ resolver print.

### Not yet verified

- the exact 1-minute NZWN temperature path between 02:00 and 02:30;
- the exact Wunderground ingestion timestamp of the 12°C-equivalent observation;
- balthazar's proprietary forecast or intended exit rule;
- whether the final resolver was 12°C versus a different higher bucket from an earlier/later Wunderground observation not reconstructed here;
- the full PnL distribution of comparable balthazar trades.

Those gaps do not prevent using the case to define the correct statistical problem.

---

# Bottom line

The T+0 problem can often be reduced to one small, highly monetizable probability:

> **Given the exact resolver airport has already printed the current integer bucket, what is the probability it fails to cross the next whole-degree threshold before the resolver locks?**

The Wellington July 21 balthazar fill is direct specialist evidence for trading this object during the local peak window.

The best next empirical build is not more generic weather forecasting. It is a station-specific **next-degree crossing table** using minute/10-minute direct airport observations, synchronized with Polymarket books.