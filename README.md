# EasyQarz - Pakistan EMI Calculator 🇵🇰
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://easyapprz-emi-calculator-nfn8ayj2hfrhplfkkknfex.streamlit.app/)
![GitHub last commit](https://img.shields.io/github/last-commit/ASR4792/EasyQarz-EMI-Calculator)

## Course Information
- **Course Name**: AF3005 – Programming for Finance  
- **Instructor**: Dr. Usama Arshad  
- **Developer**: Ahmed Saleh Riaz

## App Overview
EasyQarz is a Streamlit web application for calculating loan EMIs with Islamic banking support, specifically designed for Pakistan's financial market.

**Key Features**:
- Real-time EMI calculations
- Islamic (Musharaka) profit mode
- Interactive charts and payment schedules
- Pakistan-specific loan ranges (PKR 50,000 to 10,000,000)
- Responsive design for all devices

## Screenshots
<img width="956" alt="easyqarz" src="https://github.com/user-attachments/assets/00c702f3-9ae2-4b3e-818c-3c14a2c76377" />
<img width="955" alt="easyqarz2" src="https://github.com/user-attachments/assets/930157a1-9f02-4afb-a45d-bcab8da4dcb5" />

## Installation Guide
### Requirements
- Python 3.9+
- Streamlit
- Pandas
- Plotly
- NumPy

### Run Locally
1. Clone the repository:
   ```bash
   git clone https://github.com/ASR4792/EasyQarz-EMI-Calculator.git
   cd EasyQarz-EMI-Calculator
   pip install -r requirements.txt
   streamlit run app.py
   Access at http://localhost:8501

### Deployment
- Live App: [EasyQarz on Streamlit Share](https://easyapprz-emi-calculator-nfn8ayj2hfrhplfkkknfex.streamlit.app/)
- GitHub Repository: ASR4792/EasyQarz-EMI-Calculator

### How to Use
- Adjust loan parameters using interactive sliders:
- Loan Amount (PKR 50,000 to 10,000,000)
- Annual Rate (5% to 25%)
- Tenure (1 to 25 years)
- Toggle between Conventional/Islamic modes
- View real-time updates of:
- Monthly payment amount
- Total interest/profit
- Payment composition charts
- Detailed amortization schedule
