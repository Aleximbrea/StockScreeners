from functions import get5MinBars, getDailyBars, getLastMarketDay, filter, removeEarnings, stocks
import pandas as pd

if __name__ == "__main__":

    try:
        # Loading tables if they exist
        daily_bars = pd.read_hdf('data/daily.h5', key='dailydf')
        min5_bars = pd.read_hdf('data/min.h5', key='mindf')
        # Making sure tables are recent
        if daily_bars.index[-1].strftime('%Y-%m-%d') == getLastMarketDay():
            pass
        else:
            raise Exception('Old data')
        
    except Exception as e:

        # If tables dont exist
        # First we need to remove stocks that are near earnings

        print('Removing stocks near earnings....')
        removeEarnings(stocks)
        print('Stocks removed')
        
        print('Downloading stock data')
        daily_bars = getDailyBars(stocks)
        min5_bars = get5MinBars(stocks)
        daily_bars.to_hdf('data/daily.h5', key='dailydf', mode='w')
        min5_bars.to_hdf('data/min.h5', key='mindf', mode='w')

    sp_daily = getDailyBars('SPY')
    sp_min = get5MinBars('SPY')
    # Getting scores
    # scores = filter(sp_daily, daily_bars)