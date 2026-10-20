"""
app.py
Implements Question 7:
- Deploys the final locked champion pipeline through a rich Gradio User Interface
- Input validation with user-friendly error messages
- End-to-end inference returning predicted vulnerability tier, confidence probabilities, and plain-language explanation
- Responsible AI, POPIA compliance, and ethical limitations notice
"""

import os
import joblib
import pandas as pd
import numpy as np
import gradio as gr

# Load locked champion pipeline
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'champion_pipeline.joblib')

pipeline = None

def get_pipeline():
    global pipeline
    if pipeline is None:
        if os.path.exists(MODEL_PATH):
            pipeline = joblib.load(MODEL_PATH)
        else:
            raise FileNotFoundError(f"Champion pipeline artifact not found at {MODEL_PATH}. Run optimization first.")
    return pipeline

def predict_service_vulnerability(
    province, municipality, settlement_type, population_density,
    informal_dwelling_pct, piped_water_inside_pct, flush_toilet_pct,
    grid_electricity_pct, weekly_refuse_removal_pct, infra_age_years,
    avg_household_income_zar, unemployment_rate_pct, substation_load_factor,
    water_pipe_bursts_last_90d, unplanned_power_trips_last_90d,
    maintenance_budget_per_capita_zar, service_protest_history_3yr
):
    # =========================================================================
    # STEP 7.3: INPUT VALIDATION & HELPFUL ERROR MESSAGES
    # =========================================================================
    errors = []
    if population_density is None or population_density < 0:
        errors.append("• Population density cannot be negative or blank.")
    if avg_household_income_zar is None or avg_household_income_zar < 0:
        errors.append("• Household income cannot be negative or blank.")
    if water_pipe_bursts_last_90d is None or water_pipe_bursts_last_90d < 0:
        errors.append("• Water pipe burst count cannot be negative.")
    if unplanned_power_trips_last_90d is None or unplanned_power_trips_last_90d < 0:
        errors.append("• Power trip count cannot be negative.")
    if maintenance_budget_per_capita_zar is None or maintenance_budget_per_capita_zar < 0:
        errors.append("• Maintenance budget per capita cannot be negative.")
    if not (0 <= informal_dwelling_pct <= 100):
        errors.append("• Informal dwelling percentage must be between 0% and 100%.")
    if not (0 <= piped_water_inside_pct <= 100):
        errors.append("• Piped water percentage must be between 0% and 100%.")
    if not (0 <= grid_electricity_pct <= 100):
        errors.append("• Grid electricity percentage must be between 0% and 100%.")
    if not (0.1 <= substation_load_factor <= 3.0):
        errors.append("• Substation load factor must be between 0.1 and 3.0.")

    if errors:
        error_msg = "### [Input Validation Error]\nPlease correct the following issues:\n" + "\n".join(errors)
        badge_err = "<div style='background-color:#e74c3c; color:white; padding:15px; border-radius:8px; font-weight:bold; text-align:center;'>[VALIDATION FAILED]</div>"
        return (
            badge_err,
            {"Validation Error": 1.0},
            error_msg
        )

    # =========================================================================
    # STEP 7.2: END-TO-END PIPELINE EXECUTION
    # =========================================================================
    try:
        clf_pipe = get_pipeline()
    except Exception as e:
        badge_err = "<div style='background-color:#e74c3c; color:white; padding:15px; border-radius:8px; font-weight:bold; text-align:center;'>[PIPELINE ERROR]</div>"
        return (badge_err, {"Pipeline Error": 1.0}, f"Model pipeline failed to load: {str(e)}")

    input_dict = {
        'province': province,
        'municipality': municipality,
        'settlement_type': settlement_type,
        'population_density': float(population_density),
        'informal_dwelling_pct': float(informal_dwelling_pct),
        'piped_water_inside_pct': float(piped_water_inside_pct),
        'flush_toilet_pct': float(flush_toilet_pct),
        'grid_electricity_pct': float(grid_electricity_pct),
        'weekly_refuse_removal_pct': float(weekly_refuse_removal_pct),
        'infra_age_years': float(infra_age_years),
        'avg_household_income_zar': float(avg_household_income_zar),
        'unemployment_rate_pct': float(unemployment_rate_pct),
        'substation_load_factor': float(substation_load_factor),
        'water_pipe_bursts_last_90d': int(water_pipe_bursts_last_90d),
        'unplanned_power_trips_last_90d': int(unplanned_power_trips_last_90d),
        'maintenance_budget_per_capita_zar': float(maintenance_budget_per_capita_zar),
        'service_protest_history_3yr': 1 if service_protest_history_3yr else 0
    }

    input_df = pd.DataFrame([input_dict])

    probs = clf_pipe.predict_proba(input_df)[0]
    pred_class = int(np.argmax(probs))

    tier_labels = {
        0: ("[LOW RISK] Routine Service", "#2ecc71"),
        1: ("[MODERATE VULNERABILITY] Active Monitoring", "#f39c12"),
        2: ("[CRITICAL OUTAGE RISK] Emergency Intervention", "#e74c3c")
    }

    label_str, color = tier_labels[pred_class]
    confidence_pct = probs[pred_class] * 100

    prob_dict = {
        "Low Risk (Tier 0)": float(probs[0]),
        "Moderate Vulnerability (Tier 1)": float(probs[1]),
        "Critical Outage Risk (Tier 2)": float(probs[2])
    }

    # Plain-language explanation & municipal recommendation
    if pred_class == 0:
        explanation = (
            f"**Assessment:** Ward displays stable basic service indicators with adequate water coverage "
            f"({piped_water_inside_pct:.0f}%) and sustainable electrical substation loading ({substation_load_factor:.2f}). "
            f"Predicted with **{confidence_pct:.1f}% confidence**.\n\n"
            f"**Recommended Action:** Maintain scheduled preventative maintenance intervals. No emergency asset deployment required."
        )
    elif pred_class == 1:
        explanation = (
            f"**Assessment:** Ward shows compounding stress factors: aging distribution assets ({infra_age_years:.0f} years) "
            f"and moderate historical fault frequency ({water_pipe_bursts_last_90d} bursts, {unplanned_power_trips_last_90d} power trips). "
            f"Predicted with **{confidence_pct:.1f}% confidence**.\n\n"
            f"**Recommended Action:** Dispatch a municipal technical inspection crew within 14 days. Prioritise leak detection "
            f"and thermal transformer scanning to avert escalation to full outage."
        )
    else: # Critical
        explanation = (
            f"**Assessment:** **CRITICAL SERVICE FAILURE RISK.** High probability of catastrophic water or electrical supply failure "
            f"driven by severe asset over-utilization (Substation load factor: {substation_load_factor:.2f}, Asset age: {infra_age_years:.0f} yrs, "
            f"Informal dwelling proportion: {informal_dwelling_pct:.0f}%). Predicted with **{confidence_pct:.1f}% confidence**.\n\n"
            f"**Recommended Action:** **IMMEDIATE EMERGENCY RESPONSE REQUIRED.** Mobilise emergency engineering standby teams, "
            f"pre-position water tankers / auxiliary generators, and alert local ward councillor to mitigate civil unrest risk."
        )

    badge_html = f"<div style='background-color:{color}; color:white; padding:15px; border-radius:8px; font-size:18px; font-weight:bold; text-align:center;'>{label_str}</div>"

    return (badge_html, prob_dict, explanation)

