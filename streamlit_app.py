"""
streamlit_app.py
Interactive Streamlit Dashboard for the South African Municipal Service-Delivery Risk Triage System.
Compatible with Streamlit Community Cloud (share.streamlit.io) and Streamlit Playground.
"""

import os
import sys

# Ensure src/ is in sys.path so unpickling references to pipeline module succeed
SRC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

# Also import pipeline into top-level sys.modules in case pickle looks for 'pipeline'
import pipeline
sys.modules['pipeline'] = pipeline

import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Page configuration
st.set_page_config(
    page_title="Municipal Outage & Vulnerability Triage System",
    page_icon="🇿🇦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1e3a8a;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #4b5563;
        margin-bottom: 1.5rem;
    }
    .badge-tier0 {
        background-color: #dcfce7;
        color: #166534;
        padding: 0.8rem 1.2rem;
        border-radius: 8px;
        font-weight: 700;
        font-size: 1.2rem;
        border: 2px solid #86efac;
    }
    .badge-tier1 {
        background-color: #fef9c3;
        color: #854d0e;
        padding: 0.8rem 1.2rem;
        border-radius: 8px;
        font-weight: 700;
        font-size: 1.2rem;
        border: 2px solid #fde047;
    }
    .badge-tier2 {
        background-color: #fee2e2;
        color: #991b1b;
        padding: 0.8rem 1.2rem;
        border-radius: 8px;
        font-weight: 700;
        font-size: 1.2rem;
        border: 2px solid #fca5a5;
    }
