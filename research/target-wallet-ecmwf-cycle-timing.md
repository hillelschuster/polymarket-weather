# Target wallet Milan timing — repeated post-18Z ECMWF behavior

Snapshot: **2026-08-12**

Wallet:

`0xbddc2a7690bf600e347d5eb4a9c28f9f24e55d4f`

## Verdict

Two independently recovered Milan trades from the supplied wallet now fall in nearly the same UTC/local clock window, immediately after the prior ECMWF 18Z forecast cycle becomes available and well before the next 00Z cycle.

- **June 30 event — 35°C YES BUY:** exact fill at **2026-06-29 01:55:11 UTC** / 03:55 Rome.
- **June 25 event — 33°C YES SELL:** Struct crawl timestamp **2026-06-25 03:36 UTC**, with the wallet row displayed as **2h old**, placing the fill roughly around the 01–02 UTC region, subject to Struct's coarse relative-age display.

Both are overnight European trades, far before the local daytime temperature peak.

This materially strengthens the hypothesis that the wallet trades **forecast-cycle revisions**, not only same-day observations or static forecasts.

---

# 1. Official ECMWF dissemination window

ECMWF's official dissemination schedule for the control forecast (formerly HRES) states:

- 18 UTC run, forecast steps 0–90: **23:45 → 00:12 UTC**;
- steps 93–144: **00:12 → 00:27 UTC**;
- next 00 UTC run, steps 0–90: **05:45 → 06:12 UTC**.

Official source:

https://confluence.ecmwf.int/pages/viewpage.action?pageId=685871196

That creates a clean information window from roughly 00:27 until 05:45 UTC in which the full relevant short-range 18Z control run exists but the 00Z control run does not yet.

Open-Meteo independently documents that its Single Runs API preserves exact ECMWF IFS initialisations and that run time is **not** public availability time.

Source:

https://open-meteo.com/en/docs/single-runs-api

---

# 2. June 30 — exact post-18Z BUY

Recovered transaction:

`0xb8499e6f5331322f90a4d2245d3485085a838f67c8903eb9d1120be52c4f67b6`

Market:

**Milan June 30 — 35°C YES**.

Exact fill:

- timestamp: **2026-06-29 01:55:11 UTC**;
- raw price: ~29.38¢;
- fee: $1.05932;
- effective cost: ~30.42¢/share;
- shares: 102.116.

At 01:55 UTC:

- the June 28 18Z short-range control output had been fully disseminated for more than an hour;
- the June 29 00Z run had not yet begun dissemination.

The bucket eventually lost; 34°C resolved YES.

This remains a probabilistic trade, but its timing is highly compatible with reacting to the 18Z model state.

---

# 3. June 25 — newly recovered timing on losing-bucket SELL

Struct market:

https://explorer.struct.to/markets/highest-temperature-in-milan-on-june-25-2026-33c

The indexed page includes an absolute snapshot timestamp:

**2026-06-25 03:36 UTC**.

The supplied wallet's trade row is displayed as:

- outcome: YES;
- price: **10.9¢**;
- share change: **-193.78**;
- value: **~$21.1**;
- age: **2h**.

Struct's relative-age display is coarse, so do not claim an exact transaction second from this field. But the row clearly places the sell in the early-UTC overnight window, approximately around the 01–02 UTC region.

That means the sell occurred:

- after the June 24 18Z ECMWF short-range control run was distributed;
- before the June 25 00Z control run became available;
- many hours before Milan's normal daytime maximum.

The event ultimately resolved **35°C**; 33°C paid zero.

### Exit value saved

Gross value recovered at 10.9¢:

`193.78 * 0.109 = ~$21.122`.

If the entire exit were pessimistically treated as a taker sell at the current Weather fee formula:

`fee/share = 0.05 * 0.109 * 0.891`.

Estimated total fee:

`~$0.941`.

Estimated net sale value:

`~$20.181`.

Because the 33°C token later settled at zero, the exit preserved roughly **$20–$21 of remaining position value** versus mechanically holding those 193.78 shares to settlement.

This does not reveal the position's total realized PnL because the earlier acquisition basis is still missing.

---

# 4. Why the repeated clock time matters

One post-18Z fill could be coincidence.

Two Milan actions with opposite economic directions in almost the same overnight window are more informative:

- June 29 ~01:55 UTC: **buy** a next-day 35°C bucket;
- June 25 ~01–02 UTC: **sell** a same-day 33°C bucket that later loses.

The common object is not side. It is **fresh probability information after a model run**.

This is exactly what the composite strategy hypothesis predicts:

1. ingest a new forecast vintage;
2. rebuild the full exact-temperature probability ladder;
3. buy buckets whose posterior moves above executable all-in ask;
4. sell held buckets whose posterior falls below executable net bid.

The June 25 sell is particularly useful because it is a *negative revision* case: the bot materially reduced a bucket while other weather traders were still buying that same bucket around 11–12¢ in the same indexed table.

---

# 5. What still prevents proof

The missing decisive data are now very specific:

1. exact transaction hash and second-level timestamp for the June 25 33°C sell;
2. earlier acquisition(s) and basis for those 193.78 shares;
3. exact June 24 12Z and 18Z ECMWF IFS daily-max paths at LIMC;
4. ICON-EU / ItaliaMeteo ICON-2I / ARPEGE revisions available before the sell;
5. synchronized Polymarket ladder before and after the forecast releases.

Direct Open-Meteo Single Runs retrieval is the shortest weather-side route:

`https://single-runs-api.open-meteo.com/v1/forecast`

using:

- LIMC coordinates;
- `models=ecmwf_ifs`;
- `run=2026-06-24T12:00`;
- `run=2026-06-24T18:00`;
- hourly `temperature_2m`;
- timezone `Europe/Rome`;
- calculate maximum over June 25 local civil day.

This environment can read the documentation but currently cannot execute arbitrary parameterized Open-Meteo requests, so the actual run values are not claimed here.

---

# 6. Immediate production implication if this pattern survives a larger sample

For European temperature markets, one high-value live trigger should be the **actual availability** of the ECMWF 18Z short-range run around midnight UTC.

Minimal loop:

`new 18Z data available`

`-> compute station-specific daily-max distribution`

`-> compare q_new against previous q_old and live ladder`

`-> cancel stale maker quotes`

`-> cross only buckets with large fee-adjusted revision edge`

`-> replace maker quotes around q_new`.

The economically important feature is:

`delta_q_i = q_i(new run) - q_i(previous run)`.

Candidate taker trigger:

`q_i(new) - executable_ask_i - taker_fee_i > required_edge`

Candidate exit trigger for owned YES:

`net_bid_i > q_i(new)`.

The supplied wallet's recovered behavior is consistent with both directions of this rule.

---

# Bottom line

The strongest new directional evidence is no longer merely that the target wallet sells losers.

It is the **timing**:

> two recovered Milan trades, one entry and one exit, occur in the post-18Z/pre-00Z ECMWF window around ~02 UTC, suggesting the wallet may systematically trade fresh European forecast cycles.

The next highest-value measurement is to retrieve the exact June 24 12Z→18Z LIMC forecast change. If that revision moved the daily-max distribution away from 33°C before the wallet's sell, this becomes direct event-level evidence of the strategy's causal signal.