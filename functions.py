import yfinance as yf
import pandas as pd

# List of s&p500 stocks
try:
    stocks = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]['Symbol'].tolist()
except:
    raise Exception("Error on getting stock tickers")


if __name__ == "__main__":
    print(stocks)