# Data Pipeline Coursework

Assignments from the Data Pipelines course (USU, M.S. MIS). Each notebook covers a different aspect of building and managing data pipelines — ingestion, data quality, exception handling, and transformation.

---

| File | Description |
|------|-------------|
| `i3_tiandrataylor.ipynb` | Ingests Corgi race CSV files into PostgreSQL. Checks each file against an `ingest` table to skip already-processed files. Invalid records are routed to a `corgi_exception` sin bin table with issue descriptions and timestamps for later review. |
| `i4_tiandrataylor.ipynb` | Works through an `ExceptionLog` (sin bin) table to fix records held in purgatory. Analyzes anomalies per record, applies fixes (null building values, invalid types, date corrections), and updates the `fixstamp` once resolved so records can move to the main table. |
| `p3_tiandrataylor.ipynb` | Queries a theme park SQL Server database using CTEs to analyze household guest data — members per household, season pass counts, under-18 counts, and visit frequency. |
| `p4_tiandrataylor.ipynb` | Transforms and cleans a Corgi derby CSV — rounds and retyps weight, splits name/age columns, normalizes breed names, and parses a messy date string into a standardized `YYYY-MM-DD` format for database ingestion. |

---

*Credentials have been replaced with `os.getenv()` calls. Create a `.env` file with `DB_USER`, `DB_PASSWORD`, and `DB_HOST` to run locally.*
