# Historical GISTEMP L2 proof path — 2026-08-12

Objective: close the only major gap in the April 2026 GISTEMP alpha case: **what executable depth was actually available immediately after the decisive May 6–9 GHCNm vintages?**

## Verdict

Polymarket's own public APIs do not provide historical resting order books. They provide current L2 and historical prices/trades, which cannot reconstruct orders that were cancelled or never filled.

A third-party archive, **PolymarketData**, currently claims:

- historical full L2 bid/ask snapshots;
- full ladder, not only top of book;
- 1-minute resolution;
- coverage from market creation for markets launched since August 2025;
- open and resolved markets;
- API endpoint `/v1/markets/{id_or_slug}/books`.

Source:
https://www.polymarketdata.co/polymarket-order-book-data

That claimed coverage includes the April/May/June/July 2026 GISTEMP events and can, if accurate, turn the current April evidence from a price/probability case into an **execution-capacity backtest**.

## Pricing implication

Published tiers on 2026-08-12:

- Free: $0, 1 month history, 10-minute granularity, **no order books**;
- Trader: $60/month, 1 month history, 1-minute L2;
- Pro: $120/month, 3 months history, 1-minute L2;
- Ultra: $360/month, **unlimited history**, 1-minute L2.

Source:
https://www.polymarketdata.co/pricing

The decisive April window is May 6–9. On Aug 12 it is just outside a three-month window. Therefore their published tiers imply that the relevant historical L2 requires the **Ultra / unlimited-history tier** unless they provide a custom one-off export.

## Profitability decision

Do **not** buy the archive merely to confirm one anecdote.

The $360 spend is justified only if the extraction is designed to answer several capital questions at once:

1. April 2026: May 5–11 full six-bucket GISTEMP ladder around every GHCNm update;
2. May 2026: equivalent release window;
3. June 2026: equivalent release window;
4. July 2026: equivalent release window;
5. highest-volume annual-rank event around each monthly NASA release;
6. optionally a sample of daily-temperature ladders around major observation/model shocks.

For every GISTEMP input vintage `t`, recover synchronized L2 and calculate:

`q_i(t)` — replica probability of bracket i;

`ask_i(x,t)` — VWAP cost for size x;

`taker_fee_i(x,t)` — actual market fee;

`EV_i(x,t) = x*q_i(t) - all_in_cost_i(x,t)`;

plus the corresponding NO expression and any NegRisk route.

Key outputs:

- first timestamp at which posterior is strongly concentrated in the eventual first-release bucket;
- maximum profitable size at that timestamp;
- cumulative executable net dollars before market convergence;
- how quickly the book repriced after each GHCNm/ERSST update;
- whether maker posting would have improved or harmed realized capture;
- dollars per release and dollars per $1,000 capital-hour.

## April-specific target

Known point-in-time evidence before L2 recovery:

- May 5 03:21 UTC: winning 1.15–1.19 bracket BUY YES around 80¢; event volume ~$298.6K;
- May 5 public reconstruction still only ~80–85% main-bin probability;
- May 6 GHCNm vintage produced ~1.179077°C and removed the largest remaining bracket-crossing uncertainties;
- May 7/8/9 reconstructions stayed well inside the same bracket;
- first NASA value = 1.18°C.

The decisive L2 query should cover at least:

`2026-05-05T00:00:00Z -> 2026-05-11T16:00:00Z`

at 1-minute resolution for all six binary markets in the event.

Then align the exact GHCNm file availability times rather than using calendar-day labels.

## Evidence quality caveat

PolymarketData is an independent commercial source, not Polymarket. Its coverage claims are not yet independently audited in this project.

Before paying, use whatever free/sample access is available to verify:

- market discovery finds a known GISTEMP event;
- timestamps match known public Polymarket price history;
- book levels are internally coherent;
- snapshots around a known live period reproduce contemporaneous public L2 within the expected 1-minute sampling error.

Only then use its historical books for money conclusions.

## Bottom line

There is now a credible route to the missing April execution evidence. The economic decision is simple:

> **$360 of historical L2 is worth buying only if a multi-release extraction can determine whether GISTEMP resolver reconstruction had at least several thousand dollars of repeatable executable net EV.**

Given the observed six-figure/million-dollar historical event volumes and repeated specialist GISTEMP profits, that information value is plausibly far above $360. The archive should be treated as a research-data purchase whose payoff is a capital-allocation decision, not as infrastructure.