# T+0 observation execution economics

Generated: **2026-08-12T13:59:55.499443+00:00**

Actual Data API trade prints on the economically favorable token after the observation signal; terminal reference is CLOB historical price at +10m. Fee-adjusted markout subtracts unit taker fee r*p*(1-p) using each market CLOB fd.r. It is opportunity-volume evidence, not a claim one bot could capture every print.

| Case | Trade side after signal | +10m ref | Fee r | 0-10m printed qty | Gross positive markout $ | Fee-adjusted positive markout $ |
|---|---|---:|---:|---:|---:|---:|
| London Jul12 27C pre-breach | NO | 0.9995 | 0.0500 | 6693.22 | 60.72 | 57.73 |
| Wellington Jul21 11C pre-breach | NO | 0.999 | 0.0500 | 11036.51 | 12.43 | 11.65 |
| NYC Jul20 82-83F first-lock | YES | 0.9935 | 0.0500 | 2392.93 | 283.97 | 273.71 |
| Chicago Jun29 92-93F first-lock | YES | 0.725 | 0.0500 | 158.95 | 0.28 | 0.12 |
| Chicago Jun20 76-77F late-extrema | YES | 0.996 | 0.0500 | 466.34 | 1.40 | 1.24 |

## Repricing by elapsed time

### London Jul12 27C pre-breach

- signal: `2026-07-12T13:20:00+00:00`; favorable side: **NO**; +10m reference: **0.9995**
- first favorable-token trade after signal: `{"price": 0.907234134, "side": "BUY", "size": 211.940877, "timestamp": 1783862417, "transactionHash": "0xa4eb0554c87ac1548bea1dcef91656e4b53cbcbc265f88273cd7b68b76354cee"}`

| Seconds | Trades | Qty | VWAP | Fee-adjusted positive markout $ |
|---:|---:|---:|---:|---:|
| 0-30 | 1 | 211.94 | 0.9072 | 18.66 |
| 30-60 | 3 | 244.77 | 0.9111 | 20.64 |
| 60-120 | 7 | 828.36 | 0.9794 | 15.79 |
| 120-300 | 19 | 346.55 | 0.9984 | 0.36 |
| 300-600 | 20 | 5061.60 | 0.9990 | 2.28 |

### Wellington Jul21 11C pre-breach

- signal: `2026-07-21T02:30:00+00:00`; favorable side: **NO**; +10m reference: **0.999**
- first favorable-token trade after signal: `{"price": 0.99, "side": "BUY", "size": 11.6969, "timestamp": 1784601085, "transactionHash": "0x7be342bf56d6dbf91a720e4ba753ed8c55db353cfbe1fc2845b1af46479198c6"}`

| Seconds | Trades | Qty | VWAP | Fee-adjusted positive markout $ |
|---:|---:|---:|---:|---:|
| 0-30 | 0 | 0.00 | NA | 0.00 |
| 30-60 | 0 | 0.00 | NA | 0.00 |
| 60-120 | 2 | 58.91 | 0.9900 | 0.50 |
| 120-300 | 59 | 3722.44 | 0.9961 | 10.12 |
| 300-600 | 54 | 7255.17 | 0.9988 | 1.04 |

### NYC Jul20 82-83F first-lock

- signal: `2026-07-20T21:51:00+00:00`; favorable side: **YES**; +10m reference: **0.9935**
- first favorable-token trade after signal: `{"price": 0.5967907425, "side": "BUY", "size": 155.55, "timestamp": 1784584267, "transactionHash": "0xe5690d71925969a3f59dfa0aa0aafc5302cf3f5703872fc16f507492f2cb0d34"}`

| Seconds | Trades | Qty | VWAP | Fee-adjusted positive markout $ |
|---:|---:|---:|---:|---:|
| 0-30 | 17 | 478.67 | 0.6044 | 180.52 |
| 30-60 | 17 | 298.55 | 0.7570 | 67.87 |
| 60-120 | 17 | 607.30 | 0.9635 | 17.17 |
| 120-300 | 13 | 298.50 | 0.9793 | 3.93 |
| 300-600 | 28 | 709.91 | 0.9871 | 4.22 |

### Chicago Jun29 92-93F first-lock

- signal: `2026-06-29T20:51:00+00:00`; favorable side: **YES**; +10m reference: **0.725**
- first favorable-token trade after signal: `{"price": 0.71, "side": "SELL", "size": 5, "timestamp": 1782766364, "transactionHash": "0x03e495588915deec9abf5ebc02d4cebdebd805f491ae00eedeff9f18348e1c14"}`

| Seconds | Trades | Qty | VWAP | Fee-adjusted positive markout $ |
|---:|---:|---:|---:|---:|
| 0-30 | 0 | 0.00 | NA | 0.00 |
| 30-60 | 0 | 0.00 | NA | 0.00 |
| 60-120 | 5 | 42.41 | 0.7521 | 0.05 |
| 120-300 | 4 | 59.03 | 0.8022 | 0.00 |
| 300-600 | 5 | 57.51 | 0.8191 | 0.07 |

### Chicago Jun20 76-77F late-extrema

- signal: `2026-06-20T23:51:00+00:00`; favorable side: **YES**; +10m reference: **0.996**
- first favorable-token trade after signal: `{"price": 0.993, "side": "SELL", "size": 233.17, "timestamp": 1781999593, "transactionHash": "0xae4bde87b148d548264ba116d1ee7f1db6db15441e054b8e9161454e8c7b73a5"}`

| Seconds | Trades | Qty | VWAP | Fee-adjusted positive markout $ |
|---:|---:|---:|---:|---:|
| 0-30 | 0 | 0.00 | NA | 0.00 |
| 30-60 | 0 | 0.00 | NA | 0.00 |
| 60-120 | 0 | 0.00 | NA | 0.00 |
| 120-300 | 2 | 466.34 | 0.9930 | 1.24 |
| 300-600 | 0 | 0.00 | NA | 0.00 |
