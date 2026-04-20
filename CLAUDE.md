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

# Open a shell in the container
docker exec -it b3_analytics bash
```

## Architecture

| Layer | Technology | Notes |
|---|---|---|
| Container | Docker / docker-compose | Single service `b3-engine`, container name `b3_analytics` |
| Analysis UI | JupyterLab (port 8888) | Default CMD; no auth token |
| Query engine | DuckDB 1.4.4 | `.duckdb` file lives in `./data/` |
| Data wrangling | Polars 1.40.0 | Used in ingestion and notebooks |
| Future export | psycopg2-binary | Postgres export path, not yet wired |

### Data flow

1. Place B3 COTAHIST `.txt` files in `./data/` (volume-mounted to `/data` inside the container).
2. Run `scripts/ingest.py` to parse and load them into the DuckDB database (also in `./data/`).
3. Open JupyterLab to query DuckDB and analyse the data.

### Key paths

- `./data/` — gitignored (only `.gitkeep` is tracked); holds raw B3 files and the `.duckdb` database.
- `scripts/ingest.py` — entry point for parsing COTAHIST files and writing to DuckDB.
- `requirements.txt` — pinned Python deps; update here and rebuild the image to pick up changes.

## B3 COTAHIST format

COTAHIST files are fixed-width ASCII files published by B3. Each daily or annual file contains one header record (type `00`), detail records (type `01`, one per quote), and a trailer (type `99`). The detail record layout is documented in the official B3 specification ("Layout arquivo COTAHIST").

**Important:** Whenever the context involves the COTAHIST file layout — field names, positions, types, record structure, BDI codes, market types, or security specifications — always read `SeriesHistoricas_Layout.md` before answering or writing code.
