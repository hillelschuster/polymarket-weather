# Milan post-18Z probe — what is now known

Snapshot: **2026-08-12**

Target wallet:

`0xbddc2a7690bf600e347d5eb4a9c28f9f24e55d4f`

## Verdict

The Milan timing signal remains interesting, but the next model should **not** be a deterministic-max-direction rule.

The archived ECMWF deterministic runs show that both recovered post-18Z actions occurred after a **lower** deterministic daily-maximum revision. That does not invalidate forecast-driven trading because an exact-temperature contract is priced from a probability distribution and from the executable market price, not from the sign of the point-forecast change.

The attempted higher-value reconstruction — exact historical ECMWF ensemble mean/spread vintages — is blocked through the tested Open-Meteo route: the API explicitly reports that the requested old `ecmwf_ifs025_ensemble_mean` run is not available.

So the smallest profitable next research step is a **point-in-time multi-model distribution** from archived deterministic runs, not more broad source research.

---

## 1. Deterministic evidence already captured

Source data:

- `research/data/milan-forecast-revision-probe.json`
- `research/data/milan-forecast-revision-probe.md`

### June 25

Wallet at roughly 01:12 UTC:

- SELL 33°C YES: 193.78 shares @ ~11.42¢
- BUY 34°C YES: 65.21739 shares @ 46¢

ECMWF 12Z -> 18Z daily maxima for June 25:

- LIMC: **33.3°C -> 32.8°C**
- LIML: **34.8°C -> 34.1°C**

### June 30

Wallet at 01:55:11 UTC on June 29:

- BUY 35°C YES: 102.116 shares @ ~29.38¢ raw

ECMWF 12Z -> 18Z daily maxima for June 30:

- LIMC: **34.3°C -> 33.9°C**
- LIML: **36.1°C -> 34.9°C**

For June 30, the LIML move is a useful exact-bucket example: a point forecast can move downward while the probability of exactly 35°C rises because the center moves from above the bucket toward it.

---

## 2. Important correction to the event-study logic

A wallet BUY does **not** require `Delta q > 0`.

A wallet SELL does **not** require `Delta q < 0`.

The economically correct conditions are level-versus-price conditions after the new information arrives:

`BUY if q_new - all_in_ask > required_edge`

`SELL owned YES if net_bid - q_new > required_edge`

A forecast revision can lower both `q_33` and `q_34`, yet 34 can still be a buy and 33 a sell if the market ladder is mispriced relative to the new posterior.

Therefore the earlier diagnostic

`trade_side * Delta q`

is useful only as a secondary timing statistic. It is **not** the decisive profitability test.

The decisive event study is:

`edge_i(t) = q_i(new information set) - executable_price_i(t) - costs`

and then markout / settlement PnL conditional on that edge.

---

## 3. Ensemble archive probe

Open-Meteo currently documents:

- ECMWF ensemble mean and spread through the Ensemble Mean API;
- extended retention for ensemble mean/spread;
- individual ensemble members retained only for a short period.

Docs:

https://open-meteo.com/en/docs/ensemble-mean-api

The API implementation exposes the model identifier:

`ecmwf_ifs025_ensemble_mean`

Open-Meteo source:

https://github.com/open-meteo/open-meteo/blob/main/Sources/App/Controllers/ForecastapiController.swift

We tested exact run retrieval for:

`run=2026-06-24T18:00`

at LIMC using:

- `temperature_2m`
- `temperature_2m_spread`
- `models=ecmwf_ifs025_ensemble_mean`

The exact captured response is committed at:

`research/data/milan-ensemble-run-error.json`

API result:

```json
{
  "reason": "The requested model run is not available. Model: ecmwf_ifs025_ensemble_mean, run: 2026-06-24T18:00Z",
  "error": true
}
```

The broader four-run probe is at:

- `research/data/milan-ensemble-mean-probe.json`
- `research/data/milan-ensemble-mean-probe.md`

All tested 12Z/18Z historical run requests returned the same class of HTTP 400 failure.

This is a data-availability result, not evidence against the ensemble hypothesis.

---

## 4. Highest-value next measurement

Open-Meteo Single Runs preserves exact deterministic run vintages for ECMWF and, from April 2026 onward, other supported models.

Docs:

https://open-meteo.com/en/docs/single-runs-api

That means the Milan cases can be reconstructed as a **multi-model pseudo-ensemble** without needing unavailable old ECMWF ensemble members.

For the same pre/post-18Z windows, collect only resolver-relevant temperature paths from models that were genuinely available before the wallet trade, for example:

- ECMWF IFS;
- DWD ICON / ICON-EU;
- Météo-France ARPEGE Europe;
- ItaliaMeteo ICON-2I when its run timing qualifies.

Then convert the cross-model + station-bias state into bucket probabilities and compare directly with the executable Polymarket ladder.

The minimal object is:

`q_i = P(resolver daily max rounds/lands in bucket i | all forecasts available at t)`

not a single model's daily maximum.

---

## 5. Why this is the right next branch

It preserves the strongest part of the original thesis:

- repeatable post-release wallet timing;
- exact-temperature ladder structure;
- underused weather-model information;
- a simple probability calculation rather than infrastructure.

It also removes the weakest assumption exposed by the new data:

> that the sign of a deterministic ECMWF max revision should match the wallet trade side.

The next useful result is therefore very small and concrete:

> reconstruct the June 24 12Z/18Z **multi-model** probability state for Milan 33/34°C and the June 28 12Z/18Z state for 35°C, using only runs actually available before the fills.
