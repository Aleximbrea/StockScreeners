import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import pytz
import finnhub

# List of s&p500 stocks
finnhub_client = finnhub.Client(api_key="crjk17pr01qnnbrs87d0crjk17pr01qnnbrs87dg") # I know this should be hidden but i don't care
try:
    stocks = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]['Symbol'].tolist()
except:
    raise Exception("Error on getting stock tickers")

def removeEarnings(stocks, offset=7):
    from_date = datetime.now().date() - timedelta(days=offset)
    to_date = datetime.now().date() + timedelta(days=offset)
    for stock in stocks:
        try:
            date = finnhub_client.earnings_calendar(_from=from_date, to=to_date, symbol=stock)
            if date['earningsCalendar']:
                stocks.remove(stock)
        except:
            pass


def getLastMarketDay():
    data = yf.download('AAPL', interval='1d', period='5d', progress=False)
    print()
    i = -1
    while True:
        pastday = data.index[i].strftime('%Y-%m-%d')
        if pastday == datetime.now().strftime('%Y-%m-%d'):
            i =- 1
        else:
            break
    return pastday
        

def getDailyBars(tickers, start=None, end=None):

    # If no start date is given we get data starting from 200 days ago
    if not start:
        start = datetime.now()  - timedelta(days=365)
        start = start.strftime('%Y-%m-%d')
    if not end:
        end = datetime.strptime(getLastMarketDay(), '%Y-%m-%d') + timedelta(days=1)
        end = end.strftime('%Y-%m-%d')

    data = yf.download(tickers, start=start, end=end, interval='1d', group_by='ticker')

    # Create a list to store DataFrames for each ticker
    combined_frames = []

    if isinstance(tickers, list):
        for ticker in tickers:
            ticker_data = data[ticker]
            # Calculate SMA values
            sma_200 = ticker_data['Close'].rolling(window=200).mean().rename('SMA_200')
            sma_100 = ticker_data['Close'].rolling(window=100).mean().rename('SMA_100')
            sma_50 = ticker_data['Close'].rolling(window=50).mean().rename('SMA_50')
            # Concatenate the original data with SMA columns
            combined = pd.concat([ticker_data, sma_200, sma_100, sma_50], axis=1)
            combined_frames.append(combined)

        # Concatenate all DataFrames into a single DataFrame with a MultiIndex
        result = pd.concat(combined_frames, axis=1, keys=tickers)

    else:
        ticker_data = data
        sma_200 = ticker_data['Close'].rolling(window=200).mean().rename('SMA_200')
        sma_100 = ticker_data['Close'].rolling(window=100).mean().rename('SMA_100')
        sma_50 = ticker_data['Close'].rolling(window=50).mean().rename('SMA_50')
        # Concatenate the original data with SMA columns
        result = pd.concat([ticker_data, sma_200, sma_100, sma_50], axis=1)

    return result

def get5MinBars(tickers, start=None, end=None, offset = 7):

    if not start and not end:
        count = 1
        # We go back in the days until some data is given
        while True:
            # If no start or end date is given we get data from the day before
            end = datetime.strptime(getLastMarketDay(), '%Y-%m-%d') + timedelta(days=1)
            end = end.strftime('%Y-%m-%d')
            start = datetime.strptime(end, '%Y-%m-%d')  - timedelta(days=offset)
            start = start.strftime('%Y-%m-%d')
            data = yf.download(tickers, start=start, end=end, interval='5m', group_by='ticker')
            if not data.empty:
                break
            else:
                count =+ 1
    return data

def percentVar(open, close):
    return ((close - open) / open) * 100

def filter(sp_daily, df_daily):
    scores = {}
    sp_stats = getStats(sp_daily)

    # Assigning a score based on performance compared to spy
    for stock in df_daily.columns.levels[0]:
        stock_data = df_daily[stock]
        stats = getStats(stock_data)
        print(stock)
        print(sp_stats)
        print(stats)
        difference = {key: stats[key] - sp_stats[key] for key in stats}
        print(difference)
        stock_score = sum(difference.values())
        print(stock_score)
        input()
        scores[stock] = float(stock_score)
    return scores

def getStats(df):
    var_7d = percentVar(df.iloc[-7]['Open'], df.iloc[-1]['Close']) # 7 day % open -> close
    swing_high_7d = percentVar(df.iloc[-7]['Open'], df['High'].tail(7).max()) # % from open to highest peak
    swing_low_7d = percentVar(df.iloc[-7]['Open'], df['Low'].tail(7).min()) # % from open to lowest peak
    volume_var = percentVar(df['Volume'][-30:-1].mean(), df['Volume'].tail(1)) # % from mean volume to last day volume
    stats = {
        'var_7d': float(var_7d),
        'swing_high_7d': float(swing_high_7d),
        'swing_low_7d': float(swing_low_7d),
        'volume_var': float(volume_var)*0.33
    }
    return stats


if __name__ == "__main__":
        # daily_bars = getDailyBars(stocks)
        # min5_bars = get5MinBars(stocks)
        # daily_bars.to_hdf('data/daily.h5', key='dailydf', mode='w')
        # min5_bars.to_hdf('data/min.h5', key='mindf', mode='w')
    pass