# Ranked edge thesis

Snapshot: **2026-08-11**

This is a ranking of research hypotheses by expected value *if validated*, not a claim that each is already profitable.

## Tier 1 — likely core edge

### 1. Exact-station probabilistic calibration

**Thesis:** the market is often priced from public point forecasts / raw model outputs, while the tradable object is an exact discrete bucket at a specific station. The profitable transformation is forecast -> calibrated station-specific distribution -> settlement bucket.

Why it can persist:

- grid forecasts and airport stations have systematic local residuals;
- ensemble systems have bias and dispersion errors;
- model skill differs by city, lead time, season and weather regime;
- multi-model member counts are not comparable weights;
- raw probabilities are especially weak in tails, where payoff convexity is largest.

The basic model should therefore estimate a full CDF for the station daily maximum. EMOS/NGR-style postprocessing is a strong simple baseline because the literature explicitly targets ensemble bias and underdispersion.

**What would kill this thesis:** after point-in-time calibration and executable-price simulation, model-vs-market residuals are zero or negative after fees/spread.

### 2. Same-day conditional maximum / observation edge

**Thesis:** same-day markets become easier because the observed high is a hard lower bound on the final high, while remaining uncertainty shrinks rapidly. Public bot evidence also repeatedly focuses on T+0.

Let `M_obs(t)` be the highest station temperature observed so far and `M_future(t)` the maximum of all remaining observations. Then:

`M_final = max(M_obs(t), M_future(t))`

Any bucket below the already observed maximum should collapse to essentially zero subject to resolver/reporting semantics. More generally, probability must be recomputed from the conditional remaining-hours path distribution, not from the morning forecast.

The best same-day engine should use:

- latest METAR / official station observations;
- time of climatological daily peak;
- remaining hourly ensemble paths;
- cloud/radar/wind/sea-breeze/boundary-layer state where relevant;
- observed model error so far that day;
- exact resolver rounding/reporting behavior.

**Why attractive:** the informational half-life is short, so a thin niche book can lag an objective public observation.

### 3. Forecast-run latency

**Thesis:** scheduled model updates create discrete information shocks. If weather books are less watched than sports/crypto, prices may adjust slowly enough to monetize a new run.

Candidate catalysts:

- ECMWF ENS / AIFS ENS cycles;
- GEFS / NBM / regional model updates;
- METAR observations;
- local official weather-network updates.

The research question is not merely whether price moves after a run. It is:

`E[future mid / settlement value | forecast delta at t] - executable price at t`

as a function of seconds/minutes since the new data became available.

This edge may be largest in cities with enough liquidity to trade but too little attention to reprice instantly.

## Tier 1.5 — market-structure edge independent of superior weather forecasting

### 4. Probability-simplex / negative-risk relative value

A daily ladder has `K` mutually exclusive outcomes. Fair values satisfy:

`sum(q_i) = 1`

Polymarket's negative-risk mechanism links outcomes: one NO can be converted into YES shares for every other outcome.

Research checks:

- `sum(best_ask_yes_i + fees_i) < 1` -> buy-the-ladder candidate;
- `sum(best_bid_yes_i - fees_i) > 1` -> mint/convert-and-sell candidate, subject to exact CTF mechanics and executable depth;
- compare `NO_i` with the executable basket of `YES_j, j != i`;
- detect local shape violations: a market surface inconsistent with any plausible smooth temperature CDF;
- use our calibrated weather CDF to decide which leg of an inconsistency is actually wrong.

This is especially attractive because the signal comes from accounting identities before meteorological opinion.

### 5. Informed market making

**Thesis:** if we have better fair values, the highest-return implementation may be to provide liquidity around them rather than cross the spread.

Current Polymarket docs:

- makers pay zero platform trading fees;
- fee-enabled Weather markets use a taker fee curve with rate 0.05;
- 25% of collected Weather fees is allocated to maker rebates;
- some markets can also have explicit liquidity rewards.

Therefore quote PnL has four terms:

`forecast alpha + captured spread + maker rebate/reward - adverse selection`

The crucial weather-specific advantage is knowing when **not** to leave stale quotes up: before/after forecast runs, METAR updates, or a fast-changing same-day maximum.

This should be researched before assuming pure taker trading is optimal.

