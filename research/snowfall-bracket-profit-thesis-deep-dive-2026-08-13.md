# Snowfall bracket probability thesis — deep dive

Snapshot: **2026-08-13**

## Verdict

Among the newly explored Weather families, short-horizon **NYC snowfall amount ladders** deserve the highest research priority.

The reason is not merely that snow is forecastable. The contract geometry, resolver, public probability products and demonstrated market scale align unusually well:

- a January 24–26, 2026 Central Park snowfall ladder accumulated about **$1.448M** of volume across seven exact amount brackets;
- the winning bracket was **10–12 inches**;
- settlement used the sum of NOAA/NWS Central Park `New Snow (IN)` values for the three specified dates;
- WPC already publishes point-in-time probabilistic snowfall distributions at 24/48/72-hour horizons, including threshold exceedance probabilities and percentile accumulations;
- during the storm, observed snowfall converts most of the problem from “forecast the storm” into “forecast the remaining increment before the resolver closes.”

This is a much cleaner starting point than building a custom snowfall model from raw global ensembles.

Official sources:

- Polymarket Jan 24–26 event: https://polymarket.com/event/how-many-inches-of-snow-in-nyc-this-weekend-jan-24-26
- WPC PWPF: https://www.wpc.ncep.noaa.gov/pwpf/
- WPC PWPF methodology: https://www.wpc.ncep.noaa.gov/pwpf_24hr/about_pwpf_productsbody.html
- NWS Central Park climate data: https://www.weather.gov/wrh/climate?wfo=okx

---

## 1. Contract probability is exactly a snowfall CDF problem

Let `S` be the final resolver snowfall total for the contract window.

For an interior bracket `[L,U)`:

`q_[L,U) = P(L <= S < U) = F(U^-) - F(L^-)`

where `F(s)=P(S<=s)` and the left-limit notation preserves the rule that an exact boundary resolves to the **higher** bracket.

For the bottom bracket `<L`:

`q_<L = F(L^-)`.

For the top bracket `>=L`:

`q_>=L = 1 - F(L^-)`.

Therefore one coherent CDF prices the entire ladder. Individual binary models are unnecessary and can create incoherent probabilities.

The first goal is not “predict the winning bucket.” It is to estimate `F` more accurately, and earlier, than the market.

---

## 2. Use WPC as the prior distribution, not a point forecast

WPC's Probabilistic Winter Precipitation Forecast (PWPF) is unusually well matched to Polymarket snowfall brackets.

The operational methodology constructs a **skew-capable binormal PDF** at each grid point. The WPC deterministic forecast is used as the mode, the position of that forecast within the ensemble determines skewness, and ensemble variance controls dispersion.

Public products include:

- probabilities of snowfall exceeding fixed thresholds;
- 5th, 10th, 25th, 50th, 75th, 90th and 95th percentile accumulations;
- 24-hour, 48-hour and 72-hour windows.

This means a first production-quality research model can start from the public WPC distribution instead of inventing uncertainty from deterministic snowfall maps.

### Practical reconstruction

At the resolver point, collect:

`(x_0.05, x_0.10, x_0.25, x_0.50, x_0.75, x_0.90, x_0.95)`

and any available direct exceedance probabilities such as:

`P(S>=2), P(S>=4), P(S>=8), P(S>=12), P(S>=18), ...`

Construct a monotone CDF `F_WPC(s)` constrained by both percentile and exceedance points.

The smallest robust implementation is monotone interpolation rather than a new meteorological model. PCHIP/isotonic interpolation over the CDF points is enough for the first test.

---

## 3. Resolver calibration is the real model

WPC forecasts gridded snow accumulation. Polymarket settles on the Central Park climate report.

Those are not identical objects.

The economically useful model is therefore:

`P(Central_Park_resolver_total | WPC_distribution, regime)`.

For historical storm `n`, let final resolver total be `y_n` and the contemporaneous WPC CDF be `F_n`.

Compute the probability integral transform:

`u_n = F_n(y_n)`.

A perfectly calibrated forecast gives `u_n ~ Uniform(0,1)`.

Learn a calibration transform `G_h,r(u)` by:

- forecast horizon `h`;
- precipitation-type regime `r` (all-snow versus mixed/sleet-prone at minimum).

Then:

`F_cal(s) = G_h,r(F_WPC(s))`.

Start with one of:

- empirical/isotonic calibration;
- beta calibration;
- a simple location/scale correction to WPC snowfall if sample size is small.

Do not begin with a neural net. The key systematic errors are likely resolver-location basis, coastal mixed precipitation and horizon-dependent spread.

---

## 4. Mixed precipitation is the main NYC regime variable

The January 2026 storm is a useful example because NWS discussions explicitly shifted attention toward sleet/mixing near the coast while inland snow remained higher.

That matters because narrow 2-inch brackets are extremely sensitive to precipitation-type error.

A compact mixture model is:

`F(s) = w * F_snow(s) + (1-w) * F_mixed(s)`

where `w` is the probability that Central Park remains primarily snow through the critical high-QPF period.

Useful state for `w`:

