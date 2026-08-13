# Strongest Weather alpha theses — ranked synthesis

Snapshot: **2026-08-13**

## Executive verdict

The project now has enough research breadth to stop treating every interesting Weather family equally.

The highest-value thesis remains the one with direct live evidence:

**#0 — T+0 resolver observation / fast-source repricing.**

Among the newly expanded research lanes, the strongest order is:

1. **NYC/major-city snowfall amount ladders** — best demonstrated new-family capacity and unusually direct public probability products.
2. **ECMWF AIFS public timing** — best reusable information-timing multiplier across existing international temperature markets.
3. **Market-opening price discovery** — cheapest recurring hypothesis to test because fair value can exist before the market is listed.
4. **Mt. Washington nested wind thresholds** — cleanest non-temperature structural math plus a possible real-time-to-F6 publication lead.
5. **Spatial one-report-ahead resolver nowcast** — valuable T+0 enhancement where the resolver cadence is slower than nearby observation networks.

This ranking is based on expected research value, not claimed live profitability.

---

# 0. Existing live T+0 resolver repricing remains the benchmark

Why it remains first:

- actual synchronized source/book evidence exists;
- historical replications exist;
- the economic latency window was observed after actual source receipt;
- the strategy state is simple: running extreme + next threshold + remaining weather;
- direct high-frequency resolver precursor feeds have already been identified in several international cities.

The correct benchmark for every new lane is therefore:

> Does this produce more expected net dollars per unit of research/implementation than improving source speed and probability calibration on the already-live-evidenced T+0 lane?

New research should complement, not distract from, that benchmark.

---

# 1. Snowfall brackets — strongest new family

Deep dive:

`research/snowfall-bracket-profit-thesis-deep-dive-2026-08-13.md`

## Why it ranks first among new families

The January 24–26 Central Park snowfall ladder produced about **$1.448M** of volume across seven exact brackets. The winning 10–12 inch bucket alone traded roughly $328k.

This is a materially larger capacity demonstration than most recurring city-temperature events in the repo.

At the same time, NOAA/WPC already publishes a probability distribution rather than only a point forecast:

- 24/48/72-hour snowfall probabilities;
- threshold exceedance probabilities;
- 5/10/25/50/75/90/95 percentile accumulations;
- a skew-capable distribution whose mode is the WPC forecast and whose variance reflects an ensemble.

Thus the core problem is **resolver calibration**, not building meteorology from zero.

## Core math

One resolver CDF prices every bucket:

`q_[L,U) = F(U^-) - F(L^-)`.

Resolver-calibrate WPC using PIT/isotonic/beta calibration:

`u_n = F_WPC,n(y_n)`

`F_cal(s) = G(F_WPC(s))`.

During an active storm:

`S_final = A_t + U_t + R_t`

with official accumulation, observed-but-not-yet-finalized accumulation and remaining snowfall treated separately.

Near storm end the problem can become extremely sharp. If resolver-aligned accumulated snow is 11.4 inches:

`P(10–12) ~= P(R < 0.6)`.

## Thesis

The candidate persistent edge is:

**public probabilistic snowfall guidance + resolver-location/ptype calibration + observed accumulation state → a more coherent bracket distribution than piecemeal market pricing.**

## Decisive evidence

Reconstruct the January 24–26 event at every WPC/NWS vintage and compare `q(t)` to Polymarket prices/books.

The historical market moved substantially and the eventual winner was far from certainty in earlier indexed snapshots, but strict point-in-time forecast-vs-market alignment is still required before calling that alpha.

---

# 2. ECMWF AIFS — strongest reusable timing multiplier

Deep dive:

`research/aifs-public-timing-profit-thesis-2026-08-13.md`

## Why it ranks second

ECMWF currently states:

- open IFS is released at the **end** of the real-time dissemination schedule;
- open AIFS is released **as soon as produced**;
- AIFS Single and Ensemble run four times daily.

This creates a public information-ordering asymmetry without needing private data.

The exact usable lead for a city/date field must be logged because dissemination is progressive.

## Core math

Do not ask whether AIFS is “better than IFS.”

Ask whether its early revision predicts the later fair-value revision.

`Delta_A = maxTemp_AIFS(new) - maxTemp_AIFS(old)`

`E[Delta_consensus | Delta_A] = alpha + beta*Delta_A`.

For the ladder:

`Delta q_later ~= B * Delta q_AIFS`.

More robustly, combine with the market prior:

`q_post = softmax(log(p_market + eps) + lambda*z_AIFS)`.

AIFS only needs positive incremental information after conditioning on the market.

## Thesis

**Early public AIFS revisions can act as a leading indicator for later ECMWF/multimodel consensus and therefore for later Polymarket repricing.**

This is especially attractive in European airport exact-temperature markets and can directly extend the existing Milan forecast-revision/wallet evidence.

## Decisive evidence

20–50 live forecast cycles with:

`AIFS target field first_seen -> resolver q revision -> L2 markout -> later IFS/consensus -> final resolver`.

If the market already reprices before the relevant AIFS field is public, reject the latency thesis even if AIFS has forecast skill.

---

# 3. Market opening — lowest-cost recurring hypothesis

Deep dive:

`research/market-opening-profit-thesis-deep-dive-2026-08-13.md`

## Why it ranks third

A recurring Weather market can be listed after several useful forecast cycles already exist.

Therefore maintain `q_pre` before listing.

The market creation event then tests whether the first executable book has fully incorporated old public information.

No new forecasting engine is required.

## Core math

Pre-list vector:

`sum_i q_pre(i)=1`.

Taker discrepancy:

`EV_i = q_i - ask_i - 0.05*ask_i*(1-ask_i)`.

Maker evaluation must be fill-conditioned:

