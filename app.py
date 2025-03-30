import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from streamlit_extras.metric_cards import style_metric_cards

# Page Config
st.set_page_config(
    page_title="EasyQarz Pro | Pakistan EMI Calculator",
    page_icon="💎",
    layout="wide"
)

# Custom CSS (Light Green Theme with Hover Effects)
st.markdown("""
<style>
    /* Light Green Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%) !important;
        border-right: 1px solid #81C784;
    }
    [data-testid="stSidebar"] * {
        color: #2E7D32 !important;
    }
    
    /* Horizontal Cards */
    .horizontal-cards {
        display: flex;
        gap: 15px;
        margin-bottom: 25px;
    }
    .metric-card {
        background: white;
        border-radius: 10px;
        padding: 15px;
        flex: 1;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border-top: 3px solid #4CAF50;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .metric-card:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 16px rgba(0,0,0,0.15);
    }
    .metric-title {
        font-size: 14px;
        color: #555;
    }
    .metric-value {
        font-size: 22px;
        font-weight: bold;
        color: #2E7D32;
    }
    
    /* Chart Hover Effect */
    .stPlotlyChart:hover {
        filter: brightness(1.1);
        transition: filter 0.3s ease;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 20px;
        color: #666;
    }
</style>
""", unsafe_allow_html=True)

# ---- CALCULATION FUNCTIONS ----
def calculate_emi(P, r, n):
    """Standard EMI calculation"""
    monthly_rate = r / 12 / 100
    months = n * 12
    emi = P * monthly_rate * (1 + monthly_rate)**months / ((1 + monthly_rate)**months - 1)
    return emi

def islamic_profit(P, r, n):
    """Simplified Musharaka calculation"""
    total_payment = P * (1 + (r/100) * n)  # Linear profit rate
    return total_payment / (n * 12)  # Monthly payment

def generate_schedule(P, r, n, islamic=False):
    """Amortization schedule generator"""
    months = n * 12
    schedule = []
    balance = P
    
    if islamic:
        monthly_payment = islamic_profit(P, r, n)
        for month in range(1, months + 1):
            principal = monthly_payment
            schedule.append([month, monthly_payment, principal, 0, max(0, balance - principal)])
            balance -= principal
    else:
        monthly_rate = r / 12 / 100
        emi = calculate_emi(P, r, n)
        for month in range(1, months + 1):
            interest = balance * monthly_rate
            principal = emi - interest
            schedule.append([month, emi, principal, interest, max(0, balance - principal)])
            balance -= principal
    
    return pd.DataFrame(
        schedule,
        columns=["Month", "Payment", "Principal", "Interest", "Balance"]
    )

# ---- SIDEBAR ----
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; margin-bottom:20px;">
        <h2 style="color:#2E7D32;">EasyQarz <span style="color:#4CAF50;">Pro</span></h2>
        <p style="color:#388E3C;">Pakistan's Smart EMI Calculator</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Inputs
    loan_amount = st.slider("Loan Amount (PKR)", 50000, 10_000_000, 1_000_000, 25000)
    interest_rate = st.slider("Annual Rate (%)", 5.0, 25.0, 15.0, 0.5)
    tenure_years = st.select_slider("Tenure (Years)", options=list(range(1, 26)), value=5)
    islamic_mode = st.toggle("Islamic Banking Mode")

# ---- MAIN CALCULATIONS ----
if islamic_mode:
    monthly_payment = islamic_profit(loan_amount, interest_rate, tenure_years)
    total_payment = monthly_payment * tenure_years * 12
    total_interest = 0  # No interest in Islamic mode
else:
    monthly_payment = calculate_emi(loan_amount, interest_rate, tenure_years)
    total_payment = monthly_payment * tenure_years * 12
    total_interest = total_payment - loan_amount

# Generate schedule
schedule_df = generate_schedule(loan_amount, interest_rate, tenure_years, islamic_mode)

# ---- MAIN DISPLAY ----
st.title("📊 Payment Overview")

# 1. Horizontal Cards
st.markdown(f"""
<div class="horizontal-cards">
    <div class="metric-card">
        <div class="metric-title">Monthly Payment</div>
        <div class="metric-value">PKR {monthly_payment:,.2f}</div>
    </div>
    <div class="metric-card">
        <div class="metric-title">Total {'Profit' if islamic_mode else 'Interest'}</div>
        <div class="metric-value">PKR {total_interest:,.2f}</div>
    </div>
    <div class="metric-card">
        <div class="metric-title">Total Payment</div>
        <div class="metric-value">PKR {total_payment:,.2f}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# 2. Charts
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### Payment Composition")
    if islamic_mode:
        fig_pie = px.pie(
            values=[loan_amount], 
            names=["Principal"],
            color_discrete_sequence=["#4CAF50"],
            hole=0.5
        )
    else:
        fig_pie = px.pie(
            values=[loan_amount, total_interest], 
            names=["Principal", "Interest"],
            color_discrete_sequence=["#4CAF50", "#FF5722"],
            hole=0.5
        )
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    st.markdown("### Payment Schedule")
    if islamic_mode:
        fig = px.area(
            schedule_df,
            x="Month",
            y=["Principal"],
            color_discrete_map={"Principal": "#4CAF50"}
        )
    else:
        fig = px.area(
            schedule_df,
            x="Month",
            y=["Principal", "Interest"],
            color_discrete_map={"Principal": "#4CAF50", "Interest": "#FF5722"}
        )
    st.plotly_chart(fig, use_container_width=True)

# 3. Data Table
st.markdown("### Amortization Schedule (First 12 Months)")
st.dataframe(
    schedule_df.head(12).style.format({
        "Payment": "PKR {:,.2f}",
        "Principal": "PKR {:,.2f}",
        "Interest": "PKR {:,.2f}" if not islamic_mode else "",
        "Balance": "PKR {:,.2f}"
    }),
    hide_index=True,
    use_container_width=True
)

# ---- FOOTER ----
st.markdown("---")
st.markdown("""
<div style="text-align:center; padding:20px 0;">
    <p style="color:#666; font-size:14px; margin-bottom:8px;">
        © 2025 EasyQarz | Compliant with State Bank of Pakistan
    </p>
    <p style="color:#666; font-size:14px;">
        Built with ❤️ by <strong>Ahmed Saleh Riaz</strong> | 
        <a href="https://www.linkedin.com/in/ahmed-saleh-riaz/" style="color:#4CAF50; text-decoration:none;">LinkedIn</a> | 
        <a href="https://github.com/ASR4792" style="color:#4CAF50; text-decoration:none;">GitHub</a>
    </p>
</div>
""", unsafe_allow_html=True)