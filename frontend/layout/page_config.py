"""
Page configuration and setup
"""

import streamlit as st

def setup_page():
    """Configure the page settings"""
    st.set_page_config(
        page_title="PDEBench - Heat Equation Analysis",
        page_icon="🔥",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://github.com/yourusername/pdebench',
            'Report a bug': 'https://github.com/yourusername/pdebench/issues',
            'About': '''
            # PDEBench v1.0
            A platform for benchmarking PDE solvers
            '''
        }
    )
