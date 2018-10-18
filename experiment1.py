# Authoor:Di Wang
# gt username: dwang383
import sys
sys.path.append('..')
import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data
import BestPossibleStrategy as bp
import ManualStrategy as ms
import StrategyLearner as sl
import matplotlib.pyplot as plt
import marketsimcode as mktsim


def author(self):
    return 'dwang383'  # replace tb34 with your Georgia Tech username


def test():
    if gen_plot:
        # add code to plot here
        # add code to plot here
        df_temp = pd.concat([port_val[ndays_m:], momentum[ndays_m:]], keys=['Portfolio', 'Momentum'], axis=1)
        plot_data(df_temp, "Momentum", "Date", "Price")

        df_temp = pd.concat([port_val[ndays_sma:], sma[ndays_sma:], price_sma[ndays_sma:]],
                            keys=['Portfolio', 'SMA', 'price/SMA'], axis=1)
        plot_data(df_temp, "SMA", "Date", "Price")

        df_temp = pd.concat([port_val, bb_upper, bb_down], keys=['Portfolio', 'Upper', 'Bottom'], axis=1)
        plot_data(df_temp, "Bollinger Bands", "Date", "Price")

        df_temp = pd.concat([port_val, ema, ema12], keys=['Portfolio', 'EMA', 'EMA12'], axis=1)
        plot_data(df_temp, "Optimial Portfolio with SPY", "Date", "Price")

        pass
    # Add code here to properly compute end value
    ev = sv * (cr + 1)


if __name__ == '__main__':
    test()
