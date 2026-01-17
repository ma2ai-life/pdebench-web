"""
View for displaying comparisons
"""

import streamlit as st
from interfaces.streamlit.components.plots import create_error_plot
from interfaces.streamlit.components.metrics import display_comparison_metrics

class ComparisonView:
    @staticmethod
    def display(comparison_result, comparison_metrics, comparison_summary):
        """Display comparison results"""
        if not comparison_result['success']:
            st.warning("Comparison not available. Run both solutions first.")
            return
        
        # Display metrics
        display_comparison_metrics(
            comparison_metrics['analytical_time'],
            comparison_metrics['numerical_time'],
            comparison_metrics['max_error']
        )
        
        # Error plot
        title = "Error Analysis"
        if comparison_result['data']['grids_match']:
            title += " (Same Grid)"
        else:
            title += f" (Interpolated to {len(comparison_result['data']['common_x'])} points)"
        
        fig_error = create_error_plot(
            comparison_result['data']['error'],
            comparison_result['data']['common_x'],
            title
        )
        st.plotly_chart(fig_error, use_container_width=True)
        
        # Summary
        st.markdown("### 📊 Comparison Summary")
        st.markdown(comparison_summary)
    
    @staticmethod
    def display_status(analytical_available, numerical_available):
        """Display comparison status"""
        if not analytical_available and not numerical_available:
            st.info("👈 Run both analytical and numerical solutions to enable comparison")
        elif not analytical_available:
            st.info("👈 Run analytical solution to compare with numerical")
        elif not numerical_available:
            st.info("👈 Run numerical solution to compare with analytical")
