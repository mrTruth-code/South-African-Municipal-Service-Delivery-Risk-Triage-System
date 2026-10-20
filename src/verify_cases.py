"""
verify_cases.py
Implements Question 7.4 Demonstration:
Demonstrates 3 valid cases (Low Risk, Moderate Vulnerability, Critical Outage Risk)
and 1 invalid-input case (testing input validation and helpful error handling).
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app import predict_service_vulnerability

def run_case_demonstrations():
    print("="*70)
    print("QUESTION 7.4: USER INTERFACE VERIFICATION & CASE DEMONSTRATIONS")
    print("="*70)

    # -------------------------------------------------------------------------
    # CASE 1: Valid Low-Risk Case (Affluent Formal Metro Ward)
    # -------------------------------------------------------------------------
    print("\n[CASE 1: VALID LOW-RISK SCENARIO]")
    print("Characteristics: High piped water coverage (98%), modern electrical substation (load=0.62), low historical outages.")
    badge, probs, explanation = predict_service_vulnerability(
        province='Western Cape', municipality='City of Cape Town', settlement_type='Metro Urban',
        population_density=1800, informal_dwelling_pct=2.5, piped_water_inside_pct=98.0,
        flush_toilet_pct=96.0, grid_electricity_pct=99.0, weekly_refuse_removal_pct=98.0,
        infra_age_years=12.0, avg_household_income_zar=35000, unemployment_rate_pct=15.0,
        substation_load_factor=0.62, water_pipe_bursts_last_90d=1, unplanned_power_trips_last_90d=1,
        maintenance_budget_per_capita_zar=2200, service_protest_history_3yr=False
    )
    print("Output Badge:     ", badge)
    print("Probabilities:    ", probs)
    print("Plain Explanation:\n", explanation)

    # -------------------------------------------------------------------------
    # CASE 2: Valid Moderate-Vulnerability Case (Aging Formal Town)
    # -------------------------------------------------------------------------
    print("\n" + "-"*70)
    print("[CASE 2: VALID MODERATE-VULNERABILITY SCENARIO]")
    print("Characteristics: Aging piping infrastructure (38 yrs), moderate substation load (0.95), elevated pipe bursts.")
    badge, probs, explanation = predict_service_vulnerability(
        province='Free State', municipality='Mangaung', settlement_type='Formal Town',
        population_density=950, informal_dwelling_pct=14.0, piped_water_inside_pct=78.0,
        flush_toilet_pct=72.0, grid_electricity_pct=86.0, weekly_refuse_removal_pct=65.0,
        infra_age_years=38.0, avg_household_income_zar=12000, unemployment_rate_pct=34.0,
        substation_load_factor=0.95, water_pipe_bursts_last_90d=5, unplanned_power_trips_last_90d=4,
        maintenance_budget_per_capita_zar=850, service_protest_history_3yr=False
    )
    print("Output Badge:     ", badge)
    print("Probabilities:    ", probs)
    print("Plain Explanation:\n", explanation)

    # -------------------------------------------------------------------------
    # CASE 3: Valid Critical Outage Risk Case (Dense Informal Settlement / Overloaded Substation)
    # -------------------------------------------------------------------------
    print("\n" + "-"*70)
    print("[CASE 3: VALID CRITICAL OUTAGE RISK SCENARIO]")
    print("Characteristics: Dense informal settlement (78%), severe electrical overload (1.35), 14 power trips, protest history.")
    badge, probs, explanation = predict_service_vulnerability(
        province='Gauteng', municipality='City of Johannesburg', settlement_type='Informal Settlement',
        population_density=4800, informal_dwelling_pct=78.0, piped_water_inside_pct=32.0,
        flush_toilet_pct=22.0, grid_electricity_pct=55.0, weekly_refuse_removal_pct=18.0,
        infra_age_years=25.0, avg_household_income_zar=3800, unemployment_rate_pct=52.0,
        substation_load_factor=1.35, water_pipe_bursts_last_90d=11, unplanned_power_trips_last_90d=16,
        maintenance_budget_per_capita_zar=450, service_protest_history_3yr=True
    )
    print("Output Badge:     ", badge)
    print("Probabilities:    ", probs)
    print("Plain Explanation:\n", explanation)

    # -------------------------------------------------------------------------
    # CASE 4: Invalid-Input Case (Negative Population Density & Percentage > 100%)
    # -------------------------------------------------------------------------
    print("\n" + "-"*70)
    print("[CASE 4: INVALID-INPUT ERROR HANDLING SCENARIO]")
    print("Invalid parameters: Negative population density (-500) and impossible percentage (145%).")
    badge, probs, explanation = predict_service_vulnerability(
        province='KwaZulu-Natal', municipality='eThekwini', settlement_type='Metro Urban',
        population_density=-500, informal_dwelling_pct=145.0, piped_water_inside_pct=90.0,
        flush_toilet_pct=85.0, grid_electricity_pct=90.0, weekly_refuse_removal_pct=80.0,
        infra_age_years=-5.0, avg_household_income_zar=15000, unemployment_rate_pct=30.0,
        substation_load_factor=0.8, water_pipe_bursts_last_90d=-2, unplanned_power_trips_last_90d=1,
        maintenance_budget_per_capita_zar=1000, service_protest_history_3yr=False
    )
    print("Output Badge:     ", badge)
    print("Probabilities:    ", probs)
    print("Error Feedback:\n", explanation)
    print("="*70)
    print("ALL 4 DEMONSTRATION CASES COMPLETED SUCCESSFULLY")
    print("="*70)

if __name__ == '__main__':
    run_case_demonstrations()
