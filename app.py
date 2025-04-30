import streamlit as st
import pandas as pd
import numpy as np
from calculator import calculate_lamp_metrics

# Function to format to 2 decimal places
def format_decimal(value):
    if isinstance(value, (int, float)):
        return f"{value:.2f}"
    return value

# Set page title, layout, and theme (forcing dark mode)
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

# Title and description
st.title("Lighting Efficiency & Cost Calculator")
st.markdown("Compare different lamp options for your lighting projects")

# Gold title divider
st.markdown("<hr style='height:3px;border:none;color:#D4AF37;background-color:#D4AF37;margin:15px 0px 20px 0px;'/>", unsafe_allow_html=True)

# Preface (permanent)
st.markdown("### <span style='color:#D4AF37'>YOUR LIGHTING PROJECT – SustainabLED Cost Comparator</span>", unsafe_allow_html=True)
st.markdown("""
<div style='border-left:4px solid #D4AF37; padding-left:15px;'>
“Too good to be true” – with SustainabLED it is Too Good AND it’s absolutely True!

OUR Mission – We set out with one goal – To make the best high bay lamps in the world at prices that are unbeatable in Price, Performance, Reliability and Project Targeted.

Heavyweight – literally - they have the aluminium mass to keep them running cool forever.
End of Life – None – exchange the part for new – simply renew the lamp at fraction of cost.
Light Efficiency – at over 200 Lm/W – the energy running costs is less than half of many others and MUCH less than most. You will find this out when you use the calculator below.
8 Years Warranty – Premium Components, 3Kg heatsink, Moso/Sosen/Lifud driver and 3 times the amount of LEDs required to make the LED array run at 1/3 rated power. L90B10 – what’s this you ask – it’s certification to prove long life – ours is rated at 44,000 hours.
SustainabLED – no end of life, renewable in seconds with zero skills with exchange part.
Certified – by German reference laboratory TUV Rheinland.

Price – HOW DO WE DO IT! We sell directly to you from the factory!
</div>
""", unsafe_allow_html=True)

# Initialize session state for lamp options
if 'lamp_options' not in st.session_state:
    st.session_state.lamp_options = [
        {
            'name': "SustainabLED SHB 240",
            'make': "SustainabLED",
            'model': "SHB 240",
            'wattage': 240.0,
            'efficacy': 204.0,
            'capital_cost': 140.0
        },
        {
            'name': "SustainabLED SHB 160",
            'make': "SustainabLED",
            'model': "SHB 160",
            'wattage': 160.0,
            'efficacy': 198.0,
            'capital_cost': 102.0
        },
        {
            'name': "Comparison Lamp 1",
            'make': "",
            'model': "",
            'wattage': 0.0,
            'efficacy': 0.0,
            'capital_cost': 0.0
        },
        {
            'name': "Comparison Lamp 2",
            'make': "",
            'model': "",
            'wattage': 0.0,
            'efficacy': 0.0,
            'capital_cost': 0.0
        }
    ]

