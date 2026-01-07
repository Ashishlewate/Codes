import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import random

# Page Config
st.set_page_config(page_title="AURA Dashboard", layout="wide")

# Modern Styling
st.markdown("""
    <style>
    .main { background-color: #0E1117; color: white; }
    .stCheckbox { margin-bottom: -15px; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ AURA : Performance & Wealth")

# Top Metrics Row (Looks very "Stock Market" aesthetic)
m1, m2, m3 = st.columns(3)
m1.metric("Net Worth Growth", "+12.5%", "High")
m2.metric("Consistency Score", "85%", "Stable")
m3.metric("Daily Focus", "4.5 hrs", "+0.5")

st.markdown("---")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Investment Projections")
    principal = st.number_input("Starting Capital ($)", value=5000)
    return_rate = st.slider("Annual Return (%)", 1, 40, 12)
    years = st.slider("Horizon (Years)", 1, 30, 15)
    
    data = [{"Year": y, "Value": principal * (1 + return_rate/100)**y} for y in range(years + 1)]
    df = pd.DataFrame(data)

with col2:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['Year'], y=df['Value'],
        mode='lines',
        line=dict(color='#8a2be2', width=4),
        fill='tozeroy',
        fillcolor='rgba(138, 43, 226, 0.2)'
    ))
    fig.update_layout(template="plotly_dark", height=350, margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig, use_container_width=True)

# Fixed Habit Tracker
st.subheader("Weekly Habit Consistency")
cols = st.columns(7)
days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

for i, col in enumerate(cols):
    # Fixed the "empty label" warning by giving it a name and hiding it
    col.checkbox(days[i], key=f"day_{i}", value=(i < 5), label_visibility="visible")