# Weather specialist wallets

Snapshot: **2026-08-11**

Profitable weather wallets are an empirical dataset for discovering strategy structure. The goal is to reconstruct **what they trade, when they trade, at what price, after which information event, and how that flow predicts price or settlement**.

Polymarket's public Data API exposes trades, current positions, closed positions with realized PnL, user activity and leaderboards. That is enough to build useful behavioral fingerprints without guessing from profile screenshots.

Official endpoints:

- `GET https://data-api.polymarket.com/trades?user=<wallet>`
- `GET https://data-api.polymarket.com/positions?user=<wallet>`
- `GET https://data-api.polymarket.com/closed-positions?user=<wallet>`
- `GET https://data-api.polymarket.com/activity?user=<wallet>`
- leaderboard API with `category=WEATHER`

Docs:
https://docs.polymarket.com/market-data/overview

## Priority wallet: supplied account

Address:

`0xbddc2a7690bf600e347d5eb4a9c28f9f24e55d4f`

Profile URL:
https://polymarket.com/@0xbddc2a7690bf600e347d5eb4a9c28f9f24e55d4f-1774968947489

### 2026-08-11 visible snapshot

The account shows:

- joined March 2026;
- 792 predictions;
- about $4,522 active position value;
- $827.65 biggest win;
- +$1,018.71 past-day profile PnL.

Visible positions are overwhelmingly **YES on exact temperature buckets**, not broad NO-tail positions.

Examples:

| Market | Avg entry | Snapshot price | Shares | Visible PnL |
|---|---:|---:|---:|---:|
| Istanbul Aug 11 — 27°C | 52.6¢ | 100¢ | 856 | +$405.61 |
| Tel Aviv Aug 11 — 35°C | 56.9¢ | 100¢ | 439 | +$189.21 |
| Milan Aug 11 — 36°C | 65.0¢ | 100¢ | 308 | +$107.66 |
| Karachi Aug 11 — 32°C | 47.3¢ | 100¢ | 211 | +$111.31 |
| Munich Aug 11 — 31°C | 52.0¢ | 99.9¢ | 192 | +$92.12 |
| Madrid Aug 12 — 38°C | 31.5¢ | 53¢ | 634 | +$136.04 |
| Tel Aviv Aug 12 — 35°C | 48.7¢ | 49¢ | 821 | +$2.27 |
| Wuhan Aug 12 — 30°C | 40.1¢ | 41¢ | 623 | +$5.41 |
| Paris Aug 12 — 35°C | 51.6¢ | 63.5¢ | 194 | +$23.09 |
| Singapore Aug 12 — 32°C | 53.0¢ | 64.5¢ | 189 | +$21.70 |
| Wellington Aug 12 — 13°C | 18.7¢ | 20.5¢ | 536 | +$9.87 |
| Ankara Aug 12 — 31°C | 26.4¢ | 17¢ | 569 | -$53.35 |
| Shanghai Aug 12 — 28°C | 24.7¢ | 18.5¢ | 405 | -$25.06 |

US same-day positions include Miami 92–93°F bought at 67¢ and Denver 96–97°F at 55.3¢.

### Working inference

The visible pattern suggests a **modal-bucket exact-YES strategy** with two time horizons:

1. same-day entries where observation/peak information has sharply reduced uncertainty;
2. next-day entries where a forecast identifies a concentrated modal bucket before the crowd fully converges.

This is an inference from positions, not a verified algorithm. The decisive variable is trade time. If many winning T+0 fills occur shortly after a station observation or local peak, certainty-collapse is likely. If next-day fills cluster just after ECMWF/NBM/local-model updates, forecast-vintage latency is likely.

### Highest-value reconstruction

For each fill:

- exact timestamp;
- event date and local resolver time;
- city/station;
- T+0/T+1/T+2 horizon at fill;
- exact bucket and distance from current forecast mode;
- side and price;
- notional and fraction of wallet typical size;
- market bid/ask and spread if recoverable;
- latest station observation;
- latest available forecast vintages;
- new-vs-old forecast revision;
- final resolver outcome;
- 5m/30m/2h price markout;
- realized PnL.

Then cluster fills by information state.

## All-time weather leaders to decompose

Current all-time WEATHER profit leaderboard includes:

