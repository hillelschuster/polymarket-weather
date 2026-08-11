# Highest-value next measurements — profit-only ordering

Snapshot: **2026-08-12**

Objective:

`maximize realistic net dollars after fees + spread + depth + fills + capital lock`.

Research is ranked only by the probability that the next measurement changes profitable capital deployment.

---

# Priority 1 — prove/kill GISTEMP resolver alpha at executable depth

This is now the highest-value research question because GISTEMP combines:

- public NASA resolver code;
- exact public upstream inputs;
- scheduled release times;
- 0.05°C Polymarket brackets;
- repeated specialist GISTEMP profits;
- historical event capacity reaching hundreds of thousands to several million dollars.

## Forward August 2026 experiment

Use:

- `scripts/gistemp_input_watch.py`;
- `scripts/gistemp_market_watch.py`.

Preserve every changed:

`GHCNm qcf vintage`
`ERSST August file`
`NASA LOTI output`

and synchronized all-outcome Polymarket books.

For every input change calculate:

`replica_value_t`
`P(first_release_bucket_i | vintage_t)`
`executable YES/NO EV by depth`
`market response 5m/30m/2h later`.

After NASA publication calculate:

`t_correct = earliest vintage whose high-probability bracket matches first NASA bracket`

and:

`net executable dollars available between t_correct and market convergence`.

### Historical April forensic gap

April 2026 is already a strong natural experiment:

- May 5 03:21 UTC: event volume ~$298.6K, winning-bracket ask 80¢;
- May 5 reconstruction still only ~80–85% main-bin probability;
- May 6 GHCNm reconstruction fell to ~1.1791°C and the major remaining bracket-crossing variables disappeared;
- official first release = 1.18°C.

The missing decisive fact is **May 6–May 9 synchronized L2**, especially the first ask/depth after each qcf vintage. Recover it if a genuine archive exists. Do not fabricate it from later trades/midpoints.

If no trustworthy historical L2 exists, prospectively measuring August/September has more value than prolonged forensic approximation.

---

# Priority 2 — continuous full-ladder L2 capture for all high-dollar Weather events

Historical onchain trades cannot reconstruct canceled/off-book liquidity. Capacity therefore requires prospective L2.

Capture:

- every GISTEMP monthly outcome;
- annual GISTEMP rank outcomes;
- highest-volume daily temperature ladders;
- any unusually large precipitation/wind Weather event.

At one synchronized timestamp store:

`token`
`bid levels`
`ask levels`
`tick`
`feesEnabled / fee schedule`
`negRiskMarketID / feeBips`
`book hash`
`source-information state`.

Economic outputs:

- fillable expected dollars at $100/$1K/$5K/$25K/$100K scales;
- full-YES and full-NO/NegRisk basket economics;
- spread and stale-depth duration;
- information-response half-life;
- capital-time.

This is the dataset that distinguishes a clever probability estimate from an actual business.

---

# Priority 3 — resolver-exact daily extrema distribution

Daily temperature remains the likely high-frequency cashflow engine while climate opportunities mature.

The target is one coherent vector:

`q = P(final resolver bucket_i | exact information available now)`.

For T+0, condition on:

- exact resolver max/min already observed;
- next bucket boundary;
- remaining local-day forecast path;
- station-specific model residuals;
- source-specific finalization rules.

For T+1, condition on point-in-time forecast vintages and station/horizon residual distributions.

Do not optimize generic weather MAE. Optimize:

`fee-adjusted executable dollars`.

## Most useful state diagnostic

Compare weather and market concentration:

`H(q) = -sum q_i log q_i`

`H(p) = -sum p_i log p_i`.

If weather is materially more concentrated than market, modal/adjacent YES may dominate.
If market is too concentrated relative to weather, exact-bucket NO/fade may dominate.

This unifies profitable fee-era YES and NO specialist behavior without hard-coding either side.

---

# Priority 4 — one global marginal-dollar allocator

Every validated opportunity must produce a capacity curve:

`size -> expected net dollars -> expected capital time`.

Rank incremental dollars across:

- GISTEMP YES/NO;
- annual-rank implication trades;
- daily temperature directional trades;
- maker quotes;
- NegRisk transformations;
- source-lock terminal trades;
- precipitation/wind only when they outrank the above.

No fixed allocation like “50% climate / 50% daily.”

