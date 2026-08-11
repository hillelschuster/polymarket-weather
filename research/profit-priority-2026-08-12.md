# Profit-first priority map — 2026-08-12

Objective: maximize realistic net dollars from Polymarket Weather. This note deliberately ignores architectural completeness. It ranks only mechanisms that can plausibly produce the most money after fees, spread, depth, fills, capital lock and capacity.

## Verdict

The project should no longer be thought of as a daily-temperature bot with optional climate research.

The strongest current formulation is a **two-engine weather program**:

1. **High-capacity climate resolver reconstruction** — especially NASA GISTEMP monthly/annual markets, where the settlement algorithm and public upstream inputs can potentially be reconstructed before NASA's scheduled publication.
2. **High-frequency daily extrema trading** — coherent city-temperature distributions monetized with state-dependent YES, NO, adjacent-basket, maker and terminal trades.

Capital should flow to whichever engine currently offers the highest marginal expected net dollars at executable depth. There is no reason to reserve capital by strategy label.

The most important priority change is that **exact GISTEMP reconstruction is now Priority 1 research**. The reason is not novelty. It is the combination of:

- real Weather leaderboard profits in climate markets;
- five- and six-figure historical position capacity;
- a deterministic published resolver algorithm;
- public upstream inputs;
- scheduled release times;
- narrow 0.05°C Polymarket buckets;
- public evidence that independent researchers can reconstruct the eventual GISTEMP value to within a small fraction of one bucket before release.

Daily temperature remains the best source of repeated cashflow and rapid empirical learning.

---

# 1. Observed dollars: climate has the highest demonstrated single-opportunity capacity

Polymarket's all-time Weather leaderboard snapshot has:

- `gopfan2`: roughly **+$349k**;
- `aenews2`: roughly **+$285k**;
- `ColdMath`: roughly **+$136k**;
- `Poligarch`: roughly **+$85k**.

Official leaderboard:
https://polymarket.com/leaderboard/weather/all/profit

The leaderboard's largest Weather wins are disproportionately climate/global-temperature contracts:

- `aenews2`, July 2024 hottest on record: ~$267k cost -> ~$415k value;
- `bama124`, same family: ~$304k -> ~$389k;
- `gopfan2`, January 2025 Temperature Increase: ~$129k -> ~$179k;
- `gopfan2`, Global Heat Increase 2024: ~$165k -> ~$199k;
- `aenews2`, August 2024 hottest on record: ~$457k -> ~$482k.

Daily temperature can also absorb serious capital — e.g. Handsanitizer23's Atlanta March 17 position was roughly $18.7k cost -> $64.6k — but the historical ceiling visible in climate markets is much higher.

Current gopfan2 evidence is also large: roughly **91,697 YES shares** in “Will 2026 be the second-hottest year on record?” at about **29.3¢ average entry**, implying about **$26.9k raw cost** in one active Weather view.

Profile:
https://polymarket.com/profile/0xf2f6af4f27ec2dcf4072095ab804016e14cd5817

This is the capacity benchmark. A daily strategy does not need to beat it per trade; it needs to beat it in aggregate expected dollars after turnover.

---

# 2. GISTEMP is unusually attackable because the resolver calculation is public

NASA states that GISTEMP v4 uses:

- NOAA/NCEI adjusted GHCN v4 monthly station data (`qcf`);
- NOAA ERSST v5 ocean data.

NASA also publishes the GISTEMP v4 source package and documentation.

Official sources:

https://data.giss.nasa.gov/gistemp/sources_v4/
https://data.giss.nasa.gov/gistemp/sources/gistemp.html
https://data.giss.nasa.gov/gistemp/faq/

NASA's 2026 monthly release schedule is known in advance. The next relevant scheduled release after this research snapshot is:

**August 2026 GISTEMP -> September 10, 2026 at 11:00 AM EDT.**

Schedule:
https://data.giss.nasa.gov/gistemp/release_dates.html

This changes the problem from:

> forecast global temperature better than everyone

into the much more valuable late-cycle problem:

> reproduce the exact resolver algorithm from the same public inputs before the official table is published.

