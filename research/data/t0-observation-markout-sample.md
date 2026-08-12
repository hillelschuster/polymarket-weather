# T+0 observation-aligned markout sample

Generated: **2026-08-12T13:56:42.220685+00:00**

Price marks are CLOB historical token prices sampled within ±180 seconds of each requested horizon. They are market marks, not reconstructed historical bid/ask depth.

| Case | Anchor | YES -5m | YES 0m | YES +5m | +15m | +30m | +60m | +120m |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| London Jul12 27C pre-breach | pre_breach_trade | 0.1200 | 0.1950 | 0.1200 | 0.0005 | 0.0010 | 0.0005 | 0.0005 |
| Wellington Jul21 11C pre-breach | pre_breach_trade | 0.2120 | 0.0410 | 0.2390 | 0.1045 | 0.2715 | 0.0005 | 0.0005 |
| NYC Jul20 82-83F first-lock | first_winning_bucket_observation | 0.3300 | 0.4950 | 0.9865 | 0.9975 | 0.9955 | 0.9985 | 0.9995 |
| Chicago Jun29 92-93F first-lock | first_winning_bucket_observation | 0.5250 | 0.5050 | 0.8000 | 0.9200 | 0.7850 | 0.5950 | 0.9690 |
| Chicago Jun20 76-77F late-extrema | late_extrema_candidate | 0.9960 | 0.9960 | 0.9960 | 0.9960 | 0.9960 | 0.9960 | 0.9965 |

## Event details

### London Jul12 27C pre-breach

- market: **Will the highest temperature in London be 27°C on July 12?**
- token labels: `gamma` explicit mapping
- market trades in window: **374**; YES-token trades: **140**
- first YES trade after anchor: `{"outcome": "Yes", "price": 0.2656227502, "side": "BUY", "size": 166.68, "timestamp": 1783862192, "transactionHash": "0xa980bbca4a7df7cc9a6a80efaacf0b277181e963a73ce2625a9dc8618e8a9597"}`

### Wellington Jul21 11C pre-breach

- market: **Will the highest temperature in Wellington be 11°C on July 21?**
- token labels: `gamma` explicit mapping
- market trades in window: **991**; YES-token trades: **537**
- first YES trade after anchor: `{"outcome": "Yes", "price": 0.0590997061, "side": "BUY", "size": 29.780165, "timestamp": 1784598970, "transactionHash": "0xfde6e19660e6a98edd7328dfc68c2e4841e82b93bf7fc346c2827cc6cb5a3213"}`

### NYC Jul20 82-83F first-lock

- market: **Will the highest temperature in New York City be between 82-83°F on July 20?**
- token labels: `gamma` explicit mapping
- market trades in window: **376**; YES-token trades: **222**
- first YES trade after anchor: `{"outcome": "Yes", "price": 0.5967907425, "side": "BUY", "size": 155.55, "timestamp": 1784584267, "transactionHash": "0xe5690d71925969a3f59dfa0aa0aafc5302cf3f5703872fc16f507492f2cb0d34"}`

### Chicago Jun29 92-93F first-lock

- market: **Will the highest temperature in Chicago be between 92-93°F on June 29?**
- token labels: `gamma` explicit mapping
- market trades in window: **253**; YES-token trades: **128**
- first YES trade after anchor: `{"outcome": "Yes", "price": 0.71, "side": "SELL", "size": 5, "timestamp": 1782766364, "transactionHash": "0x03e495588915deec9abf5ebc02d4cebdebd805f491ae00eedeff9f18348e1c14"}`

### Chicago Jun20 76-77F late-extrema

- market: **Will the highest temperature in Chicago be between 76-77°F on June 20?**
- token labels: `gamma` explicit mapping
- market trades in window: **17**; YES-token trades: **12**
- first YES trade after anchor: `{"outcome": "Yes", "price": 0.993, "side": "SELL", "size": 233.17, "timestamp": 1781999593, "transactionHash": "0xae4bde87b148d548264ba116d1ee7f1db6db15441e054b8e9161454e8c7b73a5"}`
