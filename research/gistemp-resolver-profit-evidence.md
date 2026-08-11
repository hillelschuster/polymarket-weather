# GISTEMP resolver alpha — profit evidence and exact forward test

Snapshot: **2026-08-12**

Objective: decide whether NASA GISTEMP markets deserve more capital/research than another increment of daily-temperature forecasting.

## Verdict

**Yes. GISTEMP resolver reconstruction is now the highest-value Weather research track by expected dollar upside, but one missing measurement prevents calling the edge historically proven at executable depth: the exact Polymarket L2 immediately after the decisive pre-release GHCNm vintages.**

The case is strong because four facts now coexist:

1. NASA publishes the exact analysis family, input sources and release schedule;
2. independent public researchers have reproduced the eventual 0.05°C Polymarket bracket from point-in-time GHCNm/ERSST information before NASA publication;
3. actual Polymarket wallets repeatedly made thousands of dollars in 2026 GISTEMP brackets under the current fee era;
4. historical climate-resolution markets demonstrate much larger five- and six-figure capacity than ordinary daily-temperature buckets.

The correct next action is not another proxy climate model. It is to **archive every upstream input vintage, run the resolver reconstruction, and capture synchronized full Polymarket L2 so the first high-confidence production signal can be priced at real depth.**

---

# 1. Resolver is public and scheduled

NASA GISTEMP v4 says its monthly tables are updated using current:

- NOAA/NCEI **GHCN v4** meteorological-station data;
- NOAA/NCEI **ERSST v5** ocean data.

NASA's FAQ explicitly says GISTEMP uses the homogenized/adjusted **`qcf`** GHCN file, not `qcu`.

NASA also publishes the GISTEMP source package and the pipeline documentation.

Sources:

- https://data.giss.nasa.gov/gistemp/
- https://data.giss.nasa.gov/gistemp/sources_v4/
- https://data.giss.nasa.gov/gistemp/sources/gistemp.html
- https://data.giss.nasa.gov/gistemp/faq/

The 2026 release schedule is known in advance. The next release relevant to this project is:

**August 2026 GISTEMP: September 10, 2026, 11:00 AM EDT.**

Schedule:
https://data.giss.nasa.gov/gistemp/release_dates.html

The current Polymarket August market resolves from the **first reported August 2026 LOTI value** in NASA's table; later revisions do not change the contract result.

Market:
https://polymarket.com/event/august-2026-temperature-increase-c-20260728155540489

This makes the late-cycle target exceptionally clean:

`P(first NASA LOTI bracket | exact public input vintages available before publication)`.

---

# 2. April 2026 gives the clearest point-in-time natural experiment

Polymarket's April event eventually resolved to the **1.15–1.19°C** bracket.

## Market before decisive station updates

A Polymarket crawl updated **May 5, 2026 at 03:21 UTC** showed:

- total event volume: **$298,553**;
- 1.15–1.19°C displayed probability: **77%**;
- executable displayed BUY YES: **80¢**;
- 1.10–1.14°C: BUY YES 22¢;
- 1.20–1.24°C: BUY YES 5¢.

Source:
https://polymarket.com/event/april-2026-temperature-increase-c

This was a genuinely liquid market by Weather standards; the question is whether the posterior became substantially sharper while the book still offered stale depth.

## Public point-in-time reconstruction

In the public Manifold GISTEMP discussion, `JRP` reconstructed the April value as successive GHCNm vintages arrived.

### May 5 vintage

`ghcnm.v4.0.1.20260505`

raw reconstruction around **1.19249°C**. After explicitly modeling the remaining uncertain regions, the post estimated roughly **80–85%** for the 1.15–1.20°C bracket and about **14%** for the higher 1.20–1.25°C bracket.

This matters because at an 80¢ ask the current Weather taker fee is:

`0.05 * 0.80 * 0.20 = 0.008/share`.

All-in cost ≈ **80.8¢**.

Therefore May 5 itself was **not** an obvious huge taker edge if the true bracket probability was only 80–85%. At 85%, EV is only about 4.2¢/share before any additional execution effect.

This prevents hindsight overstatement.

### May 6 vintage — the important information shock

`ghcnm.v4.0.1.20260506`

reconstruction:

**1.179077°C**.

