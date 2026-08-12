# London July 12 observation-catalyst profitability

Snapshot: **2026-08-12**

## Verdict

This event materially raises the priority of **same-day resolver-observation trading** over further generic forecast-source research.

At `2026-07-12T13:16:32Z`, the supplied directional wallet paid **27.54¢ all-in** for 166.68 shares of **London 27°C YES**. London City Airport / EGLC had last reported **27.0°C** at 12:50 UTC. The next archived EGLC observation, at **13:20 UTC — only 208 seconds after the fill — was 28.0°C**. Because a daily maximum is monotone, that observation killed 27°C YES for settlement purposes. The contract ultimately resolved **28°C**.

The market repriced almost immediately:

| Horizon from target fill | 27°C YES market price | Markout vs target all-in | Dollar markout on 166.68 shares |
|---|---:|---:|---:|
| ~1m | 20.0¢ | -7.54¢/share | **-$12.56** |
| ~5m | 12.0¢ | -15.54¢/share | **-$25.90** |
| ~30m | 0.1¢ | -27.44¢/share | **-$45.73** |
| ~2h | 0.05¢ | -27.49¢/share | **-$45.82** |

If the target wallet held the fill to settlement, its all-in loss was approximately **$45.90**.

This is stronger for strategy design than another isolated forecast-revision case because the economically decisive information was tied to a **known resolver station and a recurrent observation cadence**.

---

## 1. Exact overlap with Poligarch

The same transaction directly contained the two archetypes already identified in the repository:

- target wallet `0xbddc...5d4f`: fee-paying **taker**;
- Poligarch `0xb40e...7cc9`: zero-fee **maker**.

Public trade history identifies the market as:

**Will the highest temperature in London be 27°C on July 12?**

and shows Poligarch taking the complementary **27°C NO** side in the same transaction:

- 15 NO @ 76¢;
- 5 NO @ 79¢;
- 5 NO @ 80¢.

For those 25 shares:

- cash cost = **$19.35**;
- weighted average = **77.4¢**;
- final payout after 27°C lost = **$25.00**;
- gross settlement profit = **$5.65**;
- gross return on cash cost = **29.2%**;
- maker fee on the inspected Poligarch fill path = **0** before any rebate contribution.

Do not interpret target's 26.56¢ aggregate YES sweep and Poligarch's 77.4¢ average NO fills as one exact complementary pair. The target transaction matched multiple makers and prices. The economically relevant point is that Poligarch supplied/accumulated the side that became certain shortly afterward while the target crossed aggressively into the losing side.

Poligarch was also buying 27°C NO repeatedly in the minutes before the target fill, including activity around 13:02, 13:09, 13:12 and 13:14 UTC. Public wallet activity alone does not prove every one of those fills was maker, but it does establish material NO-side inventory accumulation immediately before the threshold breach.

---

## 2. Resolver state immediately before the trade

IEM EGLC observations, used here as a point-in-time research proxy for the contract's Wunderground EGLC resolver:

| UTC | temperature |
|---|---:|
| 10:20 | 25°C |
| 10:50 | 26°C |
| 11:20 | 26°C |
| 11:50 | 27°C |
| 12:20 | 27°C |
| 12:50 | 27°C |
| **13:16:32** | **target trade** |
| **13:20** | **28°C** |
| 13:50 | 28°C |
| 14:20 | 28°C |
| 14:50 | 28°C |

So this was **not** a case where 28°C had already been publicly observed at EGLC before the target trade. The profitable information problem was shorter-horizon:

> Given a running maximum of 27°C, only minutes before the next observation, what is the probability that the station exceeds 27°C during the remaining heating window?

That is a cleaner state variable than a generic daily-temperature forecast.

---

## 3. The profitable object for T+0 exact buckets

For exact bucket `k` after the station has already reached `k`, the YES probability is approximately a **survival probability**:

`q_k(t) = P(no future resolver observation exceeds k before the daily maximum is locked | state at t)`

For the complementary NO:

