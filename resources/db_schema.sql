-- Table to store the stock quotes data
CREATE TABLE IF NOT EXISTS cotacoes (
    datpre      DATE, -- Date of the quote
    codbdi      VARCHAR, -- Classifies securities in the Daily Information Bulletin
    codneg      VARCHAR, -- Security code (ticker)
    tpmerc      VARCHAR, -- Market type
    nomres      VARCHAR, -- Full name of the security
    especi      VARCHAR,
    prazot      VARCHAR,
    modref      VARCHAR,
    preabe      DOUBLE, -- Opening price
    premax      DOUBLE, -- Maximum price
    premin      DOUBLE, -- Minimum price
    premed      DOUBLE, -- Average price
    preult      DOUBLE, -- Last price
    preofc      DOUBLE, -- Best ask price
    preofv      DOUBLE, -- Best bid price
    totneg      INTEGER, -- Total number of trades
    quatot      BIGINT, -- Total quantity of securities traded
    voltot      DOUBLE, -- Total financial volume of trades
    preexe      DOUBLE, -- Exercise price for options
    indopc      VARCHAR, 
    datven      DATE, -- Expiration date for options
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