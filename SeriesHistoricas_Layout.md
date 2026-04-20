# FILE LAYOUT — HISTORICAL QUOTES (COTAHIST)

**Chapter I — Historical Quotes File Layout — COTAHIST.YYYY.TXT**

> Public Information | Date: 05/10/2020 | Revision: 02

---

## Change History

| Update Date | Version | Notes |
|---|---|---|
| 05/10/2020 | 2.0 | Updated items in the ESPECI TABLE — VALUES FOR SPECIFICATION. |

---

## 1 Basic Concepts

The `COTAHIST.YYYY.TXT` file contains historical quote information for all market securities traded over the course of one year, sorted by Record Type, Trading Date, BDI Code, Company Name, and Ticker Code. This default ordering does not prevent users from re-sorting according to their own needs and tooling.

The filename identifies the corresponding year. Examples: `COTAHIST.1990.TXT`, `COTAHIST.1991.TXT`, etc.

---

## 2 File Structure

**Filename:** `COTAHIST.YYYY.TXT`

**Record Types:** Each file is composed of three record types:

- Record `00` — Header
- Record `01` — Daily quotes per security
- Record `99` — Trailer

**Record Length:** 245 bytes.

---

## 3 File Layout

### 3.1 Record 00 — Header

| Field Name / Description | Content | Type & Length | Start Pos. | End Pos. |
|---|---|---|---|---|
| RECORD TYPE | Fixed `"00"` | N(02) | 01 | 02 |
| FILE NAME | Fixed `"COTAHIST.YYYY"` | X(13) | 03 | 15 |
| ORIGIN CODE | Fixed `"BOVESPA"` | X(08) | 16 | 23 |
| FILE GENERATION DATE | Format `"YYYYMMDD"` | N(08) | 24 | 31 |
| RESERVED | Filled with spaces | X(214) | 32 | 245 |

---

### 3.2 Record 01 — Historical Quotes per Security

| Field Name / Description | Content | Type & Length | Start Pos. | End Pos. |
|---|---|---|---|---|
| TIPREG — RECORD TYPE | Fixed `"01"` | N(02) | 01 | 02 |
| TRADING DATE | Format `"YYYYMMDD"` | N(08) | 03 | 10 |
| CODBDI — BDI CODE used to classify securities in the Daily Information Bulletin | See BDI Code Table | X(02) | 11 | 12 |
| CODNEG — SECURITY TICKER CODE | | X(12) | 13 | 24 |
| TPMERC — MARKET TYPE — Code of the market in which the security is registered | See Market Type Table | N(03) | 25 | 27 |
| NOMRES — ABBREVIATED COMPANY NAME | | X(12) | 28 | 39 |
| ESPECI — SECURITY SPECIFICATION | See Specification Table | X(10) | 40 | 49 |
| PRAZOT — TERM MARKET DAYS TO EXPIRY | | X(03) | 50 | 52 |
| MODREF — REFERENCE CURRENCY — Currency used on the trading date | | X(04) | 53 | 56 |
| PREABE — OPENING PRICE of the security on the trading session | | (11)V99 | 57 | 69 |
| PREMAX — MAXIMUM PRICE of the security on the trading session | | (11)V99 | 70 | 82 |
| PREMIN — MINIMUM PRICE of the security on the trading session | | (11)V99 | 83 | 95 |
| PREMED — AVERAGE PRICE of the security on the trading session | | (11)V99 | 96 | 108 |
| PREULT — LAST TRADE PRICE of the security on the trading session | | (11)V99 | 109 | 121 |
| PREOFC — BEST BID PRICE for the security | | (11)V99 | 122 | 134 |
| PREOFV — BEST ASK PRICE for the security | | (11)V99 | 135 | 147 |
| TOTNEG — TOTAL NUMBER OF TRADES executed for the security on the trading session | | N(05) | 148 | 152 |
| QUATOT — TOTAL QUANTITY of securities traded | | N(18) | 153 | 170 |
| VOLTOT — TOTAL TRADING VOLUME of securities | | (16)V99 | 171 | 188 |
| PREEXE — EXERCISE PRICE for options markets, or contract value for secondary forward markets | | (11)V99 | 189 | 201 |
| INDOPC — PRICE CORRECTION INDICATOR for exercise prices or contract values in options or secondary forward markets | See Correction Table | N(01) | 202 | 202 |
| DATVEN — EXPIRY DATE for options or secondary forward markets | Format `"YYYYMMDD"` | N(08) | 203 | 210 |
| FATCOT — PRICE QUOTATION FACTOR | `1` = unit quote; `1000` = quote per lot of 1,000 shares | N(07) | 211 | 217 |
| PTOEXE — EXERCISE PRICE IN POINTS for dollar-referenced options, or contract value in points for secondary forwards. For dollar-referenced contracts, each point equals 1/100 of the previous day's closing interbank commercial dollar rate (1 point = 1/100 US$) | | (07)V06 | 218 | 230 |
| CODISI — ISIN CODE or internal security code (ISIN system used from 15/05/1995 onward) | | X(12) | 231 | 242 |
| DISMES — DISTRIBUTION NUMBER — Sequence number of the security corresponding to the current rights status | | 9(03) | 243 | 245 |

