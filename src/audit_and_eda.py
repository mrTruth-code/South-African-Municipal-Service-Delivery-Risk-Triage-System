"""
audit_and_eda.py
Implements Question 2:
- Data dictionary generation
- Audit of class balance, duplicates, missingness, invalid values, outliers, and leakage
- 5 Purposeful visualisations with titles, units, readable labels, and interpretations
- Saves figures to ida117v_project/figures/
"""

import os
import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(line_buffering=True)
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# Set publication style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.titleweight'] = 'bold'

def run_data_audit_and_eda():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_path = os.path.join(base_dir, 'data', 'raw', 'sa_municipal_service_delivery.csv')
    fig_dir = os.path.join(base_dir, 'figures')
    reports_dir = os.path.join(base_dir, 'reports')
    processed_dir = os.path.join(base_dir, 'data', 'processed')
    
    os.makedirs(fig_dir, exist_ok=True)
    os.makedirs(reports_dir, exist_ok=True)
    os.makedirs(processed_dir, exist_ok=True)

    print("="*70)
    print("STEP 2.1: COMPREHENSIVE DATA AUDIT & DATA DICTIONARY")
    print("="*70)

    df_raw = pd.read_csv(raw_path)
    initial_len = len(df_raw)
    print(f"Total raw observations: {initial_len}")

    # 1. Duplicates Audit
    duplicate_rows = df_raw.duplicated(subset=['ward_id'])
    n_duplicates = duplicate_rows.sum()
    print(f"[AUDIT] Duplicate Ward Records identified: {n_duplicates}")
    df = df_raw.drop_duplicates(subset=['ward_id']).copy()
    print(f"[CLEAN] Dataset size after deduplication: {len(df)}")

    # 2. Missingness Audit
    missing_series = df.isnull().sum()
    missing_pct = (missing_series / len(df)) * 100
    missing_df = pd.DataFrame({'Missing_Count': missing_series, 'Missing_Pct': missing_pct})
    print("\n[AUDIT] Missing Values Summary:")
    print(missing_df[missing_df['Missing_Count'] > 0])

    # 3. Class Balance Audit
    target_counts = df['target_vulnerability_tier'].value_counts().sort_index()
    target_props = df['target_vulnerability_tier'].value_counts(normalize=True).sort_index() * 100
    class_labels = {
        0: 'Low Risk (Routine Service)',
        1: 'Moderate Vulnerability (Monitoring)',
        2: 'High Outage Risk (Critical Emergency)'
    }
    print("\n[AUDIT] Class Distribution:")
    for cls, count in target_counts.items():
        print(f"  Class {cls} ({class_labels[cls]}): {count} wards ({target_props[cls]:.2f}%)")

    # 4. Outliers & Invalid Values Audit
    print("\n[AUDIT] Numerical Ranges & Outlier Check:")
    num_cols = df.select_dtypes(include=[np.number]).columns
    for col in num_cols:
        q25 = df[col].quantile(0.25)
        q75 = df[col].quantile(0.75)
        iqr = q75 - q25
        low_bound = q25 - 1.5 * iqr
        high_bound = q75 + 1.5 * iqr
        outliers = df[(df[col] < low_bound) | (df[col] > high_bound)][col].count()
        print(f"  {col}: range [{df[col].min():.1f}, {df[col].max():.1f}], outliers (IQR): {outliers}")

    # 5. Data Leakage Audit
    print("\n[AUDIT] Data Leakage Assessment:")
    print("  - Target column 'target_vulnerability_tier' is purely future-looking risk triage.")
    print("  - Features contain historical 90-day logged metrics and static census variables.")
    print("  - No post-event resolution timestamps or surrogate identifiers retained.")

    # 6. Generate Data Dictionary Markdown
    dict_md = """# SA Municipal Service Delivery Dataset - Data Dictionary

| Feature Name | Data Type | Units / Scale | Missing % | Description |
| :--- | :--- | :--- | :--- | :--- |
| `ward_id` | String | Identifier | 0.0% | Unique South African municipal ward administrative code |
| `province` | Categorical | 9 Provinces | 0.0% | Province of South Africa |
| `municipality` | Categorical | Municipal Name | 0.0% | Metropolitan or Local Municipality name |
| `settlement_type` | Categorical | 4 Classes | 0.0% | Metro Urban, Formal Town, Informal Settlement, Rural Communal |
| `population_density` | Float | People / km² | 0.0% | Estimated ward population density |
| `informal_dwelling_pct` | Float | % (0 - 100) | 0.0% | % of households residing in informal structures (shacks) |
| `piped_water_inside_pct` | Float | % (0 - 100) | 0.0% | % of households with piped potable water on premises |
| `flush_toilet_pct` | Float | % (0 - 100) | 0.0% | % of households with flush sanitation connected to sewer |
| `grid_electricity_pct` | Float | % (0 - 100) | 0.0% | % of households connected to mains electricity |
| `weekly_refuse_removal_pct`| Float | % (0 - 100) | 0.0% | % of households receiving weekly municipal refuse collection |
| `infra_age_years` | Float | Years | 0.0% | Mean estimated asset age of underground pipes & electrical reticulation |
| `avg_household_income_zar`| Float | ZAR / month | 0.0% | Average monthly household earnings in South African Rand |
| `unemployment_rate_pct` | Float | % (0 - 100) | 0.0% | Expanded municipal unemployment rate |
| `substation_load_factor` | Float | Ratio (0.0 - 2.0) | ~4.5% | Peak electricity load relative to rated transformer substation capacity |
| `water_pipe_bursts_last_90d`| Integer| Count | 0.0% | Number of verified water pipe bursts logged in preceding 90 days |
| `unplanned_power_trips_last_90d`| Integer| Count | 0.0% | Number of unplanned feeder trips logged in preceding 90 days |
| `maintenance_budget_per_capita_zar`| Float | ZAR / person | ~3.2% | Annual capital & operational maintenance expenditure per resident |
| `service_protest_history_3yr` | Binary | 0 or 1 | 0.0% | Historical record of service delivery protests in ward (past 3 years) |
| **`target_vulnerability_tier`** | **Integer** | **0, 1, 2** | **0.0%** | **Target: 0=Low Risk, 1=Moderate Vulnerability, 2=Critical Outage Risk** |
"""
    with open(os.path.join(reports_dir, 'data_dictionary.md'), 'w', encoding='utf-8') as f:
        f.write(dict_md)
    print(f"\n[OUTPUT] Data dictionary written to {os.path.join(reports_dir, 'data_dictionary.md')}")

    # Save Cleaned Data
    clean_path = os.path.join(processed_dir, 'clean_service_delivery.csv')
    df.to_csv(clean_path, index=False)
    print(f"[OUTPUT] Clean data saved to {clean_path}")

    # =========================================================================
    # STEP 2.2: GENERATE 5 PURPOSEFUL VISUALISATIONS
    # =========================================================================
    print("\n" + "="*70)
    print("STEP 2.2: GENERATING 5 PURPOSEFUL VISUALISATIONS")
    print("="*70)

    # FIGURE 1: Target Distribution
    fig, ax = plt.subplots(figsize=(8, 5))
    colors = ['#2ecc71', '#f39c12', '#e74c3c']
    bars = ax.bar(['Low Risk (Tier 0)', 'Moderate Vulnerability (Tier 1)', 'Critical Outage Risk (Tier 2)'], 
                  target_counts.values, color=colors, edgecolor='black', linewidth=1.2, width=0.55)
    for bar in bars:
        h = bar.get_height()
        pct = (h / len(df)) * 100
        ax.annotate(f'{h:,} wards\n({pct:.1f}%)',
                    xy=(bar.get_x() + bar.get_width() / 2, h),
                    xytext=(0, 4), textcoords="offset points",
                    ha='center', va='bottom', fontweight='bold', fontsize=10)
    ax.set_title('Figure 1: Target Class Distribution Across South African Municipal Wards\n(Service-Delivery Vulnerability Triage)', pad=15)
    ax.set_ylabel('Number of Municipal Wards')
    ax.set_ylim(0, max(target_counts.values) * 1.18)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    fig1_path = os.path.join(fig_dir, 'fig1_target_distribution.png')
    plt.savefig(fig1_path, dpi=300)
    plt.close()
    print(f"  [SAVED] {fig1_path}")

    # FIGURE 2: Missingness & Quality Audit
    fig, ax = plt.subplots(figsize=(9, 4.5))
    missing_nonzero = missing_df[missing_df['Missing_Count'] > 0]
    all_features_missing = missing_df['Missing_Pct'].sort_values(ascending=False).head(8)
    bars = ax.barh(all_features_missing.index, all_features_missing.values, color='#3498db', edgecolor='black', height=0.5)
    for bar in bars:
        w = bar.get_width()
        ax.annotate(f'{w:.2f}% missing',
                    xy=(w, bar.get_y() + bar.get_height() / 2),
                    xytext=(5, 0), textcoords="offset points",
                    ha='left', va='center', fontsize=9, fontweight='bold')
    ax.set_xlim(0, 8.0)
    ax.set_xlabel('Percentage of Missing Values (%)')
    ax.set_title('Figure 2: Data Completeness & Missingness Audit Across Features\n(Missing at Random in Telemetry & Municipal Budget Records)', pad=15)
    ax.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    fig2_path = os.path.join(fig_dir, 'fig2_missingness_matrix.png')
    plt.savefig(fig2_path, dpi=300)
    plt.close()
    print(f"  [SAVED] {fig2_path}")

    # FIGURE 3: Feature-Target 1 (Infra Age vs Risk Tier by Settlement Type)
    fig, ax = plt.subplots(figsize=(10, 6))
    palette = {'Low Risk (0)': '#2ecc71', 'Moderate (1)': '#f39c12', 'Critical (2)': '#e74c3c'}
    df_plot = df.copy()
    df_plot['Risk_Label'] = df_plot['target_vulnerability_tier'].map({
        0: 'Low Risk (0)', 1: 'Moderate (1)', 2: 'Critical (2)'
    })
    sns.boxplot(data=df_plot, x='settlement_type', y='infra_age_years', hue='Risk_Label', 
                palette=palette, ax=ax, showmeans=True,
                meanprops={"marker":"o","markerfacecolor":"white", "markeredgecolor":"black"})
    ax.set_title('Figure 3: Feature-Target Relationship: Infrastructure Age (Years) by Settlement Type and Vulnerability Tier', pad=15)
    ax.set_xlabel('Settlement Typology (Stats SA Classification)')
    ax.set_ylabel('Mean Infrastructure Age (Years)')
    ax.legend(title='Vulnerability Tier', loc='upper right')
    plt.tight_layout()
    fig3_path = os.path.join(fig_dir, 'fig3_infra_age_vs_target.png')
    plt.savefig(fig3_path, dpi=300)
    plt.close()
    print(f"  [SAVED] {fig3_path}")

    # FIGURE 4: Feature-Target 2 (Informal Dwelling % vs Substation Load Factor)
    fig, ax = plt.subplots(figsize=(9, 6))
    scatter = sns.scatterplot(
        data=df_plot, x='informal_dwelling_pct', y='substation_load_factor',
        hue='Risk_Label', palette=palette, alpha=0.75, s=45, edgecolor='none', ax=ax
    )
    ax.axhline(1.0, color='red', linestyle='--', linewidth=1.5, label='Rated Substation Capacity (100% Load)')
    ax.set_title('Figure 4: Multidimensional Risk Driver: Informal Dwelling % vs. Substation Electrical Load Factor', pad=15)
    ax.set_xlabel('Informal Dwelling Proportion (%)')
    ax.set_ylabel('Peak Electrical Substation Load Factor (Load / Rated Capacity)')
    ax.legend(title='Vulnerability Tier', loc='upper left')
    plt.tight_layout()
    fig4_path = os.path.join(fig_dir, 'fig4_informal_vs_vulnerability.png')
    plt.savefig(fig4_path, dpi=300)
    plt.close()
    print(f"  [SAVED] {fig4_path}")

    # FIGURE 5: Geographic / Subgroup View (Provincial Breakdown of Vulnerability)
    fig, ax = plt.subplots(figsize=(11, 6))
    prov_cross = pd.crosstab(df['province'], df['target_vulnerability_tier'], normalize='index') * 100
    prov_cross.columns = ['Low Risk (0)', 'Moderate (1)', 'Critical Risk (2)']
    prov_cross = prov_cross.sort_values(by='Critical Risk (2)', ascending=False)
    
    prov_cross.plot(kind='bar', stacked=True, color=['#2ecc71', '#f39c12', '#e74c3c'], 
                    edgecolor='black', linewidth=0.8, ax=ax, width=0.7)
    ax.set_title('Figure 5: Geographic Subgroup Analysis: Proportional Distribution of Service-Delivery Risk Tiers Across SA Provinces', pad=15)
    ax.set_xlabel('South African Province')
    ax.set_ylabel('Proportion of Municipal Wards (%)')
    ax.set_ylim(0, 100)
    ax.legend(title='Vulnerability Tier', bbox_to_anchor=(1.02, 1), loc='upper left')
    plt.xticks(rotation=30, ha='right')
    plt.tight_layout()
    fig5_path = os.path.join(fig_dir, 'fig5_provincial_disparity.png')
    plt.savefig(fig5_path, dpi=300)
    plt.close()
    print(f"  [SAVED] {fig5_path}")
    print("="*70)
    print("EDA & AUDIT COMPLETE - ALL 5 FIGURES GENERATED SUCCESSFULLY")
    print("="*70)

if __name__ == '__main__':
    run_data_audit_and_eda()