- surface temperature/dew point;
- 925/850/700 hPa thermal profile;
- warm-nose probability;
- coastal low track;
- WPC/NWS precipitation-type language;
- observed sleet/rain transition upstream and locally.

The parameter only earns a place if it improves resolver calibration beyond the WPC distribution itself.

---

## 5. The probability problem simplifies dramatically once snow starts

Decompose final resolver total at time `t` as:

`S_final = A_t + U_t + R_t`

where:

- `A_t` = snow already incorporated into trusted official climate state;
- `U_t` = snow that has physically occurred / is strongly indicated by official observations but has not yet appeared in the contractual climate total;
- `R_t` = future snow still to fall.

The uncertainties differ sharply.

### Before the storm

Almost all variance is in `R_t`.

Use calibrated WPC/NBM/ensemble guidance.

### During the storm

`U_t` becomes important. Radar, official observations and local reports constrain what has already accumulated.

### Near the end

After an official Central Park accumulation `O_t`, the relevant bucket probability is simply a remaining-increment probability.

For example, if the official/near-official total is 11.4 inches:

`P(10–12 wins) ~= P(R_t < 0.6)`

`P(12–14 wins) ~= P(0.6 <= R_t < 2.6)`.

This is much easier than forecasting a 10–14 inch storm from scratch and is likely where resolver-aware research can become most precise.

---

## 6. Historical Polymarket evidence is large enough to matter

The January 24–26 event is not a thin curiosity.

Final event volume was about **$1,447,818**:

| Bracket | Final volume | Result |
|---|---:|---|
| <4 | ~$184k | No |
| 4–6 | ~$138k | No |
| 6–8 | ~$135k | No |
| 8–10 | ~$198k | No |
| **10–12** | **~$328k** | **Yes** |
| 12–14 | ~$224k | No |
| 14+ | ~$241k | No |

This is enough capacity that modest probability improvements can matter economically.

Indexed snapshots also show the eventual 10–12 winner trading far below certainty earlier in the event. That is evidence of substantial probability movement, not yet proof that the move was predictable at the same clock time.

The decisive study is point-in-time alignment of WPC/NWS vintages with the corresponding executable Polymarket state.

---

## 7. A hard point-in-time experiment

For the January 24–26 event, reconstruct every useful information vintage from listing through storm end.

For each timestamp `t` store:

- WPC 72h/48h/24h snowfall CDF at Central Park;
- direct WPC threshold probabilities;
- latest NWS OKX snowfall range and ptype language;
- precipitation-type regime state;
- official/near-official observed Central Park snowfall;
- Polymarket full ladder bid/ask/price history where recoverable;
- market volume/trades;
- final resolver total.

Compute:

`q_i(t)` for every bracket.

For a hypothetical taker buy at ask `a_i(t)`:

`edge_taker_i(t) = q_i(t) - a_i(t) - 0.05*a_i(t)*(1-a_i(t))`.

For a passive fill at price `p`:

`markout_h = q_i(t+h) - p`

and empirically estimate fill-conditioned markout once L2/fill data exist.

Historical minute price is screening evidence only; do not pretend it is historical executable depth.

---

## 8. What should create persistence

The candidate edge has several structural reasons to persist:

1. **Resolver specificity** — Central Park climate snowfall is narrower than “NYC snowfall.”
2. **Distributional skill** — public discussion often quotes one amount/range; the contract needs full bracket probabilities.
3. **Mixed-precip nonlinearities** — small track/thermal changes redistribute large probability mass across adjacent brackets.
4. **Publication basis** — snowfall already physically observed can precede the finalized climate field.
5. **Ladder coherence** — all brackets must map to one CDF; traders may price buckets piecemeal.
6. **Large episodic information revisions** — storm track and ptype shifts can move many cents quickly.

The mechanism is not “NOAA is secret.” The data are public. The edge, if present, is faster resolver-specific probability transformation than the marginal market participant.

---

## 9. Market-opening interaction

The January 24–26 market opened on January 21 at 2:12 PM ET. NWS discussion earlier that day was already reporting increasing snow probabilities and improving guidance agreement.

Therefore a useful probability prior existed **before the market was created**.

For recurring storm markets, maintain `F_cal(s)` even if no Polymarket event exists yet. When a ladder appears, the research state already contains a coherent resolver probability vector rather than beginning forecast work after listing.

Do not infer profit from visually incoherent displayed probabilities: Polymarket displays last trade rather than midpoint when spreads exceed $0.10. Opening-market evaluation must use executable bid/ask/depth.

---

## 10. Snow research priority

Evidence grade:

- demonstrated market capacity: **very high for Weather (~$1.45M in one 3-day NYC ladder)**;
- resolver clarity: **high**;
- public probabilistic forecast quality: **high**;
- point-in-time archiveability: **high**;
- cumulative/observed-state simplification: **high**;
- direct historical net-edge evidence: **not yet established**.

### Smallest decisive next research measurement

Reconstruct the January 24–26 event at every WPC/NWS forecast vintage and compare the calibrated bracket vector against the market path.

If the resolver-calibrated WPC distribution repeatedly moves before the market—and especially if the market underreacts to ptype/observed-snow updates—snow becomes a first-class seasonal strategy rather than an auxiliary Weather market.
