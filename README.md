# polymarket-weather

Research and trading work focused on extracting durable net PnL from Polymarket weather markets.

## Current authoritative synthesis

- [`research/exploitative-alpha-discovery-2026-08-14.md`](research/exploitative-alpha-discovery-2026-08-14.md) — current executive edge matrix, top alpha theses, formulas, resolver/fee corrections, friction audit, data architecture and profit-ranked implementation roadmap.

The current highest-value implementation action is to build a **synchronized first-seen weather/model + full Polymarket L2 recorder**. It is the smallest dataset that can measure ASOS/model-release latency, stale executable depth, maker adverse selection, information-response half-life and real capacity under the same clock.

## Current money thesis

One resolver-aligned probability surface should support two execution regimes:

1. **Maker-first during ordinary information states:** maintain exact resolver probabilities across the full mutually-exclusive ladder, quote around fair value, exploit relative-value/NegRisk incoherence, and measure fill-conditioned adverse selection.
2. **Taker after fresh information shocks:** cancel stale quotes, recompute fair value from new observations/model vintages, and cross only the depth whose probability edge survives fees, spread, slippage/impact and model uncertainty.

The strongest current alpha families are:

1. forecast-aware maker / full-ladder trading;
2. US ASOS extrema / resolver-state certainty collapse;
3. AIFS / NWP first-seen probability revisions;
4. GISTEMP / annual-rank / seasonal-extreme vintage replication;
5. spatial/upwind propagation as a remaining-exceedance feature;
6. specialist-wallet reverse engineering to infer hidden sources, clocks and execution behavior;
7. pure complete-set / NegRisk structural arbitrage when executable baskets violate payout identities.

The target is **net executable expected value and realized dollar PnL**, after price, fee, depth, fill, latency and capital lock.

## Highest-value research

- [`research/exploitative-alpha-discovery-2026-08-14.md`](research/exploitative-alpha-discovery-2026-08-14.md) — current integrated alpha and implementation synthesis
- [`research/minimal-logic-material.md`](research/minimal-logic-material.md) — smallest eventual trading logic implied by the evidence
- [`research/edge-economics.md`](research/edge-economics.md) — fee-adjusted probability edge and expected-dollar math
- [`research/execution-routing.md`](research/execution-routing.md) — simple maker-vs-taker rule based on fill probability and edge decay
- [`research/next-research.md`](research/next-research.md) — profit-ranked next measurements

### Daily extrema / city forecasting

- [`research/us-asos-case-studies.md`](research/us-asos-case-studies.md) — first resolver-bucket observation in resolved US high markets
- [`research/us-asos-low-alpha.md`](research/us-asos-low-alpha.md) — same running-extreme logic for daily lows
- [`research/us-asos-observation-alpha.md`](research/us-asos-observation-alpha.md) — ASOS/METAR precision, T-groups, SPECI and extrema semantics
- [`research/point-in-time-forecast-reconstruction.md`](research/point-in-time-forecast-reconstruction.md) — replay historical forecast vintages without a weather warehouse
- [`research/model-priority-matrix.md`](research/model-priority-matrix.md) — money-ranked local/global model pairs by city
- [`research/calibration-design.md`](research/calibration-design.md) — recent bias + empirical residual distribution + minimal blends
- [`research/market-calibration-prior.md`](research/market-calibration-prior.md) — test price calibration by horizon instead of assuming favorite/longshot bias
- [`research/city-source-map.md`](research/city-source-map.md) — exact resolver and best direct/local source by high-value city
- [`research/aifs-hypothesis-finalization-2026-08-13.md`](research/aifs-hypothesis-finalization-2026-08-13.md) — AIFS dissemination advantage, parameter limitation and decisive prospective test

### Execution / market structure

- [`research/forecast-aware-maker-merge.md`](research/forecast-aware-maker-merge.md) — corrected maker + complementary inventory formulation and merge-attribution caveat
- [`research/market-microstructure.md`](research/market-microstructure.md) — CLOB, fees, rebates and ladder structure
- [`research/execution-economics-third-pass.md`](research/execution-economics-third-pass.md) — execution economics and specialist evidence

### Specialist-wallet evidence

- [`research/wallet-history-acquisition.md`](research/wallet-history-acquisition.md) — recovered exact fills, fees, timestamps and token IDs for the supplied wallet
- [`research/wallet-history-followup.md`](research/wallet-history-followup.md) — resolved outcomes, active exits and Struct history/PnL routes
- [`research/milan-18z-release-case.md`](research/milan-18z-release-case.md) — repeated Milan revaluation ~1–2h after ECMWF 18Z availability
- [`research/wallet-forecast-purity.md`](research/wallet-forecast-purity.md) — separate directional forecast skill from merge/split/negative-risk inventory activity
- [`research/specialist-archetypes.md`](research/specialist-archetypes.md) — observed profitable trader expressions under one probability-surface model
- [`research/extreme-favorite-economics.md`](research/extreme-favorite-economics.md) — why 99.8–99.9¢ weather bets can lose money despite extreme win rates
- [`research/wallets.md`](research/wallets.md) — broader specialist decomposition framework

### Climate / high-capacity GISTEMP

- [`research/gistemp-basis-alpha.md`](research/gistemp-basis-alpha.md) — direct NASA-replica thesis, ERSST/ERA5T/GHCN information ladder and capacity
- [`research/gistemp-input-vintages.md`](research/gistemp-input-vintages.md) — daily qcf vintages and the pre-NASA release clock
- [`research/gistemp-first-release-labels.md`](research/gistemp-first-release-labels.md) — 20+ settlement-faithful historical paid brackets from Polymarket
- [`research/annual-rank-alpha.md`](research/annual-rank-alpha.md) — derive annual hottest-year rank from the same monthly distributions
- [`research/profit-evidence.md`](research/profit-evidence.md) — observed WEATHER leaderboard profits and capacity by market family

## Broader reference research

- [`research/README.md`](research/README.md) — research index and current synthesis map
- [`research/edge-thesis.md`](research/edge-thesis.md) — persistence mechanisms and detailed hypotheses
- [`research/weather-math.md`](research/weather-math.md) — resolver/extrema probability math
- [`research/resolution-alpha.md`](research/resolution-alpha.md) — settlement mechanics as information
- [`research/release-timing.md`](research/release-timing.md) — forecast/observation release clocks
- [`research/minimal-data-reconstruction.md`](research/minimal-data-reconstruction.md) — smallest official Polymarket API dataset for wallet/price studies
- [`research/market-families.md`](research/market-families.md) — highs, lows, rainfall, wind and climate families
- [`research/public-bot-code-audit.md`](research/public-bot-code-audit.md) — exploitable gaps in public weather bots
- [`research/zero-edge-paper-audit.md`](research/zero-edge-paper-audit.md) — audit of the strongest negative live-weather study
- [`research/bots-and-tools.md`](research/bots-and-tools.md) — public project survey
- [`research/data-sources.md`](research/data-sources.md) — forecast/observation/market feeds
- [`research/data-quality.md`](research/data-quality.md) — point-in-time truth details
- [`research/deep-research-2026-08-11.md`](research/deep-research-2026-08-11.md) — expanded August research pass

Research snapshot: **2026-08-14**.
