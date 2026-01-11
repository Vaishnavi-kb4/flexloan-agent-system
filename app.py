import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from agents.cashflow_agent import CashflowForecastingAgent
from agents.risk_agent import RiskIntelligenceAgent
from agents.structuring_agent import LoanStructuringAgent
from agents.contract_agent import ContractEvolutionAgent
from utils.data_generator import generate_profile_data
from utils.visuals import plot_income_forecast, plot_risk_gauge
from utils.comparison_logic import calculate_fixed_loan_trajectory

# Page Config
st.set_page_config(page_title="SafeLoan Platform", layout="wide")

st.markdown("""
<style>
    .main > div {padding-top: 1rem;}
    h1 {color: #0E1117; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;}
    h3 {color: #424753;}
    .metric-box {
        border-right: 1px solid #e0e0e0; 
        padding-right: 20px;
    }
</style>
""", unsafe_allow_html=True)

st.title("SafeLoan: Adaptive Lending Platform")

# --- Sidebar Controls ---
st.sidebar.markdown("### Configuration")
profile_type = st.sidebar.selectbox("Borrower Profile", ["Gig Worker", "Freelancer", "Small Business"])
st.sidebar.divider()
initial_loan_amount = st.sidebar.number_input("Principal Amount (INR)", value=500000, step=10000)
initial_tenure = st.sidebar.slider("Tenure (Months)", 12, 60, 36)
target_dti = st.sidebar.slider("Target Affordability (DTI)", 0.2, 0.6, 0.4)

if st.sidebar.button("Reset Simulation", use_container_width=True):
    st.session_state.clear()
    st.rerun()

# --- Initialize Session State ---
if 'history' not in st.session_state:
    st.session_state.history = []
    st.session_state.current_month = 0
    st.session_state.income_data = generate_profile_data(profile_type)
    st.session_state.remaining_principal = initial_loan_amount
    st.session_state.remaining_tenure = initial_tenure
    st.session_state.current_emi = (initial_loan_amount / initial_tenure) * 1.1 
    st.session_state.contract_logs = []
    st.session_state.distress_balance = 0 
    
    st.session_state.agent_thoughts = {
        'cashflow': {},
        'risk': {},
        'structuring': {}
    }

# --- Initialize Agents ---
cashflow_agent = CashflowForecastingAgent()
risk_agent = RiskIntelligenceAgent()
structuring_agent = LoanStructuringAgent(target_dti=target_dti)
contract_agent = ContractEvolutionAgent()

# --- Simulation Stepper ---
col_head, col_btn = st.columns([4, 1])
with col_btn:
    if st.button("Advance Month ⏩", use_container_width=True, type="primary"):
        st.session_state.current_month += 1
        current_m = st.session_state.current_month
        
        if current_m > len(st.session_state.income_data):
            st.warning("Simulation Complete.")
        else:
            past_income = st.session_state.income_data.iloc[:current_m]['Income'].tolist()
            last_income = past_income[-1]
            
            # --- AGENT EXECUTION ---
            forecast = cashflow_agent.forecast_income(past_income)
            risk_state = risk_agent.assess_risk(forecast, st.session_state.current_emi)
            new_structure = structuring_agent.structure_loan(
                forecast, 
                st.session_state.remaining_principal, 
                st.session_state.remaining_tenure,
                original_tenure=initial_tenure
            )
            
            # --- UPDATE STATE ---
            old_terms = {'emi': st.session_state.current_emi, 'tenure': st.session_state.remaining_tenure}
            contract_update = contract_agent.generate_contract_update(old_terms, new_structure)
            
            st.session_state.remaining_principal = max(0, st.session_state.remaining_principal - (new_structure['new_emi'] * 0.7))
            st.session_state.remaining_tenure = new_structure['new_tenure'] - 1 if new_structure['new_tenure'] < 999 else 999
            st.session_state.current_emi = new_structure['new_emi']
            
            shortfall = max(0, new_structure['new_emi'] - last_income)
            st.session_state.distress_balance += shortfall
            
            st.session_state.agent_thoughts['cashflow'] = forecast
            st.session_state.agent_thoughts['risk'] = risk_state
            st.session_state.agent_thoughts['structuring'] = new_structure
            
            snapshot = {
                'Month': current_m,
                'Income': last_income,
                'Safe Forecast': forecast['safe_income'],
                'Risk Score': risk_state['risk_score'],
                'Zone': risk_state['zone'],
                'EMI': new_structure['new_emi'],
                'Action': new_structure['action_taken'],
                'Contract': contract_update,
                'Adaptive_Distress': st.session_state.distress_balance
            }
            st.session_state.history.append(snapshot)
            st.session_state.contract_logs.insert(0, snapshot)

