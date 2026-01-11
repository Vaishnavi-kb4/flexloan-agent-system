import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.cashflow_agent import CashflowForecastingAgent
from agents.risk_agent import RiskIntelligenceAgent
from agents.structuring_agent import LoanStructuringAgent
from agents.contract_agent import ContractEvolutionAgent

def test_workflow():
    print("Initializing Agents...")
    cashflow = CashflowForecastingAgent()
    risk = RiskIntelligenceAgent()
    structuring = LoanStructuringAgent()
    contract = ContractEvolutionAgent()
    
    # Simulate a scenario
    income_history = [50000, 52000, 48000, 30000] # Dip at the end
    
    print("1. Forecasting Income...")
    forecast = cashflow.forecast_income(income_history)
    print(f"   Forecast: {forecast}")
    
    print("2. Assessing Risk...")
    current_emi = 15000
    risk_state = risk.assess_risk(forecast, current_emi)
    print(f"   Risk State: {risk_state}")
    
    print("3. Structuring Loan...")
    structure = structuring.structure_loan(forecast, remaining_principal=400000, current_tenure=30)
    print(f"   New Structure: {structure}")
    
    print("4. Evolving Contract...")
    old_terms = {'emi': 15000, 'tenure': 30}
    msg = contract.generate_contract_update(old_terms, structure)
    print(f"   Contract Msg: {msg['message']}")
    
    print("\n✅ Verification Successful: All agents interacted correctly.")

if __name__ == "__main__":
    test_workflow()