That can collapse uncertainty from a broad climate forecast to a narrow first-release value.

---

# 3. Public reconstruction evidence says this is feasible

A public GISTEMP specialist on Manifold has been reconstructing the NASA calculation from GHCNm/ERSST vintages.

Examples found in the indexed discussion:

## Historical reconstruction example

For a prior release, eight runs after ERSST became available produced approximately:

`123.99, 125.05, 125.80, 125.46, 125.89, 125.93, 124.88, 124.88`

in hundredths °C.

Median ≈ **1.2526°C**.

The market subsequently resolved at **1.26°C**.

The median error was therefore only about **0.007°C**, far smaller than Polymarket's typical 0.05°C GISTEMP bucket width.

Source discussion:
https://manifold.markets/ChristopherRandles/global-average-temperature-february

This is not our own audited backtest yet, but it establishes technical feasibility.

## April 2026 natural experiment

In the public April-2026 GISTEMP discussion, by the `ghcnm.v4.0.1.20260506` vintage the specialist wrote that the largest remaining station-coverage variables had disappeared and that the result looked likely to land around **1.18°C**.

The official April release was scheduled for May 11.

Polymarket's April 2026 Temperature Increase event generated roughly **$130k volume** in a late indexed snapshot, with the eventual 1.15–1.19°C bucket around **48¢**.

Polymarket:
https://polymarket.com/event/april-2026-temperature-increase-c

This is not yet a timestamp-perfect executable backtest because the crawl timestamp must be aligned with the exact GHCNm vintage and book depth. But if the public reconstruction already assigned, for example, 80% probability to the 1.15–1.19 bucket while an executable ask remained near 49¢, the fee-era economics would be enormous:

`fee(0.49) = 0.05 * 0.49 * 0.51 ≈ 0.01250`

`all_in_cost ≈ 0.5025`

At `q = 0.80`:

`EV/share ≈ 0.2975`

`expected ROI on committed dollars ≈ 59%`

This is the scale of opportunity worth prioritizing.

## July 2026 lead

A current public specialist states that the July production run used `ghcnm` dated `20260707` and that the first-release value is **1.18°C**.

Source:
https://manifold.markets/ChristopherRandles/global-average-temperature-may-2026-lqlSqsCy5O

NASA's direct current table could not be independently fetched in this research environment, so **1.18°C remains secondary-source evidence here, not independently verified NASA truth**.

Polymarket crawls from earlier in the July market showed the 1.20–1.24°C bucket at roughly **79–83%**, with 1.15–1.19 much lower.

Event:
https://polymarket.com/event/july-2026-temperature-increase-c-20260608140824583

The decisive research task is the exact timeline:

`upstream input availability -> reconstructed q -> Polymarket L2 -> NASA release`.

If the wrong favorite remained expensive after the decisive upstream files were public, this could be one of the highest-dollar repeatable Weather edges in the project.

---

# 4. GISTEMP trading should use the whole six-outcome ladder

Do not reduce the climate strategy to “buy the predicted bucket.”

For each GISTEMP bracket `i`, estimate first-release probability `q_i` and compare every executable expression:

`EV_yes_i = q_i - all_in_ask_yes_i`

`EV_no_i = (1-q_i) - all_in_ask_no_i`

If the market has a false 83% favorite while the reconstruction moves almost all mass elsewhere, the best use of depth may be:

- YES on the reconstructed winner;
- NO on the stale favorite;
- multiple NOs against impossible/outdated brackets;
- a NegRisk transformation route;
- passive maker quotes if the information half-life is long enough.

Rank marginal dollars across every book level.

This is exactly the same coherent-ladder formulation as daily temperature, but the resolver distribution comes from **dataset reconstruction** instead of airport forecasting.

---

# 5. Daily-temperature directional alpha is still strongly validated in the current fee regime

Weather fees activated under the current structure on March 30, 2026, so post-March-30 evidence is economically more relevant than earlier wins.

Current fee docs:
https://docs.polymarket.com/trading/fees

## `badatmath.` — underpriced exact YES / secondary mode

