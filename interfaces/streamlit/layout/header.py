"""
Header and title components
"""

import streamlit as st

def display_header():
    """Display the main header"""
    st.markdown('<h1 class="main-title">🔥 PDEBench - Heat Equation</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Professional Platform for PDE Solver Benchmarking</p>', unsafe_allow_html=True)

def display_import_status(status_message):
    """Display import status"""
    if "⚠️" in status_message:
        st.warning(status_message)
    else:
        st.success(status_message)
