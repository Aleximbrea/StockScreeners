import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# List of s&p500 stocks
try:
    stocks = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]['Symbol'].tolist()
except:
    raise Exception("Error on getting stock tickers")

def getDailyBars(ticker, start=None, end=None):

    # If no start date is given we get data starting from 30 days ago
    if not start:
        start = datetime.now()  - timedelta(days=30)
        start = start.strftime('%Y-%m-%d')

    data = yf.download(ticker, start=start, end=end, interval='1d')
    return data

def get5MinBars(ticker, start=None, end=None):

    if not start and not end:
        count = 1
        # We go back in the days until some data is given
        while True:
            # If no start or end date is given we get data from the day before
            start = datetime.now()  - timedelta(days=count+1)
            start = start.strftime('%Y-%m-%d')
            end = datetime.now()  - timedelta(days=count)
            end = end.strftime('%Y-%m-%d')
            data = yf.download(ticker, start=start, end=end, interval='5m')
            if not data.empty:
                break
            else:
                count =+ 1
    return data


if __name__ == "__main__":
    print(get5MinBars('SPY'))