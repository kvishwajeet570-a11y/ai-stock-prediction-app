import datetime
import yfinance as yf
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import ta
from plotly_figure import candlestick, RSI, MACD, close_chart, Moving_average, price_with_rsi


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="heavy_dollar_sign",
    page_icon="💲",
    layout="wide",
)

# ---------------- TRADINGVIEW STYLE CSS ----------------
st.markdown("""
<style>

body {
    background-color: #0e1117;
}

.main {
    background-color: #0e1117;
    color: white;
}

h1, h2, h3 {
    color: #ffffff;
}

[data-testid="stMetricValue"] {
    font-size: 22px;
    font-weight: bold;
    color: #00ff88;
}

[data-testid="stMetricDelta"] {
    font-size: 16px;
}

.stDataFrame {
    background-color: #161b22;
    border-radius: 10px;
}

.stButton>button {
    background-color: #1f2937;
    color: white;
    border-radius: 8px;
}

.stSelectbox label {
    color: white !important;
}

</style>
""", unsafe_allow_html=True)


st.title("Stock Analysis Dashboard")

col1, col2, col3 = st.columns(3)

today = datetime.date.today()

with col1:
    ticker = st.text_input("Stock Ticker", "TSLA")

with col2:
    start_date = st.date_input(
        "Choose Start Date",
        datetime.date(today.year - 1, today.month, today.day),
    )

with col3:
    end_date = st.date_input(
        "Choose End Date",
        datetime.date(today.year, today.month, today.day),
    )

# ---------------- STOCK INFO ----------------
stock = yf.Ticker(ticker)
info = stock.info

st.subheader(f"{ticker} Company Overview")

st.write(info.get('longBusinessSummary', 'No summary available.'))
st.write("**Sector:**", info.get('sector', 'N/A'))
st.write("**Full Time Employees:**", info.get('fullTimeEmployees', 'N/A'))
st.write("**Website:**", info.get('website', 'N/A'))

# ---------------- METRICS ----------------
col1, col2 = st.columns(2)

with col1:
    basic_df = pd.DataFrame({
        "Metric": ["Market Cap", "Beta", "EPS", "PE Ratio"],
        "Value": [
            info.get("marketCap", "N/A"),
            info.get("beta", "N/A"),
            info.get("trailingEps", "N/A"),
            info.get("trailingPE", "N/A"),
        ]
    })

    st.subheader(" Basic Metrics")
    st.dataframe(basic_df, width='stretch')

with col2:
    financial_df = pd.DataFrame({
        "Metric": [
            "Quick Ratio",
            "Revenue per Share",
            "Profit Margins",
            "Debt to Equity",
            "Return on Equity"
        ],
        "Value": [
            info.get("quickRatio", "N/A"),
            info.get("revenuePerShare", "N/A"),
            info.get("profitMargins", "N/A"),
            info.get("debtToEquity", "N/A"),
            info.get("returnOnEquity", "N/A"),
        ]
    })

    st.subheader(" Financial Ratios")
    st.dataframe(financial_df, width='stretch')

# ---------------- PRICE DATA ----------------
data = yf.download(ticker, start=start_date, end=end_date)

if not data.empty:

    st.subheader(" Price Performance")

    colA, colB = st.columns(2)

    daily_change = data['Close'].iloc[-1] - data['Close'].iloc[-2]

    colA.metric(
        "Latest Price",
        f"${round(data['Close'].iloc[-1],2)}",
        f"{round(daily_change,2)}"
    )

    colB.metric(
        "Volume",
        int(data['Volume'].iloc[-1])
    )

    st.line_chart(data["Close"])

    last_10_df = data.tail(10).round(2)
    st.subheader("Historical Data (Last 10 Days)")
    st.dataframe(last_10_df, width='stretch')

else:
    st.warning("No data available for selected date range.")

# ---------------- PERIOD BUTTONS ----------------
if 'selected_period' not in st.session_state:
    st.session_state.selected_period = '1y'

cols = st.columns(10)
periods = ['1d','5d','1mo','3mo','6mo','1y','2y','5y','10y','max']

for i, p in enumerate(periods):
    if cols[i].button(p.upper()):
        st.session_state.selected_period = p

num_period = st.session_state.selected_period

# ---------------- CHART CONTROLS ----------------
col1, col2 = st.columns([1,1])

with col1:
    chart_type = st.selectbox("Select Chart Type", ["Line Chart", "Candlestick Chart"])

with col2:
    if chart_type == "Candlestick Chart":
        indicators = st.selectbox("Select Indicator", ['RSI', 'MACD'])
    else:
        indicators = st.selectbox("Select Indicator", ['RSI', 'Moving Average', 'MACD'])

ticker_ = yf.Ticker(ticker)
new_df1 = ticker_.history(period='max')
data = ticker_.history(period='max')
data1 = new_df1
if num_period == '':
   #-------------------Indicator----------------------------------
  if chart_type == 'Candlestick Chart' and indicators == 'RSI':
    st.plotly_chart(candlestick(data1, '1y'), use_container_width=True)
    st.plotly_chart(RSI(data1, '1y'), use_container_width=True)

  if chart_type == 'Candlestick Chart' and indicators == 'MACD':
    st.plotly_chart(candlestick(data1, '1y'), use_container_width=True)
    st.plotly_chart(MACD(data1, '1y'), use_container_width=True)

  if chart_type == 'Line Chart' and indicators == 'RSI':
    st.plotly_chart(close_chart(data1, '1y'), use_container_width=True)
    st.plotly_chart(RSI(data1, '1y'), use_container_width=True)

  if chart_type == 'Line Chart' and indicators == 'Moving Average':
    st.plotly_chart(Moving_average(data1, '1y'), use_container_width=True)

  if chart_type == 'Line Chart' and indicators == 'MACD':
    st.plotly_chart(close_chart(data1, '1y'), use_container_width=True)
    st.plotly_chart(MACD(data, '1y'), use_container_width=True)
    
else: # ---------------- CHART DISPLAY ----------------
 if chart_type == 'Candlestick Chart' and indicators == 'RSI':
    fig = price_with_rsi(new_df1, num_period)
    st.plotly_chart(fig, width='stretch')

 elif chart_type == 'Candlestick Chart' and indicators == 'MACD':
    st.plotly_chart(candlestick(new_df1, num_period), width='stretch')
    st.plotly_chart(MACD(new_df1, num_period), width='stretch')

 elif chart_type == 'Line Chart' and indicators == 'RSI':
    st.plotly_chart(close_chart(new_df1, num_period), width='stretch')
    st.plotly_chart(RSI(new_df1, num_period), width='stretch')

 elif chart_type == 'Line Chart' and indicators == 'Moving Average':
    st.plotly_chart(Moving_average(new_df1, num_period), width='stretch')
    
 elif chart_type == 'Line Chart' and indicators == 'MACD':
    st.plotly_chart(close_chart(new_df1, num_period), width='stretch')
    st.plotly_chart(MACD(new_df1, num_period), width='stretch')