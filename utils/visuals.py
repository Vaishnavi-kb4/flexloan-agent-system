import plotly.graph_objects as go
import pandas as pd

def plot_income_forecast(history_df, forecast_min, forecast_max, current_month):
    """
    Plots historical income versus the forecasted safe range for the next month.
    """
    fig = go.Figure()
    
    # Historical Data
    fig.add_trace(go.Scatter(
        x=history_df['Month'], 
        y=history_df['Income'],
        mode='lines+markers',
        name='Historical Income',
        line=dict(color='#636EFA')
    ))
    
    # Forecast Range (represented as a bar or error bar at the next month)
    next_month = current_month + 1
    
    fig.add_trace(go.Bar(
        x=[next_month],
        y=[forecast_max - forecast_min],
        base=[forecast_min],
        name='Forecasted Safe Range',
        marker_color='rgba(0, 204, 150, 0.5)',
        hoverinfo='y+name'
    ))

    fig.update_layout(
        title="Income Analysis & Forecast",
        xaxis_title="Month",
        yaxis_title="Income (INR)",
        template="plotly_white",
        showlegend=True
    )
    return fig

def plot_risk_gauge(risk_score):
    """
    Plots a gauge chart for the risk score.
    """
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = risk_score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Dynamic Risk Score"},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 30], 'color': "lightgreen"},
                {'range': [30, 70], 'color': "yellow"},
                {'range': [70, 100], 'color': "salmon"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(height=300)
    return fig
