-- Table to store the stock quotes data
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

-- Table to track ingested files
CREATE TABLE IF NOT EXISTS ingested_files (
    filename    VARCHAR PRIMARY KEY,
    ingested_at TIMESTAMP DEFAULT now()
)