The post says the Elizabeth/Antarctica coverage had arrived, the largest remaining variables were gone, and it did not expect any further update before release large enough to move the result into another bracket. It characterized the likely result as **1.18°C**.

### May 7

`117.73` hundredths-equivalent pipeline result. The researcher expected NASA to use this vintage and could not identify a plausible remaining box revision large enough to leave the bracket.

### May 8

`117.68`; no meaningful change.

### May 9

`117.78262`; with adequate coverage, the researcher described the chance of leaving the 1.15–1.20 bracket as effectively nil.

### Official result

The eventual NASA first release was **1.18°C**, and the discussion reports NASA production used GHCNm dated `20260507`, whose file timestamp was May 8 UTC.

Source:
https://manifold.markets/ChristopherRandles/global-average-temperature-april-20-UCysLsdu0L

## What is and is not proven

**Proven/observed:**

- by May 6 the public reconstruction had crossed from a meaningful two-bin uncertainty into a strongly concentrated 1.15–1.19°C view;
- the eventual first release landed at 1.18°C;
- the event had already traded almost $300k by May 5.

**Still missing:**

- exact synchronized CLOB ask/depth for the winning YES and stale-favorite NO legs immediately after the May 6 and May 7 input vintages became available.

Without that L2, do not claim a specific historical dollar arbitrage. The opportunity is a high-priority lead, not yet an audited fill simulation.

---

# 3. Wallet evidence: GISTEMP expertise has made real Polymarket dollars

Struct indexes wallet `0xa11376e9f170aaf97664cac13e9ab210a70193f4` (`ballzi.`) with repeated profitable GISTEMP positions.

Visible best wins include:

- March 2026 1.25–1.29°C YES: **+$5.02K**, buys ~$1.73K;
- April 2026 1.15–1.19°C YES: **+$3.35K**, buys ~$2.51K at ~41.7¢ average entry;
- May 2026 1.10–1.14°C YES: **+$3.18K**, buys ~$2.97K at ~52.8¢ average entry;
- February 2026 1.20–1.24°C YES: **+$2.11K**;
- October 2025 1.20–1.24°C YES: **+$1.78K**;
- November 2025 1.20–1.24°C YES: **+$1.42K**.

Source:
https://explorer.struct.to/traders/0xa11376e9f170aaf97664cac13e9ab210a70193f4

The same wallet is **negative overall across all market families** in Struct, roughly -$2.7K in the indexed snapshot. That is useful rather than embarrassing: it suggests the economically relevant object is potentially **GISTEMP-specific skill**, not generic trader reputation.

The May 2026 GISTEMP market occurred entirely after Polymarket's March 30 Fee Structure V2 expansion to Weather, so the +$3.18K May result is direct evidence that profitable GISTEMP trading survived the current fee regime.

Fee change:
https://docs.polymarket.com/changelog

Current Weather fee:
https://docs.polymarket.com/trading/fees

### Identity caveat

A Manifold participant using the handle `ballzi.` also discusses GISTEMP estimation. The matching handle is suggestive, but this research has **not independently verified cross-platform identity**. Do not use that as causal proof that the Polymarket wallet earned its profits from the exact reconstruction method described by JRP.

The stronger evidence is separate:

- public reconstruction demonstrably works;
- a Polymarket wallet demonstrably has repeated GISTEMP profits.

Joining those two causally is the next measurement, not an established fact.

---

# 4. Capacity: climate can absorb materially more than routine daily brackets

The current GISTEMP niche already reaches several thousand dollars per specialist per monthly bracket.

Older climate-resolution specialist portfolios demonstrate a much higher historical ceiling. For example, Struct's `gopfan2` page includes a 2024 global-heat bracket with roughly **$54K of buys** and **+$73.7K PnL**.

Source:
https://explorer.struct.to/traders/0xf2f6af4f27ec2dcf4072095ab804016e14cd5817

Older largest climate wins should be used as **capacity evidence**, not current net-edge evidence, because Polymarket's Weather fee structure changed on March 30, 2026.

The economically relevant current question is:

> as the August/September monthly market approaches release and liquidity builds, how many dollars can the reconstructed posterior consume before marginal all-in EV falls below the best daily-temperature alternative?

---

# 5. Current August 2026 market should be monitored, not forced

The August 2026 GISTEMP event opened July 28. The first indexed Polymarket snapshot showed essentially **zero volume** and incoherent/wide early executable quotes across its six outcomes.

