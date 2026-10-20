# SA Municipal Service Delivery Dataset - Data Dictionary

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
