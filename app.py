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

# Force dark theme through custom CSS
st.markdown("""
<style>
    /* Force the theme to dark */
    .stApp {
        background-color: #0E1117;
        color: #F0F2F6;
    }
    /* Headers and text */
    h1, h2, h3, h4, h5, h6, p, span, div, label {
        color: #F0F2F6 !important;
    }
    /* Input fields */
    .stTextInput, .stNumberInput, .stSelectbox {
        background-color: #262730 !important;
        color: #F0F2F6 !important;
    }
    /* Tabs styling */
    .stTabs [role="tab"] {
        background-color: #1E1E1E !important;
        color: #D4AF37 !important;
    }
    .stTabs [role="tab"][aria-selected="true"] {
        background-color: #2C2C2C !important;
        border-bottom: 2px solid #D4AF37 !important;
    }
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #1E1E1E !important;
        color: #F0F2F6 !important;
    }
    .streamlit-expanderContent {
        background-color: #262730 !important;
        color: #F0F2F6 !important;
    }
</style>
""", unsafe_allow_html=True)
st.title("Lighting Efficiency & Cost Calculator")
st.markdown("Compare different lamp options for your lighting projects")

# Gold title divider
st.markdown("<hr style='height:3px;border:none;color:#D4AF37;background-color:#D4AF37;margin:15px 0px 20px 0px;'/>", unsafe_allow_html=True)

# SustainabLED info section
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

# Initialize session state for lamp options
if 'lamp_options' not in st.session_state:
    # Pre-configure the first two lamps as SustainabLED options
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

# Site Requirements
st.markdown("### <span style='color:#D4AF37'>Site Requirements</span>", unsafe_allow_html=True)
st.markdown("<hr style='height:2px;border:none;color:#D4AF37;background-color:#D4AF37;margin:0px 0px 20px 0px;width:200px;'/>", unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    number_of_lamps = st.number_input("Number of Lamps", min_value=1, value=500, help="Total number of lamps needed for the project")
    hours_per_day = st.number_input("Hours per Day", min_value=0.1, value=20.0, help="Hours of operation per day")

with col2:
    required_lumens = st.number_input("Required Lumens per Lamp", min_value=1, value=30000, help="Lumens required from each lamp")
    currency = st.selectbox("Currency", options=["$", "€"], index=0)
    energy_cost = st.number_input(f"Energy Cost ({currency}/kWh)", min_value=0.01, value=0.30, help="Cost of energy per kilowatt-hour")

# Lamp Options
st.markdown("### <span style='color:#D4AF37'>Lamp Options</span>", unsafe_allow_html=True)
st.markdown("<hr style='height:2px;border:none;color:#D4AF37;background-color:#D4AF37;margin:0px 0px 20px 0px;width:200px;'/>", unsafe_allow_html=True)

# Create 4 tabs with appropriate names
tab1, tab2, tab3, tab4 = st.tabs([
    "SustainabLED SHB 240",
    "SustainabLED SHB 160",
    "Comparison Lamp 1",
    "Comparison Lamp 2"
])

tabs = [tab1, tab2, tab3, tab4]

# Update session state when inputs change
for i, tab in enumerate(tabs):
    with tab:
        # Different handling for SustainabLED lamps (first two tabs) vs comparison lamps
        if i < 2:  # SustainabLED lamps - read-only display
            st.markdown(f"### <span style='color:#D4AF37'>{st.session_state.lamp_options[i]['name']}</span>", unsafe_allow_html=True)
            st.markdown(f"**Make:** {st.session_state.lamp_options[i]['make']}")
            st.markdown(f"**Model:** {st.session_state.lamp_options[i]['model']}")

            # Gold divider for SustainabLED lamps
            st.markdown("<div style='border-bottom:1px solid #D4AF37; margin:10px 0px 15px 0px;'></div>", unsafe_allow_html=True)

            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"**Wattage:** <span style='color:#D4AF37; font-weight:bold'>{format_decimal(st.session_state.lamp_options[i]['wattage'])} W</span>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"**Efficacy:** <span style='color:#D4AF37; font-weight:bold'>{format_decimal(st.session_state.lamp_options[i]['efficacy'])} lm/W</span>", unsafe_allow_html=True)
            with col3:
                st.markdown(f"**Capital Cost:** <span style='color:#D4AF37; font-weight:bold'>{currency}{format_decimal(st.session_state.lamp_options[i]['capital_cost'])}</span>", unsafe_allow_html=True)

            st.markdown("<div style='background-color:#2C2C2C; border-left:3px solid #D4AF37; padding:10px; margin-top:15px;'>SustainabLED lamp specifications are fixed and cannot be modified.</div>", unsafe_allow_html=True)
        else:  # Comparison lamps - editable fields
            st.session_state.lamp_options[i]['name'] = st.text_input("Lamp Name", value=st.session_state.lamp_options[i]['name'], key=f"name_{i}")
            st.session_state.lamp_options[i]['make'] = st.text_input("Make", value=st.session_state.lamp_options[i]['make'], key=f"make_{i}")
            st.session_state.lamp_options[i]['model'] = st.text_input("Model", value=st.session_state.lamp_options[i]['model'], key=f"model_{i}")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.session_state.lamp_options[i]['wattage'] = st.number_input(
                    "Wattage (W)",
                    min_value=0.0,
                    value=st.session_state.lamp_options[i]['wattage'] if st.session_state.lamp_options[i]['wattage'] > 0 else 100.0,
                    key=f"wattage_{i}"
                )
            with col2:
                st.session_state.lamp_options[i]['efficacy'] = st.number_input(
                    "Efficacy (lm/W)",
                    min_value=0.0,
                    value=st.session_state.lamp_options[i]['efficacy'] if st.session_state.lamp_options[i]['efficacy'] > 0 else 100.0,
                    key=f"efficacy_{i}"
                )
            with col3:
                st.session_state.lamp_options[i]['capital_cost'] = st.number_input(
                    f"Capital Cost ({currency})",
                    min_value=0.0,
                    value=st.session_state.lamp_options[i]['capital_cost'] if st.session_state.lamp_options[i]['capital_cost'] > 0 else 50.0,
                    key=f"capital_cost_{i}"
                )

# Calculate Button with gold styling
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
        color: white;
    }
    /* Add custom styling for dataframes to enhance visibility on dark theme */
    .dataframe {
        color: #F0F2F6 !important;
        background-color: #1E1E1E !important;
    }
    .dataframe th {
        background-color: #2C2C2C !important;
        color: #D4AF37 !important;
    }
    /* Style for expander content */
    .streamlit-expander {
        border-color: #2C2C2C !important;
        background-color: #1E1E1E !important;
    }
