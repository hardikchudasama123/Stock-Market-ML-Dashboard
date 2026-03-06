import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# --- 1. Page Configuration ---
st.set_page_config(page_title="DalaalStreet.ai", layout="wide")
st.title("📈 DalaalStreet.ai")

# --- 2. Sidebar Settings ---
st.sidebar.header("NSE/BSE Input")
ticker_input = st.sidebar.text_input("Enter Ticker (e.g. RELIANCE, TCS)", value="TCS")
exchange = st.sidebar.selectbox("Exchange", ["NSE", "BSE"])
ticker_symbol = f"{ticker_input}.NS" if exchange == "NSE" else f"{ticker_input}.BO"

start_date = st.sidebar.date_input("Start Date", value=datetime.now() - timedelta(days=365*2))
end_date = st.sidebar.date_input("End Date", value=datetime.now())

# Footer in Sidebar
st.sidebar.divider()
st.sidebar.markdown("""
    <div style="text-align: center; color: gray; font-size: 11px; padding: 10px;">
    Developed by [Hardik] | © 2026 All rights reserved.
    </div>
    """, unsafe_allow_html=True)




# Fetching Data
@st.cache_data
def load_data(ticker, start, end):
    # 'multi_level_index=False' prevents Multi-Index data structure errors
    data = yf.download(ticker, start=start, end=end, multi_level_index=False)
    data.reset_index(inplace=True)
    return data

try:
    df = load_data(ticker_symbol, start_date, end_date)

    if df.empty:
        st.error("No data found. Check the ticker symbol.")
    else:
        # --- 3. Visualization ---
        st.subheader(f"Historical Price for {ticker_symbol}")
        fig = go.Figure()
        
        # --- COLOR CHANGE HERE ---
        # Changed 'line=dict(color=...)' to green
        fig.add_trace(go.Scatter(x=df['Date'], 
                                 y=df['Close'], 
                                 name="Close Price",
                                 line=dict(color='#00CC44'))) # A sharp, bright green
        
        fig.layout.update(xaxis_rangeslider_visible=True, template="plotly_dark")
        # Updated: width="stretch" removes recent console warnings
        st.plotly_chart(fig, width="stretch")

        # --- 4. Machine Learning Section ---
        st.subheader("AI Next-Day Prediction")

        # Simple Feature Engineering
        df['Day_of_Week'] = df['Date'].dt.dayofweek
        df['Month'] = df['Date'].dt.month
        df['MA_10'] = df['Close'].rolling(window=10).mean()
        df_ml = df.dropna().copy()

        # Preparing Features (X) and Target (y)
        X = df_ml[['Close', 'Day_of_Week', 'Month', 'MA_10']].values[:-1]
        y = df_ml['Close'].values[1:].ravel() # Ensure target is 1D

        # Train Model (Using shuffle=False because time series order matters)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # Predict for the very next day
        latest_features = df_ml[['Close', 'Day_of_Week', 'Month', 'MA_10']].tail(1).values
        prediction = model.predict(latest_features)[0]
        
        # Get last closing price
        last_price = float(df_ml['Close'].iloc[-1])

        # Metric Display with Rupee Symbol
        col1, col2 = st.columns(2)
        col1.metric("Current Price", f"₹{last_price:,.2f}")
        
        change_pct = ((prediction - last_price) / last_price) * 100
        col2.metric("Predicted Target Price", f"₹{prediction:,.2f}", delta=f"{change_pct:.2f}%")
        st.warning("⚠️ **Note:** This BETA model is for demonstration only. Stock markets are unpredictable")

except Exception as e:

    st.error(f"Prediction Error: {e}")

