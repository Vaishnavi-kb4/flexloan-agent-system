import numpy as np
import pandas as pd

def generate_irregular_income(months=12, base_income=50000, volatility=0.3):
    """
    Generates a synthetic income stream with irregularity.
    
    Args:
        months (int): Number of months to simulate.
        base_income (float): Average target income.
        volatility (float): Factor for random fluctuation (0.0 to 1.0).
        
    Returns:
        pd.DataFrame: DataFrame with 'Month' and 'Income'.
    """
    np.random.seed(42) # For reproducibility
    
    incomes = []
    current_trend = base_income
    
    for i in range(months):
        # Random fluctuation
        noise = np.random.normal(0, volatility * base_income)
        
        # Occasional "shock" or "bonus" (10% chance)
        event_multiplier = np.random.choice([0.5, 1.0, 1.5], p=[0.1, 0.8, 0.1])
        
        income = max(0, (current_trend + noise) * event_multiplier)
        incomes.append(int(income))
        
    return pd.DataFrame({
        'Month': range(1, months + 1),
        'Income': incomes
    })

def generate_profile_data(profile_type):
    if profile_type == "Gig Worker":
        return generate_irregular_income(base_income=30000, volatility=0.4)
    elif profile_type == "Freelancer":
        return generate_irregular_income(base_income=60000, volatility=0.5)
    elif profile_type == "Small Business":
        return generate_irregular_income(base_income=100000, volatility=0.2)
    else:
        return generate_irregular_income(base_income=40000, volatility=0.1)