---

### 3.3 Record 99 — Trailer

| Field Name / Description | Content | Type & Length | Start Pos. | End Pos. |
|---|---|---|---|---|
| RECORD TYPE | Fixed `"99"` | N(02) | 01 | 02 |
| FILE NAME | Fixed `"COTAHIST.YYYY"` | X(13) | 03 | 15 |
| ORIGIN CODE | Fixed `"BOVESPA"` | X(08) | 16 | 23 |
| FILE GENERATION DATE | Format `"YYYYMMDD"` | N(08) | 24 | 31 |
| TOTAL RECORDS | Includes Header and Trailer records | N(11) | 32 | 42 |
| RESERVED | Filled with spaces | X(203) | 43 | 245 |

---

## 4 Reference Tables

### BDI Code Table — Values for CODBDI

| Code | Description |
|---|---|
| 02 | STANDARD LOT |
| 05 | SANCTIONED UNDER BMFBOVESPA REGULATIONS |
| 06 | BANKRUPTCY PROCEEDINGS |
| 07 | EXTRAJUDICIAL RECOVERY |
| 08 | JUDICIAL RECOVERY |
| 09 | RAET — SPECIAL TEMPORARY ADMINISTRATION REGIME |
| 10 | RIGHTS AND RECEIPTS |
| 11 | INTERVENTION |
| 12 | REAL ESTATE INVESTMENT FUNDS |
| 14 | INVESTMENT CERTIFICATES / PUBLIC DEBT SECURITIES |
| 18 | OBLIGATIONS |
| 22 | BONDS (PRIVATE) |
| 26 | POLICIES / BONDS / PUBLIC SECURITIES |
| 32 | EXERCISE OF INDEX CALL OPTIONS |
| 33 | EXERCISE OF INDEX PUT OPTIONS |
| 38 | EXERCISE OF CALL OPTIONS |
| 42 | EXERCISE OF PUT OPTIONS |
| 46 | AUCTION OF UNLISTED SECURITIES |
| 48 | PRIVATIZATION AUCTION |
| 49 | ESPIRITO SANTO ECONOMIC RECOVERY FUND AUCTION |
| 50 | AUCTION |
| 51 | FINOR AUCTION |
| 52 | FINAM AUCTION |
| 53 | FISET AUCTION |
| 54 | AUCTION OF SHARES IN ARREARS |
| 56 | SALES BY COURT ORDER |
| 58 | OTHER |
| 60 | SHARE SWAP |
| 61 | META |
| 62 | FORWARD MARKET |
| 66 | DEBENTURES WITH MATURITY UP TO 3 YEARS |
| 68 | DEBENTURES WITH MATURITY GREATER THAN 3 YEARS |
| 70 | FUTURES WITH GAIN RETENTION |
| 71 | FUTURES MARKET |
| 74 | INDEX CALL OPTIONS |
| 75 | INDEX PUT OPTIONS |
| 78 | CALL OPTIONS |
| 82 | PUT OPTIONS |
| 83 | BOVESPAFIX |
| 84 | SOMA FIX |
| 90 | REGISTERED CASH FORWARD |
| 96 | ODD-LOT MARKET |
| 99 | GRAND TOTAL |

---

### Specification Table — Values for ESPECI