`q_no(t) = 1 - q_k(t)`

State should be kept minimal and point-in-time:

- running resolver maximum;
- latest resolver observation and its age;
- time to next expected station report;
- recent resolver temperature slope;
- neighboring / upstream station observations when useful;
- latest already-available high-resolution forecast for the remaining hours;
- solar/cloud/wind state only insofar as it improves exceedance probability;
- executable YES/NO prices and depth.

The trade is then ordinary EV math.

For a maker NO fill at price `p_no`:

`EV/share ≈ q_no - p_no + expected_rebate`

For a taker action, subtract the actual taker fee and impact.

The critical feature is **time-to-next-resolver-update**. When a station update can change an exact bucket from uncertain to impossible in one print, stale quotes immediately before that print have unusually high adverse-selection risk.

---

## 4. Production implication

The current highest-value live architecture should explicitly separate observation states:

### Between resolver updates

Quote passively only where the current survival/exceedance estimate leaves enough margin for fill-conditioned adverse selection.

### Approaching a high-information resolver update

Recompute `P(exceed current bucket)` from the freshest station/nearby/forecast state.

- cancel maker quotes that are vulnerable to the likely print;
- skew passive inventory toward the favored side when the edge is large enough;
- cross as taker only when the probability edge exceeds fee + spread + impact.

### Immediately after a threshold breach

The previous exact bucket is mechanically dead. Any stale positive YES bid is sellable value; any stale NO ask below near-certainty is buyable value, subject only to actual executable depth and resolver-source confidence.

This is potentially faster and more deterministic than waiting for model-cycle repricing because the state transition is tied directly to the contract's monotone resolver variable.

---

## 5. Why this matters for profitability

The London case has all the ingredients we wanted in one event:

1. exact resolver station;
2. precise target-wallet taker fill and fee;
3. same-transaction specialist maker participation;
4. public point-in-time station observations;
5. minute-level market markout;
6. a threshold breach only 208 seconds after the trade;
7. final settlement confirming the breach side.

The observed economics are large enough that execution details are not a rounding error. The target lost roughly **27.5¢/share** of all-in value within about half an hour; Poligarch's same-transaction 25-share NO slice had **22.6¢/share** of gross settlement value above acquisition cost.

This does not prove that Poligarch predicted the 13:20 print from meteorology. It proves that a profitable specialist was positioned on the right side of exactly the resolver-update transition that a production system can model explicitly.

The smallest next evidence step is therefore **not more generic model enumeration**. It is to run this exact resolver-survival reconstruction across a compact sample of same-day temperature events and measure:

`pre-update edge -> fill -> next resolver print -> 1m/5m/30m markout -> net PnL`

If the effect repeats, the first live strategy should prioritize **T+0 threshold-survival / scheduled-observation alpha**, with maker execution between updates and aggressive quote withdrawal or directional taking around likely threshold breaches.

---

## 6. Money-critical data defect discovered during this reconstruction

`markets-by-token` primary/secondary ordering must **not** be treated as Yes/No ordering.

For this London NegRisk condition:

- target token `9107618...706177` is the **secondary_token_id**;
- the CLOB market explicitly labels that same token **Yes**;
- the other / primary token is explicitly labeled **No**.

The current enrichment helper assumes `primary = Yes` and `secondary = No`. That can invert economic sides and corrupt PnL attribution on NegRisk markets. Any production or research consumer must derive outcome side from explicit CLOB/Gamma token labels, never primary/secondary position. Existing metadata cache entries created under the old assumption should be invalidated when that correction lands.

This defect was discovered because profitability reconstruction forced token, cashflow and resolver state to agree; it must be corrected before using the enriched wallet history for strategy inference.

---

## Evidence files

- `research/data/july12-overlap-profitability.json`
- `research/data/july12-overlap-profitability.md`
- `research/data/london-july12-resolver-state.json`
- `research/data/london-july12-resolver-state.md`
- `research/maker-economics-continuation-2026-08-12.md`
- `research/target-wallet-catalyst-timing.md`
