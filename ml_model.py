import yfinance as yf
import numpy as np
from sklearn.linear_model import LinearRegression

def predict_price(symbol):
    stock = yf.Ticker(symbol)
    data = stock.history(period="1mo")

    if data.empty:
        return None, None

    data = data.reset_index()
    data["Day"] = np.arange(len(data))

    X = data[["Day"]]
    y = data["Close"]

    model = LinearRegression()
    model.fit(X, y)

    next_day = [[len(data)]]
    predicted_price = model.predict(next_day)[0]

    current_price = y.iloc[-1]

    # Trend prediction
    if predicted_price > current_price:
        trend = "UP 📈"
    else:
        trend = "DOWN 📉"

    return float(predicted_price), trend