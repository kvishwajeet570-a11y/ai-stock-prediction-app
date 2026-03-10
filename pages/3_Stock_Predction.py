import streamlit as st
from model_train import (
    get_data,
    get_rolling_mean,
    get_differencing_order,
    evaluate_model,
    get_forecast
)
import pandas as pd
from plotly_figure import plotly_table, moving_average_forecast
import plotly.graph_objects as go
import numpy as np

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title=" Stock Prediction Dashboard ",
    page_icon="💲",
    layout="wide"
)

st.title(" Stock Prediction Dashboard ")

# ---------------- STOCK INPUT ----------------
col1, col2, col3 = st.columns([2,2,1])

us_stocks = ["AAPL", "TSLA", "MSFT", "NVDA", "AMZN"]
indian_stocks = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "SBIN.NS", "AMZN"]

with col1:
    market = st.selectbox("Select Market", ["US Market", "Indian Market"])

with col2:
    if market == "US Market":
        ticker = st.selectbox("Select Stock", us_stocks)
    else:
        ticker = st.selectbox("Select Stock", indian_stocks)

with col3:
    custom = st.text_input("Custom Symbol")

if custom:
    ticker = custom.upper()

st.subheader(f"30-Day Forecast for: {ticker}")

# ---------------- DATA ----------------
close_price = get_data(ticker)

if close_price.empty:
    st.error("Invalid Ticker or No Data Available")
    st.stop()

rolling_price = get_rolling_mean(close_price)

if rolling_price.empty:
    st.error("Not enough data.")
    st.stop()

differencing_order = get_differencing_order(rolling_price)

# ---------------- MODEL ----------------
rmse = evaluate_model(rolling_price, differencing_order)
forecast = get_forecast(rolling_price, differencing_order)

forecast.index = pd.to_datetime(forecast.index)

last_actual = float(rolling_price.iloc[-1].iloc[0])
last_forecast = float(forecast.iloc[-1].iloc[0])

growth_percent = ((last_forecast - last_actual) / last_actual) * 100

returns = rolling_price.pct_change().dropna()
volatility = float(returns.std().iloc[0] * np.sqrt(252) * 100)

risk_free_rate = 0.02
if returns.std().iloc[0] != 0:
    expected_return = returns.mean().iloc[0] * 252
    sharpe_ratio = (expected_return - risk_free_rate) / returns.std().iloc[0]
else:
    sharpe_ratio = 0

momentum = float(rolling_price.iloc[-1].iloc[0] - rolling_price.iloc[-10].iloc[0])

# ---------------- METRICS ----------------
colA, colB, colC, colD = st.columns(4)

colA.metric("RMSE", f"{rmse:.2f}")
colB.metric("Expected Growth %", f"{growth_percent:.2f}%")
colC.metric("Volatility %", f"{volatility:.2f}%")
colD.metric("Sharpe Ratio", f"{sharpe_ratio:.2f}")

# ---------------- SMART SIGNAL ----------------
st.markdown("### Smart AI Signal")

signal_score = 0

if growth_percent > 2:
    signal_score += 1
if sharpe_ratio > 1:
    signal_score += 1
if momentum > 0:
    signal_score += 1
if volatility < 40:
    signal_score += 1

if signal_score >= 3:
    st.success("STRONG BUY")
elif signal_score == 2:
    st.info("BUY")
elif signal_score == 1:
    st.warning("HOLD")
else:
    st.error("SELL")

# ---------------- FORECAST TABLE ----------------
st.write("### Forecast Table")

fig_tail = plotly_table(forecast.sort_index().round(3))
fig_tail.update_layout(height=250)
st.plotly_chart(fig_tail, width="stretch")

# ---------------- CONFIDENCE BAND ----------------
fig_conf = go.Figure()

fig_conf.add_trace(go.Scatter(
    x=forecast.index,
    y=forecast['Close'],
    mode='lines',
    name='Forecast'
))

upper = forecast['Close'] * 1.05
lower = forecast['Close'] * 0.95

fig_conf.add_trace(go.Scatter(
    x=forecast.index,
    y=upper,
    line=dict(width=0),
    showlegend=False
))

fig_conf.add_trace(go.Scatter(
    x=forecast.index,
    y=lower,
    fill='tonexty',
    name='Confidence Band',
    opacity=0.2
))

fig_conf.update_layout(
    template="plotly_dark",
    height=450,
    title="Forecast Confidence Range"
)

st.plotly_chart(fig_conf, width="stretch")

# ---------------- HISTORICAL + FORECAST ------------------------
rolling_price.index = pd.to_datetime(rolling_price.index)
combined_data = pd.concat([rolling_price, forecast])

plot_data = combined_data.iloc[-150:]

st.write("### Historical + Forecast")

st.plotly_chart(
    moving_average_forecast(plot_data),
    width="stretch"
)