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

    plot_data('BestPossibleStrategy','Best Strategy',policy = bp.testPolicy,sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31))
    plot_data('In Sample ManualStrategy','Manual Strategy',sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31))
    slearner = sl.StrategyLearner()
    for impact in [0.001,0.005,0.01]:
        plot_data('BestPossibleStrategy with the market impact of {}'.format(impact),'Best Strategy',policy = bp.testPolicy,sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), impact=impact)
        slearner.addEvidence(symbol='JPM',sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31),sv = 10000,impact = impact)
        plot_data('In Sample StrategyLearner with the market impact of {}'.format(impact),'RDT Strategy',policy = slearner.testPolicy, sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), impact=impact)

if __name__ == '__main__':
    test()
