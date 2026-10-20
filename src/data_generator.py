"""
data_generator.py
Synthetic South African Municipal Service-Delivery Dataset Generator.
Grounds the data in realistic Statistics South Africa (Census 2022 / Community Survey)
and municipal infrastructure realities across 9 provinces and key municipalities.
"""

import os
import numpy as np
import pandas as pd

def generate_sa_service_delivery_data(n_samples=3500, random_seed=42):
    np.random.seed(random_seed)

    provinces_municipalities = {
        'Gauteng': ['City of Johannesburg', 'City of Tshwane', 'Ekurhuleni', 'Emfuleni', 'Mogale City'],
        'Western Cape': ['City of Cape Town', 'Drakenstein', 'George', 'Stellenbosch', 'Saldanha Bay'],
        'KwaZulu-Natal': ['eThekwini', 'Msunduzi', 'uMhlathuze', 'Ray Nkonyeni', 'Newcastle'],
        'Eastern Cape': ['Nelson Mandela Bay', 'Buffalo City', 'King Sabata Dalindyebo', 'Kouga'],
        'Free State': ['Mangaung', 'Matjhabeng', 'Maluti-a-Phofung', 'Metsimaholo'],
        'Limpopo': ['Polokwane', 'Thabazimbi', 'Mogalakwena', 'Greater Tzaneen'],
        'Mpumalanga': ['City of Mbombela', 'Emalahleni', 'Govan Mbeki', 'Steve Tshwete'],
        'North West': ['Rustenburg', 'Madibeng', 'JB Marks', 'Mahikeng'],
        'Northern Cape': ['Sol Plaatje', 'Dawid Kruiper', 'Ga-Segonyana']
    }

    province_weights = [0.26, 0.16, 0.20, 0.11, 0.06, 0.07, 0.06, 0.05, 0.03]
    provinces = list(provinces_municipalities.keys())
    
    assigned_provinces = np.random.choice(provinces, size=n_samples, p=province_weights)
    assigned_municipalities = [
        np.random.choice(provinces_municipalities[prov]) for prov in assigned_provinces
    ]

    settlement_types = ['Metro Urban', 'Formal Town', 'Informal Settlement', 'Rural Communal']
    
    data = []
    for i in range(n_samples):
        prov = assigned_provinces[i]
        muni = assigned_municipalities[i]
        
        is_metro = 'City' in muni or muni in ['eThekwini', 'Ekurhuleni', 'Nelson Mandela Bay', 'Buffalo City', 'Mangaung']
        
        if is_metro:
            stype = np.random.choice(settlement_types, p=[0.55, 0.15, 0.25, 0.05])
            pop_density = np.random.lognormal(mean=7.5, sigma=0.8)  # ~1000 - 5000 /km2
        else:
            stype = np.random.choice(settlement_types, p=[0.20, 0.40, 0.15, 0.25])
            pop_density = np.random.lognormal(mean=5.5, sigma=1.0)  # ~100 - 1000 /km2
            
        if stype == 'Informal Settlement':
            informal_pct = np.clip(np.random.normal(68.0, 15.0), 20.0, 98.0)
            piped_water_pct = np.clip(np.random.normal(45.0, 18.0), 5.0, 85.0)
            flush_toilet_pct = np.clip(np.random.normal(32.0, 15.0), 2.0, 75.0)
            grid_elec_pct = np.clip(np.random.normal(60.0, 18.0), 15.0, 95.0)
            refuse_pct = np.clip(np.random.normal(30.0, 20.0), 0.0, 80.0)
            income_zar = np.clip(np.random.lognormal(8.2, 0.4), 2500, 12000)
            unemployment = np.clip(np.random.normal(48.0, 8.0), 25.0, 75.0)
            infra_age = np.clip(np.random.normal(18.0, 6.0), 2.0, 40.0)
        elif stype == 'Rural Communal':
            informal_pct = np.clip(np.random.normal(15.0, 8.0), 2.0, 45.0)
            piped_water_pct = np.clip(np.random.normal(38.0, 16.0), 5.0, 80.0)
            flush_toilet_pct = np.clip(np.random.normal(25.0, 12.0), 2.0, 60.0)
            grid_elec_pct = np.clip(np.random.normal(72.0, 14.0), 30.0, 98.0)
            refuse_pct = np.clip(np.random.normal(12.0, 10.0), 0.0, 50.0)
            income_zar = np.clip(np.random.lognormal(8.1, 0.4), 2200, 11000)
            unemployment = np.clip(np.random.normal(52.0, 7.0), 30.0, 80.0)
            infra_age = np.clip(np.random.normal(22.0, 8.0), 4.0, 50.0)
        elif stype == 'Formal Town':
            informal_pct = np.clip(np.random.normal(12.0, 6.0), 1.0, 30.0)
            piped_water_pct = np.clip(np.random.normal(82.0, 10.0), 45.0, 99.0)
            flush_toilet_pct = np.clip(np.random.normal(78.0, 11.0), 40.0, 98.0)
            grid_elec_pct = np.clip(np.random.normal(88.0, 8.0), 60.0, 100.0)
            refuse_pct = np.clip(np.random.normal(74.0, 15.0), 25.0, 98.0)
            income_zar = np.clip(np.random.lognormal(9.2, 0.6), 5500, 35000)
            unemployment = np.clip(np.random.normal(32.0, 6.0), 15.0, 55.0)
            infra_age = np.clip(np.random.normal(34.0, 10.0), 10.0, 65.0)
        else: # Metro Urban
            informal_pct = np.clip(np.random.normal(8.0, 5.0), 0.5, 25.0)
            piped_water_pct = np.clip(np.random.normal(92.0, 6.0), 65.0, 100.0)
            flush_toilet_pct = np.clip(np.random.normal(90.0, 7.0), 60.0, 100.0)
            grid_elec_pct = np.clip(np.random.normal(94.0, 5.0), 75.0, 100.0)
            refuse_pct = np.clip(np.random.normal(88.0, 9.0), 50.0, 100.0)
            income_zar = np.clip(np.random.lognormal(9.8, 0.7), 8500, 75000)
            unemployment = np.clip(np.random.normal(26.0, 5.0), 10.0, 48.0)
            infra_age = np.clip(np.random.normal(38.0, 12.0), 12.0, 75.0)

        # Telemetry & Operational Metrics
        substation_load = np.clip(np.random.normal(0.75 + (infra_age / 120.0) + (informal_pct / 200.0), 0.18), 0.35, 1.45)
        
        # Historical fault counts
        base_burst_rate = 1.5 + (infra_age * 0.15) + (100.0 - piped_water_pct) * 0.08
        bursts_90d = int(np.random.poisson(lam=max(0.5, base_burst_rate)))
        
        base_trip_rate = 1.0 + (substation_load * 4.0) + (infra_age * 0.08)
        trips_90d = int(np.random.poisson(lam=max(0.5, base_trip_rate)))
        
        # Budget per capita
        budget_per_capita = np.clip(np.random.normal(1200 if is_metro else 650, 250), 150, 2800)
        
        # Protest risk
        protest_prob = 1 / (1 + np.exp(-(-3.5 + 0.04*informal_pct + 0.03*unemployment + 0.08*(bursts_90d+trips_90d) - 0.0008*income_zar)))
        protest_history = int(np.random.rand() < protest_prob)

        # Risk Score Latent Function
        risk_score = (
            0.04 * infra_age +
            0.03 * informal_pct +
            0.85 * substation_load +
            0.12 * bursts_90d +
            0.15 * trips_90d +
            0.02 * unemployment -
            0.025 * piped_water_pct -
            0.02 * grid_elec_pct -
            0.0006 * budget_per_capita +
            0.6 * protest_history +
            np.random.normal(0, 0.6)  # Stochastic operational noise
        )
        
        # 3-Tier Classification Assignment
        # Target classes:
        # 0: Low Risk (Routine) ~ 50%
        # 1: Moderate Vulnerability (Monitoring / Planned Maintenance) ~ 32%
        # 2: High Outage Risk / Critical Emergency (Immediate Dispatch) ~ 18%
        if risk_score < 2.8:
            target = 0
        elif risk_score < 4.6:
            target = 1
        else:
            target = 2

        ward_code = f"W{np.random.randint(100, 999)}{i+1000:05d}"

        data.append({
            'ward_id': ward_code,
            'province': prov,
            'municipality': muni,
            'settlement_type': stype,
            'population_density': round(pop_density, 1),
            'informal_dwelling_pct': round(informal_pct, 2),
            'piped_water_inside_pct': round(piped_water_pct, 2),
            'flush_toilet_pct': round(flush_toilet_pct, 2),
            'grid_electricity_pct': round(grid_elec_pct, 2),
            'weekly_refuse_removal_pct': round(refuse_pct, 2),
            'infra_age_years': round(infra_age, 1),
            'avg_household_income_zar': round(income_zar, 0),
            'unemployment_rate_pct': round(unemployment, 2),
            'substation_load_factor': round(substation_load, 3),
            'water_pipe_bursts_last_90d': bursts_90d,
            'unplanned_power_trips_last_90d': trips_90d,
            'maintenance_budget_per_capita_zar': round(budget_per_capita, 1),
            'service_protest_history_3yr': protest_history,
            'target_vulnerability_tier': target
        })

    df = pd.DataFrame(data)

    # Introduce realistic missingness (MAR / MCAR) to test audit & imputation:
    # 1. substation_load_factor has ~4.5% missing values (lack of smart telemetry in remote wards)
    missing_telemetry_mask = np.random.rand(len(df)) < 0.045
    df.loc[missing_telemetry_mask, 'substation_load_factor'] = np.nan

    # 2. maintenance_budget_per_capita_zar has ~3.2% missing values (unreported municipal sub-budgets)
    missing_budget_mask = np.random.rand(len(df)) < 0.032
    df.loc[missing_budget_mask, 'maintenance_budget_per_capita_zar'] = np.nan

    # 3. Add 5 duplicate rows at the end to demonstrate deduplication audit in Q2
    duplicates = df.sample(n=5, random_state=random_seed)
    df = pd.concat([df, duplicates], ignore_index=True)

    return df

if __name__ == '__main__':
    raw_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')
    os.makedirs(raw_dir, exist_ok=True)
    out_path = os.path.join(raw_dir, 'sa_municipal_service_delivery.csv')
    df = generate_sa_service_delivery_data()
    df.to_csv(out_path, index=False)
    print(f"Generated {len(df)} records saved to {out_path}")
    print("Target distribution:")
    print(df['target_vulnerability_tier'].value_counts(normalize=True))
