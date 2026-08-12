# Milan multi-model rate-limit retry

| Case | Run | Daily max | Target-day hours |
|---|---|---:|---:|
| june25 | DWD ICON-EU 12Z | 33.20°C | 24 |
| june25 | DWD ICON-EU 18Z | 35.20°C | 24 |
| june25 | DWD ICON-EU 21Z | 35.40°C | 24 |
| june25 | ItaliaMeteo ICON-2I 12Z | 35.30°C | 24 |
| june30 | ARPEGE Europe 18Z | 32.20°C | 24 |

A run is usable for a civil-day maximum only if it covers the relevant daytime peak. `target_hours` is preserved specifically to detect partial-day short-cycle artifacts.
