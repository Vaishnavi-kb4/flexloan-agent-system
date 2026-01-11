class ContractEvolutionAgent:
    def __init__(self):
        pass

    def generate_contract_update(self, old_terms, new_terms, borrower_name="User"):
        """
        Generates a transparent explanation for the loan term adjustment.
        
        Args:
            old_terms (dict): {emi, tenure}
            new_terms (dict): {emi, tenure, action_taken}
            borrower_name (str): Name of borrower.
            
        Returns:
            dict: {
                'message': str, # User friendly message
                'contract_id': str # Simulated ID
            }
        """
        action = new_terms.get('action_taken')
        new_emi = new_terms['new_emi']
        new_tenure = new_terms['new_tenure']
        
        if action == 'Maintain Standard':
            return {
                'message': "Income verified stable. Standard repayment schedule maintained.",
                'contract_id': 'CTR-STD-KEEP',
                'event_type': 'Stable'
            }
        
        elif 'Relief' in action or 'Interest Only' in action:
             return {
                'message': f"Preventive Restructuring Triggered: EMI reduced to ₹{new_emi} to mitigate default risk.",
                'contract_id': f"CTR-RELIEF-{new_tenure}",
                'event_type': 'Relief'
            }
            
        else:
            return {
                'message': f"Repayment Calibration: EMI adjusted to ₹{new_emi} based on cashflow analysis.",
                'contract_id': f"CTR-ADJ-{new_tenure}",
                'event_type': 'Stress'
            }
