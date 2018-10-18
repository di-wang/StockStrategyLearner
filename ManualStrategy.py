"""Analyze a portfolio.
Submitted by: Di Wang
Gtusername: dwang383
Email: dwang383@gatech.edu

2017/09/03
"""

import pandas as pd
import numpy as np
import datetime as dt
from util import get_data, plot_data
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from collections import OrderedDict

# This is the function that will be tested by the autograder
# The student must update this code to properly implement the functionality
def assess_portfolio(sd = dt.datetime(2010,1,1), ed = dt.datetime(2010,12,31), \
    syms = ['GOOG','AAPL','GLD','XOM'], \
    allocs=[0.2,0.3,0.4,0.1], \
    sv=1000000, rfr=0.0, sf=252.0, \
    gen_plot=False):

    # indicator inputs
    # 1. momentum, variable, n days previous
    ndays_m = 21

    # 2. SMA
    ndays_sma = 21

    # 3. SMA
    ndays = 10





    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols
    prices.fillna(method = "ffill", inplace = True)
    prices.fillna(method = "bfill", inplace = True)
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later
    # Get daily portfolio value
    # port_val = prices_SPY # add code here to compute daily portfolio values

    def compute_stats(prices):
        # *******
        # 1. normalization
        norm_prices = prices/prices.ix[0]
        alloc_val = norm_prices * allocs
        pos_val = alloc_val * sv
        port_val = pos_val.sum (axis = 1)
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

        print port_val
        print cr, adr, sddr, sr
        print port_val.shape
        #indicator 1

        momentum = port_val.copy()

        momentum[ndays_m:] = port_val[ndays_m:]/port_val[:-ndays_m].values-1
        for i in range(ndays_m, port_val.shape[0]):
            if momentum[i]>0.3:
                print "sell", i, port_val[i]
            if momentum[i]<-0.3:
                print "buy", i, port_val[i]


        # indicator 2
        sma = port_val.copy()

        for i in range(ndays_sma, port_val.shape[0]):
            sma[i] = port_val[i-ndays_m:i].mean()

        price_sma = port_val / sma
        print price_sma

        # indicator 3
        bb = port_val.copy()
        bb= (port_val- sma)/ (2.0*sddr) - 1
        bb_upper = 2*sddr + sma
        bb_down = sma - 2*sddr

        # indicator 3 EMA
        ema = port_val.copy()
        ema[:12] = 1
        ema12 = port_val.copy()
        ema12[:12] = 1
        for i in range(12, port_val.shape[0]):
            ema[i] = port_val[i - 12:i].mean()
            ema12[i] = (port_val[i]-ema[i])*0.1538+ema[i]

        # Get portfolio statistics (note: std_daily_ret = volatility)
        # cr, adr, sddr, sr = [v1, v2, v3, v4]  # add code here to compute stats
        # *******
        # Compare daily portfolio value with SPY using a normalized plot
        if gen_plot:
            # add code to plot here
            # add code to plot here
            df_temp = pd.concat([port_val[ndays_m:], momentum[ndays_m:]], keys=['Portfolio', 'Momentum'], axis=1)
            plot_data(df_temp, "Momentum", "Date", "Price")

            df_temp = pd.concat([port_val[ndays_sma:], sma[ndays_sma:], price_sma[ndays_sma:]], keys=['Portfolio', 'SMA', 'price/SMA'], axis=1)
            plot_data(df_temp, "SMA", "Date", "Price")

            df_temp = pd.concat([port_val, bb_upper, bb_down], keys=['Portfolio', 'Upper','Bottom'], axis=1)
            plot_data(df_temp, "Bollinger Bands", "Date", "Price")

            df_temp = pd.concat([port_val, ema, ema12], keys=['Portfolio', 'EMA', 'EMA12'], axis=1)
            plot_data(df_temp, "Optimial Portfolio with SPY", "Date", "Price")

            pass
        # Add code here to properly compute end value
        ev = sv* (cr+1)

        # Plotting of the Graph

        ax = port_val.plot(title='Long and Short Entry', label='JPM')
        sma.plot(label='SMA', ax=ax)
        # upper_band.plot(label = 'Upper Bollinger Bands',ax = ax, color='c')
        # lower_band.plot(label = 'Lower Bollinger Bands',ax = ax, color='c')

        short_entries = []
        short_exits = []
        long_entries = []
        long_exits = []
        signals = []
        ymin, ymax = ax.get_ylim()
        plt.vlines(long_entries, ymin, ymax, color='g')
        # plt.vlines(long_exits,ymin,ymax)
        plt.vlines(short_entries, ymin, ymax, color='r')
        # plt.vlines(short_exits,ymin,ymax)

        ax.legend(loc='upper left')
        plt.show()

        return cr, adr, sddr, sr, ev

    return compute_stats(prices)

def test_code():
    # This code WILL NOT be tested by the auto grader
    # It is only here to help you set up and test your code

    # Define input parameters
    # Note that ALL of these values will be set to different values by
    # the autograder!
    start_date = dt.datetime(2008, 1, 1)
    end_date = dt.datetime(2009, 12, 31)
    symbols = ['JPM']
    allocations = [1]
    start_val = 1
    risk_free_rate = 0.08
    sample_freq = 252

    # Assess the portfolio
    cr, adr, sddr, sr, ev = assess_portfolio(sd = start_date, ed = end_date,\
        syms = symbols, \
        allocs = allocations,\
        sv = start_val, \
        gen_plot = True)



    # Print statistics
    print "Start Date:", start_date
    print "End Date:", end_date
    print "Symbols:", symbols, symbols.__len__()
    print "Allocations:", allocations
    print "Sharpe Ratio:", sr
    print "Volatility (stdev of daily returns):", sddr
    print "Average Daily Return:", adr
    print "Cumulative Return:", cr

if __name__ == "__main__":
    test_code()