Official profile and leaderboard crawls repeatedly show successful fee-era temperature YES positions, commonly in roughly the 10–30¢ band.

Examples include Beijing, Taipei, Seoul, Kuala Lumpur, Busan, Tokyo, Dallas, Atlanta, Panama City and Wellington.

Recent leaderboard examples include trades displayed approximately as:

- Busan: ~$331 -> ~$1,597;
- Tokyo: ~$501 -> ~$1,656;
- Dallas: ~$377 -> ~$1,406;
- Atlanta: ~$475 -> ~$1,431;
- Panama: ~$216 -> ~$1,015.

Profile:
https://polymarket.com/profile/0x8fbd7cf5f806f563080864694415829f7229a959

This strongly supports a current-fee strategy that buys exact buckets when the weather posterior is **more concentrated than the market surface**.

## `gghff` — profitable NO / exact-bucket fade

The same fee-era ecosystem contains profitable specialists repeatedly taking NO exposure on exact buckets at intermediate prices.

Examples in indexed profile snapshots include:

- San Francisco 81°F/below NO around 34.6¢;
- Shanghai 34°C NO around 70.3¢;
- Chengdu 40°C NO around 59.6¢;
- Taipei 35°C NO around 59.6¢;
- Dallas 106–107°F NO around 65.2¢;
- Seattle 94–95°F NO around 75¢.

This is the opposite apparent side but the same mathematical edge:

> the market can be **too concentrated** around one exact outcome relative to a calibrated weather distribution.

## `0x6FF...` — adjacent-bucket distribution trading

A recent monthly Weather leader repeatedly owned several adjacent YES buckets in the same city/day, with exposure concentrated near the center and smaller tail legs.

Examples included multi-bucket NYC and Paris positions.

This is direct wallet evidence that a profitable fee-era strategy can express a **probability distribution**, not merely select one mode.

---

# 6. Best daily directional state variable: market concentration versus weather concentration

The coexistence of profitable YES specialists and profitable NO specialists suggests one compact state classification.

Let coherent market probabilities be `p_i` and calibrated weather probabilities be `q_i`.

### Local residual

`r_i = q_i - p_i`

### Distribution concentration

`H(q) = -sum_i q_i log(q_i)`

`H(p) = -sum_i p_i log(p_i)`

Define:

`entropy_gap = H(p) - H(q)`

Interpretation:

- `entropy_gap > 0`: weather posterior is more concentrated than market -> favored exact/adjacent YES is more likely to be underpriced;
- `entropy_gap < 0`: market is more concentrated than weather -> modal exact bucket may be overbet, creating NO/fade value.

The actual signal remains executable EV. Entropy is a state descriptor, not a trading rule.

A large forecast revision should also be explicit:

`delta_q_i = q_i(new vintage) - q_i(previous vintage)`.

Large `|delta_q|` + stale price justifies taker execution.
Small `|delta_q|` / quiet state favors maker execution.

---

# 7. Market making remains a base monetization layer, not the sole strategy

Direct transaction evidence already proves Poligarch acted as a zero-fee Weather maker.

Polymarket currently charges Weather makers zero platform trading fee and allocates a portion of taker fees to maker rebates.

This is economically valuable during quiet information states because it can add:

- spread;
- better entry price;
- rebate;
- optional liquidity reward;
- cheap accumulation of legs useful in full-ladder/NegRisk transformations.

But the research should not turn into “build a maker because Poligarch is profitable.”

When `q` moves 15 probability points and the stale ask is available, paying a 1-point taker fee is rational. `badatmath.` and the supplied wallet provide evidence that current specialists do cross when the directional edge is large.

Correct router:

`best_action = argmax(expected_net_dollars(action, depth, capital_time))`

where actions include maker quotes, taker YES/NO, baskets, inventory exits and terminal conversions.

---

# 8. Important correction: penny-tail forecasting was over-inferred from Struct

ColdMath is genuinely profitable, but several spectacular-looking cheap Weather “wins” in Struct are **not evidence that ColdMath correctly predicted a 1¢ bucket**.

