# US ASOS observation alpha — reconstruct the integer-F resolver state before the crowd

Snapshot: **2026-08-11**

Purpose: isolate a potentially high-value same-day edge in US daily-temperature markets that comes from **measurement semantics and publication timing**, not from a more sophisticated weather forecast.

The central fact is subtle:

> **The temperature in a routine near-real-time METAR display is not necessarily the same information object as the ASOS daily maximum.**

That matters because Polymarket US high-temperature contracts resolve in whole degrees Fahrenheit, usually grouped into 2°F buckets.

---

# 1. Polymarket's US resolver object

Example: NYC June 20, 2026.

Polymarket rules state that the contract resolves to the range containing the **highest temperature recorded at LaGuardia Airport `KLGA` on Weather Underground**, in whole degrees Fahrenheit.

Rules also state:

- Weather Underground is the resolution source;
- the source is interpreted at **whole-degree Fahrenheit precision**;
- the market cannot resolve until the first datapoint of the following date is published;
- revisions before that first next-date datapoint are considered;
- later changes are ignored.

Example:
https://polymarket.com/event/highest-temperature-in-nyc-on-june-20-2026

This means the economically relevant variable is not generic NYC temperature and not an official climate-report maximum in the abstract. It is the Weather Underground airport-station value under this exact cutoff convention.

---

# 2. ASOS internally measures a different object from the routine displayed METAR temperature

NWS explains that an ASOS temperature sensor samples roughly every 10 seconds. The station forms stored one-minute values and rolling multi-minute averages, while the routine METAR temperature is transmitted under METAR reporting conventions.

NWS notes that the values seen in ordinary 5-minute observations can differ from the temperature internally tracked for the daily high/low. The true daily maximum can occur between displayed observations.

Sources:

https://www.weather.gov/lot/weather_observations_faq
https://www.weather.gov/lox/asostemperature

For US ASOS specifically, Iowa Environmental Mesonet's wagering-focused technical note summarizes the official daily max/min temperature object as a **2-minute average of high-frequency samples reported in integer Fahrenheit**.

Source:
https://mesonet.agron.iastate.edu/onsite/news.phtml?id=1469

This is exactly the precision Polymarket US buckets care about.

---

# 3. Whole-Celsius METAR transmission can lose the Fahrenheit bucket

ASOS internally stores temperature in whole Fahrenheit, but routine METAR transmission includes a mandatory whole-degree Celsius temperature field.

IEM documents the round-trip problem directly. Its example:

- station has an internal **78°F** value;
- METAR transmits **26°C**;
- converting 26°C back produces 78.8°F, which would be rounded/displayed as 79°F.

IEM therefore does not treat every apparently precise Fahrenheit conversion from whole-Celsius METAR data as reliable whole-Fahrenheit truth.

Source:
https://mesonet.agron.iastate.edu/info/datasets/metar.html

## Why this can flip a Polymarket bucket

US Polymarket ladders commonly use 2°F buckets such as:

- 86–87°F;
- 88–89°F.

But both 87°F and 88°F can map to **31°C** when reduced to a whole-Celsius METAR field.

Thus a routine `31°C` observation can be consistent with values on **opposite sides of the Polymarket 87/88°F bucket boundary**.

A strategy that simply converts the visible whole-Celsius METAR value back to Fahrenheit can therefore create false certainty at exactly the price boundary being traded.

---

# 4. The higher-fidelity METAR extrema fields

Aviation Weather Center documents additional METAR remark groups with tenths-of-Celsius precision:

## Hourly T-group

`TsnT'T'T'snT'dT'dT'd`

reports temperature/dewpoint to **0.1°C**.

## 6-hour maximum

`1snTxTxTx`

reports the **maximum temperature over the previous six hours to 0.1°C**.

## 24-hour maximum/minimum

A separate 24-hour extrema group can also be transmitted at designated times/stations.

Official specification:
https://www.connect.aviationweather.gov/help/data/

NWS confirms that 00Z, 06Z, 12Z and 18Z METARs at applicable US stations include 6-hour maximum/minimum temperatures.

Source:
https://www.weather.gov/lot/weather_observations_faq

---

# 5. The 6-hour max is particularly valuable for temperature betting

IEM's dedicated ASOS wagering note identifies three sources with reliable integer-Fahrenheit daily-extreme fidelity:

1. **METAR 6-hourly extrema summaries**;
2. **ASOS Daily Summary Message (DSM)**;
3. NWS **CLI/CF6** climate products.

IEM also states that it does **not know of a near-real-time source** that simultaneously preserves the ASOS official two-minute averaging and whole-Fahrenheit fidelity in every moment.

Source:
https://mesonet.agron.iastate.edu/onsite/news.phtml?id=1469

That data imperfection can be an information edge if the market is reacting to lower-fidelity app/website temperatures.

---

# 6. 00Z is an unusually useful daily event for US markets

The 00Z synoptic report arrives during the local evening across the continental US:

| Region | 00Z local time in summer | Approx role |
|---|---:|---|
| Eastern | 20:00 EDT | well after typical high |
| Central | 19:00 CDT | after/near end of heating |
| Mountain | 18:00 MDT | after/near high |
| Pacific | 17:00 PDT | late afternoon |

The 00Z report's 6-hour maximum therefore covers approximately:

- Eastern: 14:00–20:00 local;
- Central: 13:00–19:00;
- Mountain: 12:00–18:00;
- Pacific: 11:00–17:00.

