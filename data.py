import yfinance as yf
import pandas as pd


def get_stock_data(tickers, start_date, end_date):
    """
    Pull historical closing prices for a list of tickers.
    Returns a DataFrame where each column is a stock.
    """
    data = yf.download(tickers, start=start_date, end=end_date, auto_adjust=True)["Close"]

    # If only one ticker, yfinance returns a Series — convert to DataFrame
    if isinstance(data, pd.Series):
        data = data.to_frame(name=tickers[0])

    return data


def calculate_daily_returns(price_data):
    """
    Calculate the percentage change day over day for each stock.
    """
    return price_data.pct_change().dropna()


def calculate_cumulative_returns(daily_returns):
    """
    Shows how $1 invested on day 1 would have grown over time.
    """
    return (1 + daily_returns).cumprod()


def calculate_sharpe_ratio(daily_returns, risk_free_rate=0.05):
    """
    Sharpe Ratio = how much return you get per unit of risk.
    Higher is better. Above 1.0 is considered good.
    Risk free rate defaults to 5% (current approximate rate).
    """
    trading_days = 252  # number of trading days in a year
    excess_returns = daily_returns.mean() * trading_days - risk_free_rate
    volatility = daily_returns.std() * (trading_days ** 0.5)
    return (excess_returns / volatility).round(2)


def calculate_max_drawdown(cumulative_returns):
    """
    Max Drawdown = the biggest drop from a peak to a trough.
    Tells you the worst loss you would have experienced.
    """
    rolling_max = cumulative_returns.cummax()
    drawdown = (cumulative_returns - rolling_max) / rolling_max
    return drawdown.min().round(4)


# Quick test 
if __name__ == "__main__":
    tickers = ["AAPL", "MSFT", "GOOGL"]
    start = "2024-01-01"
    end = "2025-01-01"

    print("Fetching data...")
    prices = get_stock_data(tickers, start, end)
    print("\nFirst 5 rows of price data:")
    print(prices.head())

    daily_returns = calculate_daily_returns(prices)
    cumulative_returns = calculate_cumulative_returns(daily_returns)

    print("\nSharpe Ratios:")
    print(calculate_sharpe_ratio(daily_returns))

    print("\nMax Drawdown:")
    print(calculate_max_drawdown(cumulative_returns))