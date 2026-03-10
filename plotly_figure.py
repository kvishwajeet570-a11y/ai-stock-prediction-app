import plotly.graph_objects as go
from plotly.subplots import make_subplots
import ta
import pandas as pd


# -------------------- DARK LAYOUT --------------------
def apply_dark_layout(fig, height=600):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0e1117",
        plot_bgcolor="#0e1117",
        font=dict(color="white"),
        height=height,
        margin=dict(l=20, r=20, t=40, b=20),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=1.02,
            xanchor="right",
            x=1
        ),
        xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)"),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)")
    )
    return fig


# -------------------- DATA FILTER --------------------
def filter_data(dataframe, num_period):

    period_map = {
        "1d": 1,
        "5d": 5,
        "1mo": 30,
        "3mo": 90,
        "6mo": 180,
        "1y": 252,
        "2y": 504,
        "5y": 1260,
        "10y": 2520,
        "max": len(dataframe)
    }

    if isinstance(num_period, str):
        num_period = period_map.get(num_period, 252)

    return dataframe.tail(int(num_period))


# -------------------- CANDLESTICK --------------------
def candlestick(dataframe, num_period):

    dataframe = filter_data(dataframe, num_period)

    fig = go.Figure()

    fig.add_trace(go.Candlestick(
        x=dataframe.index,
        open=dataframe['Open'],
        high=dataframe['High'],
        low=dataframe['Low'],
        close=dataframe['Close'],
        increasing_line_color="#00ff9d",
        decreasing_line_color="#ff4d4d",
        name="Price"
    ))

    fig.update_layout(xaxis_rangeslider_visible=False)

    return apply_dark_layout(fig, height=700)


# -------------------- CLOSE PRICE --------------------
def close_chart(dataframe, num_period):

    dataframe = filter_data(dataframe, num_period)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=dataframe.index,
        y=dataframe['Close'],
        mode='lines',
        name='Close Price',
        line=dict(color="#00ff9d", width=2)
    ))

    fig.update_xaxes(rangeslider_visible=False)

    return apply_dark_layout(fig, height=600)


# -------------------- RSI --------------------
def RSI(dataframe, num_period):

    dataframe = filter_data(dataframe, num_period)

    dataframe['RSI'] = ta.momentum.RSIIndicator(
        close=dataframe['Close']
    ).rsi()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=dataframe.index,
        y=dataframe['RSI'],
        line=dict(color="#f59e0b", width=2),
        name="RSI"
    ))

    fig.add_hline(y=70, line_dash="dash", line_color="red")
    fig.add_hline(y=30, line_dash="dash", line_color="green")

    fig.update_yaxes(range=[0, 100])

    return apply_dark_layout(fig, height=300)


# -------------------- MOVING AVERAGE --------------------
def Moving_average(dataframe, num_period):

    dataframe = filter_data(dataframe, num_period)

    dataframe['SMA_50'] = ta.trend.sma_indicator(
        dataframe['Close'], window=50
    )

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=dataframe.index,
        y=dataframe['Close'],
        name="Close",
        line=dict(color="#00ff9d", width=2)
    ))

    fig.add_trace(go.Scatter(
        x=dataframe.index,
        y=dataframe['SMA_50'],
        name="SMA 50",
        line=dict(color="#f59e0b", width=2)
    ))

    return apply_dark_layout(fig, height=600)


# -------------------- MACD --------------------
def MACD(dataframe, period='1y'):

    df = dataframe.copy()

    if period != 'max':
        try:
            df = df.last(period)
        except:
            pass

    exp1 = df['Close'].ewm(span=12, adjust=False).mean()
    exp2 = df['Close'].ewm(span=26, adjust=False).mean()

    macd_line = exp1 - exp2
    signal_line = macd_line.ewm(span=9, adjust=False).mean()
    histogram = macd_line - signal_line

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df.index,
        y=macd_line,
        name='MACD',
        line=dict(color='cyan', width=2)
    ))

    fig.add_trace(go.Scatter(
        x=df.index,
        y=signal_line,
        name='Signal',
        line=dict(color='orange', width=2)
    ))

    fig.add_trace(go.Bar(
        x=df.index,
        y=histogram,
        name='Histogram'
    ))

    fig.update_layout(
        template="plotly_dark",
        height=350,
        xaxis_rangeslider_visible=False
    )

    return fig


# -------------------- PRICE + RSI --------------------
def price_with_rsi(dataframe, num_period):

    dataframe = filter_data(dataframe, num_period)

    dataframe['RSI'] = ta.momentum.RSIIndicator(
        close=dataframe['Close']
    ).rsi()

    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        row_heights=[0.7, 0.3]
    )

    fig.add_trace(
        go.Candlestick(
            x=dataframe.index,
            open=dataframe['Open'],
            high=dataframe['High'],
            low=dataframe['Low'],
            close=dataframe['Close'],
            increasing_line_color="#00ff9d",
            decreasing_line_color="#ff4d4d"
        ),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(
            x=dataframe.index,
            y=dataframe['RSI'],
            line=dict(color="#f59e0b", width=2),
            name="RSI"
        ),
        row=2, col=1
    )

    fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
    fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)

    fig.update_yaxes(range=[0, 100], row=2, col=1)

    fig.update_layout(xaxis_rangeslider_visible=False)

    return apply_dark_layout(fig, height=750)


# -------------------- TABLE --------------------
def plotly_table(dataframe):

    fig = go.Figure(data=[go.Table(
        header=dict(
            values=list(dataframe.columns),
            fill_color="#1f2937",
            font=dict(color="white")
        ),
        cells=dict(
            values=[dataframe[col] for col in dataframe.columns],
            fill_color="#111827",
            font=dict(color="white")
        )
    )])

    fig.update_layout(template="plotly_dark", height=400)

    return fig


# -------------------- FORECAST --------------------
def moving_average_forecast(data):

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['Close'],
        mode='lines',
        name='Close Price'
    ))

    fig.update_layout(
        title="Historical + Forecast Close Price",
        template="plotly_dark"
    )

    return fig