That interval often contains the day's true high.

So the 00Z 6-hour maximum can provide a high-fidelity observation of the peak window **several hours before the local civil day ends**.

This creates a simple T+0 state update:

`known_peak_window_max_F = decode(00Z six-hour max)`

then estimate only:

`P(any later temperature exceeds that max before local midnight)`.

In many stable regimes this probability may be extremely small.

---

# 7. 18Z also matters, especially for Eastern/Central cities

18Z corresponds roughly to:

- 14:00 EDT;
- 13:00 CDT;
- 12:00 MDT;
- 11:00 PDT.

The 18Z six-hour max captures the morning through early-afternoon heating window.

For cities where the peak occurs early — marine layer onset, front passage, convection, sea breeze — this report can collapse the outcome distribution before the market expects it.

The high-value update schedule is therefore initially just:

- **18Z six-hour extrema**;
- **00Z six-hour extrema**;
- relevant SPECI/current observations between them.

No high-frequency sensor feed is required to test the hypothesis.

---

# 8. The Daily Summary Message is the later truth anchor

NWS describes ASOS Daily Summary Messages as containing the previous local day's daily maximum/minimum and occurrence time.

Source:
https://www.weather.gov/asos/InformationReporting.html

IEM notes that DSM tends to arrive before the NWS CLI climate product and carries a reliable max/min temperature.

For research:

- the DSM is useful as a high-quality end-of-day validation source;
- it can also reveal discrepancies between the final official ASOS max and what a generic hourly-METAR reconstruction would have produced.

For trading, the 6-hour groups are more interesting because they arrive while the market still has useful time value.

---

# 9. Weather Underground must still be empirically mapped

Polymarket resolves against **Weather Underground**, not directly against DSM/CLI/IEM.

Therefore do not silently replace the resolver with the official ASOS daily max.

The correct research is to measure which upstream observation representation reproduces the eventual Weather Underground/Polymarket bucket most reliably.

Candidate reconstructions:

1. max of mandatory whole-C METAR temperatures converted to F;
2. max of precise METAR T-group values;
3. max including SPECI;
4. 6-hour maximum groups;
5. IEM processed `tmpf`;
6. eventual DSM/CLI maximum;
7. combinations above.

A public weather-bot post-mortem independently found that adding T-groups, SPECI and 6-hour maxima materially improved its Wunderground-resolution reconstruction, but that is secondary code evidence and should be validated against actual Polymarket events.

---

# 10. The decisive historical experiment

For each resolved US daily-high event:

## Final label

`Y = Polymarket winning Fahrenheit bucket`.

## Reconstruct several observable states

At each key report time, especially 18Z and 00Z:

`M_wholeC(t)`
`M_Tgroup(t)`
`M_6hr(t)`
`M_IEM_tmpF(t)`

Then after day end:

`M_DSM`.

## Measure

### Resolver fidelity

For each reconstruction method:

`bucket_match_rate = P(reconstructed bucket == Polymarket winning bucket)`.

### Earliest-certainty time

For each event/method, record the first timestamp at which the eventual winning bucket became overwhelmingly likely given observed max + remaining heating model.

### Market response

Using Polymarket token price history, measure the winning-bucket price:

- 5 minutes before 18Z/00Z report;
- at report availability;
- +5m;
- +15m;
- +30m;
- +60m.

If the 6-hour max contains information the market incorporates slowly, this directly reveals executable observation-latency alpha.

---

# 11. A very small live signal can express this edge

For a US city at 00Z:

1. parse the 6-hour maximum from the station METAR;
2. map it to the Polymarket Fahrenheit ladder using the resolver's native precision;
3. combine it with the max already observed in the earlier 18Z interval;
4. use HRRR/LAMP/NBM/current conditions only to estimate probability of **exceeding the known maximum later**;
5. compare resulting bucket probabilities with executable asks/bids.

This is much simpler than forecasting the entire day's high from scratch.

Near peak, the probability problem becomes:

`P(final_max > known_max | remaining_hours)`.

If that probability is 2% while the market still prices a higher bucket at 15%, the edge is structurally clear.

---

# 12. This also changes historical backtesting

A backtest using only hourly `tmpc` or a generic weather API can mislabel the resolver state.

For US markets, store the raw METAR text so the following can be replayed exactly:

- T-group;
- 6-hour max;
- SPECI timing;
- report availability;
- local civil-day grouping.

The raw text is small. There is no reason to discard it and later guess what was reported.

---

# 13. Highest-value cities for this test

Start where both liquidity and supplied-wallet activity exist:

- Miami `KMIA`;
- NYC `KLGA`;
- Chicago `KORD`;
- Denver current resolver station from event rules;
- Los Angeles `KLAX`;
- Seattle `KSEA`;
- Dallas/Houston exact resolver stations from current rules.

The supplied wallet currently has visible US positions in Miami and Denver, while broader specialist activity and volumes are strong in NYC.

---

# Bottom line

US T+0 weather may contain an edge that does not require better NWP at all:

> **Read the ASOS extrema fields correctly and earlier than traders relying on generic temperature feeds.**

The 18Z/00Z six-hour max reports are especially attractive because they can reveal the integer-Fahrenheit peak-window maximum while the Polymarket event is still live.

The shortest experiment is to replay these reports against resolved Polymarket buckets and minute price history. If the market reprices slowly after them, this becomes one of the simplest high-confidence strategies in the project.