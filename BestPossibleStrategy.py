 # Authoor:Di Wang
# gt username: dwang383


import sys
sys.path.append('..')
import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data

def testPolicy(symbol = "AAPL",sd=dt.datetime(2010,1,1), ed=dt.datetime(2011,12,31), sv = 100000,commission = 0, impact = None) :
    symbol = [symbol]
    dates = pd.date_range(sd, ed)
    prices = get_data(symbol, dates)  
    prices = prices[symbol]
    if (impact is None )| (impact == 0):
        daily_rets=prices.copy()
        daily_rets.values[1:,:]= prices.values[1:,:]-prices.values[:-1,:]
        daily_rets.values[0,:] = np.nan
    else:

        daily_buy_price = prices.copy()
        daily_buy_price =  daily_buy_price*(1+impact)

        daily_sell_price = prices.copy()
        daily_sell_price = daily_sell_price *(1-impact)

        daily_rets_buy = prices.copy()
        daily_rets_buy.values[:-1,:] = daily_buy_price.values[:-1,:] - daily_sell_price.values[1:,:]
        daily_rets_buy.values[-1,:] = np.inf

        daily_rets_sell = prices.copy()
        daily_rets_sell.values[1:,:] = daily_sell_price.values[:-1,:] - daily_buy_price.values[1:,:]
        daily_rets_sell.values[0,:] = np.inf

        daily_rets =  daily_rets_buy - daily_rets_sell
    holding = prices.copy()
    holding.values[:-1,0] =[1000 if x > 0 else -1000 for x in daily_rets[symbol].values[1:,]]
    holding.values[-1,:] = 0
    trade = holding.copy()
    trade.values[1:,:] = holding.values[1:,:] - holding.values[:-1,:]
    trade.values[0,:] = holding.values[0,:]
    trade.columns = [symbol]
   
    return trade
def author(self):
        return 'dwang383'


if __name__ == "__main__":
    df_trades = testPolicy(symbol = "JPM", sd=dt.datetime(2008,1,2), ed=dt.datetime(2009,12,31), sv = 100000)
    print df_trades
