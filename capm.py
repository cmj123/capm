import numpy as np
import pandas as pd
import yfinance as yf 
import matplotlib.pyplot as plt

# market interest rate
RISK_FREE_RATE = 0.05 
# We will consider monthly returns and we want to calculate the annual return
MONTHS_IN_YEAR = 12 

class CAPM:

    def __init__(self, stocks, start_date,end_date):
        self.data = None 
        self.stocks = stocks
        self.start_date = start_date
        self.end_date = end_date

    def download_data(self):
        data = yf.download(self.stocks, self.start_date, self.end_date)['Close']
        return data

    def initialize(self):
        stock_data = self.download_data()
        # we use montly returns instead of daily returns
        stock_data = stock_data.resample('M').last()

        self.data = pd.DataFrame({
            's_adjclose':stock_data[self.stocks[0]],
            'm_adjclose': stock_data[self.stocks[1]]
        })

        # logarithmic monthly returns
        self.data[['s_returns', 'm_returns']] = np.log(self.data[['s_adjclose', 'm_adjclose']] / self.data[['s_adjclose', 'm_adjclose']].shift(1))

        # remove the NaN values
        self.data = self.data[1:]

if __name__ == '__main__':
    capm = CAPM(['IBM', '^GSPC'], '2016-01-01', '2017-01-01')
    capm.initialize()