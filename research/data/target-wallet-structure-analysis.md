# Target wallet — complete official-trade structural analysis

Generated: **2026-08-12T06:47:48.347989+00:00**

Wallet: `0xbddc2a7690bf600e347d5eb4a9c28f9f24e55d4f`

Sources: official Polymarket Data API `/trades` with both `takerOnly=false` and `takerOnly=true`.

- total fills: **1,766**
- taker-only endpoint rows: **1,457**
- rows classified TAKER by transaction hash: **1,457**
- rows classified MAKER: **309**
- raw traded notional: **$124,766.02**
- BUY fills: **1,353**; SELL fills: **413**

## Horizon distribution (local event date minus local trade date)

- T-1: **7 fills**
- T+0: **909 fills**
- T+1: **587 fills**
- T+2: **64 fills**

T+0 local-hour fill counts: `00:14, 01:46, 02:31, 03:58, 04:41, 05:47, 06:12, 07:30, 08:51, 09:33, 10:39, 11:46, 12:39, 13:41, 14:56, 15:82, 16:108, 17:73, 18:27, 19:30, 21:2, 22:2, 23:1`

T+1 local-hour fill counts: `00:6, 01:7, 02:18, 03:59, 04:38, 05:22, 06:15, 07:10, 08:10, 09:45, 10:19, 11:19, 12:11, 13:36, 14:15, 15:28, 16:19, 17:46, 18:24, 19:27, 20:32, 21:25, 22:21, 23:35`

## Execution role

Role is inferred only from the official API differential: if the transaction appears in the same user query with `takerOnly=true`, its user trade row is classified as TAKER; otherwise MAKER.
This should be cross-checked against `OrdersMatched.takerOrderMaker` on a sample before using it for fee accounting.

- BUY: **1,305 taker / 48 maker**
- SELL: **152 taker / 261 maker**

## Sizing structure

- BUY fills within 2¢ of an exact $1 raw notional: **946/1,353**
- BUY fills within 2¢ of an exact $5 raw notional: **813/1,353**
- most common exact-dollar BUY notionals:
  - `$100`: **232 fills**
  - `$50`: **128 fills**
  - `$200`: **101 fills**
  - `$5`: **81 fills**
  - `$3`: **66 fills**
  - `$30`: **64 fills**
  - `$10`: **52 fills**
  - `$1`: **39 fills**
  - `$20`: **30 fills**
  - `$300`: **27 fills**
  - `$40`: **26 fills**
  - `$150`: **23 fills**
  - `$70`: **14 fills**
  - `$250`: **11 fills**
  - `$80`: **8 fills**
  - `$35`: **5 fills**
  - `$25`: **4 fills**
  - `$56`: **3 fills**
  - `$2`: **3 fills**
  - `$4`: **2 fills**

## City concentration

- **Tel Aviv** — 301 fills, $24,604 raw notional, 129 buys/172 sells, 148 taker/153 maker
- **Istanbul** — 211 fills, $22,917 raw notional, 159 buys/52 sells, 180 taker/31 maker
- **Madrid** — 162 fills, $15,941 raw notional, 114 buys/48 sells, 117 taker/45 maker
- **Mexico City** — 86 fills, $7,096 raw notional, 68 buys/18 sells, 74 taker/12 maker
- **Ankara** — 68 fills, $3,922 raw notional, 51 buys/17 sells, 54 taker/14 maker
- **Wellington** — 74 fills, $3,870 raw notional, 68 buys/6 sells, 56 taker/18 maker
- **Milan** — 72 fills, $3,335 raw notional, 60 buys/12 sells, 72 taker/0 maker
- **Karachi** — 43 fills, $3,200 raw notional, 35 buys/8 sells, 41 taker/2 maker
- **Dallas** — 45 fills, $2,896 raw notional, 38 buys/7 sells, 45 taker/0 maker
- **New York City** — 27 fills, $2,894 raw notional, 23 buys/4 sells, 27 taker/0 maker
- **Paris** — 54 fills, $2,737 raw notional, 51 buys/3 sells, 52 taker/2 maker
- **Singapore** — 35 fills, $2,735 raw notional, 28 buys/7 sells, 35 taker/0 maker
- **Austin** — 34 fills, $2,390 raw notional, 29 buys/5 sells, 34 taker/0 maker
- **London** — 54 fills, $2,117 raw notional, 51 buys/3 sells, 46 taker/8 maker
- **Moscow** — 19 fills, $2,098 raw notional, 19 buys/0 sells, 19 taker/0 maker
- **Miami** — 37 fills, $1,815 raw notional, 36 buys/1 sells, 37 taker/0 maker
- **Wuhan** — 16 fills, $1,780 raw notional, 16 buys/0 sells, 16 taker/0 maker
- **Helsinki** — 30 fills, $1,756 raw notional, 27 buys/3 sells, 30 taker/0 maker
- **Lucknow** — 27 fills, $1,718 raw notional, 25 buys/2 sells, 27 taker/0 maker
- **Los Angeles** — 28 fills, $1,565 raw notional, 23 buys/5 sells, 22 taker/6 maker
- **Warsaw** — 24 fills, $1,421 raw notional, 20 buys/4 sells, 23 taker/1 maker
- **Shanghai** — 27 fills, $1,383 raw notional, 13 buys/14 sells, 14 taker/13 maker
- **Denver** — 23 fills, $1,362 raw notional, 22 buys/1 sells, 23 taker/0 maker
- **Munich** — 32 fills, $1,287 raw notional, 29 buys/3 sells, 32 taker/0 maker
- **Houston** — 34 fills, $1,168 raw notional, 33 buys/1 sells, 34 taker/0 maker