`EV_maker = P(fill) * [E(q(t+h)-p | fill) + rebate - inventory_cost]`.

Cold-start convergence:

`e_i(t)=market_i(t)-q_pre_i`

`e_i(t) ~= e_i(0)*exp(-lambda*t)`.

The half-life only matters after controlling for new weather information arriving after listing.

## Thesis

**New Weather ladders may take nonzero time to discover already-public resolver probability information, especially under wide initial spreads and thin maker competition.**

## Important correction

Visually incoherent Polymarket probabilities are not sufficient evidence. When spreads exceed $0.10, Polymarket can display last trade rather than midpoint.

Opening research must use executable L2, not UI probability sums.

## Decisive evidence

30–100 openings with precommitted `q_pre`, first L2, weather-info timestamps and fill-conditioned markout.

This hypothesis is cheap to kill if specialists already make openings efficient immediately.

---

# 4. Mt. Washington wind — strongest structural non-temperature math

Deep dive:

`research/mt-washington-threshold-profit-thesis-2026-08-13.md`

## Why it ranks fourth

The July event reached roughly $57k–$64k across threshold markets. Capacity is below the best snowfall markets, but the structure is exceptionally clean.

Let monthly max gust be `W` and thresholds `K1<K2`.

### Exact payoff identity

`YES(W>=K1) + NO(W>=K2)` pays:

- $1 if `W<K1`;
- $2 if `K1<=W<K2`;
- $1 if `W>=K2`.

Therefore:

`fair pair value = 1 + P(K1<=W<K2)`

`= 1 + q_K1 - q_K2`.

Any **simultaneously fillable all-in cost below $1** is a strict cross-threshold pricing inconsistency independent of meteorology.

This is the cleanest newly found structural identity.

## Remaining weather math

For uncrossed threshold `K`:

`q_K(t) = 1 - product_d (1-h_d(K))`

or approximately:

`q_K = 1 - exp(-Lambda_K)`.

One station-specific extreme-gust distribution can price all thresholds coherently.

## Publication-basis thesis

Mt. Washington exposes current summit data while the F6 record used by the contract is updated nightly.

Measure:

`live gust threshold first_seen -> later F6 inclusion -> market repricing`.

If live threshold crossings map reliably to F6, the running maximum can become known before the contractual publication catches up.

---

# 5. Spatial one-report-ahead nowcast — best T+0 enhancement

Deep dive:

`research/spatial-one-report-ahead-profit-thesis-2026-08-13.md`

## Why it ranks below direct feeds

Several resolver cities already have exact-station 1–10 minute precursor feeds. Those are simpler and stronger.

Spatial data matters when it can predict the **next resolver report before it arrives**.

## Core target

For next resolver time `t1` and boundary `B`:

`p_cross = P(T_resolver(t1) >= B | X_t)`.

Model next resolver temperature:

`T_next = mu(X_t) + epsilon`

then:

`p_cross = 1-F_epsilon(B-mu(X_t))`.

Nearby stations should be basis-corrected and weighted by advective geometry rather than raw distance.

## Thesis

**A small wind-aware station graph can provide an incremental crossing probability during the gap between resolver observations, particularly around fronts, sea breezes and cloud/convective transitions.**

## Decisive evidence

The spatial signal must improve next-report Brier/log loss after conditioning on:

- resolver's own recent observations;
- current forecast state;
- market price.

Then it must produce probability revisions before the actual resolver report and before market repricing.

---

# Comparative economics

| Thesis | Existing evidence | Recurrence | Demonstrated capacity | Math simplicity | Main missing measurement |
|---|---|---:|---:|---:|---|
| T+0 direct resolver/fast source | **live synchronized** | daily | medium/high | high | faster source + realized fills |
| Snowfall brackets | market + resolver + official prob products | episodic/seasonal | **very high (~$1.45M case)** | high | PIT forecast vs market |
| AIFS timing | official timing asymmetry + existing model-revision thesis | 4 cycles/day across cities | leverages daily temp capacity | high | exact first-seen + markout |
| Market opening | recurring listings + pre-existing weather info | daily | established city volume | very high | first L2/fill markout |
| Mt Washington wind | structural rules + ~$60k event | monthly/seasonal | medium | **very high** | L2 pair scan + source/F6 basis |
| Spatial one-report nowcast | physical mechanism + T+0 cases | many reports/day | leverages temp capacity | medium | incremental crossing skill |

---

# Research capital allocation

The practical sequencing is:

### Immediate / always-on

Continue improving the already-live-evidenced T+0 resolver-source lane.

### Next empirical study

**Snowfall Jan 24–26 reconstruction.**

It has the best combination of capacity, exact resolver, public probability archive and narrow bracket structure.

### Parallel lightweight measurement

**AIFS first-seen logging.**

This costs little and can reveal whether a reusable timing advantage exists across many temperature markets.

### Passive data collection

**Market openings.**

Precompute q and record first L2; do not spend broad engineering effort before the first 30–100 observations show persistent error.

### Structural scan

**Mt. Washington threshold pair economics.**

This is mathematically simple enough that any historical/current L2 data should be screened for cross-threshold floor violations and relative-value gaps.

### Enhancement only

**Spatial nowcast** after exact-station fast-source coverage is exploited.

---

# Unifying thesis

The strongest Weather opportunities share one pattern:

`information/state already knowable`  
`+ exact resolver transformation`  
`+ coherent probability/payoff math`  
`- market price-discovery delay/cost`.

The most profitable work is therefore unlikely to come from a giant universal weather model.

It should come from a small set of resolver-specific transformations where:

- the information arrives on a measurable clock;
- the outcome geometry constrains probabilities strongly;
- market capacity is real;
- the market does not instantly incorporate the information.

That is the standard each new Weather thesis should meet before implementation expands.