# --- Main Interface ---
if st.session_state.history:
    # Key Stats Row
    latest = st.session_state.history[-1]
    s1, s2, s3, s4 = st.columns(4)
    s1.metric("Month", st.session_state.current_month)
    s2.metric("Rating", f"{latest['Risk Score']} ({latest['Zone']})")
    s3.metric("Outstanding Principal", f"₹{st.session_state.remaining_principal:,.0f}")
    s4.metric("Current EMI", f"₹{latest['EMI']:,.0f}")
    
    st.divider()

    # Tabs
    tab1, tab2, tab3 = st.tabs(["Dashboard", "Decision Engine", "Audit Trail"])
    
    with tab1:
        st.subheader("Performance & Impact Analysis")
        # Run Comparison
        current_incomes = st.session_state.income_data.iloc[:st.session_state.current_month]['Income'].tolist()
        fixed_hist, fixed_defaults, fixed_penalties = calculate_fixed_loan_trajectory(current_incomes, initial_loan_amount, initial_tenure)
        fixed_df = pd.DataFrame(fixed_hist)
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Defaults Avoided", f"{fixed_defaults}", delta="SafeLoan Protected")
        c2.metric("Financial Stress (Traditional)", f"₹{fixed_df.iloc[-1]['Fixed_Distress']:,.0f}")
        c3.metric("Financial Stress (SafeLoan)", f"₹{st.session_state.distress_balance:,.0f}", delta="Optimized")
        
        # Chart
        fig_comp = go.Figure()
        fig_comp.add_trace(go.Bar(x=fixed_df['Month'], y=fixed_df['Fixed_Distress'], name='Traditional Distress', marker_color='#EF553B'))
        fig_comp.add_trace(go.Bar(x=[h['Month'] for h in st.session_state.history], y=[h['Adaptive_Distress'] for h in st.session_state.history], name='SafeLoan Distress', marker_color='#00CC96'))
        fig_comp.update_layout(title="Stress Accumulation Analysis", barmode='group', template='plotly_white', height=400)
        st.plotly_chart(fig_comp, use_container_width=True)

        # --- NEW: Affordability Chart ---
        st.markdown("#### 📉 Affordability Logic: EMI vs Safe Income")
        
        months = [h['Month'] for h in st.session_state.history]
        safe_incomes = [h['Safe Forecast'] for h in st.session_state.history]
        emis = [h['EMI'] for h in st.session_state.history]
        
        # Calculate Ratios (Handle div by 0)
        ratios = []
        for emi, safe in zip(emis, safe_incomes):
            if safe > 0:
                ratios.append((emi / safe) * 100)
            else:
                ratios.append(0) # Or Handle as 100%? Default to 0 for chart safety
        
        target_line = [target_dti * 100] * len(months)
        
        fig_afford = go.Figure()
        fig_afford.add_trace(go.Scatter(x=months, y=ratios, mode='lines+markers', name='Actual EMI Burden (%)', line=dict(color='#636EFA', width=3)))
        fig_afford.add_trace(go.Scatter(x=months, y=target_line, mode='lines', name=f'Target DTI Limit ({int(target_dti*100)}%)', line=dict(color='gray', dash='dot')))
        
        fig_afford.update_layout(
            yaxis_title="Percentage of Safe Income",
            xaxis_title="Month",
            template='plotly_white',
            height=350,
            yaxis=dict(range=[0, 100]) # Fix range to 0-100% for clarity
        )
        st.plotly_chart(fig_afford, use_container_width=True)

        # --- NEW: Explain EMI Logic ---
        with st.expander(f"💡 Why is my EMI ₹{latest['EMI']:,.0f}? (Click to Explain)"):
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("1. Safe Income", f"₹{latest['Safe Forecast']:,.0f}", help="Conservative monthly capacity")
            c2.metric("2. Target DTI", f"{int(target_dti*100)}%", help="Affordability Limit")
            c3.metric("3. Risk Score", f"{latest['Risk Score']}/100", help="Influence on decision")
            
            # Tenure Logic
            is_cap_reached = 'Interest Only' in latest['Action']
            cap_status = "🛑 Max Cap" if is_cap_reached else "✅ Standard"
            c4.metric("4. Tenure", cap_status, help="Safeguard status")
            
            st.caption(f"**rationale:** {st.session_state.agent_thoughts['structuring'].get('rationale', 'Standard calculation.')}")
        
    with tab2:
        st.subheader("Agent Intelligence Breakdown")
        
        c_forecast = st.session_state.agent_thoughts['cashflow']
        c_risk = st.session_state.agent_thoughts['risk']
        c_struct = st.session_state.agent_thoughts['structuring']
        
        ec1, ec2, ec3 = st.columns(3)
        
        with ec1:
            st.markdown("### 📈 Cashflow Analysis")
            if c_forecast:
                safe = c_forecast.get('safe_income', 0)
                potential = c_forecast.get('potential_income', 0)
                vol = c_forecast.get('volatility', 0)
                
                vol_msg = "low volatility" if vol < 0.2 else "high volatility"
                vol_desc = "earnings are predictable and reliable" if vol < 0.2 else "income fluctuates significantly"
                
                st.markdown(f"""
                **Income Forecast: {vol_msg.title()}**  
                We estimate your safe monthly income at **₹{safe:,.0f}**, while your earning potential may reach **₹{potential:,.0f}**.
                
                Your income shows {vol_msg}, meaning {vol_desc}.
                """)
            else:
                st.info("Awaiting data...")

        with ec2:
            st.markdown("### 🛡️ Risk Intelligence")
            if c_risk:
                score = c_risk.get('risk_score', 0)
                zone = c_risk.get('zone', 'Unknown')
                
                color_map = {'Safe': '🟢', 'Watch': '⚠️', 'Critical': '🔴'}
                icon = color_map.get(zone, '⚪')
                
                st.markdown(f"""
                {icon} **Risk Level: {zone.upper()} (Score: {score} / 100)**
                """)
                
                breakdown = c_risk.get('breakdown', {})
                if score < 40:
                    st.markdown("Your loan stress is very low.")
                    st.markdown("- ✅ EMI affordability is comfortable")
                    st.markdown("- ✅ Income volatility is manageable")
                elif score < 70:
                    st.markdown("Your loan stress is moderate.")
                    st.markdown("- ⚠️ Managing tight cashflow")
                    st.markdown("- ⚠️ Income volatility requires attention")
                else:
                    st.markdown("Risk level is critical.")
                    st.markdown("- 🔴 High stress detected")
                    st.markdown("- 🔴 Immediate restructuring recommended")

                st.markdown(f"💡 *You are {'well within' if score < 40 else 'approaching limits of'} a safe repayment zone.*")
            else:
                st.info("Awaiting assessment...")

        with ec3:
            st.markdown("### ⚙️ Loan Structuring")
            if c_struct:
                action = c_struct.get('action_taken', '')
                rationale = c_struct.get('rationale', '')
                new_emi = c_struct.get('new_emi', 0)
                
                st.markdown(f"""
                **Decision: {action}**
                
                {rationale}
                
                👉 **New EMI set to ₹{new_emi:,.0f}**
                """)
            else:
                st.info("Awaiting decision...")
            
    with tab3:
        st.subheader("Contract Evolution Ledger")
        for log in st.session_state.contract_logs:
            event_type = log['Contract'].get('event_type')
            color = "green" if event_type == 'Stable' else "red" if event_type == 'Stress' else "orange"
            
            st.markdown(f"""
            **Month {log['Month']}** | <span style='color:{color}'>{event_type}</span> <br>
            {log['Contract']['message']}
            <hr style='margin: 5px 0;'>
            """, unsafe_allow_html=True)

else:
    st.info("System Ready. Initialize Simulation via Sidebar.")