# Build Gradio Blocks Application
def build_app():
    provinces = ['Gauteng', 'Western Cape', 'KwaZulu-Natal', 'Eastern Cape', 'Free State', 'Limpopo', 'Mpumalanga', 'North West', 'Northern Cape']
    municipalities = ['City of Johannesburg', 'City of Cape Town', 'eThekwini', 'Ekurhuleni', 'City of Tshwane', 'Nelson Mandela Bay', 'Buffalo City', 'Mangaung', 'Polokwane', 'City of Mbombela', 'Rustenburg', 'Sol Plaatje']
    settlements = ['Metro Urban', 'Formal Town', 'Informal Settlement', 'Rural Communal']

    with gr.Blocks(title="South Africa Municipal Service Delivery Risk Predictor") as demo:
        gr.Markdown(
            """
            # 🇿🇦 South African Municipal Service-Delivery Risk Triage System
            ### Module: IDA117V | Introduction to Data Science (S2 2026)
            **A Statistically Validated Machine-Learning Solution for Equitable Public Resource Allocation**
            """
        )

        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### 📍 Geographic & Demographic Parameters")
                province = gr.Dropdown(provinces, value='Gauteng', label="Province")
                municipality = gr.Dropdown(municipalities, value='City of Johannesburg', label="Municipality")
                settlement_type = gr.Dropdown(settlements, value='Informal Settlement', label="Settlement Typology")
                pop_density = gr.Number(value=3200, label="Population Density (people/km²)", minimum=0)
                informal_pct = gr.Slider(0, 100, value=65.0, label="Informal Dwelling Proportion (%)")
                income_zar = gr.Number(value=4500, label="Avg Monthly Household Income (ZAR)", minimum=0)
                unemployment_pct = gr.Slider(0, 100, value=48.0, label="Unemployment Rate (%)")

            with gr.Column(scale=1):
                gr.Markdown("### 🚰 Basic Service Infrastructure & Quality")
                water_pct = gr.Slider(0, 100, value=40.0, label="Piped Water Inside Dwelling/Yard (%)")
                toilet_pct = gr.Slider(0, 100, value=35.0, label="Flush Sanitation Connected to Sewer (%)")
                elec_pct = gr.Slider(0, 100, value=60.0, label="Grid Electricity Access (%)")
                refuse_pct = gr.Slider(0, 100, value=25.0, label="Weekly Municipal Refuse Collection (%)")
                infra_age = gr.Slider(0, 80, value=28.0, label="Estimated Distribution Asset Age (Years)")

            with gr.Column(scale=1):
                gr.Markdown("### ⚡ Operational Telemetry & History")
                substation_load = gr.Slider(0.1, 2.5, value=1.25, step=0.05, label="Substation Electrical Load Factor (Load/Rating)")
                bursts_90d = gr.Number(value=8, label="Water Pipe Bursts Logged (Last 90 Days)", precision=0)
                trips_90d = gr.Number(value=12, label="Unplanned Power Feeder Trips (Last 90 Days)", precision=0)
                budget_per_capita = gr.Number(value=650, label="Annual Maintenance Spend (ZAR/capita)", minimum=0)
                protest_history = gr.Checkbox(value=True, label="Service Delivery Protest Logged in Last 3 Years")
                
                predict_btn = gr.Button("🔍 Predict Service Delivery Vulnerability", variant="primary", size="lg")

        gr.Markdown("---")
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### 🎯 Classification Result")
                out_badge = gr.HTML(label="Predicted Vulnerability Tier")
                out_probs = gr.Label(num_top_classes=3, label="Confidence Probabilities")
            with gr.Column(scale=2):
                gr.Markdown("### 📋 Plain-Language Stakeholder Guidance")
                out_explanation = gr.Markdown(label="Municipal Action Plan")

        predict_btn.click(
            fn=predict_service_vulnerability,
            inputs=[
                province, municipality, settlement_type, pop_density,
                informal_pct, water_pct, toilet_pct, elec_pct, refuse_pct,
                infra_age, income_zar, unemployment_pct, substation_load,
                bursts_90d, trips_90d, budget_per_capita, protest_history
            ],
            outputs=[out_badge, out_probs, out_explanation]
        )

        gr.Markdown(
            """
            ---
            ### ⚖️ Responsible AI, POPIA Compliance & Ethical Governance Notice
            * **POPIA Compliance (Act No. 4 of 2013):** This application processes only aggregated ward-level spatial statistics. Zero Personally Identifiable Information (PII) is acquired, ingested, or displayed.
            * **Human-in-the-Loop Requirement:** This machine-learning model is an advisory decision-support instrument for municipal planning departments. It does **NOT** substitute for certified municipal engineering assessments or democratic budget allocation protocols.
            * **Algorithmic Fairness:** The model has been calibrated to compensate for historical reporting disparities (wards with lower citizen smartphone access) by prioritizing objective infrastructural loading metrics over logged ticket volumes alone.
            """
        )

    return demo

# Top-level exports required by serverless hosting providers (Vercel, Hugging Face, AWS Lambda, Render, WSGI/ASGI)
# Gradio Blocks instances expose the underlying FastAPI/Starlette application via `.app`
demo = build_app()
app = getattr(demo, "app", demo)
application = app
handler = app

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Launch Gradio Service Delivery Outage Triage Dashboard")
    parser.add_argument('--share', action='store_true', help='Generate a temporary public URL via Gradio Live')
    parser.add_argument('--port', type=int, default=7860, help='Port to bind the web server (default: 7860)')
    parser.add_argument('--server-name', type=str, default="127.0.0.1", help='Server IP to bind (use 0.0.0.0 for LAN access)')
    args, _ = parser.parse_known_args()

    print(f"\n" + "="*70)
    print("🚀 LAUNCHING MUNICIPAL OUTAGE TRIAGE DASHBOARD (IDA117V)")
    print(f"👉 Local Access URL: http://{args.server_name}:{args.port}")
    if args.share:
        print("🌐 Generating Public Share Link (Gradio Live)...")
    print("="*70 + "\n")
    demo.launch(server_name=args.server_name, server_port=args.port, share=args.share)
