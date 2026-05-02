# Option Performance Analysis

Compares the historical price performance of a CALL and a PUT against their underlying stock over a chosen date range.

## Parameters

| Parameter | Description |
|---|---|
| `TICKER` | Underlying stock ticker (e.g. `PETR4`) |
| `START_DATE` | Start of the analysis — must be a trading day with ingested data |
| `TARGET_DATE` | End of the analysis — option expiry is selected nearest to this date |

Edit only **Cell 4** to run a new analysis.

## How options are selected

1. The stock's closing price on `START_DATE` becomes the target strike.
2. All monthly options for `TICKER` on `START_DATE` are filtered by share class (`especi`) to distinguish e.g. PETR4 (PN) from PETR3 (ON). Weekly options (tickers ending in W1–W5) are excluded.
3. The expiry date nearest to `TARGET_DATE` that has **both** a CALL and a PUT available is chosen.
4. For that expiry, the CALL and PUT whose strike is closest to the stock price (nearest ATM) are selected.

## Chart

Dual Y-axis Plotly chart:

- **Left axis** — stock price (white line)
- **Right axis** — option prices: CALL (green), PUT (red)
- Dotted vertical lines mark **Start**, **Expiry**, and **Target** dates

## Prerequisites

The DuckDB database must be populated before running. See [`colab_ingest.ipynb`](colab_ingest.ipynb).
