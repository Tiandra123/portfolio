# NFL Sports Betting ETL Pipeline 🏈

**Python · PostgreSQL · ETL · SQL · OLS Regression**

*Graduate Project — Utah State University, M.S. MIS · Fall 2025*
*Built in collaboration with [Brock Jessop](https://github.com/BrockJessop)*

---

We designed and built a full ETL pipeline to move NFL game and betting data from two source systems into a clean, normalized PostgreSQL database — then used it to answer real analytical questions with SQL and machine learning. This was a semester-long project covering everything from schema design to regression modeling, and it's the project where a lot of things we learned in class clicked into place together.

The pipeline ingests NFL schedule data (2015–2023) from CSV files and 200,000+ betting records from a SQL Server source, transforms and validates the data across 6 tables, and loads it into PostgreSQL with full referential integrity. On top of the database, we wrote 7 analytical SQL queries and built an OLS regression model to predict customer net value from demographic features.

**What we built:**
- Full ETL pipeline: extract from CSV + SQL Server → transform + validate → load into PostgreSQL
- Normalized schema across 6 tables: `betting_log`, `customer`, `schedule`, `stadium`, `teams`, `exception`
- Exception table pattern to capture and log problematic rows without halting ingestion
- 7 analytical SQL queries covering commission analysis, win rates, spread performance, and house profitability by week
- OLS regression model predicting customer net value from age, income, household size, customer type, and mode color

---

## Database Schema

```
Customer ──────────────── Betting_Log ──────────────── Schedule
  customer_id (PK)           bet_id (PK)                 game_id (PK)
  first_name                 customer_id (FK)             game_code
  last_name                  game_code (FK)               game_date
  age                        bet_on                       schedule_season
  customer_type              bet_amount                   home_team_id (FK) ──── Teams
  customer_since             result                       away_team_id (FK)        team_pk (PK)
  customer_income            commission                   team_favorite_id         team_name
  household_size                                          spread_favorite          team_conference
  mode_color                                              over_under_line          team_division
                                                          stadium_id (FK) ──── Stadium
                                                          weather_temp              stadium_id (PK)
                                                          winner_line               stadium_name
                                                          winner_ou                 stadium_location
                                                                                    stadium_type
Exception                                                                           latitude / longitude
  exception_id (PK)
  row_data
  filename
```

Full schema documented in `docs/data_dictionary.md` and `docs/erd.pdf`.

---

## ETL Pipeline

### Extract
- NFL schedule + game data from **CSV files** (2015–2023 seasons, filtered on ingest)
- Customer and betting records from **SQL Server** via `pymssql`

### Transform
- Split `customer_name` → `first_name` / `last_name`
- Null handling across all tables using pandas `.where(pd.notnull(df), None)`
- Type coercion for `stadium_open`, `stadium_close`, `stadium_capacity`, coordinates
- Weather station code validation: 4-digit codes zero-padded, non-numeric codes routed to exception table
- Special character handling (Mexico City stadium address)
- Batch insert pattern with exception logging for failed rows

### Load
- PostgreSQL via `psycopg2` with row-by-row and batch insert strategies
- `exception` table captures malformed rows with source filename for auditability
- Referential integrity enforced via foreign key constraints

---

## Analytical Queries

| # | Question |
|---|----------|
| 1 | What % of customers have paid more than $20K in total commissions? |
| 2 | Top 20 customers by total commissions paid |
| 3 | Top 10 customers by win percentage (min. 6 bets placed) |
| 4 | Top 20 customers by net loss to the house |
| 5 | House profitability by week — % of games where house kept more than it paid |
| 6 | Per-team: total games, wins, losses, spread covers, bets for vs. against |
| 7 | OLS regression: predict customer net value from demographic features |

---

## Machine Learning: OLS Regression

Used `statsmodels` OLS to model customer net value (how much a customer is worth to the house) from demographic and behavioral features.

**Features:** `age`, `customer_income`, `household_size`, `customer_type` (dummy encoded), `mode_color` (grouped: positive/negative/other), `customer_since`

**Key decisions:**
- Dropped `customer_type_local` to resolve multicollinearity (perfectly predicted by the other two dummies)
- Grouped `mode_color` into behavioral categories (`negative`: purple/blue/black, `positive`: white) based on domain logic
- Created `household_size_below_5` binary feature after observing non-linear relationship

---

## Repository Structure

```
nfl-betting-pipeline/
├── notebook/
│   └── fp_BrockJessop_TiandraTaylor.ipynb   # Full ETL + queries + ML
├── docs/
│   ├── erd.pdf                               # Entity-Relationship Diagram
│   └── data_dictionary.md                   # Full schema documentation
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Getting Started

### Prerequisites
- Python 3.8+
- PostgreSQL instance
- Access to source data files (CSV + SQL Server)

### Installation
```bash
git clone https://github.com/Tiandra123/nfl-betting-pipeline.git
cd nfl-betting-pipeline
pip install -r requirements.txt
```

### Configure Credentials
Create a `.env` file:
```
PG_DATABASE=your_database
PG_USER=your_user
PG_PASSWORD=your_password
PG_HOST=your_host
PG_PORT=5432

MSSQL_SERVER=your_server
MSSQL_USER=your_user
MSSQL_PASSWORD=your_password
MSSQL_DATABASE=your_database
```

---

## Tech Stack
- **Python:** pandas, psycopg2, pymssql, statsmodels, NumPy
- **Database:** PostgreSQL (normalized schema, FK constraints, exception table)
- **Source Data:** CSV files + SQL Server
- **ML:** statsmodels OLS regression
- **Docs:** ERD, IWDM, data dictionary
