# Data quality traps

Snapshot: **2026-08-11**

Weather trading is unusually vulnerable to subtle target-definition errors. Several public projects already contain examples where the strategy looked valid until the data mapping was corrected.

## 1. `WEATHER` category is not a clean meteorological universe

Polymarket's WEATHER leaderboard is useful for discovering accounts, but the category/tag is not sufficient for research filtering.

Observed example: a recent WEATHER monthly leaderboard page listed `England-Mexico game rescheduled to different time?` among the category's biggest wins.

Therefore:

- category-level PnL is evidence about the platform category, not automatically daily-temperature PnL;
- identify actual meteorological contracts from event title + series + resolution rules;
- build daily-temperature and climate datasets separately.

## 2. All-time WEATHER PnL is heavily influenced by climate contracts

The all-time leaderboard's largest wins include:

- `2024 July hottest on record?`;
- global/January temperature-increase markets;
- hottest-year / hottest-month contracts;
- several large daily-airport-temperature wins.

So the six-figure leaders prove weather/climate markets can produce large profits, but their leaderboard totals do **not** by themselves prove a six-figure repeatable daily-high strategy.

Daily-high profitability must be measured independently.

## 3. Resolution station can differ from what a city name suggests

Examples in 2026 rules:

- NYC -> LaGuardia (`KLGA`);
- London -> London City Airport (`EGLC`);
- Milan -> Malpensa (`LIMC`);
- Paris -> Paris-Le Bourget (`LFPB`).

Using a consumer forecast for “Paris” or the nearest obvious large airport can solve the wrong problem.

A public bot has explicitly documented a historical wrong-Paris-station bug. That is enough reason to treat station mapping as immutable event data, not hard-coded city folklore.

## 4. Resolver display is not identical to raw meteorological truth

Contracts often reference a particular public historical page such as Wunderground and specify whole °F/°C outcomes. The value we forecast is the value that page will finalize under the event rules.

Potential differences from raw METAR/reanalysis include:

- integer reporting/rounding;
- special 6-hour maximum groups;
- local-day boundaries;
- late/revised station reports;
- source processing conventions.

Empirically learn the raw-observation -> resolver-display map.

## 5. Local date must be station-local

A UTC-date implementation can attach the wrong day's observations to US/Asia markets. This is a concrete failure mode visible in public bot code comments/fixes.

Every event needs:

- station timezone;
- settlement local date;
- exact cutoff for which observation belongs to which day.

## 6. Historical forecast != historical weather

Reanalysis/ERA5 is an estimate of what happened. It is not what the model predicted at trade time.

For strategy research distinguish:

- **forecast issued before trade** — valid predictor input;
- **observation known before trade** — valid predictor input;
- **reanalysis / final observation after event** — outcome/evaluation only.

Using the latter as a forecast input is look-ahead leakage.

## 7. “Historical forecast API” timestamps need scrutiny

Aggregators can expose old model runs conveniently, but we still need to know:

- model cycle time;
- first public availability time;
- data processing delay;
- whether values were later corrected/reprocessed;
- exact model version.

This is critical for forecast-release latency studies.

## 8. Open-Meteo `best_match` is not a stable research model identity

`best_match` is useful operationally, but it can select/compose model sources according to provider logic. For a scientific comparison, store named model outputs separately.

We need to know whether an edge came from ECMWF, GFS/NBM, a local model, or an aggregator change.

## 9. Ensemble member counts are not comparable across models

Fifty ECMWF members plus thirty-ish GFS members does not mean ECMWF deserves 5/8 of the predictive weight. Member count is a numerical design choice, not evidence weight.

Calibrate per model, then blend distributions.

## 10. CLOB midpoint is not fill price

Polymarket's UI/display can use midpoint; a real buyer pays asks. Historical midpoint backtests systematically overstate edge when spreads are wide.

For every economic result label which price was used:

- last trade;
- midpoint;
- best bid/ask;
- depth-walked fill estimate;
- actual fill.

Only the latter two are executable proxies.

## 11. Current fee regime is market-specific

Current docs define Weather taker fees and maker rebates, but fee applicability is per market (`feesEnabled`) and the platform's fee structure changed in 2026.

Do not retroactively charge today's schedule to older markets without checking their actual regime.

## 12. Negative-risk transaction logs are easy to misread

Current CTF Exchange V2 can settle complementary, mint and merge matches involving many orders. The exchange contract can appear as a counterparty in emitted events.

The user-supplied `0xbddc...55d4f` wallet is a concrete example: public Polygon transactions contain aggregate negative-risk settlements where the address appears in different maker/taker contexts inside one transaction.

For wallet strategy inference:

- decode the whole match;
- distinguish signed taker order from maker fills;
- do not infer “market maker” from one log field.

## 13. Off-chain quotes are not all in the blockchain archive

Polymarket matches orders off-chain and settles fills on-chain. Resting order placements and cancellations are therefore not fully recoverable from fill logs alone.

Historical wallet classification can confidently use executed behavior, but not reconstruct every quote the wallet posted.

## 14. Public bot PnL is self-reported until reproduced

GitHub README claims can be useful hypothesis generators. They are not evidence equivalent to:

- public wallet realized PnL;
- raw resolved market data;
- point-in-time forecasts;
- executable price reconstruction.

Keep those evidence classes separate in every research note.

## 15. Profile/proxy/address identity can be messy

Polymarket APIs commonly use the user's profile/proxy wallet. On-chain settlement can involve proxy/safe/base addresses and exchange adapters. A username can also change.

Canonical research key should be the **proxy wallet returned by Polymarket for the profile/leaderboard**, with aliases recorded separately.

The user's example profile suffix `-1774968947489` is presentation/account naming; the underlying address is the 40-hex wallet portion.

## 16. Resolved PnL and cash flow are different

Do not estimate wallet profitability by summing trade cash flows alone. Polymarket now exposes closed positions with realized PnL, positions and accounting snapshots; use those where appropriate and reconcile with trades/on-chain fills.

## Research rule

Every result table should carry these provenance columns where relevant:

`source, observed_at, issue_time, valid_time, resolver_station, resolver_rule_version, price_type, fee_regime`

That is enough to prevent most silent false edges without building a heavyweight data-governance system.

## References

- Polymarket WEATHER leaderboard: https://polymarket.com/leaderboard/weather/all/profit
- Leaderboard API docs: https://docs.polymarket.com/api-reference/core/get-trader-leaderboard-rankings
- Closed positions: https://docs.polymarket.com/api-reference/core/get-closed-positions-for-a-user
- Accounting snapshot: https://docs.polymarket.com/api-reference/misc/download-an-accounting-snapshot-zip-of-csvs
- CLOB orderbook: https://docs.polymarket.com/trading/orderbook
- Fees: https://docs.polymarket.com/trading/fees
- CTF Exchange V2: https://github.com/Polymarket/ctf-exchange-v2
