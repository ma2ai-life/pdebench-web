"""
Metrics display components
"""

import streamlit as st
import numpy as np

def calculate_solution_metrics(u, x=None):
    """Calculate various metrics for a solution"""
    metrics = {}
    
    # Basic statistics
    metrics['max_value'] = float(np.max(u[-1, :]))
    metrics['min_value'] = float(np.min(u[-1, :]))
    metrics['mean_value'] = float(np.mean(u[-1, :]))
    metrics['l2_norm'] = float(np.linalg.norm(u[-1, :]))
    
    # Energy (integral of u²)
    if x is not None:
        try:
            metrics['energy'] = float(np.trapz(u[-1, :]**2, x))
        except:
            dx = x[1] - x[0]
            metrics['energy'] = float(np.sum((u[-1, :-1]**2 + u[-1, 1:]**2) / 2 * dx))
    
    return metrics

def display_solution_metrics(metrics, computation_time=None, title="Metrics"):
    """Display metrics in a formatted way"""
    st.markdown(f"#### {title}")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("L² Norm", f"{metrics.get('l2_norm', 0):.4f}")
    
    with col2:
        st.metric("Max Value", f"{metrics.get('max_value', 0):.4f}")
    
    with col3:
        if 'energy' in metrics:
            st.metric("Energy", f"{metrics['energy']:.4f}")
        else:
            st.metric("Mean", f"{metrics.get('mean_value', 0):.4f}")
    
    with col4:
        if computation_time is not None:
            st.metric("Time (s)", f"{computation_time:.4f}")
        else:
            st.metric("Min Value", f"{metrics.get('min_value', 0):.4f}")

def display_comparison_metrics(analytical_time, numerical_time, max_error):
    """Display comparison metrics between two solutions"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        delta_analytical = analytical_time - numerical_time
        st.metric(
            "Analytical Time", 
            f"{analytical_time:.6f}s",
            delta=f"{delta_analytical:.6f}s"
        )
    
    with col2:
        delta_numerical = numerical_time - analytical_time
        st.metric(
            "Numerical Time", 
            f"{numerical_time:.6f}s",
            delta=f"{delta_numerical:.6f}s"
        )
    
    with col3:
        if analytical_time > 0:
            speedup = numerical_time / analytical_time
            st.metric("Speedup", f"{speedup:.2f}x")
        else:
            st.metric("Speedup", "N/A")
    
    with col4:
        st.metric("Max Error", f"{max_error:.6f}")