- `gopfan2` — about +$349k;
- `aenews2` — about +$285k;
- `ColdMath` — about +$136k;
- `gopfan` — about +$118k;
- `bama124` — about +$87k;
- `Poligarch` — about +$85k;
- `Hans323` — about +$84k;
- `ShyGuy1` — about +$74k;
- `Handsanitizer23` — about +$71k;
- `automatedAItradingbot` — about +$65k;
- `WeatherTraderBot` — about +$57k;
- `HighTempTation` — about +$54k.

Source:
https://polymarket.com/leaderboard/weather/all/profit

The volume leaderboard includes `dpnd`, `largeleeks888`, `Poligarch`, `OraculumNobius`, `TENETENET`, `planktonXD`, `ColdMath`, `KingZeManel` and `aenews2` with roughly $10M+ weather turnover.

High PnL plus high volume suggests repeatable activity worth decomposing. High PnL with low frequency can instead reveal large climate-index bets.

# Current specialist archetypes visible from profiles

Current public profile snapshots reveal that “top WEATHER trader” is not one strategy class.

## `gopfan2` — large-capacity climate/index archetype

Current profile:
https://polymarket.com/profile/0xdd42ffb8aabe818f7538d93c175a9f9e2da9990d

Visible August 2026 position:

- **“Will 2026 be the second-hottest year on record?”**
- ~91,697.5 YES shares;
- average entry ~29.3¢;
- recent mark ~54¢;
- position value ~49.5k;
- unrealized gain shown around +$22.6k.

This is directly relevant because `gopfan2` is also the all-time WEATHER PnL leader in the category snapshot. It demonstrates that the highest-dollar weather program should include **global-temperature / annual-rank basis models**, not only daily city markets.

### Research implication

Build a climate-wallet segment separately:

- GISTEMP monthly buckets;
- hottest-month ranks;
- hottest-year ranks;
- monthly→annual cross-market consistency;
- entry timing relative to ERA5T/NOAA/Berkeley/NASA releases.

## `Poligarch` — high-frequency city-temperature / ladder archetype

Current profile:
https://polymarket.com/profile/0xb40e89677d59665d5188541ad860450a6e2a7cc9

Profile snapshot shows ~39k predictions and many simultaneous daily-temperature positions. Examples from one July 22 slate include:

- Hong Kong 33°C YES around 65¢;
- Paris 25°C NO around 57.4¢;
- London 25°C YES around 49–54¢;
- Paris 26°C YES around 42.7¢;
- London 26°C NO around 65.7¢;
- Madrid 40°C NO around 75.7¢;
- Hong Kong 32°C NO around 67¢;
- Munich 25°C YES around 57.9¢;
- Munich 23°C NO around 88.8¢;
- Warsaw 22°C YES around 68.6¢.

Several of these later displayed large positive mark-to-market or settled-value gains.

### Inference

This pattern looks much closer to **full distribution / ladder trading** than one-outcome gambling. Simultaneous YES on one modal bucket and NO on neighboring/distant buckets is exactly how a trader with an internal probability surface can monetize multiple mispricings in the same event.

### Research implication

For Poligarch, reconstruct positions at the **event portfolio** level:

`event PnL = Σ outcome-expression PnL`

rather than analyze each YES/NO trade independently.

Compare the wallet's net implied distribution with:

- coherent market distribution;
- our weather distribution;
- final outcome.

## `ColdMath` — high-frequency near-certainty / favorite expression candidate

Current profile shows more than 8k predictions and recent positions such as NO on very high-priced London low-temperature alternatives around 97–99¢.

This is consistent with a possible strategy class that monetizes **near-certainty / resolution-state** prices rather than seeking only large percentage edges.

Full closed-position decomposition is needed to determine whether this is a major historical weather strategy or simply the most recent visible state.

## `aenews2` — broad cross-category high-capital trader

Current public profile is dominated by non-weather positions despite ranking near the top of WEATHER PnL historically. That means its weather edge should be reconstructed from closed WEATHER positions rather than inferred from current active portfolio.

This is an important segmentation lesson: current profile state can identify active archetypes, but historical WEATHER category skill requires category-filtered fills/closed positions.

# Separate wallet skill by market family

WEATHER category PnL mixes several distinct mathematical problems. Score each wallet separately on:

