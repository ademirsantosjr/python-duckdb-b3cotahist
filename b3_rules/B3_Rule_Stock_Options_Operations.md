# Specification: Stock Options on B3

> Technical documentation on the expiration calendar and operation of stock options traded on the Brazilian Stock Exchange B3.

## 1. Overview

Stock options are derivatives that give the holder the right (but not the obligation) to buy or sell an underlying asset at a predetermined price (strike) on a specific expiration date.

## 2. Option Types

| Type | Description |
|------|-------------|
| **Call** | Right to buy the asset at strike |
| **Put** | Right to sell the asset at strike |

### Style

- **European**: Can only be exercised on the expiration date
- **American**: Can be exercised at any time until expiration

## 3. Expiration Calendar

### 3.1 Monthly Stock Options

| Month | Expiration Date | Call Letter | Put Letter |
|-------|-----------------|-------------|-----------|
| January | 3rd Friday | A | M |
| February | 3rd Friday | B | N |
| March | 3rd Friday | C | O |
| April | 3rd Friday | D | P |
| May | 3rd Friday | E | Q |
| June | 3rd Friday | F | R |
| July | 3rd Friday | G | S |
| August | 3rd Friday | H | T |
| September | 3rd Friday | I | U |
| October | 3rd Friday | J | V |
| November | 3rd Friday | K | W |
| December | 3rd Friday | L | X |

**Rule**: If the 3rd Friday is not a trading day, expiration occurs on the previous business day.

### 3.2 Weekly Stock Options

- **Expiration**: Every Friday of the month, except the 3rd Friday
- **Available assets**: 15 selected tickers (ABEV3, B3SA3, BBAS3, BBDC4, BHIA3, BOVA11, BOVV11, GGBR4, HAPV3, ITUB4, MGLU3, NTCO3, PETR4, SUZB3, VALE3)

## 4. Trading Code

### Structure (Monthly)

```
[ASSET][LETTER][STRIKE]
```

| Component | Description | Example |
|-----------|-------------|---------|
| ASSET | Stock ticker | PETR4 |
| LETTER | Month/Type (A-L=Call, M-X=Put) | F |
| STRIKE | Strike price (x100) | 200 = R$ 20.00 |

**Examples**:
- `PETR4F200`: PETR4 Call, June expiration, R$ 20.00 strike
- `VALE3L45`: VALE3 Put, December expiration, R$ 4.50 strike
- `ITUB4E270`: ITUB4 Call, May expiration, R$ 27.00 strike

### Structure (Weekly)

```
[ASSET][STYLE][SERIE][W][WEEK]
```

- **STYLE**: B (Call) or S (Put)
- **SERIE**: 1 to 3
- **W**: Weekly identifier
- **WEEK**: 1 to 5 (week of month)

**Example**: `B3SAB11W1` = B3SA3 Call, 1st Friday of February

## 5. Exercise Rules

### Automatic Exercise

On the expiration date, B3 automatically exercises:

- ITM (in-the-money) options where the holder did not block exercise
- Writer positions not exercised

### American Style Options

Can be exercised at any time until expiration upon holder's request.

### Settlement

- **Premium**: Cash settlement on the next business day after trade
- **Exercise**: Physical delivery of asset at strike (or cash, for indices)

## 6. Calendar 2026 (Reference)

### Stock Options

| Month | Expiration |
|-------|------------|
| January | 16/01 |
| February | 20/02 |
| March | 20/03 |
| April | 17/04 |
| May | 15/05 |
| June | 19/06 |
| July | 17/07 |
| August | 21/08 |
| September | 18/09 |
| October | 16/10 |
| November | 19/11 |
| December | 18/12 |

### Ibovespa Options

| Month | Expiration |
|-------|------------|
| January | 14/01 |
| February | 18/02 |
| March | 18/03 |
| April | 15/04 |
| May | 13/05 |
| June | 17/06 |
| July | 15/07 |
| August | 12/08 |
| September | 16/09 |
| October | 14/10 |
| November | 18/11 |
| December | 16/12 |

### Brazil Index-50 (IBrX-50) Options

| Month | Expiration |
|-------|------------|
| January | - |
| February | 02/02 |
| March | - |
| April | 01/04 |
| May | - |
| June | 01/06 |
| July | - |
| August | 03/08 |
| September | - |
| October | 01/10 |
| November | - |
| December | 01/12 |

## 7. Technical Specifications

| Parameter | Value |
|-----------|-------|
| Contract size | 1 lot (100 shares) |
| Quotation | Premium in BRL per unit |
| Minimum tick | BRL 0.01 |
| Last trading day | Expiration date |
| Trading hours at expiry | Up to 1 hour before close |

## 8. References

- [B3 - Stock Options](http://www.b3.com.br/pt_br/produtos-e-servicos/negociacao/renda-variavel/opcoes-sobre-acoes.htm)
- [B3 - Expiration Calendar](https://www.b3.com.br/pt_br/solucoes/plataformas/puma-trading-system/para-participantes-e-traders/calendario-de-negociacao/vencimentos/calendario-de-vencimentos-de-opcoes-sobre-acoes-e-indices/)
- [B3 - Weekly Stock Options](https://clientes.b3.com.br/w/opcoes-semanais-de-acoes)