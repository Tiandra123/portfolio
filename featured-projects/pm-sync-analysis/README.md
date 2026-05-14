# PM Sync Failure Analysis 

**Python · pandas · Parquet · Matplotlib · API Integration · Root Cause Analysis**

*Developed at Entrata — full code omitted per company data privacy policy*

---

At Entrata, property management sync pipelines process thousands of transactions daily across 6 platforms: Yardi, RealPage, AppFolio, ResMan, MRI, and Entrata's own system. The support team was reacting to failures individually with no systematic understanding of what was actually driving them. I independently scoped and executed a comprehensive failure analysis to bring data-driven clarity to the problem.

I extracted 200,000+ failure records via API over a 90-day window, organized the data hierarchically by PMS → client → community, and stored it as Parquet files for efficient processing. The biggest challenge was that error messages were completely unstructured - thousands of unique strings with no standardization. I built a Python keyword-matching categorization system for each of the 6 platforms, then created a full suite of visualizations: community distribution by platform, total failures vs. failure rates, job type breakdowns per PMS, and monthly trend lines. The analysis revealed that 80% of all failures traced to 5 root cause categories, giving the engineering team clear, data-driven prioritization for the first time.

**What I built:**
- API data collection script pulling daily failure records across a 90-day window, saved as Parquet files
- Lookup table mapping community IDs to their PMS and client, used to split data into 6 platform-specific DataFrames
- Per-platform keyword matching categorization system classifying thousands of unstructured error messages
- Visualization suite: community distribution pie chart, annual failure totals vs. failure rates, monthly trend lines, job type breakdowns per PMS
- Findings are being built into a real-time Domo dashboard used by Customer Success and Data teams

---

## Tech Stack
- **Python:** pandas, matplotlib, NumPy, pathlib
- **Storage:** Parquet (raw + processed)
- **Data Source:** Internal REST API (RentDynamics)
- **Visualization:** matplotlib