A concrete example is Wellington March 28 16°C: Struct attributes a large positive row to that token because substantial value exited through `merge`, while the actual event resolved to a different temperature.

Therefore:

- ColdMath remains strong evidence for profitable inventory / transformation mechanics;
- those rows should **not** be used as proof of a magical penny-tail forecasting strategy;
- event-level cashflow accounting is mandatory for merge-heavy traders.

This demotes “cheap tail accumulation” as a standalone top-priority strategy.

Tails remain tradable only when `q_i` justifies them.

---

# 9. Capital allocation should be a global marginal-dollar queue

Do not preallocate 50% climate / 50% daily or any other fixed mix.

For every executable opportunity, estimate a marginal capacity curve:

`(dollars_in, expected_net_dollars, expected_lock_time)`.

Then rank incremental capital by something close to:

`capital_score = expected_net_dollars / expected_capital_time`

with correlation/overlap accounted for only when it materially changes portfolio return.

Typical ordering by state may be:

1. near-deterministic GISTEMP reconstruction with stale high-capacity book;
2. large fresh daily forecast/observation shock with stale depth;
3. profitable passive maker inventory in quiet markets;
4. smaller daily residuals / adjacent baskets;
5. terminal source-lock conversions / stale near-resolution quotes;
6. weak or speculative tails.

The ordering is empirical, not permanent.

---

# 10. Highest-value measurements from here

## Priority 1 — exact GISTEMP point-in-time reconstruction

For every month, snapshot every relevant upstream vintage and run the NASA algorithm.

Record:

`source_available_time`
`GHCNm qcf vintage`
`ERSST vintage`
`reconstructed LOTI`
`plausible production-vintage distribution`
`NASA first-release LOTI`
`Polymarket synchronized ladder/book`

Main statistic:

`P(correct 0.05C bucket | data available at t)`

Then compute executable PnL at the actual book.

The most important late-cycle uncertainty is often **which GHCNm vintage NASA will use**, not meteorology itself. Treat candidate input vintages as an ensemble.

## Priority 2 — live synchronized Weather L2

Historical on-chain trades cannot reconstruct canceled/resting orders because Polymarket's order placement and cancellation are off-chain.

Therefore continuously capture live full ladders to measure:

- real depth;
- maker fills;
- adverse selection;
- spread/rebate capture;
- forecast-release response;
- source-lock response;
- NegRisk basket capacity.

## Priority 3 — fee-era daily probability surface

For daily temperature cities, estimate `q_i` from exact resolver station/model/observation state and calculate all YES/NO/subset opportunities.

The minimum model comparison is:

- coherent market only;
- weather only;
- weather + market;
- weather + market + specialist flow only if flow adds executable PnL.

---

# 11. Smallest production architecture implied by the money

Only three economic engines are needed initially:

### Climate resolver engine

`public upstream climate data -> GISTEMP first-release distribution -> Polymarket ladder EV`

### Daily resolver engine

`weather vintages + observations -> exact-extrema distribution -> Polymarket ladder EV`

### Execution router

`all opportunities -> depth/fee/fill/capital-time -> highest expected net dollars`

Everything else is support.

---

# Bottom line

The project is now more profit-minded by making one hard priority change:

> **Do not spend all research effort squeezing another few points of skill from daily weather while the highest-profit Weather wallets demonstrate much larger climate-market capacity and the GISTEMP resolver itself is publicly reproducible.**

The strongest current portfolio of edges is:

1. **GISTEMP resolver reconstruction** for rare, high-capacity, potentially near-deterministic dislocations;
2. **daily exact-temperature distribution trading** for frequent cashflow — YES when the market is too diffuse, NO when it is too concentrated, adjacent baskets when multiple buckets are jointly cheap;
3. **maker execution** during quiet states to preserve edge and earn spread/rebates;
4. **fast taker execution** only for large information shocks;
5. **source-lock / NegRisk terminal trades** when uncertainty collapses;
6. tails only as probability-priced opportunities, not a strategy identity.

The next dollar of research should go into reproducing GISTEMP point-in-time and capturing live L2, because those two measurements determine both **edge** and **capacity** for the highest-dollar opportunities now visible.