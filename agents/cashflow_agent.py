import numpy as np

class CashflowForecastingAgent:
    def __init__(self, lookback_period=3):
        self.lookback_period = lookback_period

    def forecast_income(self, income_history):
        """
        Analyzes historical income to predict a safe and potential range for the next month.
        
        Args:
            income_history (list or np.array): List of past income values.
            
        Returns:
            dict: {
                'safe_income': float, # Conservative estimate (e.g., avg - std_dev)
                'potential_income': float, # Optimistic estimate (e.g., avg + std_dev)
                'volatility': float # Coefficient of variation
            }
        """
        if len(income_history) < 1:
            return {'safe_income': 0, 'potential_income': 0, 'volatility': 0}
            
        # Use only recent history for relevance
        recent_data = income_history[-self.lookback_period:]
        
        avg_income = np.mean(recent_data)
        std_dev = np.std(recent_data) if len(recent_data) > 1 else 0
        
        # Conservative forecast: Lower bound of 1 std dev, but not negative
        safe_income = max(0, avg_income - std_dev)
        
        # Potential forecast: Average
        potential_income = avg_income + (std_dev * 0.5)
        
        volatility = (std_dev / avg_income) if avg_income > 0 else 0
        
        return {
            'safe_income': round(safe_income, 2),
            'potential_income': round(potential_income, 2),
            'volatility': round(volatility, 3)
        }
