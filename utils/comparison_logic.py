def calculate_fixed_loan_trajectory(income_history, initial_principal, initial_tenure, interest_rate_annual=0.12):
    """
    Simulates a traditional fixed EMI loan against the same income history.
    
    Returns:
        list of dicts: Snapshot of fixed loan state [Month, Balance, Distress_Accumulated]
    """
    r = interest_rate_annual / 12
    # Calculate Fixed EMI once
    fixed_emi = (initial_principal * r * ((1+r)**initial_tenure)) / (((1+r)**initial_tenure) - 1)
    
    balance = initial_principal
    history = []
    default_count = 0
    distress_balance = 0 
    penalties = 0
    consecutive_defaults = 0
    missed_payments_count = 0
    
    for i, income in enumerate(income_history):
        month = i + 1
        
        # Interest Component
        interest = balance * r
        principal_comp = fixed_emi - interest
        
        balance -= principal_comp
        if balance < 0: balance = 0
        
        # Check affordability
        if fixed_emi > income:
            shortfall = fixed_emi - income
            distress_balance += shortfall
            consecutive_defaults += 1
            missed_payments_count += 1
            
            # Simulated Penalty: 500 INR + 2% of shortfall
            penalty = 500 + (shortfall * 0.02)
            penalties += penalty
        else:
            # If surplus, pay down distress
            surplus = income - fixed_emi
            distress_balance = max(0, distress_balance - surplus)
            consecutive_defaults = 0
            
        history.append({
            'Month': month,
            'Fixed_Balance': balance,
            'Fixed_Distress': distress_balance + penalties, # Total financial impact
            'Fixed_EMI': fixed_emi,
            'Is_Default': fixed_emi > income
        })
        
    return history, missed_payments_count, penalties
