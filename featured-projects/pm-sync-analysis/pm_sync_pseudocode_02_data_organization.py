# PSEUDOCODE — PM Sync Failure Analysis
# Phase 2: Data Organization — Lookup Table + PMS-Specific DataFrames
# Proprietary implementation omitted per company data privacy policy.
# This pseudocode accurately represents the logic and architecture of the original code.

import pandas as pd
from pathlib import Path

# -----------------------------------------------------------------------
# LOOKUP TABLE
# Community IDs map to their PMS system and client.
# Source: internal CSV exported from database.
# -----------------------------------------------------------------------

def build_lookup_table(csv_path):
    """
    Load community → PMS + client mapping from CSV into a lookup dict.

    Input CSV columns: ComID, PMSystem, ClientID

    Returns:
        dict: { community_id: [pms_name, client_id] }

    Example:
        { 10045: ['Yardi', 312], 10046: ['RealPage', 88], ... }
    """
    df = pd.read_csv(csv_path)

    lookup = {}
    for _, row in df.iterrows():
        com_id    = row['ComID']
        pms       = row['PMSystem']
        client_id = row['ClientID']
        lookup[com_id] = [pms, client_id]

    return lookup


# -----------------------------------------------------------------------
# SPLIT INTO PMS-SPECIFIC DATAFRAMES
# -----------------------------------------------------------------------

def build_pms_dataframes(lookup, parquet_dates):
    """
    Loop through all daily Parquet files, match each failure record to its
    PMS using the lookup table, and bucket records into platform-specific lists.

    Logic:
    - For each date, load the corresponding Parquet file
    - For each row, get communityId and look it up in the lookup dict
    - Append the row (+ client_id) to the correct PMS bucket
    - After all files processed, convert each bucket to a DataFrame
    - Save each PMS DataFrame as a processed Parquet file

    Args:
        lookup:        dict from build_lookup_table()
        parquet_dates: list of date strings (e.g. ['05-03', '05-04', ...])

    Returns:
        dict of DataFrames keyed by PMS name:
        { 'Yardi': df, 'RealPage': df, 'AppFolio': df, ... }
    """
    buckets = {
        'AppFolio': [],
        'Entrata':  [],
        'MRI':      [],
        'Other':    [],
        'RealPage': [],
        'ResMan':   [],
        'Yardi':    [],
    }

    for date_str in parquet_dates:
        file_path = f"data/raw_parquets/sync_jobs_2025-{date_str}.parquet"
        df = pd.read_parquet(file_path)

        for _, row in df.iterrows():
            com_id = row['communityId']

            if com_id in lookup:
                pms_name, client_id = lookup[com_id]
                row_dict = row.to_dict()
                row_dict['client_id'] = client_id

                if pms_name in buckets:
                    buckets[pms_name].append(row_dict)

    # Convert buckets to DataFrames and save
    output_dir = Path("data/processed")
    output_dir.mkdir(parents=True, exist_ok=True)

    pms_dfs = {}
    for pms_name, records in buckets.items():
        if pms_name == 'Other':
            continue  # Excluded from analysis
        df_pms = pd.DataFrame(records)
        pms_dfs[pms_name] = df_pms
        df_pms.to_parquet(output_dir / f"{pms_name}_failure.parquet")

    return pms_dfs


if __name__ == "__main__":
    lookup = build_lookup_table("data/PMS_ClientID_ComID.csv")

    # Date range: May 3 – August 1, 2025
    parquet_dates = [
        '05-03', '05-04', '05-05',  # ... full list in original implementation
        '07-31', '08-01'
    ]

    pms_dfs = build_pms_dataframes(lookup, parquet_dates)

    for pms, df in pms_dfs.items():
        print(f"{pms}: {df.shape[0]} failure records")
