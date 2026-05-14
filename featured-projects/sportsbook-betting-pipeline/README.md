# NFL Sports Betting ETL Pipeline

**Python · PostgreSQL · ETL · SQL · OLS Regression**

*Utah State University, M.S. MIS · Fall 2025
Built in collaboration with Brock Jessop (https://www.linkedin.com/in/jacob-brock-jessop/)*

---

Built as a graduate final project, this is a full ETL pipeline that ingests NFL schedule data (2015–2023) from CSV files and 200,000+ betting records from a SQL Server source, transforms and validates the data, and loads it into a DataMart, PostgreSQL database, across 6 tables. We designed the schema from scratch (ERD and data dictionary) and built an exception table pattern to capture malformed rows without halting ingestion.

On top of the database, we wrote 7 analytical SQL queries and an OLS regression model to predict customer net value from demographic features. This project covered the full data engineering lifecycle: source analysis, schema design, pipeline implementation, data validation, and analytics.

**What we built:**
- ETL pipeline: CSV + SQL Server → transform/validate → PostgreSQL (6 tables, FK constraints)
- Exception table to log and audit problematic rows by source file
- 7 SQL queries: commission analysis, win rates, spread performance, house profitability by week
- OLS regression predicting customer net value (age, income, household size, customer type, mode color)

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
Create a `.env` file in the project root:
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
 
### Run
Open `notebook/fp_BrockJessop_TiandraTaylor.ipynb` in Jupyter and run cells in order.
 
---
 
## Tech Stack
- **Python:** pandas, psycopg2, pymssql, statsmodels, NumPy
- **Database:** PostgreSQL
- **Source Data:** CSV files + SQL Server
- **ML:** statsmodels OLS regression