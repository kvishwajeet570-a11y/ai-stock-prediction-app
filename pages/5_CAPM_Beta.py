import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px

# ------- PAGE TITLE ------------
st.title("CAPM Beta Dashboard")

stock_name = st.text_input("Enter Stock Name", "AAPL")

if st.button("Calculate Beta"):

    # ----------- download data -----------
    stock = yf.download(stock_name, period="2y", progress=False)
    market = yf.download("^GSPC", period="2y", progress=False)

    # ---------- returns ----------
    stock_return = stock["Close"].pct_change().dropna()
    market_return = market["Close"].pct_change().dropna()

    # ----------- merge -----------
    df = pd.concat([stock_return, market_return], axis=1)
    df.columns = ["Stock", "Market"]
    df.dropna(inplace=True)

    # ------------ BETA CALCULATION ---------------

    beta = np.cov(df["Stock"], df["Market"])[0][1] / np.var(df["Market"])

    st.success(f"CAPM Beta is: {round(beta,2)}")

    # ----------- SHOW DATA TABLE ----------------

    st.subheader("Return Data")

    st.dataframe(df, use_container_width=True)

    # -------- GRAPH WITH TRENDLINE ---------------

    fig = px.scatter(
        df,
        x="Market",
        y="Stock",
        title="Beta Visualization",
        trendline="ols"  
    )
    fig.update_layout(template="plotly_dark")

    st.plotly_chart(fig, use_container_width=True)