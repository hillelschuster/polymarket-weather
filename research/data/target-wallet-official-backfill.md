# Official Polymarket target-wallet backfill

Generated: **2026-08-12T06:45:21.060065+00:00**

Wallet: `0xbddc2a7690bf600e347d5eb4a9c28f9f24e55d4f`

Source: official public Polymarket Data API `/trades` with `takerOnly=false`.

- rows returned by API: **1,766**
- weather-classified rows: **1,766**
- response hit 10,000-row cap: **False**
- earliest classified weather fill: **2026-04-26T09:18:52+00:00**
- latest classified weather fill: **2026-08-12T05:07:42+00:00**

## Milan June 25 / June 30 rows

- `2026-06-24T01:58:13+00:00` — **BUY 61.224488 @ 0.489999998** — Will the highest temperature in Milan be 34°C on June 25? / Yes — tx `0x70aecaf3a7a926c7cdc25c0a1e8ad45b1b5adaa897e4481c35b4d2d2ee335a15`
- `2026-06-24T02:28:49+00:00` — **BUY 193.784116 @ 0.1548114449** — Will the highest temperature in Milan be 33°C on June 25? / Yes — tx `0xb83e0e6410a0d45427d92446ca3b3c4c1c4e7a39f252bda7bda0c4956e1712a3`
- `2026-06-25T01:11:47+00:00` — **SELL 193.78 @ 0.114191351** — Will the highest temperature in Milan be 33°C on June 25? / Yes — tx `0xcf30826455e3efd4804cbae0b02545c5d63651d3efce93b4c3ff72f695a24974`
- `2026-06-25T01:12:02+00:00` — **BUY 65.21739 @ 0.4599999939** — Will the highest temperature in Milan be 34°C on June 25? / Yes — tx `0xd15ca66b5762c6b8b249ed20ba3dd3ef1c25d3449f78d039c76637eaa483f706`
- `2026-06-29T01:55:11+00:00` — **BUY 102.116 @ 0.2937835403** — Will the highest temperature in Milan be 35°C on June 30? / Yes — tx `0xb8499e6f5331322f90a4d2245d3485085a838f67c8903eb9d1120be52c4f67b6`

## Acquisition note

The API URL is intentionally not persisted with any credentials because this endpoint is public and unauthenticated.
If the response hits 10,000 rows, the next backfill should page by timestamp windows rather than treating this file as complete.
