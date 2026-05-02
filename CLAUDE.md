# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This project ingests B3 (Brazilian stock exchange) COTAHIST flat-file quotes into DuckDB and exposes a JupyterLab interface for analysis. The full environment runs inside Docker.

## Commands

```bash
# Build and start JupyterLab (http://localhost:8888, no token)
docker-compose up -d --build

# Run the ingest script inside the running container
docker exec -it b3_analytics python scripts/ingest.py

# Override data/db paths via env vars (useful outside Docker)
B3_DATA_DIR=/my/data B3_DB_PATH=/my/data/b3.duckdb python scripts/ingest.py

# Open a shell in the container
docker exec -it b3_analytics bash
```

## Architecture

| Layer | Technology | Notes |
|---|---|---|
| Container | Docker / docker-compose | Single service `b3-engine`, container name `b3_analytics` |
| Analysis UI | JupyterLab (port 8888) | Default CMD; no auth token |
| Alternative UI | Google Colab | Drive-backed; uses `notebooks/colab_*.ipynb` |
| Query engine | DuckDB 1.4.4 | `.duckdb` file lives in `./data/` |
| Data wrangling | Polars 1.40.0 | Used in ingestion and notebooks |
| Future export | psycopg2-binary | Postgres export path, not yet wired |

### Data flow

1. Place B3 COTAHIST `.txt` files in `./data/` (volume-mounted to `/data` inside the container).
2. Run `scripts/ingest.py` to parse and load them into the DuckDB database (also in `./data/`).
3. Open JupyterLab to query DuckDB and analyse the data.

### Key paths

- `./data/` — gitignored (only `.gitkeep` is tracked); holds raw B3 files and the `.duckdb` database.
- `scripts/ingest.py` — entry point for parsing COTAHIST files and writing to DuckDB. `run_ingest(data_dir, db_path)` is the callable API used by Colab notebooks; `main()` wraps it reading `B3_DATA_DIR` / `B3_DB_PATH` env vars.
- `notebooks/` — Colab-compatible notebooks: `colab_ingest.ipynb` (runs ingest) and `colab_analysis.ipynb` (queries and charts).
- `resources/db_schema.sql` — canonical DDL for the `cotacoes` and `ingested_files` tables; reference when writing schema migrations.
- `b3_rules/` — B3 business rules documentation (e.g. stock options operations).
- `requirements.txt` — pinned Python deps for Docker; update here and rebuild the image to pick up changes.
- `requirements_colab.txt` — minimal extra deps for Google Colab (DuckDB + Polars only).

## B3 COTAHIST format

COTAHIST files are fixed-width ASCII files published by B3. Each daily or annual file contains one header record (type `00`), detail records (type `01`, one per quote), and a trailer (type `99`). The detail record layout is documented in the official B3 specification ("Layout arquivo COTAHIST").

**Important:** Whenever the context involves the COTAHIST file layout — field names, positions, types, record structure, BDI codes, market types, or security specifications — always read `SeriesHistoricas_Layout.md` before answering or writing code.

### Linking options to their underlying stock

B3 option tickers use a **4-character company root** in `codneg` (e.g. `PETR`, not `PETR4`), so both PETR3 (ON) and PETR4 (PN) options share the same root. A `codneg LIKE 'PETR4%'` filter is unreliable. The correct approach requires **two** filters:

1. `codneg LIKE '{TICKER[:4]}%'` — match on the 4-char root.
2. `SUBSTR(especi, 1, 2) = SUBSTR(underlying.especi, 1, 2)` — match the share class from the underlying stock's own `especi` field. Options inherit the `especi` of their underlying: ordinary shares (PETR3) → `ON…`, preferred shares (PETR4) → `PN…`.

Always fetch the underlying's `especi` from `cotacoes` (with `codbdi = '02'`) and apply this two-part filter whenever querying options for a specific stock.

## Google Colab

An alternative to the Docker/JupyterLab workflow. The database lives in Google Drive (`MyDrive/b3_data/`); notebooks copy it to `/content/` at session start for performance and sync it back before closing. See the **Google Colab Quick-Start** section in `README.md` for the full setup, Drive folder layout, and the file-lock warning.