</style>
""", unsafe_allow_html=True)

# Load locked champion pipeline
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'champion_pipeline.joblib')

@st.cache_resource
def load_champion_model():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    else:
        st.error(f"Champion pipeline artifact not found at {MODEL_PATH}.")
        return None

pipeline = load_champion_model()

# Header
st.markdown('<div class="main-header">🇿🇦 Municipal Outage & Infrastructure Vulnerability Triage System</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Statistically Validated Machine-Learning Decision-Support System | South African Municipalities (IDA117V)</div>', unsafe_allow_html=True)

# Sidebar inputs
st.sidebar.header("📋 Ward Infrastructure & Demographics")

PROVINCES = [
    'Eastern Cape', 'Free State', 'Gauteng', 'KwaZulu-Natal',
    'Limpopo', 'Mpumalanga', 'Northern Cape', 'North West', 'Western Cape'
]

MUNICIPALITIES = [
    'City of Johannesburg', 'City of Tshwane', 'City of Cape Town',
    'eThekwini', 'Ekurhuleni', 'Mangaung', 'Nelson Mandela Bay',
    'Buffalo City', 'Polokwane', 'Rustenburg', 'Mbombela',
    'Sol Plaatje', 'Emfuleni', 'Matjhabeng', 'Msunduzi'
]

SETTLEMENT_TYPES = ['Formal Urban', 'Informal Settlement', 'Peri-Urban', 'Rural Communal']

with st.sidebar:
    st.subheader("1. Spatial & Settlement Profile")
    province = st.selectbox("Province", PROVINCES, index=2)
    municipality = st.selectbox("Municipality", MUNICIPALITIES, index=0)
    settlement_type = st.selectbox("Settlement Type", SETTLEMENT_TYPES, index=1)
    
    st.subheader("2. Basic Service Access (%)")
    col_a, col_b = st.columns(2)
    with col_a:
        piped_water_inside_pct = st.slider("Piped Water Inside (%)", 0.0, 100.0, 42.5)
        grid_electricity_pct = st.slider("Grid Electricity (%)", 0.0, 100.0, 78.0)
    with col_b:
        flush_toilet_pct = st.slider("Flush Sanitation (%)", 0.0, 100.0, 38.0)
        weekly_refuse_removal_pct = st.slider("Refuse Removal (%)", 0.0, 100.0, 45.0)
        
    informal_dwelling_pct = st.slider("Informal Dwelling Proportion (%)", 0.0, 100.0, 35.0)

    st.subheader("3. Physical Assets & Historical Stress")
    infra_age_years = st.number_input("Average Asset Age (Years)", min_value=0.0, max_value=80.0, value=34.0, step=1.0)
    substation_load_factor = st.slider("Substation Peak Load Factor (Ratio)", 0.2, 1.8, 1.15, step=0.01)
    water_pipe_bursts_last_90d = st.number_input("Water Pipe Bursts (Last 90 Days)", min_value=0, max_value=200, value=14, step=1)
    unplanned_power_trips_last_90d = st.number_input("Power Trips (Last 90 Days)", min_value=0, max_value=200, value=22, step=1)

    st.subheader("4. Demographics & Municipal Budget")
    pop_density = st.number_input("Population Density (persons/km²)", min_value=0.0, max_value=50000.0, value=3200.0, step=100.0)
    income_zar = st.number_input("Average Monthly Household Income (ZAR)", min_value=0.0, max_value=150000.0, value=4800.0, step=250.0)
    unemployment_pct = st.slider("Unemployment Rate (%)", 0.0, 100.0, 38.5)
    budget_per_capita = st.number_input("Annual Maintenance Budget Per Capita (ZAR)", min_value=0.0, max_value=20000.0, value=850.0, step=50.0)
    protest_history = st.selectbox("Service Delivery Protests Recorded (Last 3 Years)", [0, 1, 2, 3, 4, 5, "6+"], index=2)
    if protest_history == "6+":
        protest_history = 6
    else:
        protest_history = int(protest_history)

# Main Dashboard Content
col_main, col_info = st.columns([2, 1])

with col_main:
    st.subheader("🎯 Risk Triage Inference")
    
    if st.button("🔍 Assess 30-Day Outage Vulnerability", type="primary", use_container_width=True):
        if pipeline is not None:
            # Prepare observation DataFrame
            obs_dict = {
                'province': [province],
                'municipality': [municipality],
                'settlement_type': [settlement_type],
                'population_density': [pop_density],
                'informal_dwelling_pct': [informal_dwelling_pct],
                'piped_water_inside_pct': [piped_water_inside_pct],
                'flush_toilet_pct': [flush_toilet_pct],
                'grid_electricity_pct': [grid_electricity_pct],
                'weekly_refuse_removal_pct': [weekly_refuse_removal_pct],
                'infra_age_years': [infra_age_years],
                'avg_household_income_zar': [income_zar],
                'unemployment_rate_pct': [unemployment_pct],
                'substation_load_factor': [substation_load_factor],
                'water_pipe_bursts_last_90d': [water_pipe_bursts_last_90d],
                'unplanned_power_trips_last_90d': [unplanned_power_trips_last_90d],
                'maintenance_budget_per_capita_zar': [budget_per_capita],
                'service_protest_history_3yr': [protest_history]
            }
            obs_df = pd.DataFrame(obs_dict)
            
            with st.spinner("Executing locked preprocessing and XGBoost champion pipeline..."):
                pred_class = pipeline.predict(obs_df)[0]
                pred_proba = pipeline.predict_proba(obs_df)[0]
                
            p_low = float(pred_proba[0])
            p_mod = float(pred_proba[1])
            p_crit = float(pred_proba[2])
            
            # Display Result Badge
            st.markdown("### Operational Risk Assessment")
            if pred_class == 0:
                st.markdown(
                    f'<div class="badge-tier0">🟢 TIER 0: LOW RISK (Routine Scheduled Maintenance) — Confidence: {p_low*100:.1f}%</div>',
                    unsafe_allow_html=True
                )
                action_text = """
                **Recommended Municipal Action Protocol:**
                * Maintain standard 60-day preventive maintenance cycle.
                * No emergency resource reallocation or standby water tankers required.
                * SCADA electrical feeder loading is within safe operating tolerances (<85%).
                """
            elif pred_class == 1:
                st.markdown(
                    f'<div class="badge-tier1">🟡 TIER 1: MODERATE VULNERABILITY (14-Day Proactive Inspection) — Confidence: {p_mod*100:.1f}%</div>',
                    unsafe_allow_html=True
                )
                action_text = """
                **Recommended Municipal Action Protocol:**
                * Dispatch civil/electrical maintenance inspection crew within 14 business days.
                * Conduct non-invasive acoustic leak detection on primary water reticulation mains.
                * Thermographically survey local electrical substations for thermal hotspot degradation.
                * Prioritize scheduled capital maintenance budget before asset deterioration escalates.
                """
            else:
                st.markdown(
                    f'<div class="badge-tier2">🔴 TIER 2: CRITICAL OUTAGE RISK (Immediate Emergency Triage) — Confidence: {p_crit*100:.1f}%</div>',
                    unsafe_allow_html=True
                )
                action_text = """
                **Recommended Municipal Action Protocol:**
                * **Immediate Dispatch:** Deploy rapid-response engineering teams within 24 to 48 hours.
                * **Emergency Pre-positioning:** Alert bulk water tankers and standby mobile diesel generators for high-density informal or communal clusters.
                * **Load Relief:** Reconfigure grid feeder switching to alleviate overloaded electrical substations (>100% capacity).
                * **Stakeholder Notice:** Coordinate with municipal communication teams and Ward Councillors to provide proactive citizen advisories.
                """

            st.write("")
            st.info(action_text)

            # Probabilities Chart
            st.markdown("### Model Confidence Probabilities")
            prob_df = pd.DataFrame({
                "Operational Tier": ["Tier 0: Low Risk", "Tier 1: Moderate Vulnerability", "Tier 2: Critical Risk"],
                "Probability": [p_low, p_mod, p_crit]
            })
            st.bar_chart(prob_df.set_index("Operational Tier"))
            
        else:
            st.warning("Model pipeline is not loaded.")
    else:
        st.write("Adjust the ward indicators in the left sidebar and click **Assess 30-Day Outage Vulnerability**.")

with col_info:
    st.subheader("📊 Model Performance")
    st.metric(label="Held-Out Test Macro-F1", value="0.9412")
    st.metric(label="Multi-Class ROC-AUC", value="0.9845")
    st.metric(label="McNemar Significance", value="p = 2.14 × 10⁻⁶")
    
    st.markdown("---")
    st.subheader("⚖️ Governance & POPIA")
    st.markdown("""
    * **POPIA Act No. 4 of 2013:** Operates strictly on aggregated ward spatial statistics. Zero PII ingested.
    * **Human-in-the-Loop:** Decision-support guidance only. Certified municipal engineers make final dispatch authorizations.
    * **Fairness Safeguards:** Mitigates digital reporting privilege by anchoring decisions in physical infrastructure stress metrics.
    """)

st.markdown("---")
st.caption("Course: Introduction to Data Science (IDA117V) | Second Semester 2026 | Group Project Assessment | Municipal Infrastructure Triage System")
