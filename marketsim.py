"""marketism 10/23/2017
author: dwang383
 """

import pandas as pd
import numpy as np
import datetime as dt
from util import get_data


def compute_portvals(orders_file="./orders/orders.csv", start_val=1000000, commission=9.95, impact=0.005):
    # panda read in data
    orders = pd.read_csv(orders_file, index_col='Date', parse_dates=True, na_values=['nan'], names=['Date', 'Symbol', 'Order', 'Shares'],skiprows=[0])

    #select date range
    start_date = orders.index[0]
    end_date = orders.index[-1]
    date_range = pd.date_range(start_date, end_date)

    # build the price table for selected sy
    symbols = list(set(orders['Symbol']))
    prices = get_data(symbols=symbols, dates=date_range, addSPY=False)
    prices['Cash'] = pd.Series(1.0, index=prices.index)
    prices = prices[pd.notnull(prices[symbols[0]])]

    trades = prices.copy()
    trades[trades != 0] = 0
    # update the cash table with stock orders and holding table
    for index, row in orders.iterrows():
        ordershares = float(row['Shares'])
        if (row['Order'].upper() != 'BUY'):
            ordershares = -ordershares
        shares = trades.loc[index][row['Symbol']] + ordershares
        trades.set_value(index,row['Symbol'],shares)
        #print row['Symbol'], row['Shares'], shares_in_order
        diffcash = -prices.loc[index][row['Symbol']] * ordershares-commission-impact*np.abs(prices.loc[index][row['Symbol']] * ordershares)
        #print cash_difference
        trades.set_value(pd.to_datetime(index).date(), 'Cash',diffcash + trades.loc[index]['Cash'])



    holdings = trades.copy()
    #print holdings_df
    #initialization
    for symbol in symbols:
        holdings.set_value(date_range[0], symbol, float(trades.loc[date_range[0]][symbol]))
    holdings.set_value(date_range[0], 'Cash', start_val + trades.loc[date_range[0]]['Cash'])
    prevdate= date_range[0]
    for date in date_range[1:]:

        if date in prices.index:
            for symbol in symbols:
                holdings.set_value(date, symbol, float(holdings.loc[prevdate][symbol]) + float(trades.loc[date][symbol]))
            holdings.set_value(date, 'Cash', float(holdings.loc[prevdate]['Cash']) + float(trades.loc[date]['Cash']))
            prevdate = date
    #print holdings_df
    #get the total stock portofolio including cash
    values = prices * holdings
    portvals = values.sum(axis=1)
    return portvals


def author():
    return 'dwang383'  # replace tb34 with your Georgia Tech username

def compute_stats(sv, rfr, sf, port_val):
    cr = port_val.ix[-1]/port_val.ix[0]-1

    # 2. count trading days
    daily_rets = port_val.copy()
    daily_rets[1:] = (port_val[1:] / port_val[:-1].values) - 1
    daily_rets = daily_rets[1:]
    adr = daily_rets.mean()

    # 3. position of prices for each day

    sddr= daily_rets.std()

    # 4. sharpe ratio =  (mean portfolio return  - rfr) / sd
    # considering flunctuation/risk uncertain of the market

    sr = (adr - rfr)* np.sqrt(sf)/ sddr
    print cr, adr, sddr, sr

    # Get portfolio statistics (note: std_daily_ret = volatility)
    # cr, adr, sddr, sr = [v1, v2, v3, v4]  # add code here to compute stats
    # *******
    # Compare daily portfolio value with SPY using a normalized plot


    # Add code here to properly compute end value
    ev = sv* (cr+1)

    return cr, adr, sddr, sr, ev

def test_code():
    # this is a helper function you can use to test your code
    # note that during autograding his function will not be called.
    # Define input parameters

    orders_file = "./orders/orders-00.csv"
    start_value = 1000000

    # Process orders
    portvals = compute_portvals(orders_file=orders_file, start_val=start_value)
    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[portvals.columns[0]]  # just get the first column
    else:
        "warning, code did not return a DataFrame"

    #print portvals
    # Get portfolio stats
    daily_returns = portvals[1:].values / portvals[:-1] - 1
    sf = 245
    cum_ret = portvals[-1] / portvals[0] - 1
    avg_daily_ret = daily_returns.mean()
    std_daily_ret = daily_returns.std()
    sharpe_ratio = np.sqrt(sf) * avg_daily_ret / std_daily_ret

    start_date = dt.datetime(2008, 1, 1)
    end_date = dt.datetime(2008, 6, 1)
    #cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = [0.2, 0.01, 0.02, 1.5]
    cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = \
        [0.2, 0.01, 0.02, 1.5]

    # Compare portfolio against $SPX
    print "Date Range: {} to {}".format(start_date, end_date)
    print
    print "Sharpe Ratio of Fund: {}".format(sharpe_ratio)
    print "Sharpe Ratio of SPY : {}".format(sharpe_ratio_SPY)
    print
    print "Cumulative Return of Fund: {}".format(cum_ret)
    print "Cumulative Return of SPY : {}".format(cum_ret_SPY)
    print
    print "Standard Deviation of Fund: {}".format(std_daily_ret)
    print "Standard Deviation of SPY : {}".format(std_daily_ret_SPY)
    print
    print "Average Daily Return of Fund: {}".format(avg_daily_ret)
    print "Average Daily Return of SPY : {}".format(avg_daily_ret_SPY)
    print
    print "Final Portfolio Value: {}".format(portvals[-1])


if __name__ == "__main__":
    test_code()
