# Weather market-opening efficiency

Snapshot: **2026-08-13**

## Research thesis

Recurring daily-temperature markets often become tradeable roughly two days before the target date. By that point, several forecast cycles and station-specific priors already exist. This creates a distinct question from forecast-release latency:

> How long does it take a newly created Weather ladder to converge from its first prices to a probability surface consistent with the information that was already public before the market opened?

If convergence is slow, market creation itself is an information-friction event.

---

## 1. Evidence that major recurring markets open well before the target day

Examples from resolved London markets:

| Target date | Market opened | Event volume |
|---|---|---:|
| July 1, 2026 | June 29, 12:01 AM ET | ~$138.5k |
| July 7, 2026 | July 5, 12:02 AM ET | ~$183.9k |
| July 12, 2026 | July 10, 12:02 AM ET | ~$133.9k |
| July 17, 2026 | July 15, 12:02 AM ET | ~$160.2k |
| July 18, 2026 | July 16, 1:03 AM ET | ~$218.3k |

Official Polymarket pages:

- https://polymarket.com/event/highest-temperature-in-london-on-july-1-2026
- https://polymarket.com/event/highest-temperature-in-london-on-july-7-2026
- https://polymarket.com/event/highest-temperature-in-london-on-july-12-2026
- https://polymarket.com/event/highest-temperature-in-london-on-july-17-2026
- https://polymarket.com/event/highest-temperature-in-london-on-july-18-2026

The important point is not London's specific schedule. It is that a recurring market can appear after the weather information needed to form a reasonable prior already exists.

---

## 2. Pre-list probability surface

For each expected recurring city/date, define a point-in-time probability surface immediately before market creation:

`q_pre(i) = P(final resolver result is bucket i | all data available before listing)`

The pre-list surface should use only information that would have been available at that time:

- previous and current global/regional model cycles;
- ensemble distribution;
- station-specific bias/residual distribution;
- recent observations;
- local/aviation guidance where useful;
- exact resolver rules and precision.

The research object is then the discrepancy between `q_pre` and the first market state.

---

## 3. What could make opening prices inefficient

Several mechanisms are plausible:

1. **Cold-start pricing** — first liquidity is posted without a mature reference midpoint.
2. **Incomplete ladder normalization** — individual buckets may be seeded independently before the whole distribution becomes coherent.
3. **Generic-city forecasts** — early traders may use city-level weather rather than exact resolver-airport calibration.
4. **Thin early competition** — capable specialists may not arrive immediately at every listing.
5. **Stale forecast prior** — an initial quote can reflect an older model cycle even though a newer cycle existed before listing.
6. **Tail neglect** — low-probability buckets can remain mechanically quoted after the distribution has already narrowed.

These are hypotheses. The opening study should determine whether any survive at executable prices.

---

## 4. Maker economics are part of the opening study

Current official Polymarket documentation states that Weather makers pay zero platform trading fee and Weather maker rebates receive 25% of the eligible taker-fee pool.

Sources:

- https://docs.polymarket.com/trading/fees
- https://docs.polymarket.com/market-makers/maker-rebates

Rebates are competitive within each market, so opening periods with few other makers could have different economics from mature periods.

A separate Liquidity Rewards program can compensate qualifying resting orders in markets with an active incentive allocation. Its configuration is market-specific; do not assume a Weather event is incentivized merely because the program exists.

Source:

- https://docs.polymarket.com/market-makers/liquidity-rewards

For research, keep separate columns for:

- spread / valuation markout;
- maker rebate;
- any explicit liquidity reward;
- fill-conditioned adverse selection.

This avoids attributing subsidy to forecasting skill or vice versa.

---

## 5. Minimum event dataset

For each market creation:

- event/city/date;
- resolver station/source;
- market creation timestamp;
- first observed token/ladder state;
- first trade time;
- first 5m/15m/30m/1h/2h price path;
- pre-list `q_pre` by bucket;
- model vintages available before creation;
- eventual resolver result;
- market volume/liquidity later in lifecycle.

For forward/live collection, add:

- initial best bid/ask/depth;
- quote competition by bucket;
- fill timestamps;
- 5s/30s/5m fill-conditioned markout;
- realized maker rebate/reward if any.

Historical price history is useful for screening but cannot reconstruct initial resting depth. Future L2 capture is required for production-fidelity maker evidence.

---

## 6. Useful statistics

### Initial calibration error

For each bucket:

`opening_error_i = first_market_probability_i - q_pre(i)`

Study absolute and signed error by:

- city;
- forecast horizon at opening;
- bucket rank (modal/adjacent/tail);
- spread/liquidity;
- time of day;
- latest model cycle age.

### Convergence half-life

Measure the first time the market enters a tolerance band around the later stable surface.

This answers whether opening inefficiency lasts seconds, minutes or hours.

### Information already available versus genuinely new information

Separate price changes caused by:

- market simply discovering old information;
- a new forecast/observation arriving after listing.

Only the first class is true market-opening inefficiency.

---

## 7. Market-creation detection

Polymarket's market WebSocket documentation includes a `new_market` event when custom features are enabled.

Source:

- https://docs.polymarket.com/market-data/websocket/market-channel

Operational behavior should be measured rather than inferred: verify whether a connection/subscription configuration reliably surfaces the full relevant Weather universe. A narrow periodic discovery process is an adequate research fallback because this hypothesis does not require sub-second market discovery.

---

## 8. Economic priority

Why this deserves a high research rank:

- daily recurrence;
- substantial eventual capacity in established cities;
- reuses the existing probability engine;
- no need to forecast an unpredictable shock;
- potentially favorable early spreads and maker competition;
- independent from the already-demonstrated T+0 observation mechanism.

Main uncertainty:

- sophisticated Weather specialists may already make new ladders efficient almost immediately.

The smallest decisive measurement is therefore:

> Build `q_pre` before the next few listings and record the complete first market state and its convergence path.

If opening errors are repeatedly multi-cent and persist long enough to be executable, this is a high-frequency recurring research lane with very low incremental meteorological complexity.