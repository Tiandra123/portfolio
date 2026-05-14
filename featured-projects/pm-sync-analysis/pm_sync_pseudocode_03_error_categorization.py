# PSEUDOCODE — PM Sync Failure Analysis
# Phase 3: Error Categorization + Visualization
# Proprietary implementation omitted per company data privacy policy.
# This pseudocode accurately represents the logic and architecture of the original code.

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from pathlib import Path

# -----------------------------------------------------------------------
# ERROR CATEGORIES
# Each platform has its own keyword lists because third-party APIs
# generate error messages in different formats with different terminology.
# Categories are checked in priority order — first match wins.
# -----------------------------------------------------------------------

# Shared base categories (present across most platforms)
BASE_CATEGORIES = {
    "Timeout Errors":                  ["timeout", "timed out", "per hour threshold exceeded", "response ended prematurely"],
    "Authorization/Permission Errors": ["unauthorized", "doesn't have permission", "not authorized",
                                        "password is incorrect", "does not have permission", "login failed"],
    "Missing Object / Doesn't Exist":  ["not found", "does not exist", "no records found", "could not be found"],
    "HTTP / Gateway Errors":           ["gateway", "503", "502", "500", "520", "httperror"],
    "Connection Errors":               ["connection could not be established", "transport connection",
                                        "connectiondata not configured", "deprecated"],
    "Object Disposed":                 ["disposed object"],
    "Conflict / Deadlock":             ["conflict occurred", "deadlock"],
    "Null / Missing Value":            ["null", "missing value", "object reference not set"],
    "Integration Problems":            ["license expired", "not configured", "web service requires schema"],
    "General Errors":                  ["an error occurred", "failed with exception", "general error"],
}

# Platform-specific keyword additions (layered on top of base categories)
# Each platform's third-party API uses slightly different error message formats.
PLATFORM_OVERRIDES = {
    "AppFolio": {
        "Missing Object / Doesn't Exist": ["no corresponding appfolioproperty"],
    },
    "Entrata": {
        "Missing Object / Doesn't Exist": ["no corresponding entrataproperty", "no entratapropertyid configured"],
        "Out of Bounds":                  ["is outside the window"],
    },
    "MRI": {
        "Missing Object / Doesn't Exist": ["no corresponding mriproperty"],
        "No Route to Host":               ["no route to host"],
    },
    "RealPage": {
        "Missing Object / Doesn't Exist": ["no corresponding realpageproperty", "pmcid", "siteid"],
        "Authorization/Permission Errors": ["does not have access", "no access"],
    },
    "ResMan": {
        "Missing Object / Doesn't Exist": ["no corresponding resmanproperty"],
        "Authorization/Permission Errors": ["insufficient privileges"],
        "Conflict / Deadlock":            ["would be truncated"],
    },
    "Yardi": {
        "Missing Object / Doesn't Exist": ["no corresponding yardiproperty", "no valid floorplans returned",
                                           "found no valid types", "no endpoint", "didn't match up"],
        "Authorization/Permission Errors": ["does not have rights", "insufficient privileges"],
        "Out of Bounds":                  ["move-out threshold", "limit reached for web method",
                                           "out of range", "outofmemoryexception"],
    },
}


# -----------------------------------------------------------------------
# CATEGORIZATION ENGINE
# -----------------------------------------------------------------------

def categorize_error_message(status_msg, pms_name):
    """
    Classify a single unstructured error message string into a root cause category.

    Logic:
    - Merge base categories with any platform-specific overrides
    - Check each category's keyword list against the lowercased message
    - Return the first matching category
    - Return None if no match (logged separately for manual review)

    Args:
        status_msg: str, raw error message from the API
        pms_name:   str, PMS platform name (e.g. 'Yardi')

    Returns:
        str: category name, or None if no match
    """
    msg_lower = status_msg.lower()

    # Merge base + platform overrides
    categories = {**BASE_CATEGORIES}
    if pms_name in PLATFORM_OVERRIDES:
        for cat, keywords in PLATFORM_OVERRIDES[pms_name].items():
            if cat in categories:
                categories[cat] = categories[cat] + keywords
            else:
                categories[cat] = keywords

    for category, keywords in categories.items():
        if any(kw in msg_lower for kw in keywords):
            return category

    return None  # Unmatched — logged for manual review


def categorize_pms_failures(df, pms_name):
    """
    Apply categorization across all failure records for one platform.
    Organizes results into a nested dict: category → job_id → community_id → [messages]

    Args:
        df:       DataFrame for one PMS (from Phase 2)
        pms_name: str, platform name

    Returns:
        dict: nested structure of categorized failure records
    """
    error_categories = {}

    for _, row in df.iterrows():
        job_id       = row['jobId']
        community_id = row['communityId']

        for msg_dict in row['communityJobStatusMessages']:
            status_msg       = msg_dict['statusMessage']
            community_job_id = msg_dict['communityJobId']
            created_on       = msg_dict['createdOn']

            category = categorize_error_message(status_msg, pms_name)
            if category is None:
                continue  # Skip unmatched; log separately in production

            # Build nested dict: category → job_id → community_id → [messages]
            error_categories.setdefault(category, {})
            error_categories[category].setdefault(job_id, {})
            error_categories[category][job_id].setdefault(community_id, [])
            error_categories[category][job_id][community_id].append({
                'communityJobId': community_job_id,
                'createdOn':      created_on,
                'statusMessage':  status_msg,
            })

    return error_categories


