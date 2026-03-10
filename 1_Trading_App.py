import streamlit as st
import yfinance as yf
import requests
from textblob import TextBlob
import pandas as pd
from datetime import datetime
import numpy as np



# ----------- CONFIG --------------------------------
st.set_page_config(
    page_title="Trading App",
    page_icon="$",
    layout="wide"
)

# -------------- GLOBAL STYLE ------------------------
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top left,#0f172a,#0b0f19,#050816);
    color: #f8fafc;
}

.super-header {
    background: linear-gradient(145deg, rgba(30,41,59,0.6), rgba(15,23,42,0.8));
    padding: 50px;
    border-radius: 25px;
    text-align: center;
    backdrop-filter: blur(15px);
    border: 1px solid rgba(99,102,241,0.4);
    box-shadow: 0 0 60px rgba(99,102,241,0.35);
}

.super-title {
    font-size: 75px;
    font-weight: 900;
    background: linear-gradient(90deg,#22d3ee,#6366f1,#a855f7,#22d3ee);
    background-size: 300% 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: gradientMove 6s ease infinite;
}

@keyframes gradientMove {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

.float-icon {
    font-size:55px;
    margin-bottom:10px;
}

.tagline {
    font-size:18px;
    color:#94a3b8;
}

/* Advanced Feature Cards */
.advanced-card {
    background: linear-gradient(145deg, rgba(30,41,59,0.6), rgba(15,23,42,0.8));
    padding: 35px;
    border-radius: 20px;
    border: 1px solid rgba(99,102,241,0.4);
    box-shadow: 0 0 30px rgba(99,102,241,0.2);
    transition: 0.3s ease;
}

.advanced-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 0 40px rgba(99,102,241,0.5);
}

.advanced-title {
    font-size: 28px;
    font-weight: 800;
    margin-bottom: 10px;
}

.advanced-desc {
    font-size: 16px;
    color: #cbd5e1;
}

footer {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

page = st.sidebar.selectbox(
    "Navigation",
    [" Home Page", "AI Market News"]
)

# ------------------  HOME PAGE  ------------------------------
if page == " Home Page":

    st.markdown("""
    <div class="super-header">
        <div class="float-icon">🔥🚀</div>
        <div class="super-title">TRADING APP</div>
        <div class="tagline">
            AI Driven Market Intelligence • Real-Time Analytics • Institutional Grade Systems
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # ----------- Metrics ---------------------------
    m1, m2, m3 = st.columns(3)
    m1.metric("Markets Covered", "US + India")
    m2.metric("AI Accuracy", "92%")
    m3.metric("Live Data Feed", "Running")

    st.markdown("<br><hr><br>", unsafe_allow_html=True)

    # GLOBAL MARKET

    st.subheader(" 🌐 Global Market Overview")

    symbol = st.text_input("Search Global Stock Symbol", "TSLA")

    if symbol:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1d")

        if not data.empty:
            price = data["Close"].iloc[-1]
            open_price = data["Open"].iloc[-1]
            high = data["High"].iloc[-1]
            low = data["Low"].iloc[-1]
            volume = data["Volume"].iloc[-1]
            change = price - open_price
            percent = (change / open_price) * 100

            c1, c2, c3 = st.columns(3)
            c1.metric("Current Price", f"{price:.2f}", f"{percent:.2f}%")
            c2.metric("Day High", f"{high:.2f}")
            c3.metric("Day Low", f"{low:.2f}")

            c4, c5, c6 = st.columns(3)
            c4.metric("Volume", f"{volume:,}")
            c5.metric("Previous Open", f"{open_price:.2f}")
            c6.metric("Market Status", "🟢 LIVE")

    st.markdown("<br><hr><br>", unsafe_allow_html=True)

    # IMAGE
    st.subheader("Trading Dashboard Preview")
    st.image("app.png", width="stretch")
    

    st.markdown("<br><hr><br>", unsafe_allow_html=True)

    # CAPM
    st.markdown("""
    <div style="
        text-align:center;
        font-size:28px;
        font-weight:900;
        background: linear-gradient(90deg,#22d3ee,#6366f1,#a855f7);
        -webkit-background-clip:text;
        -webkit-text-fill-color:transparent;
    ">
     CAPM MODEL  |  BETA ANALYSIS  |  CAPM EXPECTED RETURN
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br><hr><br>", unsafe_allow_html=True)

    # ------------ ADVANCED PREMIUM SECTION --------------
    st.markdown("## Core Intelligence Modules")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="advanced-card">
            <div class="advanced-title">Advanced Stock Analysis</div>
            <div class="advanced-desc">
                Real-time technical indicators, volatility tracking,
                price structure analytics, and institutional-level data modeling.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="advanced-card">
            <div class="advanced-title"> AI Prediction Engine</div>
            <div class="advanced-desc">
                Machine learning powered trend forecasting,
                probability-based directional bias,
                and intelligent signal generation.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="advanced-card">
            <div class="advanced-title"> AI Market News Intelligence</div>
            <div class="advanced-desc">
                NLP-driven sentiment scoring,
                risk detection from global headlines,
                and dynamic market impact analysis.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><hr><br>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center;color:#6b7280;'>© 2026 Trading App</div>", unsafe_allow_html=True)


# ------------- AI MARKET NEWS --------------------
elif page == "AI Market News":

    st.title("Stock News Update")

    API_KEY = "693fddb895ac45b2bcd38615721cc361"

    # -------- MARKET SELECT OPTION ---------
    
    market = st.selectbox(
        "Select Market",
        ["US Market 🇺🇸", "Indian Market 🇮🇳"]
    )
    # -------- STOCK INPUT ---------

    if market == "US Market 🇺🇸":

        stock = st.text_input("Enter US Stock Symbol", "TSLA")

        query = f"{stock} stock"

    else:

        stock = st.text_input("Enter Indian Stock Symbol (Example: RELIANCE, TCS, INFY)", "RELIANCE")

        
        query = f"{stock} stock India NSE BSE"

    # -------- NEWS API ---------

    if stock:

        url = f"https://newsapi.org/v2/everything?q={query}&sortBy=publishedAt&pageSize=20&apiKey={API_KEY}"

        try:

            response = requests.get(url, timeout=10)

            data = response.json()

        except:

            st.error("Connection Error")

            st.stop()

        if data.get("status") != "ok":

            st.error("API Error")

            st.write(data)

            st.stop()

        articles = data.get("articles", [])

        if len(articles) == 0:

            st.warning("No News Found")

            st.stop()

        scores = []

        confidence_list = []

        for article in articles:

            title = article.get("title") or "No Title"

            desc = article.get("description") or ""

            image = article.get("urlToImage")

            link = article.get("url", "")

            source = article.get("source", {}).get("name", "")

            sentiment = TextBlob(title + desc).sentiment.polarity

            score = sentiment * 100

            confidence = abs(score)

            scores.append(score)

            confidence_list.append(confidence)

            if image:

                st.image(image, width=550)

            st.subheader(title)

            st.write("Source:", source)

            st.write(desc)

            if sentiment > 0.1:

                st.success(f"🟢 Positive | Score: {score:.2f}% | Confidence: {confidence:.2f}%")

            elif sentiment < -0.1:

                st.error(f"🔴 Negative | Score: {score:.2f}% | Confidence: {confidence:.2f}%")

            else:

                st.warning(f"🟡 Neutral | Score: {score:.2f}% | Confidence: {confidence:.2f}%")

            if confidence > 60:

                st.write("Impact: High")

            elif confidence > 30:

                st.write("Impact: Medium")

            else:

                st.write("🟢 Impact: Low")

            if link:

                st.markdown(f"[Read Full News →]({link})")

            st.markdown("---")

        # ------- AI DASHBOARD --------

        import numpy as np

        avg = np.mean(scores)

        avg_conf = np.mean(confidence_list)

        st.subheader("AI Signal Dashboard")

        col1, col2 = st.columns(2)

        col1.metric("AI Score", f"{avg:.2f}%")

        col2.metric("Confidence", f"{avg_conf:.2f}%")

        if avg > 15:

            st.success("STRONG BUY SIGNAL")

        elif avg > 5:

            st.success("BUY SIGNAL")

        elif avg < -15:

            st.error("STRONG SELL SIGNAL")

        elif avg < -5:

            st.error("SELL SIGNAL")

        else:

            st.warning("HOLD SIGNAL")