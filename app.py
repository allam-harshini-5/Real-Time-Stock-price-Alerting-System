import streamlit as st
import yfinance as yf
import smtplib
import time
from email.mime.text import MIMEText

# Title
st.title("📈 Real-Time Stock Price Alert System")

# Inputs
stock_symbol = st.text_input("Enter Stock Symbol (e.g., AAPL, TSLA)")
target_price = st.number_input("Enter Target Price", min_value=0.0, format="%.2f")

sender_email = st.text_input("Your Gmail")
app_password = st.text_input("App Password", type="password")
receiver_email = st.text_input("Receiver Email")

# Output area
output_area = st.empty()

# Function to get stock price
def get_stock_price(symbol):
    stock = yf.Ticker(symbol)
    data = stock.history(period="1d")
    return data["Close"].iloc[-1]

# Function to send email
def send_email(price):
    msg = MIMEText(f"{stock_symbol} has reached your target price!\nCurrent Price: {price}")
    msg["Subject"] = "Stock Price Alert 🚨"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        output_area.write(f"❌ Email Error: {e}")
        return False

# Start Monitoring
if st.button("Start Monitoring"):

    if stock_symbol and target_price and sender_email and app_password and receiver_email:
        output_area.write("📊 Monitoring started...")

        while True:
            try:
                current_price = get_stock_price(stock_symbol)
                output_area.write(f"📈 Current Price of {stock_symbol}: {current_price}")

                if current_price >= target_price:
                    output_area.write("✅ Target reached! Sending email...")
                    if send_email(current_price):
                        output_area.write("📧 Email sent successfully!")
                    break

                time.sleep(10)  # Check every 10 seconds

            except Exception as e:
                output_area.write(f"❌ Error: {e}")
                break

    else:
        st.warning("⚠️ Please fill all fields!")