# -----------------------------------------------------------------------
# VISUALIZATION
# -----------------------------------------------------------------------

def plot_error_categories_bar(error_categories, pms_name, output_dir):
    """
    Bar chart: total failure count per error category for one PMS.
    """
    category_counts = {}
    for category, jobs in error_categories.items():
        total = sum(
            len(msgs)
            for communities in jobs.values()
            for msgs in communities.values()
        )
        category_counts[category] = total

    colors = cm.Set3(np.linspace(0, 1, len(category_counts)))
    plt.figure(figsize=(12, 8))
    bars = plt.bar(category_counts.keys(), category_counts.values(), color=colors)

    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2., height * 1.01,
                 str(int(height)), ha='center', va='bottom')

    plt.title(f'{pms_name} — Failures by Error Category')
    plt.xlabel('Error Category')
    plt.ylabel('Number of Failures')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(Path(output_dir) / f"{pms_name}_error_categories.png", dpi=300, bbox_inches='tight')
    plt.close()


def plot_monthly_failure_rate_trends(pms_df, output_dir):
    """
    Line chart: monthly failure rate (%) per PMS on a single chart.
    Reveals whether failure rates are improving or worsening over time.
    """
    pms_df = pms_df[pms_df['PMS'] != 'Other'].copy()
    pms_df['Date'] = pms_df['Month'].astype(str).str.zfill(2) + '-' + pms_df['Year'].astype(str)
    pms_df['FailureRatePct'] = pms_df['FailureRate'] * 100

    plt.figure(figsize=(12, 8))
    for pms in ['AppFolio', 'Entrata', 'MRI', 'RealPage', 'ResMan', 'Yardi']:
        data = pms_df[pms_df['PMS'] == pms].sort_values(['Year', 'Month'])
        plt.plot(data['Date'], data['FailureRatePct'], marker='o', label=pms)

    plt.title('Monthly Failure Rate Trends by PMS')
    plt.xlabel('Month')
    plt.ylabel('Failure Rate (%)')
    plt.legend()
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(Path(output_dir) / "monthly_failure_rate_trends.png", dpi=300, bbox_inches='tight')
    plt.close()


def plot_annual_pms_summary(pms_df, output_dir):
    """
    Side-by-side bar charts:
    Left:  Annual total failures per PMS (raw volume)
    Right: Annual average failure rate per PMS (%)

    Key insight: Yardi has highest volume; RealPage has highest failure RATE.
    Volume alone is misleading without context of how many syncs each platform runs.
    """
    pms_df = pms_df[pms_df['PMS'] != 'Other'].copy()
    summary = pms_df.groupby('PMS').agg(
        TotalFailures=('TotalFailures', 'sum'),
        AvgFailureRate=('FailureRate', 'mean')
    ).reset_index()
    summary['AvgFailureRatePct'] = summary['AvgFailureRate'] * 100

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    fig.suptitle('Annual PMS Failure Summary', fontsize=16)

    ax1.bar(summary['PMS'], summary['TotalFailures'])
    ax1.set_title('Total Failures by PMS')
    ax1.set_ylabel('Total Failures')
    ax1.tick_params(axis='x', rotation=45)

    ax2.bar(summary['PMS'], summary['AvgFailureRatePct'])
    ax2.set_title('Average Failure Rate by PMS (%)')
    ax2.set_ylabel('Failure Rate (%)')
    ax2.tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.savefig(Path(output_dir) / "annual_pms_summary.png", dpi=300, bbox_inches='tight')
    plt.close()


def plot_community_distribution_pie(output_dir):
    """
    Pie chart: how communities are distributed across PMS platforms.
    Context: ~50% of communities are on Yardi, which explains high failure volume.
    """
    community_counts = {
        'Yardi':    20401,
        'AppFolio':  9694,
        'Entrata':   5974,
        'ResMan':    3631,
        'RealPage':  1227,
        'MRI':         50,
    }

    plt.figure(figsize=(10, 8))
    plt.pie(
        list(community_counts.values()),
        labels=list(community_counts.keys()),
        autopct='%1.1f%%',
        startangle=90
    )
    plt.title('Community Distribution by PMS System', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(Path(output_dir) / "community_distribution_pie.png", dpi=300, bbox_inches='tight')
    plt.close()


if __name__ == "__main__":
    # Load processed PMS DataFrames from Phase 2
    pms_names = ['AppFolio', 'Entrata', 'MRI', 'RealPage', 'ResMan', 'Yardi']
    output_dir = Path("data/analysis")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Categorize errors and generate bar charts per PMS
    for pms in pms_names:
        df = pd.read_parquet(f"data/processed/{pms}_failure.parquet")
        error_categories = categorize_pms_failures(df, pms)
        plot_error_categories_bar(error_categories, pms, output_dir)

    # Load summary-level data for trend charts
    pms_summary_df = pd.read_parquet("data/processed/pms_data.parquet")
    plot_monthly_failure_rate_trends(pms_summary_df, output_dir)
    plot_annual_pms_summary(pms_summary_df, output_dir)
    plot_community_distribution_pie(output_dir)