Source:
https://polymarket.com/event/august-2026-temperature-increase-c-20260728155540489

By comparison, the July market later reached roughly **$36.7K volume**, and April reached almost $300K as resolution approached.

Therefore the profit-maximizing action today is not to deploy capital into an immature book. It is to:

1. preserve the exact upstream GHCNm/ERSST vintages now;
2. preserve full synchronized L2 from now forward;
3. wait for both posterior concentration and executable capacity;
4. then rank the GISTEMP trade against every live daily-weather opportunity by marginal expected dollars.

This is information preparation with a direct economic purpose, not a waiting rule.

---

# 6. Production evidence chain now implemented

Two compact collectors have been added to the repository.

## `scripts/gistemp_input_watch.py`

Archives changed point-in-time copies of:

- GHCNm adjusted `qcf`;
- target-month ERSST v5;
- NASA LOTI output.

For each retrieval it stores:

- receipt timestamp;
- ETag / Last-Modified;
- SHA256;
- bytes;
- archive path;
- append-only check log.

This preserves overwritten upstream vintages that cannot be reconstructed honestly after the fact.

## `scripts/gistemp_market_watch.py`

For one GISTEMP event slug it:

- fetches the Gamma event metadata;
- resolves every YES/NO `clobTokenId`;
- fetches all 12 books in one CLOB batch for a six-outcome event;
- saves full L2 depth with timestamps/hashes;
- calculates depth-aware full-YES-basket economics;
- calculates full-NO NegRisk conversion economics when `negRiskFeeBips` is available;
- records the fee assumption explicitly.

The collector uses public unauthenticated Polymarket market-data endpoints.

Relevant docs:

- https://docs.polymarket.com/api-reference/events/get-event-by-slug
- https://docs.polymarket.com/api-reference/market-data/get-order-books-request-body
- https://docs.polymarket.com/market-data/websocket/market-channel

The REST batch snapshot is intentionally the smallest first implementation. If the expected edge becomes fast enough that polling loses meaningful dollars, switch the same token set to the public market WebSocket.

---

# 7. Trading logic if the reconstruction becomes concentrated

Suppose reconstructed bracket probabilities are `q_i` and current full books are known.

Do not automatically buy the predicted YES.

At each depth level compare:

### Winning-bracket YES

`EV_yes_i = q_i - ask_i - taker_fee(ask_i)`

### NO against a stale favorite

`EV_no_j = (1-q_j) - ask_no_j - taker_fee(ask_no_j)`

### Multiple stale brackets

Evaluate the set of NOs and any available NegRisk transformation at actual depth.

### Maker alternative

If the upstream-data posterior is changing slowly and the next important vintage is not imminent, compare a passive quote against the immediate taker trade.

### Capital ranking

For every marginal book level:

`score = expected_net_dollars / expected_capital_time`

Then compare against daily-temperature opportunities.

The GISTEMP engine earns priority only when its actual marginal dollars win that comparison.

---

# 8. One important fee-era lesson from April

At 80¢ ask, current Weather taker cost is about **80.8¢** per share.

Therefore a model saying merely “the winner is probably 82%” is not useful enough. The valuable state is the **May 6-style collapse**, where one newly available input eliminates the major remaining bracket-crossing scenarios.

This suggests the optimal information trigger is not a fixed number of days before release. It is event-driven:

`new upstream vintage -> recompute bracket posterior -> measure entropy collapse / q jump -> compare to live depth`.

That is directly analogous to the daily-temperature forecast-revision engine, except GHCNm station coverage replaces ECMWF/METAR as the information shock.

---

# Bottom line

GISTEMP has moved from an interesting side track to the project's highest-value research engine because it combines:

- **resolver-exact public data and code**;
- **scheduled releases**;
- **public evidence of near-bracket-certainty before publication**;
- **real repeated Polymarket GISTEMP profits**;
- **historically large climate-market capacity**.

But the standard of proof remains money:

> the edge becomes validated only when a point-in-time reconstructed `q` is joined to synchronized executable L2 and produces positive fee-adjusted dollars at meaningful size.

The forward August 2026 capture is the fastest credible route to that evidence. Until the book develops, daily-temperature engines remain the likely source of frequent deployable capital; when GISTEMP reaches a May-6-style information state with depth, it should compete for capital immediately.