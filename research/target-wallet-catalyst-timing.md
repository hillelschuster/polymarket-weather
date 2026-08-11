# Target wallet catalyst timing — directional taker evidence

Snapshot: **2026-08-11**

Wallet:

`0xbddc2a7690bf600e347d5eb4a9c28f9f24e55d4f`

Purpose: refine the supplied-wallet hypothesis after recovering exact on-chain timing for two fee-paying purchases and a coarse early-hours exit.

## Verdict

The supplied wallet should currently be treated as a **directional information taker**, not as the maker/merge archetype represented by Poligarch and ColdMath.

The evidence supports a narrower rule than “trade the 18Z ECMWF release”:

> **Cross the book when a newly available forecast/observation state moves the calibrated exact-bucket probability enough to clear taker fee + spread + impact; later sell or otherwise neutralize a bucket when the posterior collapses.**

The Milan trades suggest the previous 18Z global cycle is one important catalyst window. The July 12 purchase proves it is not the only one.

---

# 1. Milan June 30 — exact fee-paying taker purchase

Transaction:

`0xb8499e6f5331322f90a4d2245d3485085a838f67c8903eb9d1120be52c4f67b6`

PolygonScan:

https://polygonscan.com/tx/0xb8499e6f5331322f90a4d2245d3485085a838f67c8903eb9d1120be52c4f67b6

Timestamp:

`2026-06-29 01:55:11 UTC`

Headline action:

- bought **102.116 YES** shares;
- Milan June 30 — 35°C;
- headline consideration **$30.00**.

The transaction logs resolve the execution role unambiguously:

`OrdersMatched.takerOrderMaker = supplied wallet`

and the target OrderFilled row contains:

- `side = 0`;
- target token = Milan June 30 35°C YES token;
- `makerAmountFilled = 30.000000 pUSD`;
- `takerAmountFilled = 102.116000 shares`;
- `fee = 1.059320 pUSD`.

The wallet transferred **31.05932 pUSD** to the exchange.

Therefore:

- raw price = `30 / 102.116 = 29.3783¢`;
- fee/share = `1.05932 / 102.116 = 1.03736¢`;
- all-in cash/share = `31.05932 / 102.116 = 30.4157¢`.

This is direct proof that the wallet accepted the Weather taker fee to acquire the view immediately.

The event later resolved 34°C, so this exact 35°C bucket lost if the wallet retained it through settlement.

---

# 2. Information window for the Milan purchase

Open-Meteo's official Single Runs documentation states that major global models generally require approximately **4–6 hours** after initialization before forecast data becomes available, and ECMWF HRES-style runs are initialized every six hours.

Official docs:

https://open-meteo.com/en/docs/single-runs-api

At the 01:55 UTC purchase:

- the prior Jun 28 **18Z** global cycle was the latest six-hour cycle plausibly fully disseminated;
- the Jun 29 **00Z** cycle would generally still be processing/unavailable under a 4–6 hour release lag.

This makes the trade consistent with reacting to information available after the 18Z forecast refresh.

It does **not** prove that ECMWF alone generated the signal. Other global/regional sources and observation updates may also have been available.

The decisive historical test remains:

`Δq_35 = q_35(after latest available vintages) - q_35(before prior vintages)`

and whether `Δq_35` was large enough that:

`q_35_new > 0.304157 + required_execution_margin`.

---

# 3. Milan June 25 — early-hours losing-bucket reduction

Struct market:

https://explorer.struct.to/markets/highest-temperature-in-milan-on-june-25-2026-33c

Indexed market snapshot:

`2026-06-25 03:36 UTC`.

The supplied wallet row shows:

- YES 33°C;
- price ~10.9¢;
- share change **-193.78**;
- ~$21.1 value;
- relative age `2h`.

The coarse age label places the reduction roughly in the early UTC hours, plausibly around **01–02 UTC**, before Milan's daytime maximum developed.

The final winning bucket was 35°C.

### Inference

The timing makes an **overnight forecast revision** more plausible than a reaction to the day's realized maximum.

The same broad information window as the Jun 29 01:55 purchase is suggestive: both lie after a plausible 18Z global-model dissemination window and before the next 00Z global run would ordinarily be available.

But this remains only a two-case clue because:

- Struct age is rounded/coarse;
- exact sell transaction hash is not recovered;
- preceding 33°C acquisition is missing;
- exact forecast vintages are not yet retrieved.

Do not hard-code an 18Z strategy from this evidence.

---

# 4. July 12 — exact counterexample to an 18Z-only rule

Transaction:

`0xa980bbca4a7df7cc9a6a80efaacf0b277181e963a73ce2625a9dc8618e8a9597`

