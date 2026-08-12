# T+0 observation profitability replication

Snapshot: **2026-08-12**

## Verdict

The five-case replication shows that same-day resolver observations can be followed by large short-horizon Polymarket repricing, but the effect is highly event-dependent.

Two cases are economically strong: **NYC July 20** and **London July 12**. Wellington is positive but much thinner. Chicago June 29 is unstable under a +10m reference. Chicago June 20 is a useful negative control where the information was already almost fully priced.

Primary artifacts:

- `research/data/t0-observation-markout-sample.json`
- `research/data/t0-observation-execution.json`

## Five-case price paths

| Case | -5m | 0m | +5m | +15m | +30m | +60m |
|---|---:|---:|---:|---:|---:|---:|
| London Jul12 27C before 28C breach | 0.1200 | 0.1950 | 0.1200 | 0.0005 | 0.0010 | 0.0005 |
| Wellington Jul21 11C before 12C breach | 0.2120 | 0.0410 | 0.2390 | 0.1045 | 0.2715 | 0.0005 |
| NYC Jul20 82-83F first winning-bucket observation | 0.3300 | 0.4950 | 0.9865 | 0.9975 | 0.9955 | 0.9985 |
| Chicago Jun29 92-93F first winning-bucket observation | 0.5250 | 0.5050 | 0.8000 | 0.9200 | 0.7850 | 0.5950 |
| Chicago Jun20 76-77F late-extrema report | 0.9960 | 0.9960 | 0.9960 | 0.9960 | 0.9960 | 0.9960 |

This rejects a blanket “trade every observation” thesis. Some observation states carry very large new information; others carry almost none.

## Actual post-signal prints

The execution reconstruction uses actual Data API trade prints on the economically favorable token after each observation timestamp and a CLOB historical price at +10m as a short-horizon reference.

For fee adjustment it uses each market's CLOB fee parameter `r=0.05` and subtracts `r*p*(1-p)` per share. These totals measure historical opportunity volume; they do not assume one participant could capture every print.

| Case | Favorable token | 0-10m printed qty | Gross positive markout | Fee-adjusted positive markout |
|---|---|---:|---:|---:|
| London Jul12 | NO | 6,693.22 | $60.72 | **$57.73** |
| Wellington Jul21 | NO | 11,036.51 | $12.43 | **$11.65** |
| NYC Jul20 | YES | 2,392.93 | $283.97 | **$273.71** |
| Chicago Jun29 | YES | 158.95 | $0.28 | **$0.12** |
| Chicago Jun20 | YES | 466.34 | $1.40 | **$1.24** |

## London July 12

At `13:20 UTC`, EGLC printed 28C after previously topping at 27C. That observation mechanically eliminated the 27C exact bucket if the resolver path incorporated the report normally.

The first observed 27C NO trade after the timestamp was about **0.9072**. During the first minute:

- 0-30s: 211.94 shares, VWAP ~0.9072, fee-adjusted +10m markout **$18.66**;
- 30-60s: 244.77 shares, VWAP ~0.9111, fee-adjusted +10m markout **$20.64**.

Combined first-minute evidence: **456.71 shares** and approximately **$39.30** of fee-adjusted +10m markout in actual prints.

This is the cleanest case because the key state change is monotone: once a higher daily maximum is validly recorded, the lower exact maximum cannot later become the winner.

## NYC July 20

At `21:51 UTC`, the KLGA precise T-group entered the eventual 82-83F winning bucket.

The YES mark moved roughly:

`0.495 at anchor -> 0.9865 by +5m -> ~0.9935 around +10m`.

The first recorded YES trade after the observation timestamp was **155.55 shares at 0.59679**.

First-minute actual prints:

- 0-30s: 478.67 shares, VWAP ~0.6044, fee-adjusted +10m markout **$180.52**;
- 30-60s: 298.55 shares, VWAP ~0.7570, fee-adjusted +10m markout **$67.87**.

Combined: **777.22 shares** and approximately **$248.39** of fee-adjusted +10m markout.

Unlike London, entering the bucket did not mathematically guarantee it would remain the final maximum, so this case still requires a calibrated probability of no later threshold crossing.

## Wellington July 21

At the 02:30 UTC observation, NZWN crossed from the 11C bucket into 12C+, eliminating 11C as the final exact maximum under the observed path.

The favorable NO side was already near 0.99 by the first observed post-signal trade. Despite more than 11k printed shares over ten minutes, fee-adjusted positive markout was only about **$11.65**.

This shows the same structural event can have much less residual economic value when the market has already repriced or reacts faster.

## Negative controls

### Chicago June 29

The price path moved sharply at some horizons, but the +10m reference was only 0.725 and the path was volatile. Fee-adjusted positive markout in the sampled ten-minute prints was only **$0.12**. This is not strong executable evidence.

### Chicago June 20

The bucket was already around 0.996 before the late extrema report. The new report added almost no market information. This is the correct behavior for a scanner to classify as already priced.

## What the sample says about profitability

The promising edge is not “weather observations are good.” It is narrower:

> **Certain resolver-state changes create abrupt probability discontinuities, and in some historical events actual market prints remained materially away from the later short-horizon price after the observation timestamp.**

The largest remaining uncertainty is **true source availability latency**. METAR observation time is not automatically identical to the instant the report became publicly retrievable. NYC repriced inside the first minute and London produced a strongly favorable print within seconds, so exact publication/ingestion timestamps matter materially.

## Highest-value next measurement

Do a live shadow measurement on active T+0 markets using one clock:

`source arrival timestamp -> resolver state change -> contemporaneous CLOB book -> 1m/5m/10m markout`.

The historical sample is now sufficient to justify measuring that latency directly rather than expanding broad meteorological research first.
