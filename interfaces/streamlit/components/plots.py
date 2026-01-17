"""
Plotting components for 2D and 3D visualizations
"""

import plotly.graph_objects as go
import numpy as np

def create_2d_plot(u, x, t, title="Solution", color='red'):
    """Create a 2D plot of solution evolution"""
    fig = go.Figure()
    
    # Initial condition
    fig.add_trace(go.Scatter(
        x=x, y=u[0, :],
        name='Initial (t=0)',
        line=dict(color='blue', dash='dash', width=2),
        hovertemplate='x=%{x:.3f}<br>u=%{y:.3f}<extra></extra>'
    ))
    
    # Final solution
    fig.add_trace(go.Scatter(
        x=x, y=u[-1, :],
        name=f'Final (t={t[-1]:.2f})',
        line=dict(color=color, width=3),
        hovertemplate='x=%{x:.3f}<br>u=%{y:.3f}<extra></extra>'
    ))
    
    # Update layout
    fig.update_layout(
        title=dict(text=title, font=dict(size=18)),
        xaxis_title="Position (x)",
        yaxis_title="Temperature u(x,t)",
        height=400,
        template="plotly_white",
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor='rgba(255, 255, 255, 0.8)'
        ),
        hovermode='x unified'
    )
    
    return fig

def create_3d_plot(u, x, t, title="3D View", colorscale='Viridis'):
    """Create a 3D surface plot of solution evolution"""
    X, T_mesh = np.meshgrid(x, t)
    
    fig = go.Figure(data=[
        go.Surface(
            z=u,
            x=X,
            y=T_mesh,
            colorscale=colorscale,
            opacity=0.9,
            contours={
                "z": {"show": True, "usecolormap": True}
            },
            hovertemplate='x=%{x:.3f}<br>t=%{y:.3f}<br>u=%{z:.3f}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=20)),
        scene=dict(
            xaxis_title='Position (x)',
            yaxis_title='Time (t)',
            zaxis_title='Temperature u(x,t)',
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))
        ),
        height=500,
        margin=dict(l=0, r=0, b=0, t=40)
    )
    
    return fig

def create_error_plot(error, x, title="Error Analysis"):
    """Create an error plot"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=x, y=error,
        mode='lines',
        name='Absolute Error',
        line=dict(color='red', width=2),
        hovertemplate='x=%{x:.3f}<br>error=%{y:.6f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title="Position (x)",
        yaxis_title="Error |u_numeric - u_analytic|",
        height=350,
        template="plotly_white"
    )
    
    return fig
