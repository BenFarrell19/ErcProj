import yfinance as yf
import pandas as pd
import pandas_market_calendars as mcal
from datetime import datetime as dt
from quantopian.pipeline import Pipeline
from quantopian.research import run_pipeline

def make_pipeline():
    # Empty Pipeline
    return Pipeline()

run_pipeline(make_pipeline(), '2017-01-01', '2017-05-01')

# basic price history function using yfinance module, return pd dataframe
def get_price_history(ticker_symbol, start, end, interval):
    ticker_data = yf.Ticker(ticker_symbol)
    df = ticker_data.history(interval=interval, start=start, end=end)
    return df

# function required to find dates
def closest_dates(dates, pivot, n):
    return sorted((d for d in dates if d < pivot), key=lambda t: abs(t - pivot))[:n - 1]


# calculating relative volatility

nyse = mcal.get_calendar('NYSE')
schedule = nyse.schedule(start_date='2000-01-01', end_date=dt.now())

# 1 year
spy_year = get_price_history('spy', dt(2019,1,1), dt(2019,12,31), '1h')

# 1 month
spy_month = get_price_history('spy', dt(2019,1,1), dt(2019,12,31), '1m')

# 1 week
spy_week = get_price_history('spy', dt(2019,1,1), dt(2019,12,31), '5m')

# 1 day
spy_day = get_price_history('spy', dt(2019,1,1), dt(2019,12,31), '1m')
