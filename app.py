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
    /* Step styling */
    .step-container {
        background-color: #1E1E1E;
        padding: 15px;
        border-radius: 5px;
        border-left: 5px solid #D4AF37;
        margin-bottom: 20px;
    }
    .step-number {
        color: #D4AF37;
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 5px;
    }
    .step-content {
        margin-left: 10px;
    }
</style>
""", unsafe_allow_html=True)
st.title("Lighting Efficiency & Cost Calculator")
st.markdown("Compare different lamp options for your lighting projects")

# Gold title divider
st.markdown("<hr style='height:3px;border:none;color:#D4AF37;background-color:#D4AF37;margin:15px 0px 20px 0px;'/>", unsafe_allow_html=True)

# SustainabLED info section
with st.expander("About SustainabLED", expanded=false):
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
    number_of_lamps = st.number_input("Number of Lamps", min_value=1, value=None, placeholder="Enter number of lamps", help="Total number of lamps needed for the project")
    hours_per_day = st.number_input("Hours per Day", min_value=0.1, value=None, placeholder="Enter hours of operation", help="Hours of operation per day")

with col2:
    required_lumens = st.number_input("Required Lumens per Lamp", min_value=1, value=None, placeholder="Enter lumens requirement", help="Lumens required from each lamp")
    currency = st.selectbox("Currency", options=["$", "€"], index=0)
    energy_cost = st.number_input(f"Energy Cost ({currency}/kWh)", min_value=0.01, value=None, placeholder="Enter energy cost", help="Cost of energy per kilowatt-hour")

# Step 2: Lamp Options
st.markdown("""
<div class="step-container">
    <div class="step-number">STEP 2: Enter Comparison Lamp Details</div>
    <div class="step-content">
        Enter details for the lamps you want to compare with our SustainabLED options. Our SHB 240 and SHB 160 specifications are pre-filled for your convenience.
    </div>
</div>
""", unsafe_allow_html=True)

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
                    value=None if st.session_state.lamp_options[i]['wattage'] == 0.0 else st.session_state.lamp_options[i]['wattage'],
                    placeholder="Enter wattage",
                    key=f"wattage_{i}"
                )
            with col2:
                st.session_state.lamp_options[i]['efficacy'] = st.number_input(
                    "Efficacy (lm/W)",
                    min_value=0.0,
                    value=None if st.session_state.lamp_options[i]['efficacy'] == 0.0 else st.session_state.lamp_options[i]['efficacy'],
                    placeholder="Enter efficacy",
                    key=f"efficacy_{i}"
                )
            with col3:
                st.session_state.lamp_options[i]['capital_cost'] = st.number_input(
                    f"Capital Cost ({currency})",
                    min_value=0.0,
                    value=None if st.session_state.lamp_options[i]['capital_cost'] == 0.0 else st.session_state.lamp_options[i]['capital_cost'],
                    placeholder="Enter cost",
                    key=f"capital_cost_{i}"
                )

# Step 3: Calculate and View Results
st.markdown("""
<div class="step-container">
    <div class="step-number">STEP 3: Calculate and Check Your Savings</div>
    <div class="step-content">
        Click the button below to calculate and compare all lamp options. The results will show you potential savings over time.
    </div>
</div>
""", unsafe_allow_html=True)

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
    # Check if required fields are filled
    if number_of_lamps is None or hours_per_day is None or required_lumens is None or energy_cost is None:
        st.error("Please fill in all the site requirement fields before calculating.")
    else:
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
            if lamp['wattage'] and lamp['efficacy']:  # Only calculate for lamps with valid data
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

            # Savings Calculation
            st.markdown("#### <span style='color:#D4AF37'>Your Savings with SustainabLED</span>", unsafe_allow_html=True)
            
            # Find the SustainabLED lamps and comparison lamps
            sustainabled_results = [r for r in results if "SustainabLED" in r['name']]
            comparison_results = [r for r in results if "SustainabLED" not in r['name']]
            
            if sustainabled_results and comparison_results:
                # Find the best SustainabLED option (lowest 5-year cost)
                best_sustainabled = min(sustainabled_results, key=lambda x: float(x['total_5year_cost']))
                
                # Calculate savings against each comparison lamp
                savings_data = []
                for comp in comparison_results:
                    if comp['wattage'] > 0 and comp['efficacy'] > 0:  # Only show valid lamps
                        five_year_savings = float(comp['total_5year_cost']) - float(best_sustainabled['total_5year_cost'])
                        annual_savings = five_year_savings / 5
                        savings_data.append({
                            'Comparison Lamp': comp['name'],
                            f'Annual Savings ({currency})': format_decimal(annual_savings),
                            f'5-Year Savings ({currency})': format_decimal(five_year_savings)
                        })
                
                if savings_data:
                    savings_df = pd.DataFrame(savings_data)
                    # Style the savings with green color for positive values
                    def color_savings(val):
                        try:
                            value = float(val)
                            if value > 0:
                                return 'color: #00FF00; font-weight: bold'
                            else:
                                return 'color: #FF6B6B; font-weight: bold'
                        except:
                            return ''
                    
                    st.dataframe(savings_df.style.applymap(color_savings, subset=[f'Annual Savings ({currency})', f'5-Year Savings ({currency})']))
                    
                    # Highlight the best option
                    st.markdown(f"""
                    <div style='background-color:#2C2C2C; border-left:3px solid #00FF00; padding:15px; margin-top:15px;'>
                        <h4 style='color:#D4AF37;'>Recommendation</h4>
                        <p>Based on your requirements, <strong style='color:#D4AF37;'>{best_sustainabled['name']}</strong> offers the best long-term value with potential savings shown above compared to your alternatives.</p>
                    </div>
                    """, unsafe_allow_html=True)

            # Detailed Comparison
            with st.expander("View Detailed Comparison"):
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