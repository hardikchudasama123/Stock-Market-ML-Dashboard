DalaalStreet.ai is a high-performance, machine-learning-powered financial dashboard designed specifically for the Indian equity markets. By integrating real-time data from Yahoo Finance, it provides traders and analysts with an interactive environment to visualize historical trends, monitor technical health, and generate AI-driven price forecasts for the next trading day.

Key Features
Direct NSE/BSE Integration: Automated ticker suffix handling for seamless search of Indian stocks like RELIANCE, TCS, and ZOMATO.

Intelligent Visualization: Dynamic, high-visibility green line charts powered by Plotly for clear trend identification.

ML Price Forecasting: Utilizes a Random Forest Regressor trained on historical close prices, 10-day moving averages, and seasonal patterns (day/month) to predict tomorrow's closing price.

Localized Metrics: All financial data is rendered in Indian Rupees (₹) with percentage deltas for immediate impact assessment.

Error Profiling: Includes a built-in Mean Absolute Error (MAE) tracker to provide transparency regarding the model's historical accuracy.

The Tech Stack
Frontend: Streamlit (Modern Web Interface).

Data API: yfinance (Financial Data Scraping).

Machine Learning: Scikit-Learn (Random Forest Regression).

Analytics: Pandas & NumPy (Data Wrangling).

Plotting: Plotly (Interactive Graphic Objects).

How it Works
Data Ingestion: The app pulls the latest price data from the NSE/BSE servers, automatically correcting for recent yfinance multi-index data changes.

Feature Engineering: It calculates technical signals like the 10-day Moving Average and extracts temporal features from the date.

Training: Upon user request, the model trains on years of historical data to find hidden patterns.

Insight: The dashboard displays the "Current Price" vs. the "AI Predicted Price," giving users a data-backed starting point for their daily market research.
