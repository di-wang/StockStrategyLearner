# Authoor:Di Wang
# gt username: dwang383


import sys
sys.path.append('..')
import datetime as dt
import numpy as np
import pandas as pd
import util as ut
import random
import RTLearner as rt
import BestPossibleStrategy as bps
import indicators as ind
class StrategyLearner(object):

    def __init__(self, verbose = False, impact=0.0):
        self.verbose = verbose
        self.impact = impact
        self.learner = rt.RTLearner(leaf_size=5)
        self.lookback = 14
    def addEvidence(self, symbol = "IBM", \
        sd=dt.datetime(2008,1,1), \
        ed=dt.datetime(2009,1,1), \
        sv = 10000, \
        impact = 0):

        syms=[symbol]
        dates = pd.date_range(sd, ed)
        daily_rets = bps.testPolicy( symbol,sd,ed,sv,impact = impact )
        holding = np.cumsum(daily_rets)
        self.bps = holding
        df = pd.concat([self.addIndicator(sd,ed,symbol,14),self.bps],axis = 1)
        self.learner.addEvidence(df.ix[:,0:-1],df.ix[:,-1])

    def addIndicator(self,sd,ed,symbol,lookback):
        sma = ind.sma(sd , ed ,syms = [symbol],lookback = 14, ratio = False)
        bb = ind.bb(sd , ed ,syms = [symbol],lookback = 14)
        so = ind.so(sd , ed ,syms = [symbol],lookback = 14)
        df = pd.concat([sma,bb[[symbol]],so[[symbol]]],axis = 1)
        return df

    def author(self):
        return 'dwang383'  # replace tb34 with your Georgia Tech username

    def testPolicy(self, symbol = "JPM", \
        sd=dt.datetime(2008,1,1), \
        ed=dt.datetime(2010,1,1), \
        sv = 100000,impact = None):

        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data([symbol], dates)  # automatically adds SPY
        indicators = self.addIndicator(sd,ed,symbol,14)
        holding = self.learner.query(indicators)

        trades = holding.copy()
        trades.values[1:] = holding.values[1:] - holding.values[:-1]
        trades.values[0] = holding.values[0]
        trades.columns = [symbol]

        return trades

if __name__=="__main__":
    print "One does not simply think up a strategy"
