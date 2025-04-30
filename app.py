import streamlit as st
import pandas as pd
import numpy as np
from calculator import calculate_lamp_metrics

# Function to format to 2 decimal places
def format_decimal(value, decimals=2, comma=False):
    try:
        formatted = f"{value:,.{decimals}f}" if comma else f"{value:.{decimals}f}"
        if decimals == 0:
            formatted = formatted.replace('.00', '')
        return formatted
    except:
        return value

# Set page title and layout
st.set_page_config(
    page_title="Lighting Efficiency & Cost Calculator",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom dark theme styling
st.markdown("""
<style>
    .stApp { background-color: #0E1117; color: #F0F2F6; }
    h1, h2, h3, h4, h5, h6, p, span, div, label { color: #F0F2F6 !important; }
    .stTextInput, .stNumberInput, .stSelectbox {
        background-color: #262730 !important;
        color: #F0F2F6 !important;
    }
</style>
""", unsafe_allow_html=True)

# New permanent preface text
st.title("YOUR LIGHTING PROJECT – SustainabLED Cost Comparator")

st.markdown("""
“Too good to be true” – with SustainabLED it is Too Good AND it’s absolutely True!

**OUR Mission** – We set out with one goal – To make the best high bay lamps in the world at prices that are unbeatable in Price, Performance, Reliability and Project Targeted.

- **Heavyweight** – literally - they have the aluminium mass to keep them running cool forever.
- **End of Life** – None – exchange the part for new – simply renew the lamp at fraction of cost.
- **Light Efficiency** – over 200 Lm/W – less than half the energy cost of many others.
- **8 Years Warranty** – Premium Components, 3Kg heatsink, certified drivers and more.
- **SustainabLED** – no end of life, renewable in seconds with zero skills with exchange part.
- **Certified** – by German reference laboratory TUV Rheinland.

**Price** – HOW DO WE DO IT? We sell directly to you from the factory!

---
""")

# Step 1: Site Requirements
st.header("STEP 1: Enter Your Site Requirements")
col1, col2 = st.columns(2)
with col1:
    number_of_lamps = st.number_input("Number of Lamps", min_value=1, value=None)
    hours_per_day = st.number_input("Hours per Day", min_value=0.1, value=None)
with col2:
    required_lumens = st.number_input("Required Lumens per Lamp", min_value=1, value=None)
    energy_cost = st.number_input("Energy Cost (per kWh)", min_value=0.01, value=None)

# Step 2: Lamp Options
st.header("STEP 2: Enter Comparison Lamp Details")
st.markdown("Enter just 3 pieces of information about the lamps you wish to compare. You can also add Make and Model for your reference.")

if 'lamp_options' not in st.session_state:
    st.session_state.lamp_options = [
        {'make': "SustainabLED", 'model': "SHB 240", 'wattage': 240.0, 'efficacy': 204.0, 'capital_cost': 140.0},
        {'make': "SustainabLED", 'model': "SHB 160", 'wattage': 160.0, 'efficacy': 198.0, 'capital_cost': 102.0},
        {'make': "", 'model': "", 'wattage': 0.0, 'efficacy': 0.0, 'capital_cost': 0.0},
        {'make': "", 'model': "", 'wattage': 0.0, 'efficacy': 0.0, 'capital_cost': 0.0}
    ]

for i in range(4):
    st.subheader(f"Lamp {i+1} ({'SustainabLED' if i < 2 else 'Comparison'})")
    with st.container():
        st.session_state.lamp_options[i]['make'] = st.text_input("Make", value=st.session_state.lamp_options[i]['make'], key=f"make_{i}")
        st.session_state.lamp_options[i]['model'] = st.text_input("Model", value=st.session_state.lamp_options[i]['model'], key=f"model_{i}")
        if i >= 2:
            st.session_state.lamp_options[i]['wattage'] = st.number_input("Wattage (W)", min_value=0.0, value=st.session_state.lamp_options[i]['wattage'], key=f"wattage_{i}")
            st.session_state.lamp_options[i]['efficacy'] = st.number_input("Efficacy (lm/W)", min_value=0.0, value=st.session_state.lamp_options[i]['efficacy'], key=f"efficacy_{i}")
            st.session_state.lamp_options[i]['capital_cost'] = st.number_input("Capital Cost", min_value=0.0, value=st.session_state.lamp_options[i]['capital_cost'], key=f"capital_{i}")

# Step 3: Results
st.header("STEP 3: Calculate the Capital + Energy Costs over a 5 year period")
if st.button("⚡ Calculate and Compare ⚡"):
    if None in [number_of_lamps, hours_per_day, required_lumens, energy_cost]:
        st.error("Please fill in all fields")
    else:
        site = {'number_of_lamps': number_of_lamps, 'hours_per_day': hours_per_day, 'required_lumens': required_lumens, 'energy_cost': energy_cost}
        results = [calculate_lamp_metrics(lamp, site) for lamp in st.session_state.lamp_options if lamp['wattage'] and lamp['efficacy']]

        df = pd.DataFrame(results)

        st.subheader("Suitability Check – A simple cross-check of required lumens against delivered lumens output of each lamp model")
        suit_cols = ['name', 'make', 'model', 'light_output_per_lamp', 'suitability']
        suit_df = df[suit_cols]
        st.dataframe(suit_df)

        st.subheader("Cost Efficiency")
        cost_cols = ['name', 'cost_per_1000lm_hour', 'cost_per_req_lumens']
        cost_df = df[cost_cols].copy()
        cost_df['cost_per_1000lm_hour'] = cost_df['cost_per_1000lm_hour'].apply(lambda x: format_decimal(x, 4))
        st.dataframe(cost_df)

        st.subheader("Total Costs")
        total_cols = ['name', 'total_capital_cost', 'total_5year_cost']
        total_df = df[total_cols].copy()
        total_df['total_capital_cost'] = total_df['total_capital_cost'].apply(lambda x: format_decimal(x, 0, True))
        total_df['total_5year_cost'] = total_df['total_5year_cost'].apply(lambda x: format_decimal(x, 0, True))
        total_df.rename(columns={'total_5year_cost': '5 Year Costs – Capital Cost + Energy Running Costs'}, inplace=True)
        st.dataframe(total_df)

        st.success("Comparison Complete. See recommendation and details above.")
