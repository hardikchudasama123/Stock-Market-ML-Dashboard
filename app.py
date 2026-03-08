import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- Page Configuration ---
st.set_page_config(page_title="DalaalStreet.ai", layout="wide")
st.title("📈 DalaalStreet.ai - Strategy Dashboard")

# --- Sidebar ---
st.sidebar.header("Stock Input")

ticker_input = st.sidebar.text_input("Enter Ticker (e.g. RELIANCE, TCS)", value="TCS")
exchange = st.sidebar.selectbox("Exchange", ["NSE", "BSE"])

ticker_symbol = f"{ticker_input}.NS" if exchange == "NSE" else f"{ticker_input}.BO"

start_date = st.sidebar.date_input(
    "Start Date", value=datetime.now() - timedelta(days=365)
)
end_date = st.sidebar.date_input("End Date", value=datetime.now())

# Sidebar footer
st.sidebar.divider()
st.sidebar.markdown(
"""
<div style="text-align:center; font-size:11px; color:gray;">
Developed by Hardik | © 2026
</div>
""",
unsafe_allow_html=True
)

# --- Load Data ---
@st.cache_data
def load_data(ticker, start, end):

    data = yf.download(
        ticker,
        start=start,
        end=end,
        multi_level_index=False
    )

    data.reset_index(inplace=True)

    return data


try:

    df = load_data(ticker_symbol, start_date, end_date)

    if df.empty:
        st.error("No data found for this ticker.")
        st.stop()

    df = df.copy()

    # Ensure numeric values
    df['Close'] = pd.to_numeric(df['Close'])

    # --- Indicator Calculations ---

    # EMA
    df['EMA20'] = df['Close'].ewm(span=20).mean()
    df['EMA50'] = df['Close'].ewm(span=50).mean()

    # --- RSI Calculation ---
    delta = df['Close'].diff()

    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()

    rs = gain / loss

    df['RSI'] = 100 - (100 / (1 + rs))

    # --- Strategy Logic (Momentum Pullback Strategy) ---

    df['Buy_Signal'] = np.where(
        (df['Close'] > df['EMA50']) &
        (df['EMA20'] > df['EMA50']) &
        (df['RSI'] > 40) &
        (df['RSI'] < 50) &
        (abs(df['Close'] - df['EMA20']) / df['EMA20'] < 0.01),
        1,
        0
    )

    buy_signals = df[df['Buy_Signal'] == 1]

    # --- Chart ---
    st.subheader(f"{ticker_symbol} Strategy Chart")

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df['Date'],
            y=df['Close'],
            name="Close Price"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df['Date'],
            y=df['EMA20'],
            name="EMA20"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df['Date'],
            y=df['EMA50'],
            name="EMA50"
        )
    )

    # Buy signals
    fig.add_trace(
        go.Scatter(
            x=buy_signals['Date'],
            y=buy_signals['Close'],
            mode='markers',
            name='Buy Signal',
            marker=dict(
                symbol="triangle-up",
                size=12
            )
        )
    )

    fig.update_layout(
        template="plotly_dark",
        xaxis_rangeslider_visible=True
    )

    st.plotly_chart(fig, width="stretch")

    # --- Show Recent Signals ---
    st.subheader("Recent Buy Signals")

    st.dataframe(
        buy_signals[['Date', 'Close', 'RSI']].tail(10)
    )

    st.warning(
        "⚠️ Educational use only. Not financial advice."
    )

except Exception as e:

    st.error(f"Application Error: {e}")
