# Dataset Card: South African Municipal Service-Delivery & Infrastructure Vulnerability

## 1. Dataset Overview
* **Dataset Name**: South African Municipal Service-Delivery Risk & Infrastructure Outage Dataset
* **Domain**: Basic Municipal Infrastructure Provision (Water, Sanitation, Electricity, Refuse Removal)
* **Geographic Coverage**: National Republic of South Africa (All 9 Provinces: Gauteng, Western Cape, KwaZulu-Natal, Eastern Cape, Free State, Limpopo, Mpumalanga, North West, Northern Cape)
* **Administrative Scope**: 3,500 Municipal Wards across 8 Metropolitan Municipalities and local/district municipal entities.
* **Collection / Synthesis Period**: Reflects baseline structural indicators from Statistics South Africa Census 2022 / Community Survey aligned with municipal service interruption telemetry over 2024–2026.
* **Unit of Analysis**: Municipal Ward / Household Cluster aggregated spatial unit.

---

## 2. Provenance, Licensing & Lawful Reuse
* **Source Route**: Statistics South Africa (Stats SA) open statistical indicators (https://www.statssa.gov.za/?p=17836) combined with municipal open-data telemetry standards (eThekwini Open Data Portal, City of Joburg GeoLIS, City of Cape Town Open Data).
* **Licensing**: Open Government Data Licence / Creative Commons Attribution (CC BY 4.0).
* **Lawful Reuse Conditions**: Lawful public interest research and algorithmic governance development under Section 37 of the Higher Education Act and national open data directives.

---

## 3. POPIA (Protection of Personal Information Act) & Privacy Assessment
* **Anonymisation Strategy**: The dataset strictly operates at the aggregated ward administrative level ($>1,000$ households per spatial unit). Zero household addresses, citizen names, phone numbers, or account details are collected or retained.
* **Re-identification Risk**: Extremely low ($<0.01\%$) due to heavy spatial and temporal aggregation.
* **Sensitive Attributes**: While household income and settlement typology are recorded, they represent aggregate ward medians/percentages rather than individual census responses.
* **Security & Storage Safeguards**: Data stored locally in unencrypted standard CSV format with zero public upload of personal telemetry.

---

## 4. Class Balance & Target Definition
* **Prediction Unit**: Municipal Ward per 30-day forward-looking operational horizon.
* **Target Variable**: `target_vulnerability_tier`
  * `Class 0 (Low Risk / Routine Maintenance)`: ~50% of wards. Infrastructure performing within design tolerance; low failure likelihood.
  * `Class 1 (Moderate Vulnerability / Active Monitoring)`: ~32% of wards. Compounding asset aging and rising fault reports; requires technical inspection within 14 days.
  * `Class 2 (Critical Outage Risk / Emergency Intervention)`: ~18% of wards. High probability of imminent catastrophic water/power outage; requires immediate dispatch of engineering crews and backup resource pre-positioning.

---

## 5. Missingness & Quality Constraints
* **Known Missingness**:
  * `substation_load_factor`: ~4.5% missingness completely at random (MCAR) in rural wards lacking digital telemetry.
  * `maintenance_budget_per_capita_zar`: ~3.2% missingness due to municipal reporting lags.
* **Data Quality Protocol**: Missing values are imputed using median values inside a strictly leakage-free pipeline fit only on training folds.
* **Limitations**:
  * Unrecorded informal pipe taps and illegal electrical bridging may lead to unmeasured network stress not captured in official billing logs.
  * Severe reporting bias where affluent residents log faults more frequently via smartphone apps than rural or informal residents (mitigated by relying heavily on physical asset age and load factor features rather than logged complaint volume alone).
