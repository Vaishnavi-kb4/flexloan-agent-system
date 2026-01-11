class LoanStructuringAgent:
    def __init__(self, target_dti=0.40, interest_rate_annual=0.12):
        self.target_dti = target_dti # Target Debt-to-Income ratio
        self.interest_rate_monthly = interest_rate_annual / 12

    def structure_loan(self, income_forecast, remaining_principal, current_tenure, original_tenure):
        """
        Determines the optimal EMI and Tenure based on safe income forecast, with safeguards.
        Args:
            income_forecast (dict): Output from CashflowForecastingAgent.
            remaining_principal (float): Outstanding loan.
            current_tenure (int): Current months remaining.
            original_tenure (int): Baseline tenure for cap calculation.
        """
        safe_income = income_forecast['safe_income']
        max_allowed_tenure = original_tenure * 2 # Cap at 2x original
        
        if remaining_principal <= 0:
            return {'new_emi': 0, 'new_tenure': 0, 'action_taken': 'Loan Paid Off', 'rationale': 'Debt cleared.'}

        # Calculate minimal interest coverage
        interest_due = remaining_principal * self.interest_rate_monthly
        
        # Ideal Adaptive EMI
        adaptive_emi = safe_income * self.target_dti
        
        # Constraint 1: Must cover at least interest? 
        # For this prototype, if adaptive_emi < interest_due, we capitalize interest or set to min.
        # Let's enforce that we pay at least interest if possible, else partial.
        
        # Scenario: Income is strong
        if adaptive_emi >= interest_due + (remaining_principal / current_tenure):
            # Can pay off faster or stick to schedule
            # Stick to schedule but ensure affordability
            # Recalculate standard EMI for current tenure
            # Standard EMI formula: P * r * (1+r)^n / ((1+r)^n - 1)
            # Simplified for prototype validation:
            
            standard_emi = self._calculate_pmt(remaining_principal, self.interest_rate_monthly, current_tenure)
            
            if standard_emi <= adaptive_emi:
                return {
                    'new_emi': round(standard_emi, 2),
                    'new_tenure': current_tenure,
                    'action_taken': 'Maintain Standard',
                    'rationale': 'Income is sufficient to support standard repayment schedule.'
                }
            else:
                # Need to extend slightly or pay what we can
                return {
                    'new_emi': round(adaptive_emi, 2),
                    'new_tenure': self._calculate_tenure(remaining_principal, self.interest_rate_monthly, adaptive_emi),
                    'action_taken': 'Adjust Tenure (Minor)',
                    'rationale': f'Income dip detected. EMI re-calibrated to {int(self.target_dti*100)}% of safe income to maintain affordability.'
                }

        # Scenario: Income is weak (Adaptive Mode)
        else:
             # If adaptive EMI covers interest, great. If not, minimal payment.
             payable_emi = max(adaptive_emi, 100) # Minimum token amount
             
             # If low payment, tenure extends drastically
             if payable_emi <= interest_due:
                 # Negative amortization or interest only
                 # For safety, lets say we pay interest only at minimum
                 payable_emi = interest_due
                 new_tenure = current_tenure + 1 # Extends indefinitely basically
                 action = 'Interest Only / Relief Mode'
                 rationale = 'Critical income drop. Freezing principal repayment to prevent default. Interest-only mode activated.'
             else:
                 calculated_metric = self._calculate_tenure(remaining_principal, self.interest_rate_monthly, payable_emi)
                 
                 # GUARDRAIL: Tenure Cap
                 if calculated_metric > max_allowed_tenure:
                     # Cap Reached -> Interest Only Mode
                     payable_emi = interest_due
                     new_tenure = current_tenure # Pause tenure countdown ideally, or just drift
                     action = 'Safeguard: Interest Only'
                     rationale = f'Tenure extension cap ({max_allowed_tenure}m) reached. Switching to Interest-Only to prevent eternal debt.'
                 else:
                     new_tenure = calculated_metric
                     action = 'Extend Tenure (Relief)'
                     rationale = 'High stress detected. Extending tenure to lower monthly burden.'
                 
             return {
                 'new_emi': round(payable_emi, 2),
                 'new_tenure': int(new_tenure),
                 'action_taken': action,
                 'rationale': rationale
             }

    def _calculate_pmt(self, p, r, n):
        if r == 0: return p / n
        return p * r * ((1 + r)**n) / (((1 + r)**n) - 1)

    def _calculate_tenure(self, p, r, emi):
        import math
        if emi <= p * r:
            return 999 # Perpetual
        try:
             # Formula for n = -log(1 - (r*P)/EMI) / log(1+r)
             numerator = -math.log(1 - (r * p) / emi)
             denominator = math.log(1 + r)
             return math.ceil(numerator / denominator)
        except:
            return 999
