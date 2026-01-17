"""
CSS styles and themes for PDEBench
"""

MAIN_CSS = """
<style>
    /* Main Titles */
    .main-title {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 700;
    }
    
    .sub-title {
        color: #4B5563;
        text-align: center;
        margin-bottom: 2rem;
        font-size: 1.2rem;
    }
    
    /* Cards and Boxes */
    .equation-box {
        background: #F8FAFC;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #E2E8F0;
        margin: 1rem 0;
    }
    
    .solution-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #E2E8F0;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #F0F9FF, #E0F2FE);
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #0EA5E9;
        margin-bottom: 1rem;
    }
    
    .warning-box {
        background: linear-gradient(135deg, #FEF3C7, #FDE68A);
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #F59E0B;
        margin: 1rem 0;
    }
    
    /* Section Titles */
    .section-title {
        color: #1E3A8A;
        border-bottom: 2px solid #3B82F6;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
        font-size: 1.5rem;
    }
    
    /* Status Indicators */
    .status-success {
        color: #059669;
        background: #D1FAE5;
        padding: 0.5rem;
        border-radius: 5px;
        border-left: 4px solid #059669;
    }
    
    .status-warning {
        color: #D97706;
        background: #FEF3C7;
        padding: 0.5rem;
        border-radius: 5px;
        border-left: 4px solid #D97706;
    }
    
    /* Button Styles */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
    }
    
    .primary-button {
        background: linear-gradient(135deg, #3B82F6, #1D4ED8) !important;
        color: white !important;
    }
    
    .secondary-button {
        background: #E5E7EB !important;
        color: #374151 !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        border-radius: 8px;
        padding: 0 1rem;
    }
</style>
"""

def apply_css():
    """Apply all CSS styles to the Streamlit app"""
    import streamlit as st
    st.markdown(MAIN_CSS, unsafe_allow_html=True)
