
# -------- IMPORT LIBRARIES ------------

import streamlit as st
import pandas as pd
import yfinance as yf
import datetime
import numpy as np
import plotly.express as px

# ------------ FUNCTIONS ---------------

def interactive_plot(df):
    fig = px.line(df, x="Date", y=df.columns[1:])
    fig.update_layout(height=500)
    return fig


def normalize(df):
    df_copy = df.copy()
    for col in df_copy.columns[1:]:
        df_copy[col] = df_copy[col] / df_copy[col].iloc[0]
    return df_copy


def daily_return(df):
    df_return = df.copy()
    for col in df.columns[1:]:
        df_return[col] = df[col].pct_change() * 100
    df_return.fillna(0, inplace=True)
    return df_return


def calculate_beta(df, stock):
    x = df['sp500']
    y = df[stock]
    beta, alpha = np.polyfit(x, y, 1)
    return beta

# ---------- PAGE CONFIG -----------------

st.set_page_config(page_title="CAPM Dashboard", layout="wide")
st.title("CAPM Dashboard")

# ------------- USER INPUT ----------------

col1, col2 = st.columns(2)
with col1:
    stocks_list = st.multiselect(
        "Select Stocks",
        ['TSLA','AAPL','MSFT','AMZN','GOOGL','NVDA'],
        default=['TSLA','AAPL']
    )
with col2:
    year = st.slider("Select Years", 1, 10, 1)


# ------------- MAIN LOGIC ----------------------

if len(stocks_list) == 0:
    st.warning("Please select at least one stock.")
    st.stop()

try:
    
    end = datetime.date.today()
    start = datetime.date(end.year - year, end.month, end.day)

    # ----- Download Market Data -----
    sp500 = yf.download("^GSPC", start=start, end=end, progress=False)

    # ---- Download Stock Data ----
    stocks_df = pd.DataFrame()

    for stock in stocks_list:
        data = yf.download(stock, start=start, end=end, progress=False)
        stocks_df[stock] = data["Close"]

    stocks_df.reset_index(inplace=True)
    sp500.reset_index(inplace=True)

    sp500 = sp500[['Date','Close']]
    sp500.columns = ['Date','sp500']

    stocks_df = pd.merge(stocks_df, sp500, on="Date")

    st.success("Data Loaded Successfully")

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Head")
        st.dataframe(stocks_df.head(), use_container_width=True)

    with c2:
        st.subheader("Tail")
        st.dataframe(stocks_df.tail(), use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        st.subheader("Stock Prices")
        st.plotly_chart(interactive_plot(stocks_df), use_container_width=True)

    with c4:
        st.subheader("Normalized Prices")
        st.plotly_chart(interactive_plot(normalize(stocks_df)), use_container_width=True)

    # --------- DAILY RETURNS ---------------

    returns_df = daily_return(stocks_df)

    # ----------- BETA -------------

    beta_dict = {}

    for stock in stocks_list:
        beta_dict[stock] = round(calculate_beta(returns_df, stock), 2)

    beta_df = pd.DataFrame({
        "Stock": beta_dict.keys(),
        "Beta": beta_dict.values()
    })

    # -------- CAPM RETURN ------------

    rf = 0
    rm = returns_df["sp500"].mean() * 252

    return_df = pd.DataFrame({
        "Stock": beta_dict.keys(),
        "Expected Return": [
            round(rf + beta*(rm-rf), 2)
            for beta in beta_dict.values()
        ]
    })

    c5, c6 = st.columns(2)

    with c5:
        st.subheader("Beta Values")
        st.dataframe(beta_df, use_container_width=True)

    with c6:
        st.subheader("CAPM Expected Return")
        st.dataframe(return_df, use_container_width=True)

except Exception as e:
    st.error(f"Error: {e}")