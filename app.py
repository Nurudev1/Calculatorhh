import streamlit as st
import pandas as pd
import numpy as np
from calculator import calculate_lamp_metrics

# Set page title, layout, and theme
st.set_page_config(
    page_title="Lighting Efficiency & Cost Calculator",
    layout="wide", 
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "Lighting Efficiency & Cost Calculator © SustainabLED"
    }
)

# Force dark theme through custom CSS
st.markdown("""
<style>
    .stApp { background-color: #0E1117; color: #F0F2F6; }
    h1, h2, h3, h4, h5, h6, p, span, div, label { color: #F0F2F6 !important; }
    .stTextInput, .stNumberInput, .stSelectbox {
        background-color: #262730 !important; color: #F0F2F6 !important;
    }
    .stTabs [role="tab"] {
        background-color: #1E1E1E !important; color: #D4AF37 !important;
    }
    .stTabs [role="tab"][aria-selected="true"] {
        background-color: #2C2C2C !important; border-bottom: 2px solid #D4AF37 !important;
    }
    .streamlit-expanderHeader { background-color: #1E1E1E !important; color: #F0F2F6 !important; }
    .streamlit-expanderContent { background-color: #262730 !important; color: #F0F2F6 !important; }
</style>
""", unsafe_allow_html=True)

st.title("Lighting Efficiency & Cost Calculator")
st.markdown("Compare different lamp options for your lighting projects")
st.markdown("<hr style='height:3px;border:none;color:#D4AF37;background-color:#D4AF37;margin:15px 0px 20px 0px;'/>", unsafe_allow_html=True)

