#!/usr/bin/env python3
"""
Ingest B3 COTAHIST fixed-width files into DuckDB.

Supports .TXT and .ZIP (extracts in memory). Skips files already present
in the `ingested_files` tracking table. Appends to /data/b3_data.duckdb.

Field positions follow the official B3 layout spec (1-based, inclusive):
  SeriesHistoricas_Layout.md
"""
import os
import duckdb
import polars as pl
import zipfile
from pathlib import Path


def ensure_schema(con: duckdb.DuckDBPyConnection) -> None:
    con.execute("""
        CREATE TABLE IF NOT EXISTS cotacoes (
            datpre      DATE,
            codbdi      VARCHAR,
            codneg      VARCHAR,
            tpmerc      VARCHAR,
            nomres      VARCHAR,
            especi      VARCHAR,
            prazot      VARCHAR,
            modref      VARCHAR,
            preabe      DOUBLE,
            premax      DOUBLE,
            premin      DOUBLE,
            premed      DOUBLE,
            preult      DOUBLE,
            preofc      DOUBLE,
            preofv      DOUBLE,
            totneg      INTEGER,
            quatot      BIGINT,
            voltot      DOUBLE,
            preexe      DOUBLE,
            indopc      VARCHAR,
            datven      DATE,
            fatcot      INTEGER,
            ptoexe      DOUBLE,
            codisi      VARCHAR,
            dismes      INTEGER,
            source_file VARCHAR
        )
    """)
    con.execute("""
        CREATE TABLE IF NOT EXISTS ingested_files (
            filename    VARCHAR PRIMARY KEY,
            ingested_at TIMESTAMP DEFAULT now()
        )
    """)


def already_ingested(con: duckdb.DuckDBPyConnection, filename: str) -> bool:
    return con.execute(
        "SELECT COUNT(*) FROM ingested_files WHERE filename = ?", [filename]
    ).fetchone()[0] > 0


def read_file_bytes(path: Path) -> tuple[bytes, str]:
    """Return (raw_bytes, canonical_filename). Handles .TXT and .ZIP."""
    if path.suffix.upper() == ".ZIP":
        with zipfile.ZipFile(path) as zf:
            members = [
                n for n in zf.namelist()
                if n.upper().startswith("COTAHIST") and n.upper().endswith(".TXT")
            ]
            if not members:
                raise ValueError(f"No COTAHIST*.TXT found inside {path.name}")
            with zf.open(members[0]) as f:
                return f.read(), members[0]
    return path.read_bytes(), path.name


def parse_type01(raw_bytes: bytes) -> pl.DataFrame:
    """
    Parse record-type-01 lines from a COTAHIST byte string.

    All slice offsets are 0-based. Field widths come from the layout spec:
      - Prices (11)V99  → 13 chars, divide by 100
      - VOLTOT (16)V99  → 18 chars, divide by 100
      - PTOEXE (07)V06  → 13 chars, divide by 1_000_000
    """
    lines = pl.Series("raw", raw_bytes.decode("latin-1").splitlines())
    lines = lines.filter(lines.str.slice(0, 2) == "01")

    if len(lines) == 0:
        return pl.DataFrame()

    df = lines.to_frame("raw")

    def price(offset: int) -> pl.Expr:
        return pl.col("raw").str.slice(offset, 13).cast(pl.Float64) / 100.0

    return (
        df.select([
            pl.col("raw").str.slice(2, 8).alias("datpre"),
            pl.col("raw").str.slice(10, 2).str.strip_chars().alias("codbdi"),
            pl.col("raw").str.slice(12, 12).str.strip_chars().alias("codneg"),
            pl.col("raw").str.slice(24, 3).str.strip_chars().alias("tpmerc"),
            pl.col("raw").str.slice(27, 12).str.strip_chars().alias("nomres"),
            pl.col("raw").str.slice(39, 10).str.strip_chars().alias("especi"),
            pl.col("raw").str.slice(49, 3).str.strip_chars().alias("prazot"),
            pl.col("raw").str.slice(52, 4).str.strip_chars().alias("modref"),
            price(56).alias("preabe"),
            price(69).alias("premax"),
            price(82).alias("premin"),
            price(95).alias("premed"),
            price(108).alias("preult"),
            price(121).alias("preofc"),
            price(134).alias("preofv"),
            pl.col("raw").str.slice(147, 5).cast(pl.Int32).alias("totneg"),
            pl.col("raw").str.slice(152, 18).cast(pl.Int64).alias("quatot"),
            (pl.col("raw").str.slice(170, 18).cast(pl.Float64) / 100.0).alias("voltot"),
            price(188).alias("preexe"),
            pl.col("raw").str.slice(201, 1).alias("indopc"),
            pl.col("raw").str.slice(202, 8).alias("_datven_raw"),
            pl.col("raw").str.slice(210, 7).cast(pl.Int32).alias("fatcot"),
            (pl.col("raw").str.slice(217, 13).cast(pl.Float64) / 1_000_000.0).alias("ptoexe"),
            pl.col("raw").str.slice(230, 12).str.strip_chars().alias("codisi"),
            pl.col("raw").str.slice(242, 3).cast(pl.Int32).alias("dismes"),
        ])
        .with_columns([
            pl.col("datpre").str.to_date("%Y%m%d"),
            pl.col("_datven_raw").str.to_date("%Y%m%d", strict=False).alias("datven"),
        ])
        .drop("_datven_raw")
    )


def ingest_file(con: duckdb.DuckDBPyConnection, path: Path) -> None:
    raw_bytes, filename = read_file_bytes(path)

    if already_ingested(con, filename):
        print(f"  skip  {filename} (already ingested)")
        return

    print(f"  parse {filename} ...", end=" ", flush=True)
    df = parse_type01(raw_bytes)

    if df.is_empty():
        print("0 rows")
        con.execute("INSERT INTO ingested_files (filename) VALUES (?)", [filename])
        return

    df = df.with_columns(pl.lit(filename).alias("source_file"))

    con.execute("INSERT INTO cotacoes BY NAME SELECT * FROM df")
    con.execute("INSERT INTO ingested_files (filename) VALUES (?)", [filename])
    print(f"{len(df):,} rows inserted")


def run_ingest(
    data_dir: Path | str = Path("/data"),
    db_path: Path | str | None = None,
) -> None:
    """
    Callable entry point for both Docker (CLI) and Colab (notebook import).

    data_dir  – directory containing COTAHIST TXT/ZIP files.
    db_path   – path to the DuckDB file; defaults to <data_dir>/b3_data.duckdb.
    """
    data_dir = Path(data_dir)
    if db_path is None:
        db_path = data_dir / "b3_data.duckdb"
    db_path = Path(db_path)

    candidates = sorted(
        p for p in data_dir.iterdir()
        if p.stem.upper().startswith("COTAHIST")
        and p.suffix.upper() in {".TXT", ".ZIP"}
    )

    if not candidates:
        print(f"No COTAHIST files found in {data_dir}")
        return

    with duckdb.connect(str(db_path)) as con:
        ensure_schema(con)
        for path in candidates:
            print(f"→ {path.name}")
            ingest_file(con, path)

    print("Done.")


def main() -> None:
    data_dir = Path(os.environ.get("B3_DATA_DIR", "/data"))
    db_path  = Path(os.environ.get("B3_DB_PATH", str(data_dir / "b3_data.duckdb")))
    run_ingest(data_dir, db_path)


if __name__ == "__main__":
    main()