</style>
""", unsafe_allow_html=True)

if st.button("⚡ Calculate and Compare ⚡", type="primary"):

    site_requirements = {
        'number_of_lamps': number_of_lamps,
        'hours_per_day': hours_per_day,
        'required_lumens': required_lumens,
        'energy_cost': energy_cost,
        'currency': currency
    }

    # Calculate metrics for each lamp option
    results = []
    for lamp in st.session_state.lamp_options:
        if lamp['wattage'] > 0 and lamp['efficacy'] > 0:  # Only calculate for lamps with valid data
            result = calculate_lamp_metrics(lamp, site_requirements)
            results.append(result)

    if results:
        # Display results
        st.markdown("### <span style='color:#D4AF37'>Comparison Results</span>", unsafe_allow_html=True)
        st.markdown("<hr style='height:2px;border:none;color:#D4AF37;background-color:#D4AF37;margin:0px 0px 20px 0px;width:300px;'/>", unsafe_allow_html=True)

        # Convert results to DataFrame for easier display
        results_df = pd.DataFrame(results)

        # Format all numeric columns to 2 decimal places
        numeric_cols = results_df.select_dtypes(include=np.number).columns
        results_df[numeric_cols] = results_df[numeric_cols].applymap(format_decimal)

        # Suitability Check
        st.markdown("#### <span style='color:#D4AF37'>Suitability Check</span>", unsafe_allow_html=True)
        suitability_df = results_df[['name', 'make', 'model', 'light_output_per_lamp', 'total_light_output', 'suitability']].copy()
        suitability_df.columns = ['Lamp Name', 'Make', 'Model', 'Light Output per Lamp (lm)', 'Total Light Output (lm)', 'Suitability']

        # Style the suitability column
        def color_suitability(val):
            if val == "OKAY":
                return 'background-color: #005700; color: #FFFFFF; font-weight: bold'
            else:
                return 'background-color: #8B0000; color: #FFFFFF; font-weight: bold'

        # Display the styled dataframe
        st.dataframe(suitability_df.style.applymap(color_suitability, subset=['Suitability']))

        # Cost Efficiency
        st.markdown("#### <span style='color:#D4AF37'>Cost Efficiency</span>", unsafe_allow_html=True)
        efficiency_df = results_df[['name', 'cost_per_1000lm_hour', 'cost_per_req_lumens']].copy()
        efficiency_df.columns = ['Lamp Name', f'Cost per 1000 lm/hour ({currency})', f'Cost per Required Lumens ({currency})']
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
        total_df.columns = [
            'Lamp Name',
            f'Total Capital Cost ({currency})',
            f'Total 5-Year Cost ({currency})'
        ]
        st.dataframe(total_df)
# Detailed Comparison
        st.markdown("#### <span style='color:#D4AF37'>Detailed Comparison</span>", unsafe_allow_html=True)

        # Create a comprehensive comparison with all metrics
        detailed_cols = [
            'name', 'wattage', 'efficacy', 'light_output_per_lamp', 'total_light_output', 'suitability',
            'cost_per_1000lm_hour', 'cost_per_req_lumens',
            'energy_cost_per_day', 'energy_cost_per_year', 'energy_cost_5years',
            'total_capital_cost', 'total_5year_cost'
        ]

        detailed_df = results_df[detailed_cols].copy()
        detailed_df.columns = [
            'Lamp Name', 'Wattage (W)', 'Efficacy (lm/W)', 'Light Output per Lamp (lm)', 'Total Light Output (lm)', 'Suitability',
            f'Cost per 1000 lm/hour ({currency})', f'Cost per Required Lumens ({currency})',
            f'Energy Cost/Day ({currency})', f'Energy Cost/Year ({currency})', f'Energy Cost/5 Years ({currency})',
            f'Total Capital Cost ({currency})', f'Total 5-Year Cost ({currency})'
        ]

        # Add this line to display the detailed dataframe
        st.dataframe(detailed_df.style.applymap(color_suitability, subset=['Suitability']))
    else:
        st.error("Please enter valid data for at least one lamp option.")

        # Add explanations
with st.expander("Understanding the Calculations"):
    st.markdown("""
    ### Formulas Used
    
    - **Light Output per Lamp** = Wattage × Efficacy
    - **Total Light Output** = Light Output per Lamp × Number of Lamps
    - **Suitability** = "OKAY" if Light Output per Lamp ≥ Required Lumens, otherwise "NOT SUITABLE"
    - **Cost per 1000 lm/hour** = (Wattage × Energy Cost) / (Efficacy × 1000)
    - **Cost per Required Lumens** = (Cost per 1000 lm/hour × Required Lumens) / 1000
    - **Energy Cost per Day** = Number of Lamps × Wattage × Hours per Day × Energy Cost / 1000
    - **Energy Cost per Year** = Energy Cost per Day × 365
    - **Energy Cost for 5 Years** = Energy Cost per Year × 5
    - **Total Capital Cost** = Number of Lamps × Capital Cost per Lamp
    - **Total 5-Year Cost** = Total Capital Cost + Energy Cost for 5 Years
    
    ### Tips for Using the Calculator
    
    - Enter accurate wattage and efficacy values for precise calculations
    - Higher efficacy (lm/W) means better energy efficiency
    - Consider both capital costs and long-term energy costs
    - Ensure the total light output meets your requirements
    """)

# Footer with gold styling
st.markdown("<hr style='height:2px;border:none;color:#D4AF37;background-color:#D4AF37;margin-top:30px;'/>", unsafe_allow_html=True)
st.markdown("<div style='display:flex;justify-content:center;margin-top:20px;'><h3 style='color:#D4AF37;'>Lighting Efficiency & Cost Calculator © SustainabLED</h3></div>", unsafe_allow_html=True)
st.markdown("<div style='display:flex;justify-content:center;'><em>Compare your lighting options to find the most efficient and cost-effective solution</em></div>", unsafe_allow_html=True)