# B3 COTAHIST Analytics Engine

Ingests historical B3 (Brazilian Stock Exchange) quote files into DuckDB and exposes a JupyterLab interface for analysis. The entire environment runs inside Docker.

---

## Quick Start

```bash
# 1. Build the image and start the container
docker-compose up -d --build

# 2. Drop one or more COTAHIST files into ./data/
#    Accepted formats: COTAHIST.YYYY.TXT  or  COTAHIST.YYYY.ZIP

# 3. Run the ingest script
docker exec -it b3_analytics python scripts/ingest.py

# 4. Open JupyterLab
open http://localhost:8888
```

---

## Ingest Service (`scripts/ingest.py`)

### What it does

Reads B3 COTAHIST fixed-width text files, parses every daily quote record (type `01`), and appends the results to a persistent DuckDB database at `/data/b3_data.duckdb`.

### Input files

Place files in the `./data/` directory (volume-mounted to `/data` inside the container). The script accepts:

| Format | Example |
|---|---|
| Plain text | `COTAHIST.2024.TXT` |
| Zip archive | `COTAHIST.2024.ZIP` |

ZIP files are extracted entirely in memory — no temporary files are written to disk.

The script scans for any file whose name starts with `COTAHIST` and has a `.TXT` or `.ZIP` extension. It processes all matches found in a single run.

### Deduplication

An `ingested_files` table in DuckDB tracks every file that has been successfully loaded. Re-running the script is always safe: files already present in that table are skipped immediately without re-parsing.

### Parsing pipeline

The source files are fixed-width ASCII encoded in `latin-1`, with each record exactly 245 bytes. The script:

1. Decodes the raw bytes as `latin-1`.
2. Loads all lines into a Polars Series.
3. Filters to record type `01` (quote records) — header (`00`) and trailer (`99`) lines are discarded.
4. Extracts every field via positional string slicing (no CSV parsing, no regex).
5. Applies type conversions (see table below).
6. Inserts the resulting Polars DataFrame into DuckDB via its native Arrow interface.

All transformations run inside Polars' vectorised engine — there are no Python-level loops over rows.

### Field mapping

Full field reference: [`SeriesHistoricas_Layout.md`](SeriesHistoricas_Layout.md)

| Field | Column | Positions | Type | Notes |
|---|---|---|---|---|
| Record type | — | 01–02 | — | Filter only; must equal `"01"` |
| Trading date | `datpre` | 03–10 | `DATE` | Format `YYYYMMDD` |
| BDI code | `codbdi` | 11–12 | `VARCHAR` | See BDI code table |
| Ticker | `codneg` | 13–24 | `VARCHAR` | Whitespace stripped |
| Market type | `tpmerc` | 25–27 | `VARCHAR` | See market type table |
| Company name | `nomres` | 28–39 | `VARCHAR` | Abbreviated |
| Specification | `especi` | 40–49 | `VARCHAR` | See specification table |
| Term days | `prazot` | 50–52 | `VARCHAR` | Forward market only |
| Currency | `modref` | 53–56 | `VARCHAR` | |
| Open price | `preabe` | 57–69 | `DOUBLE` | `(11)V99` ÷ 100 |
| High price | `premax` | 70–82 | `DOUBLE` | `(11)V99` ÷ 100 |
| Low price | `premin` | 83–95 | `DOUBLE` | `(11)V99` ÷ 100 |
| Average price | `premed` | 96–108 | `DOUBLE` | `(11)V99` ÷ 100 |
| Close price | `preult` | 109–121 | `DOUBLE` | `(11)V99` ÷ 100 |
| Best bid | `preofc` | 122–134 | `DOUBLE` | `(11)V99` ÷ 100 |
| Best ask | `preofv` | 135–147 | `DOUBLE` | `(11)V99` ÷ 100 |
| Trade count | `totneg` | 148–152 | `INTEGER` | |
| Total quantity | `quatot` | 153–170 | `BIGINT` | |
| Total volume | `voltot` | 171–188 | `DOUBLE` | `(16)V99` ÷ 100 |
| Exercise price | `preexe` | 189–201 | `DOUBLE` | `(11)V99` ÷ 100; options/forwards only |
| Price correction | `indopc` | 202–202 | `VARCHAR` | See correction table |
| Expiry date | `datven` | 203–210 | `DATE` | Options/forwards only; null otherwise |
| Quote factor | `fatcot` | 211–217 | `INTEGER` | `1` = unit; `1000` = per 1,000 shares |
| Exercise points | `ptoexe` | 218–230 | `DOUBLE` | `(07)V06` ÷ 1,000,000 |
| ISIN code | `codisi` | 231–242 | `VARCHAR` | From 15/05/1995 |
| Distribution no. | `dismes` | 243–245 | `INTEGER` | |
| Source file | `source_file` | — | `VARCHAR` | Injected by the script |

### Price format

Prices are stored as packed integers in the source file. The notation `(11)V99` means 11 integer digits followed by 2 implied decimal digits, giving 13 total characters. To convert to decimal Reais the script casts the 13-character string to `Float64` and divides by `100`. The same logic applies to all price fields. `VOLTOT` uses `(16)V99` (18 chars ÷ 100) and `PTOEXE` uses `(07)V06` (13 chars ÷ 1,000,000).

### Database schema

Two tables are created automatically on first run:

**`cotacoes`** — one row per security per trading day.

**`ingested_files`** — one row per processed file.

```sql
SELECT filename, ingested_at FROM ingested_files ORDER BY ingested_at;
```

---

## Analysis

Open JupyterLab at `http://localhost:8888` (no token required). Connect to DuckDB from a notebook:

```python
import duckdb

con = duckdb.connect("/data/b3_data.duckdb")

# Resources Tip
con.execute("SET threads TO 2;")
con.execute("SET memory_limit = '2GB';")

# Example
con.sql("""
    SELECT datpre, codbdi, codneg, especi, preult, totneg, quatot, voltot, preexe, datven
    FROM cotacoes
    WHERE codneg = 'PETR4' AND YEAR(datpre) = 2025
    ORDER BY datpre
""").df()
```

---

## Project Structure

```
.
├── data/                  # Gitignored — source .TXT/.ZIP files and b3_data.duckdb
├── scripts/
│   └── ingest.py          # ETL entry point
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── SeriesHistoricas_Layout.md   # B3 field layout reference (English)
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Container | Docker / docker-compose |
| Analysis UI | JupyterLab (port 8888) |
| Query engine | DuckDB 1.4.4 |
| Data processing | Polars 1.40.0 |
| Source data | B3 COTAHIST fixed-width files |
