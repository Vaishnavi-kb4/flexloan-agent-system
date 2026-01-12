# 🛡️ SafeLoan: Agentic Adaptive Lending System

> **AI-Powered Financial Inclusion for Irregular Income Workers**

## 🚩 Problem Statement
Traditional lending systems rely on fixed monthly repayments (EMIs), which are fundamentally incompatible with the financial reality of gig workers, freelancers, and small business owners. 
*   **Volatility Mismatch:** A single low-income month can trigger late fees, credit score damage, and default.
*   **Rigid Structures:** Banks lack the tools to dynamically adjust terms in real-time without expensive manual intervention.

## 💡 Solution Description
**SafeLoan** is an autonomous agentic system that restructures loans in real-time. It moves beyond static underwriting to **continuous adaptive lifecycle management**.
*   **Dynamic EMIs:** Monthly payments adjust automatically based on income forecasts.
*   **Safety Nets:** Built-in safeguards like "Interest-Only Mode" prevent default during crises.
*   **Zero Stress:** The system prioritizes keeping the borrower solvent, ensuring higher recovery rates for lenders.

## 🏗️ Architecture
SafeLoan is powered by a multi-agent AI architecture, where each agent specializes in a critical financial task.

## 🔄 Monthly Agent Loop

### 1. Income Input
The system ingests the borrower’s income for the current month.

### 2. Cashflow Agent (Forecaster)
*   Analyzes historical income trends
*   Predicts future earnings
*   Calculates a conservative **Safe Income**
*   Measures income volatility

### 3. Risk Intelligence Agent (Analyst)
*   Evaluates affordability using Debt-to-Income ratios
*   Generates a **Risk Score (0–100)**
*   Assigns a Risk Zone:
    *   🟢 **Safe**
    *   🟡 **Watch**
    *   🔴 **Critical**

### 4. Loan Structuring Agent (Architect)
*   Determines the optimal EMI for the next month
*   Extends tenure when income drops
*   Switches to **Interest-Only Mode** during high-risk periods
*   Ensures repayments remain affordable and default-free

### 5. Contract Evolution Agent (Communicator)
*   Translates AI decisions into clear, human-readable explanations
*   Builds transparency and borrower trust

### 6. Dashboard Update
*   UI updates EMIs, risk gauges, distress balance, and defaults avoided
*   Parallel comparison shows how a traditional fixed-EMI loan would fail under the same conditions

## 🧠 Tech Stack Used

### Frontend & UI
*   **Streamlit** (interactive dashboards and simulation controls)

### Backend & AI Logic
*   **Python**
*   **Agent-based architecture** (custom autonomous agents)

### Data & Analytics
*   **Pandas**
*   **NumPy**

### Visualization
*   **Plotly** (charts, gauges, comparisons)

### Development & Deployment
*   **GitHub** (version control)
*   **Streamlit Cloud** (deployment)

## ⚙️ Setup and Execution Steps

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/Vaishnavi-kb4/flexloan-agent-system.git
    cd finance_agent_system
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Application**
    ```bash
    streamlit run app.py
    ```

The interactive dashboard will open in your browser.

## 🚀 Prototype Link
*   **Live Demo:** [https://safeloan-flexloan.streamlit.app](https://safeloan-flexloan.streamlit.app)

## 🌍 Impact
SafeLoan demonstrates how **Agentic AI** can create fair, transparent, and adaptive financial systems. By preventing defaults instead of penalizing them, SafeLoan enables sustainable credit access for millions of workers with irregular income.
