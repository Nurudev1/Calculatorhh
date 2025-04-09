def calculate_lamp_metrics(lamp, site_requirements):
    """
    Calculate all metrics for a lamp option based on site requirements.
    
    Parameters:
    - lamp: Dictionary containing lamp specifications
    - site_requirements: Dictionary containing site requirements
    
    Returns:
    - Dictionary with all calculated metrics
    """
    # Extract values from inputs
    wattage = lamp['wattage']
    efficacy = lamp['efficacy']
    capital_cost = lamp['capital_cost']
    
    number_of_lamps = site_requirements['number_of_lamps']
    hours_per_day = site_requirements['hours_per_day']
    required_lumens = site_requirements['required_lumens']
    energy_cost = site_requirements['energy_cost']  # Energy cost per kWh
    currency = site_requirements['currency']
    
    # Calculate light output for a single lamp
    light_output_per_lamp = wattage * efficacy
    
    # Calculate total light output for all lamps
    total_light_output = light_output_per_lamp * number_of_lamps
    
    # Determine suitability - compare lamp output to required lumens
    suitability = "OKAY" if light_output_per_lamp >= required_lumens else "NOT SUITABLE"
    
    # Calculate cost metrics
    # Cost per 1000 lumen-hour (updated formula)
    cost_per_1000lm_hour = ((energy_cost * wattage / 1000) / (light_output_per_lamp / 1000))
    
    # Cost per required lumens (e.g., 30,000 lm)
    cost_per_req_lumens = cost_per_1000lm_hour * (required_lumens / 1000)
    
    # Calculate energy costs (updated formula)
    # Daily energy cost
    energy_cost_per_day = hours_per_day * number_of_lamps * cost_per_req_lumens
    
    # Yearly energy cost
    energy_cost_per_year = energy_cost_per_day * 365
    
    # 5-year energy cost
    energy_cost_5years = energy_cost_per_year * 5
    
    # Calculate capital and total costs
    total_capital_cost = number_of_lamps * capital_cost
    
    # Total 5-year cost (capital + energy)
    total_5year_cost = total_capital_cost + energy_cost_5years
    
    # Return all metrics in a dictionary
    # added a rounding factor
    return {
        'name': lamp['name'],
        'make': lamp['make'],
        'model': lamp['model'],
        'wattage': round(wattage, 2),
        'efficacy': round(efficacy, 2),
        'light_output_per_lamp': round(light_output_per_lamp, 2),
        'total_light_output': round(total_light_output, 2),
        'suitability': suitability,
        'cost_per_1000lm_hour': round(cost_per_1000lm_hour, 2),
        'cost_per_req_lumens': round(cost_per_req_lumens, 2),
        'energy_cost_per_day': round(energy_cost_per_day, 2),
        'energy_cost_per_year': round(energy_cost_per_year, 2),
        'energy_cost_5years': round(energy_cost_5years, 2),
        'total_capital_cost': round(total_capital_cost, 2),
        'total_5year_cost': round(total_5year_cost, 2)
    }