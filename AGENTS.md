# AGENTS.md — Make Money From Weather Forecasting

## Objective

Maximize realistic long-run net income from Polymarket weather markets.

Everything in this repository exists to improve one of these variables:

- forecast probability accuracy at the exact settlement target;
- information timing;
- executable price;
- fill quality;
- fee/rebate economics;
- capacity;
- bankroll compounding.

Realized net PnL is the scoreboard.

## Operating rules

1. **Search for alpha, not architecture.** Find the strongest profitable formulation of each weather-market inefficiency. Add code, data and infrastructure in proportion to their expected PnL contribution.
2. **Model the resolver.** The prediction target is the contract's exact station, source, measurement convention, civil-day window, precision and revision rule. Generic city weather is a weaker proxy.
3. **Forecast distributions, not temperatures.** Convert point, ensemble and observation data into calibrated probabilities for the exact Polymarket buckets.
4. **Exploit monotone state.** Daily highs, daily lows, monthly rainfall totals and monthly maxima accumulate information through time. Update fair value as the realized state becomes constrained.
5. **Exploit information timing.** Track when model runs, METAR/SPECI/official observations, climate datasets and resolver updates first become available, then measure market repricing latency.
6. **Use the entire ladder.** Temperature buckets form one mutually-exclusive probability surface. Enforce probability coherence and exploit relative-value discrepancies across outcomes and negative-risk conversions.
7. **Optimize executable EV.** Use bid/ask/depth, fee schedule, maker rebates, fill probability and expected markout. Midpoint edge is descriptive; executable net edge makes money.
8. **Treat market price as information.** Measure the incremental predictive value of weather data, wallet flow and microstructure relative to the market rather than pretending the crowd contains no signal.
9. **Reverse-engineer profitable specialists.** Public wallet trades, positions and realized PnL are a dataset. Extract timing, city, horizon, bucket, direction, price and markout fingerprints.
10. **Prefer causal, structural edges.** Resolver mechanics, forecast-vintage latency, observation conditioning, calibration error, longshot bias, negative-risk relationships and maker economics deserve priority over generic indicators.
11. **Use point-in-time evidence.** Every forecast, observation and price used in research carries its actual availability timestamp. This preserves genuine alpha measurement.
12. **Preserve promising strategies.** When evidence is incomplete, improve measurement and adjust economic confidence. When evidence identifies a defect, fix the smallest money-relevant defect while preserving the underlying edge.
13. **Keep implementation small.** Direct APIs, explicit formulas, compact data tables and understandable code are preferred. Complexity earns its place through expected net income.
14. **Rank by dollars, not beauty.** Compare expected PnL/day, capacity, turnover, capital lock, correlation and decay. A smaller percentage edge with much larger capacity can dominate.

## Current implementation priority — 2026-08-14

Read first:

- `research/exploitative-alpha-discovery-2026-08-14.md`
- `research/next-research.md`

The next highest-value component is a **single synchronized first-seen information + Polymarket L2 recorder**. It should capture exact resolver metadata, raw station observations, model-vintage first availability, complete relevant order-book state and order/fill lifecycle timestamps under one clock.

This measurement comes before another broad model build because it determines:

- whether ASOS/METAR information actually leads the book;
- whether AIFS/GFS/HRRR revisions actually lead the book;
- how much stale executable depth exists after each information shock;
- maker adverse selection and information-response half-life;
- the real capacity curve of each candidate signal.

Production routing should use one resolver-aligned probability surface:

- **ordinary state:** maker-first around calibrated fair value;
- **fresh information shock:** cancel stale quotes, then take only depth with positive marginal EV after fee, spread, impact and model uncertainty;
- **structural opportunity:** continuously scan full-ladder / NegRisk equivalents, but count profit only after all leg costs and fill risk.

Never hard-code city -> resolver station assumptions. Parse and archive the exact contract rules/source/station/unit/bucket/cutoff metadata before a market becomes tradeable.

## Core research question

> What information about a weather settlement becomes knowable before Polymarket prices it correctly, and what is the highest-PnL way to monetize that gap?

## Behavioral constraints

1. **Answer only what is asked.** Provide direct answers to questions. Do not run commands, restart processes, modify files, or spawn subagents unless explicitly instructed.
2. **Require explicit confirmation.** Never edit code, modify configuration, or execute system actions without prior user approval. Propose first and wait for a clear green light.
3. **Strict output formatting.** No tables, no flowcharts, no ASCII diagrams. Use clean markdown bullet points, code snippets, and indented text only.
4. **No superlatives or false certainty.** Never use terms like '100% guaranteed win', 'mathematically impossible', 'risk-free', or 'physical certainty' regarding weather outcomes or trading strategies. Calibrate confidence levels strictly to historical empirical data. Weather systems exhibit non-monotonic behavior (warm advection, nocturnal heat spikes, downslope winds, convective frontal collapses, sensor anomalies). Treat all weather outcomes as probabilistic distributions with tail risk.
