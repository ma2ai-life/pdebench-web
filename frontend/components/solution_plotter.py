import plotly.graph_objects as go
import numpy as np
import streamlit as st

def plot_2d_solution(x, u_final, u_initial=None, title="Solution"):
    """Create 2D plot of solution"""
    fig = go.Figure()
    
    if u_initial is not None:
        fig.add_trace(go.Scatter(
            x=x, y=u_initial,
            mode='lines',
            name='Initial (t=0)',
            line=dict(color='blue', dash='dash', width=2)
        ))
    
    fig.add_trace(go.Scatter(
        x=x, y=u_final,
        mode='lines',
        name='Final Solution',
        line=dict(color='red', width=3)
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title="Position (x)",
        yaxis_title="Temperature u(x,t)",
        height=400,
        template="plotly_white",
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
    )
    
    return fig

def plot_3d_solution(x, t, u, title="Time Evolution"):
    """Create 3D surface plot"""
    X, T_mesh = np.meshgrid(x, t)
    
    fig = go.Figure(data=[
        go.Surface(
            z=u,
            x=X,
            y=T_mesh,
            colorscale='Viridis',
            opacity=0.9,
            contours={
                "z": {"show": True, "usecolormap": True}
            }
        )
    ])
    
    fig.update_layout(
        title=title,
        scene=dict(
            xaxis_title='Position (x)',
            yaxis_title='Time (t)',
            zaxis_title='Temperature u(x,t)',
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))
        ),
        height=500
    )
    
    return fig

def plot_error(x, u_numerical, u_analytical, title="Error Analysis"):
    """Plot error between numerical and analytical solutions"""
    error = np.abs(u_numerical - u_analytical)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x, y=error,
        mode='lines',
        name='Absolute Error',
        line=dict(color='red', width=2)
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title="Position (x)",
        yaxis_title="Error |u_numeric - u_analytic|",
        height=350,
        template="plotly_white"
    )
    
    return fig