# Step 1: Site Requirements
st.markdown("""
<div class="step-container">
    <div class="step-number">STEP 1: Enter Your Site Requirements</div>
    <div class="step-content">
        Fill in the details about your project requirements below. These will be used to calculate costs and determine suitability.
    </div>
</div>
""", unsafe_allow_html=True)
st.markdown("### <span style='color:#D4AF37'>Site Requirements</span>", unsafe_allow_html=True)
st.markdown("<hr style='height:2px;border:none;color:#D4AF37;background-color:#D4AF37;margin:0px 0px 20px 0px;width:200px;'/>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    number_of_lamps = st.number_input("Number of Lamps", min_value=1, value=1, help="Total number of lamps needed for the project")
    hours_per_day = st.number_input("Hours per Day", min_value=0.0, value=0.0, help="Hours of operation per day")
with col2:
    required_lumens = st.number_input("Required Lumens per Lamp", min_value=0.0, value=0.0, help="Lumens required from each lamp")
    currency = "€"
    energy_cost = st.number_input(f"Energy Cost ({currency}/kWh)", min_value=0.0, value=0.0, help="Cost of energy per kilowatt-hour")

# Step 2: Enter Lamp Options
st.markdown("""
<div class="step-container">
    <div class="step-number">STEP 2: Enter Comparison Lamp Details</div>
    <div class="step-content">
        Enter just 3 pieces of information about the lamps you wish to compare - Make, Model, Wattage, Efficacy, and Capital Cost. You can enter 2 lamps (Comparison Lamp 1 and Comparison Lamp 2) at one time to compare with our SustainabLED lamps that are already data embedded.
    </div>
</div>
""", unsafe_allow_html=True)
st.markdown("### <span style='color:#D4AF37'>Lamp Options</span>", unsafe_allow_html=True)
st.markdown("<hr style='height:2px;border:none;color:#D4AF37;background-color:#D4AF37;margin:0px 0px 20px 0px;width:200px;'/>", unsafe_allow_html=True)
tabs = st.tabs(["SustainabLED SHB 240", "SustainabLED SHB 160", "Comparison Lamp 1", "Comparison Lamp 2"])
for i, tab in enumerate(tabs):
    with tab:
        if i < 2:
            st.markdown(f"### <span style='color:#D4AF37'>{st.session_state.lamp_options[i]['name']}</span>", unsafe_allow_html=True)
            st.markdown(f"**Make:** {st.session_state.lamp_options[i]['make']}")
            st.markdown(f"**Model:** {st.session_state.lamp_options[i]['model']}")
            st.markdown("<div style='border-bottom:1px solid #D4AF37; margin:10px 0px 15px 0px;'></div>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"**Wattage:** <span style='color:#D4AF37'>{format_decimal(st.session_state.lamp_options[i]['wattage'])} W</span>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"**Efficacy:** <span style='color:#D4AF37'>{format_decimal(st.session_state.lamp_options[i]['efficacy'])} lm/W</span>", unsafe_allow_html=True)
            with col3:
                st.markdown(f"**Capital Cost:** <span style='color:#D4AF37'>{format_decimal(st.session_state.lamp_options[i]['capital_cost'])}</span>", unsafe_allow_html=True)
            st.markdown("<div style='background-color:#2C2C2C; border-left:3px solid #D4AF37; padding:10px;'>Note: these fields are fixed and cannot be modified.</div>", unsafe_allow_html=True)
        else:
            st.session_state.lamp_options[i]['make'] = st.text_input("Make", value=st.session_state.lamp_options[i]['make'], key=f"make_{i}")
            st.session_state.lamp_options[i]['model'] = st.text_input("Model", value=st.session_state.lamp_options[i]['model'], key=f"model_{i}")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.session_state.lamp_options[i]['wattage'] = st.number_input("Wattage (W)", min_value=0.0, value=st.session_state.lamp_options[i]['wattage'], key=f"wattage_{i}")
            with col2:
                st.session_state.lamp_options[i]['efficacy'] = st.number_input("Efficacy (lm/W)", min_value=0.0, value=st.session_state.lamp_options[i]['efficacy'], key=f"efficacy_{i}")
            with col3:
                st.session_state.lamp_options[i]['capital_cost'] = st.number_input(f"Capital Cost ({currency})", min_value=0.0, value=st.session_state.lamp_options[i]['capital_cost'], key=f"capital_cost_{i}")

# Step 3: Calculate and View Results
st.markdown("""
<div class="step-container">
    <div class="step-number">STEP 3: Calculate the Capital + Energy Costs over a 5 year period</div>
    <div class="step-content">
        WE ARE CONFIDENT our products will offer best prices for lamps that are of much greater quality and performance. Compare Price, Running costs, Warranty Period, Steady State Run temperature (our lamps run super cool at just 50°C).
        <br><br>
        Failures are expensive to get up to. Protect your reputation. Buy Quality - SustainabLED.
        <br><br>
        Now you have all the information to Make an Informed and Better Decision.
        <br><br>
        NOTE – Prices are for 1-50 pieces – If you are interested in becoming a Value Added Reseller please write to us at Partners@SustainabLED.io  Home of the World’s Best High Bay Lamps
    </div>
</div>
""", unsafe_allow_html=True)
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
        background-color: #B8860B;
    }
