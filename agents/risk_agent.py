class RiskIntelligenceAgent:
    def __init__(self):
        pass

    def assess_risk(self, income_forecast, current_emi, missed_payments=0):
        """
        Calculates a dynamic risk score based on forecasted income and current obligations.
        
        Args:
            income_forecast (dict): Output from CashflowForecastingAgent.
            current_emi (float): Current monthly installment.
            missed_payments (int): Number of recent missed payments.
            
        Returns:
            dict: {
                'risk_score': int, # 0-100 (Higher is riskier)
                'status': str # 'Healthy', 'At Risk', 'Critical'
            }
        """
        safe_income = income_forecast['safe_income']
        volatility = income_forecast['volatility']
        
        if safe_income == 0:
            return {'risk_score': 100, 'status': 'Critical'}
            
        # Calculate Repayment Stress (DTI based on safe income)
        stress_ratio = current_emi / safe_income
        
        # Base score from stress
        # If EMI is 30% of safe income, score ~ 30. If 60%, score ~ 60.
        base_score = min(100, stress_ratio * 100)
        
        # Add penalty for volatility (up to 20 points)
        volatility_penalty = min(20, volatility * 50)
        
        # Add penalty for missed payments (huge drift)
        missed_penalty = missed_payments * 15
        
        final_score = base_score + volatility_penalty + missed_penalty
        final_score = min(100, max(0, final_score)) # Clamp to 0-100
        
        # Determine zone and color
        if final_score <= 40:
            zone = 'Safe'
            zone_color = 'green'
        elif final_score <= 70:
            zone = 'Watch'
            zone_color = 'orange'
        else:
            zone = 'Critical'
            zone_color = 'red'
            
        status = zone
            
        return {
            'risk_score': int(final_score),
            'status': status,
            'zone': zone,
            'zone_color': zone_color,
            'breakdown': {
                'Affordability Stress': int(base_score),
                'Income Volatility': int(volatility_penalty),
                'Missed Payments': int(missed_penalty)
            }
        }
