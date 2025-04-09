import streamlit as st
import pandas as pd

st.set_page_config(page_title="Lamp Comparison Tool", layout="wide")

st.markdown("<h1 style='text-align: center; color: #D4AF37;'>💡 Lamp Comparison Tool</h1>", unsafe_allow_html=True)
st.markdown("### Enter Site Requirements:")

# User Input
number_of_lamps = st.number_input("Number of Lamps", min_value=1, value=10)
hours_per_day = st.number_input("Operating Hours per Day", min_value=1, max_value=24, value=8)
required_lumens = st.number_input("Required Total Lumens", min_value=100, value=10000)
energy_cost = st.number_input("Energy Cost (per kWh)", min_value=0.01, value=0.15)
currency = st.selectbox("Currency", ["$", "€", "£", "₦", "₹"])

st.markdown("### Add Lamp Options:")

# Session state for storing multiple lamp options
if "lamp_options" not in st.session_state:
    st.session_state.lamp_options = []

with st.form("lamp_form", clear_on_submit=True):
    name = st.text_input("Lamp Name")
    make = st.text_input("Make")
    model = st.text_input("Model")
    wattage = st.number_input("Wattage (W)", min_value=1.0)
    efficacy = st.number_input("Efficacy (lm/W)", min_value=1.0)
    capital_cost = st.number_input("Capital Cost per Lamp", min_value=0.0)

    submitted = st.form_submit_button("Add Lamp Option")

    if submitted:
        st.session_state.lamp_options.append({
            "name": name,
            "make": make,
            "model": model,
            "wattage": wattage,
            "efficacy": efficacy,
            "capital_cost": capital_cost
        })

# Show current lamps
if st.session_state.lamp_options:
    st.markdown("#### Current Lamp Options")
    st.table(pd.DataFrame(st.session_state.lamp_options))

# Calculation Logic
def calculate_lamp_metrics(lamp, site):
    light_output_per_lamp = lamp['efficacy'] * lamp['wattage']
    total_light_output = light_output_per_lamp * site['number_of_lamps']
    suitability = "OKAY" if total_light_output >= site['required_lumens'] else "NOT OKAY"

    total_power_kw = (lamp['wattage'] * site['number_of_lamps']) / 1000
    energy_per_day = total_power_kw * site['hours_per_day']
    cost_per_day = energy_per_day * site['energy_cost']
    cost_per_year = cost_per_day * 365
    cost_per_5years = cost_per_year * 5

    cost_per_1000lm_hour = (site['energy_cost'] * lamp['wattage']) / (lamp['efficacy'] / 1000)
    cost_per_req_lumens = (site['energy_cost'] * lamp['wattage'] * site['hours_per_day']) / site['required_lumens']

    return {
        **lamp,
        'light_output_per_lamp': light_output_per_lamp,
        'total_light_output': total_light_output,
        'suitability': suitability,
        'cost_per_1000lm_hour': cost_per_1000lm_hour,
        'cost_per_req_lumens': cost_per_req_lumens,
        'energy_cost_per_day': cost_per_day,
        'energy_cost_per_year': cost_per_year,
        'energy_cost_5years': cost_per_5years
    }

# Main calculation and output
if st.button("⚡ Calculate and Compare ⚡"):
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

        # Round numerical values
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

        # Suitability Table
        st.markdown("#### <span style='color:#D4AF37'>Suitability Check</span>", unsafe_allow_html=True)
        suitability_df = results_df[['name', 'make', 'model', 'light_output_per_lamp', 'total_light_output', 'suitability']]
        suitability_df.columns = ['Lamp Name', 'Make', 'Model', 'Light Output per Lamp (lm)', 'Total Light Output (lm)', 'Suitability']

        def color_suitability(val):
            return 'background-color: #005700; color: white; font-weight: bold' if val == "OKAY" else 'background-color: #8B0000; color: white; font-weight: bold'

        st.dataframe(suitability_df.style.applymap(color_suitability, subset=['Suitability']))

        # Cost Efficiency Table
        st.markdown("#### <span style='color:#D4AF37'>Cost Efficiency</span>", unsafe_allow_html=True)
        efficiency_df = results_df[['name', 'cost_per_1000lm_hour', 'cost_per_req_lumens']]
        efficiency_df.columns = ['Lamp Name', f'Cost per 1000 lm/hour ({currency})', f'Cost per Required Lumens ({currency})']
        st.dataframe(efficiency_df)

        # Energy Costs Table
        st.markdown("#### <span style='color:#D4AF37'>Energy Costs</span>", unsafe_allow_html=True)
        energy_df = results_df[['name', 'energy_cost_per_day', 'energy_cost_per_year', 'energy_cost_5years']]
        energy_df.columns = [
            'Lamp Name',
            f'Energy Cost per Day ({currency})',
            f'Energy Cost per Year ({currency})',
            f'Energy Cost over 5 Years ({currency})'
        ]
        st.dataframe(energy_df)

        # Consolidated Table
        st.markdown("#### <span style='color:#D4AF37'>🔍 Full Comparison Overview</span>", unsafe_allow_html=True)
        final_df = results_df[[
            'name', 'make', 'model',
            'wattage', 'efficacy', 'capital_cost',
            'light_output_per_lamp', 'total_light_output', 'suitability',
            'cost_per_1000lm_hour', 'cost_per_req_lumens',
            'energy_cost_per_day', 'energy_cost_per_year', 'energy_cost_5years'
        ]]
        final_df.columns = [
            'Lamp Name', 'Make', 'Model',
            'Wattage (W)', 'Efficacy (lm/W)', f'Capital Cost ({currency})',
            'Light Output per Lamp (lm)', 'Total Light Output (lm)', 'Suitability',
            f'Cost per 1000 lm/hr ({currency})', f'Cost per Required Lumens ({currency})',
            f'Energy per Day ({currency})', f'Energy per Year ({currency})', f'Energy in 5 Years ({currency})'
        ]
        st.dataframe(final_df)
