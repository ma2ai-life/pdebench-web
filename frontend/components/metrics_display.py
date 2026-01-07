import numpy as np
import streamlit as st

def calculate_metrics(u_final, u_initial=None, x=None):
    """Calculate performance metrics"""
    metrics = {}
    
    # L2 norm
    metrics["l2_norm"] = np.linalg.norm(u_final)
    
    # Maximum value
    metrics["max_value"] = np.max(u_final)
    if u_initial is not None:
        metrics["max_initial"] = np.max(u_initial)
    
    # Energy (integral of u²)
    if x is not None:
        try:
            metrics["energy"] = np.trapz(u_final**2, x)
        except:
            dx = x[1] - x[0]
            metrics["energy"] = np.sum((u_final[:-1]**2 + u_final[1:]**2) / 2 * dx)
    
    # Conservation error (for heat equation, energy should decay)
    if u_initial is not None and x is not None:
        try:
            energy_initial = np.trapz(u_initial**2, x)
            energy_final = np.trapz(u_final**2, x)
            metrics["energy_decay"] = (energy_initial - energy_final) / energy_initial * 100
        except:
            pass
    
    return metrics

def display_metrics(metrics, computation_time=None):
    """Display metrics in a clean format"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("L² Norm", f"{metrics.get('l2_norm', 0):.4f}")
    
    with col2:
        st.metric("Max Value", f"{metrics.get('max_value', 0):.4f}")
    
    with col3:
        if 'energy' in metrics:
            st.metric("Energy", f"{metrics['energy']:.4f}")
    
    with col4:
        if computation_time:
            st.metric("Time (s)", f"{computation_time:.3f}")
        elif 'energy_decay' in metrics:
            st.metric("Energy Decay", f"{metrics['energy_decay']:.1f}%")