PolygonScan:

https://polygonscan.com/tx/0xa980bbca4a7df7cc9a6a80efaacf0b277181e963a73ce2625a9dc8618e8a9597

Exact timestamp:

`2026-07-12 13:16:32 UTC`.

The transaction again identifies:

`OrdersMatched.takerOrderMaker = supplied wallet`.

Target OrderFilled row:

- token `91076181803621459956200090324917139595424901620108017335569536029558392706177`;
- `makerAmountFilled = 44.274000 pUSD`;
- `takerAmountFilled = 166.680000 shares`;
- `fee = 1.625690 pUSD`.

The target wallet transferred **45.89969 pUSD** into the exchange.

Therefore:

- raw price = `44.274 / 166.68 = 26.5611¢`;
- fee/share = `1.62569 / 166.68 = 0.97532¢`;
- all-in price = `45.89969 / 166.68 = 27.5364¢`.

This is another direct example where the wallet paid almost one cent/share in Weather taker fee because it preferred immediate execution.

The transaction occurred at 13:16 UTC, so the strategy cannot be reduced to a single overnight 18Z cycle.

The specific market identity of this token remains unresolved in the indexed sources used here. The neg-risk transaction includes Poligarch among counterparties, but that does not imply they held opposite meteorological views after economic normalization.

---

# 5. Economic implication: conviction must be materially larger than the displayed fee

The two directly recovered taker buys paid:

- Milan: **~1.037¢ fee/share**;
- Jul 12: **~0.975¢ fee/share**.

This is before considering the spread already embedded in the ask and any book-walking impact.

Therefore the target wallet is not behaving as if a 0.5–1 probability-point model disagreement is sufficient.

The relevant threshold is:

`q_new - executable_ask - fee - impact > required_margin`.

If the eventual research model cannot generate **several percentage points** of credible probability revision on these fills, it is probably missing the wallet's actual information source or calibration edge.

---

# 6. Updated catalyst model

Do not organize the eventual collector around only ECMWF clock times.

For every city maintain an event stream of **information availability**, including:

- ECMWF/global deterministic cycles;
- regional/high-resolution model cycles;
- local national-agency guidance;
- ensemble updates where available;
- METAR/SPECI and resolver-source observations;
- observed running maximum/minimum;
- source corrections/finalization;
- neighboring market moves if they reveal external information first.

At each catalyst `r` calculate:

`Δq_i(r) = q_i(after r) - q_i(before r)`.

Then test the target-wallet fill process against:

- sign agreement between trade and `Δq_i`;
- magnitude of `|Δq_i|`;
- time from source availability to fill;
- market price change before fill;
- 5m / 30m / 2h markout;
- settlement outcome;
- realized PnL if later exits are recovered.

The highest-value statistic is not whether trades occur at a particular clock hour. It is:

> **how much target-wallet trade intensity and post-fill markout rise as fresh calibrated probability revision increases.**

---

# 7. Execution synthesis with maker/merge research

The current specialist evidence supports two complementary execution regimes.

## Quiet / slowly changing fair value

Prefer the Poligarch/ColdMath-style maker path:

- post zero-fee maker liquidity around own fair probability;
- skew quotes by inventory and forecast uncertainty;
- acquire complementary inventory when profitable;
- merge matched YES/NO to recycle collateral;
- add rebates/rewards only when actually earned/eligible.

## Fresh large catalyst

Prefer the supplied-wallet-style taker path when:

`EV_cross > EV_wait_for_maker_fill`.

Actions:

- cancel stale maker quotes first;
- cross only depth that remains materially mispriced after current taker fee;
- update all ladder buckets coherently;
- later reduce positions when posterior value drops below executable exit/transform value.

The eventual strategy is therefore not “maker” versus “taker.” It is **state-dependent routing driven by information half-life and edge size**.

---

# 8. Highest-value remaining data

For the supplied wallet:

1. exact Jun 25 sell transaction + all preceding 33°C buys;
2. all fills surrounding the Jun 30 35°C buy, especially any later exit;
3. direct point-in-time forecast vintages bracketing both Milan actions;
4. a larger sample of target-wallet transaction timestamps to measure catalyst clustering;
5. post-fill market markouts.

For monetization:

1. one chronological Poligarch/ColdMath Weather binary with complementary maker fills followed by merge;
2. matched-lot pair capture and first-leg exposure time;
3. maker adverse selection around the same forecast/observation catalysts.

Together these answer the two questions that matter:

- **when is the weather information worth crossing for?**
- **when is the edge slow enough to monetize passively and recycle through merge?**