## Multi-bucket event expression

- unique event slugs traded: **715**
- events where wallet traded >=2 binary buckets: **87**
- median distinct buckets/event: **1**

Top multi-bucket events by raw notional:
- `highest-temperature-in-tel-aviv-on-august-12-2026` — **2 buckets**, 6 fills, **$1,471.76**
- `highest-temperature-in-madrid-on-july-27-2026` — **2 buckets**, 9 fills, **$1,374.40**
- `highest-temperature-in-karachi-on-july-23-2026` — **2 buckets**, 6 fills, **$1,310.77**
- `highest-temperature-in-madrid-on-july-21-2026` — **2 buckets**, 18 fills, **$1,056.29**
- `highest-temperature-in-tel-aviv-on-july-20-2026` — **2 buckets**, 8 fills, **$1,017.15**
- `highest-temperature-in-tel-aviv-on-august-7-2026` — **2 buckets**, 5 fills, **$1,003.72**
- `highest-temperature-in-tel-aviv-on-july-16-2026` — **2 buckets**, 7 fills, **$1,002.54**
- `highest-temperature-in-istanbul-on-august-4-2026` — **2 buckets**, 11 fills, **$973.77**
- `highest-temperature-in-istanbul-on-august-5-2026` — **2 buckets**, 9 fills, **$798.51**
- `highest-temperature-in-madrid-on-july-25-2026` — **2 buckets**, 11 fills, **$748.08**
- `highest-temperature-in-tel-aviv-on-july-31-2026` — **2 buckets**, 5 fills, **$682.12**
- `highest-temperature-in-madrid-on-july-17-2026` — **2 buckets**, 21 fills, **$663.47**
- `highest-temperature-in-istanbul-on-august-3-2026` — **2 buckets**, 6 fills, **$660.47**
- `highest-temperature-in-tel-aviv-on-august-2-2026` — **2 buckets**, 3 fills, **$614.53**
- `highest-temperature-in-tel-aviv-on-august-11-2026` — **2 buckets**, 3 fills, **$603.72**
- `highest-temperature-in-istanbul-on-august-11-2026` — **2 buckets**, 8 fills, **$600.00**
- `highest-temperature-in-madrid-on-july-26-2026` — **2 buckets**, 7 fills, **$517.41**
- `highest-temperature-in-los-angeles-on-july-14-2026` — **2 buckets**, 7 fills, **$485.84**
- `highest-temperature-in-nyc-on-july-27-2026` — **2 buckets**, 3 fills, **$456.00**
- `highest-temperature-in-tel-aviv-on-august-3-2026` — **2 buckets**, 2 fills, **$400.00**

## Fast within-event SELL → BUY rotations (<=5 minutes)

- total detected: **1**
- exact-C bucket deltas: `+1°C:1`

- `2026-06-25T01:11:47+00:00` `highest-temperature-in-milan-on-june-25-2026` — SELL 33°C @ 0.114191351 → 15s → BUY 34°C @ 0.4599999939; delta `1`; roles TAKER/TAKER

## UTC fill-hour histogram

`00:120, 01:88, 02:93, 03:40, 04:67, 05:99, 06:90, 07:79, 08:84, 09:84, 10:60, 11:57, 12:122, 13:175, 14:120, 15:59, 16:72, 17:59, 18:36, 19:33, 20:12, 21:24, 22:44, 23:49`

## Milan June 25 / June 30 — exact official rows

- `2026-06-24T01:58:13+00:00` — **BUY 61.224488 @ 0.489999998** ($29.999999 raw) — Will the highest temperature in Milan be 34°C on June 25? — **TAKER** — tx `0x70aecaf3a7a926c7cdc25c0a1e8ad45b1b5adaa897e4481c35b4d2d2ee335a15`
- `2026-06-24T02:28:49+00:00` — **BUY 193.784116 @ 0.1548114449** ($29.999999 raw) — Will the highest temperature in Milan be 33°C on June 25? — **TAKER** — tx `0xb83e0e6410a0d45427d92446ca3b3c4c1c4e7a39f252bda7bda0c4956e1712a3`
- `2026-06-25T01:11:47+00:00` — **SELL 193.78 @ 0.114191351** ($22.128000 raw) — Will the highest temperature in Milan be 33°C on June 25? — **TAKER** — tx `0xcf30826455e3efd4804cbae0b02545c5d63651d3efce93b4c3ff72f695a24974`
- `2026-06-25T01:12:02+00:00` — **BUY 65.21739 @ 0.4599999939** ($29.999999 raw) — Will the highest temperature in Milan be 34°C on June 25? — **TAKER** — tx `0xd15ca66b5762c6b8b249ed20ba3dd3ef1c25d3449f78d039c76637eaa483f706`
- `2026-06-29T01:55:11+00:00` — **BUY 102.116 @ 0.2937835403** ($30.000000 raw) — Will the highest temperature in Milan be 35°C on June 30? — **TAKER** — tx `0xb8499e6f5331322f90a4d2245d3485085a838f67c8903eb9d1120be52c4f67b6`

### Milan June 25 33°C realized raw round trip

- matched shares: **193.780000**
- entry: **15.4811¢**
- exit: **11.4191¢**
- raw price PnL before fees: **$-7.8714**
- holding time: **22.72 hours**

## Evidence-quality note

The file is complete with respect to the current official `/trades` response because it returned fewer than 10,000 rows. It still does not include CTF merge/split/redemption actions, so event-level cash PnL requires a later `/activity`/on-chain reconciliation.

