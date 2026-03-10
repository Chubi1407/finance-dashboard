import yfinance as yf
import pandas as pd

def get_stock_data(tickers, start_date, end_date):
    # grab closing prices for each stock over the date range
    data = yf.download(tickers, start=start_date, end=end_date, auto_adjust=True)["Close"]

    # yfinance returns a Series for single tickers, convert it to a DataFrame
    if isinstance(data, pd.Series):
        data = data.to_frame(name=tickers[0])

    return data

def calculate_daily_returns(price_data):
    # day over day percentage change
    return price_data.pct_change().dropna()

def calculate_cumulative_returns(daily_returns):
    # tracks how $1 invested on day 1 grows over time
    return (1 + daily_returns).cumprod()

def calculate_sharpe_ratio(daily_returns, risk_free_rate=0.05):
    # how much return you get per unit of risk taken
    # above 1.0 is good, above 2.0 is exceptional
    trading_days = 252
    excess_returns = daily_returns.mean() * trading_days - risk_free_rate
    volatility = daily_returns.std() * (trading_days ** 0.5)
    return (excess_returns / volatility).round(2)

def calculate_max_drawdown(cumulative_returns):
    # worst drop from peak to bottom over the period
    # risk managers use this to understand downside exposure
    rolling_max = cumulative_returns.cummax()
    drawdown = (cumulative_returns - rolling_max) / rolling_max
    return drawdown.min().round(4)
