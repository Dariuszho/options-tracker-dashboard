import yfinance as yf
import pandas as pd
import streamlit as st

# -----------------------------
# Title of the Streamlit App
# -----------------------------
st.set_page_config(layout="wide")
st.title("📈 Options Chain Viewer (Paper Trading Tool)")

# -----------------------------
# Input Ticker Symbol from User
# -----------------------------
ticker_symbol = st.text_input("Enter a stock or ETF symbol:", value="AAPL").upper()

# Only continue if ticker is entered
if ticker_symbol:
    try:
        # Get the ticker data from Yahoo Finance
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info  # Get metadata

        # Try getting company name and price (fallback to history if needed)
        company_name = info.get("longName", "Company Name Not Found")
        current_price = info.get("currentPrice", None)

        # If price not found, get last close price from history
        if not current_price:
            hist = ticker.history(period="1d")
            current_price = hist["Close"].iloc[-1] if not hist.empty else "N/A"

        # Display the company info
        st.markdown(f"### 🏢 {company_name} ({ticker_symbol})")
        st.markdown(f"**Current Price:** ${current_price:.2f}" if isinstance(current_price, float) else "**Price not available**")

        # -----------------------------
        # Expiration Dates Dropdown
        # -----------------------------
        st.subheader("Select Expiration Date")
        exp_dates = ticker.options

        if exp_dates:
            expiry = st.selectbox("Choose Expiration Date", exp_dates)

            # Get the option chain for selected expiration
            opt_chain = ticker.option_chain(expiry)

            # Separate Calls and Puts
            calls = opt_chain.calls
            puts = opt_chain.puts

            # -----------------------------
            # Clean and Display CALLS Table
            # -----------------------------
            st.subheader("📞 Call Options")
            calls_display = calls[['strike', 'lastPrice', 'bid', 'ask', 'volume', 'openInterest', 'impliedVolatility']]
            calls_display.columns = ['Strike', 'Last Price', 'Bid', 'Ask', 'Volume', 'Open Interest', 'IV']
            st.dataframe(calls_display.set_index('Strike'))

            # -----------------------------
            # Clean and Display PUTS Table
            # -----------------------------
            st.subheader("📉 Put Options")
            puts_display = puts[['strike', 'lastPrice', 'bid', 'ask', 'volume', 'openInterest', 'impliedVolatility']]
            puts_display.columns = ['Strike', 'Last Price', 'Bid', 'Ask', 'Volume', 'Open Interest', 'IV']
            st.dataframe(puts_display.set_index('Strike'))

        else:
            st.warning("No options data available for this symbol.")

    except Exception as e:
        st.error(f"Error fetching data: {e}")