| Code | Description |
|---|---|
| BDR | BDR (Brazilian Depositary Receipt) |
| BNS | SUBSCRIPTION BONUS IN MISCELLANEOUS SHARES |
| BNS B/A | SUBSCRIPTION BONUS IN PREFERRED SHARES |
| BNS ORD | SUBSCRIPTION BONUS IN ORDINARY SHARES |
| BNS P/A | SUBSCRIPTION BONUS IN PREFERRED SHARES |
| BNS P/B | SUBSCRIPTION BONUS IN PREFERRED SHARES |
| BNS P/C | SUBSCRIPTION BONUS IN PREFERRED SHARES |
| BNS P/D | SUBSCRIPTION BONUS IN PREFERRED SHARES |
| BNS P/E | SUBSCRIPTION BONUS IN PREFERRED SHARES |
| BNS P/F | SUBSCRIPTION BONUS IN PREFERRED SHARES |
| BNS P/G | SUBSCRIPTION BONUS IN PREFERRED SHARES |
| BNS P/H | SUBSCRIPTION BONUS IN PREFERRED SHARES |
| BNS PRE | SUBSCRIPTION BONUS IN PREFERRED SHARES |
| CDA | DEPOSIT CERTIFICATE OF ORDINARY SHARES |
| CI | INVESTMENT FUND |
| CI ATZ | Investment Fund — Adjusted |
| CI EA | Investment Fund — Ex-Adjustment |
| CI EBA | Investment Fund — Ex-Bonus and Ex-Adjustment |
| CI ED | Investment Fund — Ex-Dividend |
| CI ER | Investment Fund — Ex-Income |
| CI ERA | Investment Fund — Ex-Income and Ex-Adjustment |
| CI ERB | Investment Fund — Ex-Income and Ex-Bonus |
| CI ERS | Investment Fund — Ex-Income and Ex-Subscription |
| CI ES | Investment Fund — Ex-Subscription |
| CPA | CERTIFICATE OF ADDITIONAL CONSTRUCTION POTENTIAL |
| DIR | SUBSCRIPTION RIGHTS — MISCELLANEOUS (BONUS) |
| DIR DEB | Debenture Right |
| DIR ORD | SUBSCRIPTION RIGHTS IN ORDINARY SHARES |
| DIR P/A | SUBSCRIPTION RIGHTS IN PREFERRED SHARES |
| DIR P/B | SUBSCRIPTION RIGHTS IN PREFERRED SHARES |
| DIR P/C | SUBSCRIPTION RIGHTS IN PREFERRED SHARES |
| DIR P/D | SUBSCRIPTION RIGHTS IN PREFERRED SHARES |
| DIR P/E | SUBSCRIPTION RIGHTS IN PREFERRED SHARES |
| DIR P/F | SUBSCRIPTION RIGHTS IN PREFERRED SHARES |
| DIR P/G | SUBSCRIPTION RIGHTS IN PREFERRED SHARES |
| DIR P/H | SUBSCRIPTION RIGHTS IN PREFERRED SHARES |
| DIR PR | SUBSCRIPTION RIGHTS IN REDEEMABLE SHARES |
| DIR PRA | SUBSCRIPTION RIGHTS IN REDEEMABLE SHARES |
| DIR PRB | SUBSCRIPTION RIGHTS IN REDEEMABLE SHARES |
| DIR PRC | SUBSCRIPTION RIGHTS IN REDEEMABLE SHARES |
| DIR PRE | SUBSCRIPTION RIGHTS IN PREFERRED SHARES |
| FIDC | RECEIVABLES INVESTMENT FUND |
| LFT | TREASURY FINANCIAL NOTE |
| M1 REC | MISCELLANEOUS SUBSCRIPTION RECEIPT |
| ON | ORDINARY REGISTERED SHARES |
| ON ATZ | Ordinary Shares — Adjusted |
| ON EB | Ordinary Shares — Ex-Bonus |
| ON ED | Ordinary Shares — Ex-Dividend |
| ON EDB | Ordinary Shares — Ex-Dividend and Ex-Bonus |
| ON EDJ | Ordinary Shares — Ex-Dividend and Ex-Interest |
| ON EDR | Ordinary Shares — Ex-Dividend and Ex-Income |
| ON EG | Ordinary Shares — Ex-Reverse Split |
| ON EJ | Ordinary Shares — Ex-Interest |
| ON EJB | Ordinary Shares — Ex-Interest and Ex-Bonus |
| ON EJS | Ordinary Shares — Ex-Interest and Ex-Subscription |
| ON ER | Ordinary Shares — Ex-Income |
| ON ERJ | Ordinary Shares — Ex-Income and Ex-Interest |
| ON ES | Ordinary Shares — Ex-Subscription |
| ON P | ORDINARY REGISTERED SHARES WITH RIGHTS |
| ON REC | SUBSCRIPTION RECEIPT IN ORDINARY SHARES |
| OR | REDEEMABLE ORDINARY REGISTERED SHARES |
| OR P | REDEEMABLE ORDINARY REGISTERED SHARES |
| PCD | CONSOLIDATED DEBT POSITION |
| PN | PREFERRED REGISTERED SHARES |
| PN EB | Preferred Shares — Ex-Bonus |
| PN ED | Preferred Shares — Ex-Dividend |
| PN EDB | Preferred Shares — Ex-Dividend and Ex-Bonus |
| PN EDJ | Preferred Shares — Ex-Dividend and Ex-Interest |
| PN EDR | Preferred Shares — Ex-Dividend and Ex-Income |
| PN EJ | Preferred Shares — Ex-Interest |
| PN EJB | Preferred Shares — Ex-Interest and Ex-Bonus |
| PN EJS | Preferred Shares — Ex-Interest and Ex-Subscription |
| PN ES | Preferred Shares — Ex-Subscription |
| PN P | PREFERRED REGISTERED SHARES WITH RIGHTS |
| PN REC | SUBSCRIPTION RECEIPT IN PREFERRED SHARES |
| PNA | CLASS A PREFERRED REGISTERED SHARES |
| PNA EB | Class A Preferred Shares — Ex-Bonus |
| PNA EDR | Class A Preferred Shares — Ex-Dividend and Ex-Income |
| PNA EJ | Class A Preferred Shares — Ex-Interest |
| PNA ES | Class A Preferred Shares — Ex-Subscription |
| PNA P | CLASS A PREFERRED REGISTERED SHARES WITH RIGHTS |
| PNA REC | SUBSCRIPTION RECEIPT IN PREFERRED SHARES |
| PNB | CLASS B PREFERRED REGISTERED SHARES |
| PNB EB | Class B Preferred Shares — Ex-Bonus |
| PNB ED | Class B Preferred Shares — Ex-Dividend |
| PNB EDR | Class B Preferred Shares — Ex-Dividend and Ex-Income |
| PNB EJ | Class B Preferred Shares — Ex-Interest |
| PNB P | CLASS B PREFERRED REGISTERED SHARES WITH RIGHTS |
| PNB REC | SUBSCRIPTION RECEIPT IN PREFERRED SHARES |
| PNC | CLASS C PREFERRED REGISTERED SHARES |
| PNC ED | Class C Preferred Shares — Ex-Dividend |
| PNC P | CLASS C PREFERRED REGISTERED SHARES WITH RIGHTS |
| PNC REC | SUBSCRIPTION RECEIPT IN PREFERRED SHARES |
| PND | CLASS D PREFERRED REGISTERED SHARES |
| PND ED | Class D Preferred Shares — Ex-Dividend |
| PND P | CLASS D PREFERRED REGISTERED SHARES WITH RIGHTS |
| PND REC | SUBSCRIPTION RECEIPT IN PREFERRED SHARES |
| PNE | CLASS E PREFERRED REGISTERED SHARES |
| PNE ED | Class E Preferred Shares — Ex-Dividend |
| PNE P | CLASS E PREFERRED REGISTERED SHARES WITH RIGHTS |
| PNE REC | SUBSCRIPTION RECEIPT IN PREFERRED SHARES |

---

### Contract Correction Table — Values for INDOPC

| Code | Description |
|---|---|
| 1 | US$ — Correction by the Dollar Rate |
| 2 | TJLP — Correction by TJLP (Long-Term Interest Rate) |
| 8 | IGPM — Correction by IGP-M — Protected Options |
| 9 | URV — Correction by URV (Real Value Unit) |

---

### Market Type Table — Values for TPMERC

| Code | Description |
|---|---|
| 010 | SPOT (CASH) |
| 012 | EXERCISE OF CALL OPTIONS |
| 013 | EXERCISE OF PUT OPTIONS |
| 017 | AUCTION |
| 020 | ODD-LOT |
| 030 | FORWARD |
| 050 | FUTURES WITH GAIN RETENTION |
| 060 | FUTURES WITH CONTINUOUS SETTLEMENT |
| 070 | CALL OPTIONS |
| 080 | PUT OPTIONS |
