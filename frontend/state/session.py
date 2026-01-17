"""
Session state management
"""

import streamlit as st

def initialize_session_state():
    """Initialize all session state variables"""
    if 'analytical_data' not in st.session_state:
        st.session_state.analytical_data = None
    if 'numerical_data' not in st.session_state:
        st.session_state.numerical_data = None
    if 'current_params' not in st.session_state:
        st.session_state.current_params = {}

def clear_analytical():
    """Clear analytical solution data"""
    st.session_state.analytical_data = None

def clear_numerical():
    """Clear numerical solution data"""
    st.session_state.numerical_data = None

def clear_all():
    """Clear all session data"""
    st.session_state.clear()

def store_analytical_solution(u, x, t, comp_time, params):
    """Store analytical solution in session state"""
    st.session_state.analytical_data = {
        'u': u, 'x': x, 't': t,
        'time': comp_time,
        'params': params,
        'type': 'analytical'
    }

def store_numerical_solution(u, x, t, comp_time, params):
    """Store numerical solution in session state"""
    st.session_state.numerical_data = {
        'u': u, 'x': x, 't': t,
        'time': comp_time,
        'params': params,
        'type': 'numerical'
    }

def get_solution_data(solution_type):
    """Get solution data by type"""
    if solution_type == 'analytical':
        return st.session_state.analytical_data
    elif solution_type == 'numerical':
        return st.session_state.numerical_data
    else:
        return None