- daily high temperature;
- daily low temperature;
- monthly/global temperature anomaly;
- hottest-year/month records;
- precipitation totals;
- wind/extrema;
- other weather contracts.

A trader with climate-index expertise should receive near-zero prior weight in an airport daily-high signal until evidence shows cross-family skill.

## Behavioral fingerprints

### A. Modal-bucket sniper

Fingerprint:

- exact YES bucket;
- entry price often 20–70¢ rather than pennies;
- concentration on the current mode;
- short holding period or settlement hold;
- high same-day activity.

Interpretation: forecast/observation precision.

### B. Tail seller / NO buyer

Fingerprint:

- BUY_NO on low-probability YES outcomes;
- repeated entries in similar NO price bands;
- positive returns driven by longshot overpricing.

Interpretation: calibration/behavioral bias rather than superior modal forecast.

### C. Release-latency trader

Fingerprint:

- fills cluster in minutes after ECMWF/NBM/METAR/local-source updates;
- positive near-term markout;
- broad geographic coverage following known model schedules.

Interpretation: fast information processing.

### D. Resolver specialist

Fingerprint:

- same-day fills after authoritative station data;
- exact winning bucket bought while generic weather sites still disagree;
- focus on stations with tricky source/rounding mechanics.

Interpretation: oracle/source advantage.

### E. Climate-index nowcaster

Fingerprint:

- monthly GISTEMP/global-record markets;
- large positions held toward scheduled release dates;
- entries after early global datasets become informative.

Interpretation: dataset-basis model.

### F. Structural arbitrageur / ladder trader

Fingerprint:

- simultaneous activity across multiple outcomes in one event;
- combinations of YES modal bucket + NO neighbors/tails;
- repeated YES/NO basket relationships;
- PnL can be driven by relative mispricing as much as final directional view.

Interpretation: full probability-surface trading, negative-risk structure and/or liquidity strategy.

## Wallet skill statistics

For wallet `w` and segment `s`, estimate:

- `N` trades / positions;
- realized PnL;
- ROI on deployed cost;
- median entry price;
- hit rate versus price-implied expectation;
- Brier-style calibration residual;
- 5m/30m/2h markout;
- average time to settlement;
- concentration by city;
- PnL per dollar of turnover;
- PnL persistence through time.

### Price-controlled alpha

The key statistic is excess outcome performance relative to entry probability.

For YES fills:

`alpha_outcome = y - p_entry`

where `y ∈ {0,1}`.

Aggregate by wallet/segment with dollar or information weighting.

A wallet buying 60¢ contracts and winning 65% has smaller informational edge than one buying 30¢ contracts and winning 50%, even if raw win rate looks higher.

### Markout alpha

For trade at price `p_t`:

`markout_τ = signed_direction * (p_{t+τ} - p_t)`.

Positive markout indicates the wallet tends to trade before price convergence. Settlement alpha indicates the underlying prediction is good. The two together distinguish information timing from lucky late fills.

## Wallet consensus signal

Independent specialists agreeing on the same outcome can be more informative than one wallet.

One simple factor:

`W_i(t) = Σ_w skill_w(segment) * exp(-(t-t_w)/τ) * signed_notional_w`

Enhancements:

- normalize notional by each wallet's typical trade size;
- weight same-city historical skill;
- weight fills more strongly when they occur after a fresh weather update;
- reduce weight after the market has already repriced most of the move;
- calculate consensus separately for YES and NO expressions.

The economic question is whether adding `W_i(t)` increases incremental net PnL over a weather+market baseline.

## Public-data limitation that matters to interpretation

Polymarket's public Data API exposes fill-level activity. The off-chain order-placement/cancellation lifecycle is not fully attributable to addresses in public archives, so fill history alone cannot identify a wallet's complete maker quoting policy.

This affects one inference only: wallet data is excellent for **what got filled and at what price**, while full resting-order behavior requires our own live book observation or authenticated self-data.

## Practical wallet research output

Produce one compact table per specialist:

`wallet × family × city × horizon × direction × price_band × timing_bucket`

with:

- count;
- turnover;
- realized PnL;
- excess win probability over price;
- short-horizon markout;
- forecast-release alignment.

Then rank wallet-derived features by incremental expected net PnL.
