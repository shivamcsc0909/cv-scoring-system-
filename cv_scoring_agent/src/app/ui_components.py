import plotly.graph_objects as go

def draw_score_chart(score):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={'text': "CV Match Score"},
        gauge={'axis': {'range': [0, 100]}}
    ))
    return fig
