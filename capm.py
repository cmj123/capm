import numpy as np
import pandas as pd
import yfinance as yf 
import matplotlib.pyplot as plt
from datetime import date, timedelta
# market interest rate
RISK_FREE_RATE = 0.01 
# We will consider monthly returns and we want to calculate the annual return
MONTHS_IN_YEAR = 12 

class CAPM:

    def __init__(self, stocks, start_date,end_date):
        self.data = None 
        self.stocks = stocks
        self.start_date = start_date
        self.end_date = end_date
        self.beta = None
        self.alpha= None
        self.expected_return = None
        self.market_risk_premium = None

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
        self.data = self.data.dropna()

        return None

    def calculate_beta(self):
        # covariance matrix: the diagonal items are the variances
        # off diagonals are the covariances
        # the matrix is symmetric: cov[0,1] = cov[1,0]
        covariance_matrix = np.cov(self.data["s_returns"], self.data["m_returns"])
        # calculating beta accroding to the formula
        beta = covariance_matrix[0,1] / covariance_matrix[1,1]
        print(f'\nBeta from formula {beta}')
        return None


    def regression(self):
        # using linear regression to fit a line to the data
        # [stock_retirns, market_returns] - slope is the beta
        self.beta, self.alpha = np.polyfit(self.data['m_returns'], self.data['s_returns'], deg=1)

        # Calculate the expected return
        self.market_return = self.data['m_returns'].mean()*MONTHS_IN_YEAR
        self.market_risk_premium = self.market_return - RISK_FREE_RATE
        self.expected_return = RISK_FREE_RATE + self.beta * self.market_risk_premium

        # Statement of expected return and beta
        er_beta_str = "Expected Return - " + str(np.round(self.expected_return*100, 2)) + '%. The beta - ' + str(np.round(self.beta,2))
        
        # # Plot figure
        # fig, axis = plt.subplots(1, figsize=(10,6))
        # axis.scatter(self.data["m_returns"], self.data['s_returns'], label="Data Points")
        # axis.plot(self.data["m_returns"], beta*self.data["m_returns"] + alpha, color='red', label="CAPM Line")
        # plt.title('Capital Asset Pricing Model, finding alpha and beta')
        # plt.xlabel('Market return $R_m$')
        # plt.ylabel('Stock return $R_a$')
        # plt.text(0.8, 0.15, er_beta_str , horizontalalignment='right', verticalalignment='top', transform=axis.transAxes)
        # plt.legend()
        # plt.grid(True)
        # plt.show()
        # 
        return None    

if __name__ == '__main__':
    capm = CAPM(['0P0001KCAG.L', '^GSPC'], date.today()- timedelta(days=6*365), date.today())
    capm.initialize()
    # capm.calculate_beta() #Interested in beta calculation using covariance matrix
    capm.regression()