</style>
""", unsafe_allow_html=True)
if st.button("Calculate"):
    site_requirements = {
        'number_of_lamps': number_of_lamps,
        'hours_per_day': hours_per_day,
        'required_lumens': required_lumens,
        'energy_cost': energy_cost,
        'currency': currency
    }
    results = []
    for lamp in st.session_state.lamp_options:
        if lamp['wattage'] and lamp['efficacy']:
            result = calculate_lamp_metrics(lamp, site_requirements)
            results.append(result)

    if results:
        st.markdown("### <span style='color:#D4AF37'>Comparison Results</span>", unsafe_allow_html=True)
        st.markdown("<hr style='height:2px;border:none;color:#D4AF37;background-color:#D4AF37;margin:0px 0px 20px 0px;width:300px;'/>", unsafe_allow_html=True)
        results_df = pd.DataFrame(results)
        numeric_cols = results_df.select_dtypes(include=np.number).columns
        results_df[numeric_cols] = results_df[numeric_cols].applymap(format_decimal)

        # Suitability Check
        st.markdown("#### <span style='color:#D4AF37'>Suitability Check – A simple cross-check of required lumens vs delivered lumens output of each lamp model</span>", unsafe_allow_html=True)
        suitability_df = results_df[['name', 'make', 'model', 'light_output_per_lamp', 'suitability']].copy()
        suitability_df.columns = ['Lamp Name', 'Make', 'Model', 'Light Output per Lamp (lm)', 'Suitability']
        def color_suitability(val):
            return 'background-color: #006400; color: #FFFFFF; font-weight: bold' if val == 'OKAY' else 'background-color: #8B0000; color: #FFFFFF; font-weight: bold'
        st.dataframe(suitability_df.style.applymap(color_suitability, subset=['Suitability']))

        # Cost Efficiency
        st.markdown("#### <span style='color:#D4AF37'>Cost Efficiency</span>", unsafe_allow_html=True)
        efficiency_df = results_df[['name', 'cost_per_1000lm_hour', 'cost_per_req_lumens']].copy()
        efficiency_df.columns = ['Lamp Name', f'Cost per 1000 lm/hour ({currency})', f'Cost per Required Lumens ({currency})']
        efficiency_df[f'Cost per 1000 lm/hour ({currency})'] = efficiency_df[f'Cost per 1000 lm/hour ({currency})'].apply(lambda x: f"{float(x):.4f}")
        efficiency_df[f'Cost per Required Lumens ({currency})'] = efficiency_df[f'Cost per Required Lumens ({currency})'].apply(lambda x: f"{float(x):.4f}")
        
        st.dataframe(efficiency_df)

        # Energy Costs
        st.markdown("#### <span style='color:#D4AF37'>Energy Costs</span>", unsafe_allow_html=True)
        energy_df = results_df[['name', 'energy_cost_per_day', 'energy_cost_per_year', 'energy_cost_5years']].copy()
        energy_df.columns = [
            'Lamp Name',
            f'Energy Cost per Day ({currency})',
            f'Energy Cost per Year ({currency})',
            f'Energy Cost 5 Years ({currency})'
        ]
        st.dataframe(energy_df)

        # Total Costs
        st.markdown("#### <span style='color:#D4AF37'>Total Costs</span>", unsafe_allow_html=True)
        total_df = results_df[['name', 'total_capital_cost', 'total_5year_cost']].copy()
        total_df.columns = ['Lamp Name', f'Total Capital Cost ({currency})', f'Total 5-Year Cost ({currency})']
        total_df[f'Total Capital Cost ({currency})'] = total_df[f'Total Capital Cost ({currency})'].apply(lambda x: f"{int(float(x)):,.0f}")
        total_df[f'Total 5-Year Cost ({currency})'] = total_df[f'Total 5-Year Cost ({currency})'].apply(lambda x: f"{int(float(x)):,.0f}")
        st.dataframe(total_df)

        # Recommendation
        st.markdown(f"""
        <div style='background-color:#2C2C2C; border-left:3px solid #00FF00; padding:15px; margin-top:15px;'>
            <h4 style='color:#D4AF37;'>Recommendation</h4>
            <p>Based on your requirements, <strong>{results_df.loc[results_df['total_5year_cost'].astype(float).idxmin(), 'name']}</strong> offers the best value and potential savings shown above compared to your alternatives.</p>
        </div>
        """, unsafe_allow_html=True)
        

# Footer with gold styling
st.markdown("<hr style='height:2px;border:none;color:#D4AF37;background-color:#D4AF37;margin-top:30px;'/>", unsafe_allow_html=True)
st.markdown("<div style='display:flex;justify-content:center;margin-top:20px;'><h3 style='color:#D4AF37;'>Lighting Efficiency & Cost Calculator © SustainabLED</h3></div>", unsafe_allow_html=True)
st.markdown("<div style='display:flex;justify-content:center;'><em>Compare your lighting options to find the most efficient and cost-effective solution</em></div>", unsafe_allow_html=True)