# SustainabLED Info
with st.expander("About SustainabLED", expanded=True):
    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown("### <span style='color:#D4AF37'>SustainabLED</span>", unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style='border-left:4px solid #D4AF37; padding-left:15px;'>
        SustainabLED offers high-efficiency lighting solutions that reduce energy costs and environmental impact.

        Our SHB 240 and SHB 160 models feature industry-leading efficacy ratings and are built for durability 
        and performance in demanding environments.

        This calculator allows you to compare our lighting solutions against alternatives to see the 
        cost savings over time.
        </div>
        """, unsafe_allow_html=True)

# Initialize lamp options
if 'lamp_options' not in st.session_state:
    st.session_state.lamp_options = [
        {'name': "SustainabLED SHB 240", 'make': "SustainabLED", 'model': "SHB 240", 'wattage': 240.0, 'efficacy': 204.0, 'capital_cost': 140.0},
        {'name': "SustainabLED SHB 160", 'make': "SustainabLED", 'model': "SHB 160", 'wattage': 160.0, 'efficacy': 198.0, 'capital_cost': 102.0},
        {'name': "Comparison Lamp 1", 'make': "", 'model': "", 'wattage': 0.0, 'efficacy': 0.0, 'capital_cost': 0.0},
        {'name': "Comparison Lamp 2", 'make': "", 'model': "", 'wattage': 0.0, 'efficacy': 0.0, 'capital_cost': 0.0}
    ]

# Site Requirements
st.markdown("### <span style='color:#D4AF37'>Site Requirements</span>", unsafe_allow_html=True)
st.markdown("<hr style='height:2px;border:none;color:#D4AF37;background-color:#D4AF37;margin:0px 0px 20px 0px;width:200px;'/>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    number_of_lamps = st.number_input("Number of Lamps", min_value=1, value=500)
    hours_per_day = st.number_input("Hours per Day", min_value=0.1, value=20.0)
with col2:
    required_lumens = st.number_input("Required Lumens per Lamp", min_value=1, value=30000)
    currency = st.selectbox("Currency", options=["$", "€"])
    energy_cost = st.number_input(f"Energy Cost ({currency}/kWh)", min_value=0.01, value=0.30)

# Lamp Tabs
st.markdown("### <span style='color:#D4AF37'>Lamp Options</span>", unsafe_allow_html=True)
st.markdown("<hr style='height:2px;border:none;color:#D4AF37;background-color:#D4AF37;margin:0px 0px 20px 0px;width:200px;'/>", unsafe_allow_html=True)
tabs = st.tabs(["SustainabLED SHB 240", "SustainabLED SHB 160", "Comparison Lamp 1", "Comparison Lamp 2"])

for i, tab in enumerate(tabs):
    with tab:
        lamp = st.session_state.lamp_options[i]
        if i < 2:
            st.markdown(f"### <span style='color:#D4AF37'>{lamp['name']}</span>", unsafe_allow_html=True)
            st.markdown(f"**Make:** {lamp['make']}")
            st.markdown(f"**Model:** {lamp['model']}")
            st.markdown("<div style='border-bottom:1px solid #D4AF37; margin:10px 0px 15px 0px;'></div>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            col1.markdown(f"**Wattage:** <span style='color:#D4AF37; font-weight:bold'>{lamp['wattage']} W</span>", unsafe_allow_html=True)
            col2.markdown(f"**Efficacy:** <span style='color:#D4AF37; font-weight:bold'>{lamp['efficacy']} lm/W</span>", unsafe_allow_html=True)
            col3.markdown(f"**Capital Cost:** <span style='color:#D4AF37; font-weight:bold'>{currency}{lamp['capital_cost']}</span>", unsafe_allow_html=True)
            st.markdown("<div style='background-color:#2C2C2C; border-left:3px solid #D4AF37; padding:10px; margin-top:15px;'>SustainabLED lamp specifications are fixed and cannot be modified.</div>", unsafe_allow_html=True)
        else:
            lamp['name'] = st.text_input("Lamp Name", value=lamp['name'], key=f"name_{i}")
            lamp['make'] = st.text_input("Make", value=lamp['make'], key=f"make_{i}")
            lamp['model'] = st.text_input("Model", value=lamp['model'], key=f"model_{i}")
            col1, col2, col3 = st.columns(3)
            lamp['wattage'] = col1.number_input("Wattage (W)", min_value=0.0, value=lamp['wattage'] if lamp['wattage'] > 0 else 100.0, key=f"wattage_{i}")
            lamp['efficacy'] = col2.number_input("Efficacy (lm/W)", min_value=0.0, value=lamp['efficacy'] if lamp['efficacy'] > 0 else 100.0, key=f"efficacy_{i}")
            lamp['capital_cost'] = col3.number_input(f"Capital Cost ({currency})", min_value=0.0, value=lamp['capital_cost'] if lamp['capital_cost'] > 0 else 50.0, key=f"capital_cost_{i}")

# Calculate Button
st.markdown("""
<style>
    div.stButton > button:first-child {
        background-color: #D4AF37;
        color: #0E1117;
        font-weight: bold;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
    }
    div.stButton > button:hover {
        background-color: #B8860B; color: white;
    }
</style>
""", unsafe_allow_html=True)

if st.button("⚡ Calculate and Compare ⚡", type="primary"):
    site = {
        'number_of_lamps': number_of_lamps,
        'hours_per_day': hours_per_day,
        'required_lumens': required_lumens,
        'energy_cost': energy_cost,
        'currency': currency
    }

    results = []
    for lamp in st.session_state.lamp_options:
        if lamp['wattage'] > 0 and lamp['efficacy'] > 0:
            results.append(calculate_lamp_metrics(lamp, site))

    if results:
        results_df = pd.DataFrame(results)

        # Round values for display
        def safe_round(df, cols, decimals):
            for col in cols:
                if col in df.columns:
                    df[col] = df[col].round(decimals)
            return df

        results_df = safe_round(results_df, [
            'light_output_per_lamp', 'total_light_output',
            'cost_per_1000lm_hour', 'cost_per_req_lumens',
            'energy_cost_per_day', 'energy_cost_per_year', 'energy_cost_5years'
        ], 2)

        # Suitability Check
        st.markdown("#### <span style='color:#D4AF37'>Suitability Check</span>", unsafe_allow_html=True)
        suitability_df = results_df[['name', 'make', 'model', 'light_output_per_lamp', 'total_light_output', 'suitability']]
        suitability_df.columns = ['Lamp Name', 'Make', 'Model', 'Light Output per Lamp (lm)', 'Total Light Output (lm)', 'Suitability']

        def color_suitability(val):
            return 'background-color: #005700; color: #FFFFFF; font-weight: bold' if val == "OKAY" else 'background-color: #8B0000; color: #FFFFFF; font-weight: bold'

        st.dataframe(suitability_df.style.applymap(color_suitability, subset=['Suitability']))

        # Cost Efficiency
        st.markdown("#### <span style='color:#D4AF37'>Cost Efficiency</span>", unsafe_allow_html=True)
        efficiency_df = results_df[['name', 'cost_per_1000lm_hour', 'cost_per_req_lumens']]
        efficiency_df.columns = ['Lamp Name', f'Cost per 1000 lm/hour ({currency})', f'Cost per Required Lumens ({currency})']
        st.dataframe(efficiency_df)

        # Energy Costs
        st.markdown("#### <span style='color:#D4AF37'>Energy Costs</span>", unsafe_allow_html=True)
        energy_df = results_df[['name', 'energy_cost_per_day', 'energy_cost_per_year', 'energy_cost_5years']]
        energy_df.columns = [
            'Lamp Name', 
            f'Energy Cost per Day ({currency})', 
            f'Energy Cost per Year ({currency})', 
            f'Energy Cost over 5 Years ({currency})'
        ]
        st.dataframe(energy_df)