Primary ranking quantity:

`expected_net_dollars / expected_capital_time`

with correlation accounted for only when shared exposure materially changes portfolio economics.

---

# Priority 5 — maker versus taker routing measured from identical signals

Weather taker fee is economically large near 50¢; makers pay zero platform trading fee and can receive rebates.

For every fair-value revision compare:

### Cross now

`EV_cross = realized fillable q - actual ask/bid - fee - impact`.

### Make

`EV_maker = P(fill before edge decay) * (fair_at_fill - quote + rebate - adverse_markout)`.

Required measurements:

- fill probability;
- time to fill;
- 10s/1m/5m adverse markout;
- spread captured;
- rebate actually earned;
- missed opportunity when no fill.

Expected result should be state-dependent:

- large fresh information shock -> taker;
- quiet state / slow edge decay -> maker;
- near deterministic source lock -> take stale depth aggressively when EV survives costs.

---

# Priority 6 — propagate monthly GISTEMP information into annual rank

Do not build a separate annual climate model.

NASA annual GISTEMP is the equal-weight average of monthly values. Use monthly distributions directly:

`A_2026 = sum(M_1...M_12) / 12`.

After every meaningful monthly/GISTEMP revision:

1. update annual distribution;
2. compare with historical annual rank thresholds;
3. derive rank probabilities;
4. compare with the direct annual-rank book.

This is attractive because the annual event has demonstrated multi-million-dollar volume and specialist positions in the tens of thousands of dollars.

The monthly information acquisition can therefore create more than one PnL opportunity.

---

# Priority 7 — specialist decomposition only where it can change a signal

Wallet archaeology is no longer a top-level objective.

Continue it only for one of three reasons:

1. identify an information source/catalyst we do not yet consume;
2. estimate real capacity/sizing at a validated edge;
3. improve execution timing after controlling for our own fair value.

High-value targets:

- `badatmath.` — fee-era exact YES / secondary-mode behavior;
- `gghff` — fee-era exact-bucket NO/fade behavior;
- supplied wallet — large directional taker after information revisions;
- Poligarch — passive Weather maker behavior;
- GISTEMP specialists — market-family PnL/timing around qcf/ERSST updates.

Do **not** infer strategy from Struct token-level PnL when merge/conversion cashflows are involved. Reconcile event-level cashflows.

---

# Priority 8 — source-lock / NegRisk terminal layer

The math is strong but direct wallet-PnL attribution is weaker than the priorities above.

For daily temperature events, after the contractual resolver value is locked but before formal Polymarket resolution:

- search stale winning YES;
- search stale losing NO;
- compare multi-NO NegRisk conversion;
- include current market-specific conversion `feeBips`;
- rank by dollars per capital-time.

This becomes high priority only when live L2 proves repeated, meaningful capacity.

---

# What has been demoted

## Generic tail strategy

Cheap YES is not a strategy. Some spectacular-looking Struct penny-tail “wins” were merge-accounting artifacts. Buy tails only when calibrated `q` makes them positive EV.

## Broad model zoo

Add another weather/climate source only when it improves out-of-sample/executable dollars beyond the current resolver model.

## Generic wallet copying

Profitable specialists express different edges. Their public flow is useful only if it adds predictive/execution value after our own weather/climate probability and current market state.

## General infrastructure

No dashboards, services, abstractions or broad data platform unless a measured opportunity needs them.

---

# Minimal evidence pipeline

The smallest data chain that now serves the highest-dollar hypotheses is:

1. **resolver inputs/vintages** — GISTEMP and daily station/model data with true availability time;
2. **synchronized L2** — complete event books at the same information timestamp;
3. **fair probability vector** — contract-native buckets;
4. **action/capacity curves** — maker/taker/NegRisk/hold;
5. **realized cashflows** — actual fill, fee, rebate, transformation and settlement PnL.

Everything else is secondary.

---

# Bottom line

The next research dollar should go to the measurement with the largest potential capital consequence:

> **Can public GISTEMP inputs make one 0.05°C bracket near-deterministic while Polymarket still offers meaningful stale depth?**

That can plausibly produce far larger dollars per opportunity than another incremental improvement to airport-temperature forecasting.

The forward August/September capture now provides the cleanest possible proof. Daily extrema work remains active in parallel because it supplies high-frequency opportunities and a faster feedback loop.