## Tier 2 — potentially large amplifiers

### 6. Wallet-derived alpha

Public weather winners provide a labeled dataset of decisions made by unknown private models.

Do not merely copy trades. Reverse-engineer them:

- city preference;
- lead time at entry;
- YES vs NO asymmetry;
- entry-price distribution;
- tail distance from forecast center;
- position sizing;
- maker/taker behavior where inferable;
- trade timing relative to forecast releases;
- whether they ladder adjacent buckets;
- whether they exit before settlement or hold;
- performance by city / price band / horizon / regime.

Then ask whether wallet action adds predictive information **after conditioning on our weather model and current market price**.

A useful form is:

`logit(P(outcome)) = weather_features + market_features + informed_wallet_flow`

If the wallet coefficient remains positive out of sample, the wallet is an information source rather than just a copy target.

### 7. Market-as-a-forecaster

Ignoring market price is also wasteful. The crowd may know things our model misses.

Instead of treating market sentiment as either sacred or useless, estimate when it adds information:

`logit(q_final) = a + b_w * logit(q_weather) + b_m * logit(p_market) + regime terms`

Potential regime terms:

- time to resolution;
- spread/depth;
- latest forecast-run age;
- city;
- observation availability;
- market concentration / wallet flow.

The target is not to beat the market on every contract. It is to identify contexts where weather data deserves more weight than price.

### 8. City/regime specialization

A universal model is convenient but likely leaves money behind. Each station has different failure modes:

- coastal sea breeze;
- urban heat island;
- elevation/grid mismatch;
- monsoon convection;
- fog/cloud burn-off;
- airport exposure;
- local sensor/reporting peculiarities.

Per-station residual structure should determine where capital goes. A smaller set of highly calibrated stations can outperform broad shallow coverage.

## Tier 3 — separate but important weather markets

### 9. Climate / monthly / record-temperature contracts

The weather leaderboard's biggest historical wins include monthly/global temperature anomalies and record-temperature contracts, not just daily airport highs.

These need a different model stack:

- reanalysis / climate index definitions;
- anomaly-baseline details;
- publication schedules and revisions;
- seasonal forecast systems;
- climate trend priors.

Do not mix their statistics with daily temperature ladders. They may nevertheless offer larger capacity and slower-moving information.

## Candidate behavioral mispricings to test, not assume

1. **Longshot bias / tail overpricing:** one public bot reports a profitable T+0 BUY_NO price-band regime and claims extreme YES outcomes were overpriced. This is self-reported and must be independently rebuilt from historical data.
2. **Round-number anchoring:** traders may overweight central point-forecast buckets instead of distributing probability over adjacent bins.
3. **Stale-run anchoring:** price may remain centered on an older deterministic run after ensemble consensus moves.
4. **Forecast-app anchoring:** retail may use city-center consumer forecasts while contracts resolve at airports.
5. **Adjacent-bucket inconsistency:** independently traded binary books can form an implausible shape even when their sum is near one.

## Priority ordering for eventual implementation

If the research holds up, the minimal profitable stack should probably be developed in this order:

1. exact event/station/rules parser;
2. point-in-time forecast + observation archive;
3. calibrated daily-max probability surface;
4. executable order-book / fee model;
5. forecast-release event study;
6. wallet reverse-engineering;
7. maker / cross-bucket optimizer.

That ordering is about information value, not software architecture.

## Sources

- Polymarket negative risk: https://docs.polymarket.com/advanced/neg-risk
- Polymarket fees: https://docs.polymarket.com/trading/fees
- Maker rebates: https://docs.polymarket.com/market-makers/maker-rebates
- Liquidity rewards: https://docs.polymarket.com/market-makers/liquidity-rewards
- ECMWF ENS guide: https://confluence.ecmwf.int/spaces/FUG/pages/673550376/Section+2A.1.2.1+Medium+Range+Ensemble+forecasts
- NOAA NBM probabilistic elements: https://vlab.noaa.gov/web/mdl/nbm-weather-elements
- Gneiting et al. (2005), EMOS: https://doi.org/10.1175/MWR2904.1
- Wilks & Hamill (2007), Ensemble-MOS using reforecasts: https://doi.org/10.1175/MWR3402.1
