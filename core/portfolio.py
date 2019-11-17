import pandas as pd
import dill as pickle
import config as config


class PortfolioBase:
    """
    Base Class of portfolios
    AllPortfolio and Portfolio are subclasses of PortfolioBase
    """

    def __init__(self, period, des):
        """
        Initialize the base portfolio.
        When initialize, call _set_up__ to get the all tradeDates in the period.
        Name, Period, tickers and des are set according to config, other attributes are set to None.
        :param
            period: (start_date, end_date)
            des: description of current class
        """
        self.period = period  # Period: tuple (start_date, end_date)
        self.des = des  # Description

        self.trade_dates = [date for date in config.trade_dates if period[0] < date < period[1]]  # Valid trading Dates
        self.ret = pd.DataFrame(index=self.trade_dates)  # Return of the portfolio

    def _cal_return__(self, *args, **kwargs):
        """
        Calculate the return of the portfolio.
        :return:
        """
        pass

    def print(self):
        """
        Print the Name and Description of the portfolio.
        :return:
        """
        pass

    def set_des(self, description):
        """
        Set the description of the portfolio
        :param description: Description
        """
        self.des = description

    def to_pickle(self, path):
        """
        Save current object to pickle file.
        :param path: File name
        """
        f = open(path, 'wb')
        pickle.dump(self, f)

    @classmethod
    def load_pickle(cls, file_path):
        """
        Load object from pickle file
        :param file_path: path of the pickle file
        :return:
        """
        f = open(file_path, 'rb')
        return pickle.load(f)


class Portfolio(PortfolioBase):
    def __init__(self, period, des='', ret=pd.DataFrame(), mv=pd.DataFrame()):
        super().__init__(period, des)
        self.tickers = []
        self.portfolio_return = pd.Series(index=self.trade_dates)
        self.mv = pd.DataFrame()
        self.load_ret_and_mv(ret, mv)

    def load_ret_and_mv(self, ret, mv):
        self.tickers = [ticker for ticker in ret.columns.to_list() and mv.columns.to_list()]
        self.ret = ret.loc[self.period[0]:self.period[1], self.tickers]
        self.mv = mv.loc[self.period[0]:self.period[1], self.tickers]

    def print(self):
        print('Num of stocks:   {0}\n'
              'Period:          {1} to {2}\n'
              'Description:     {3}'.format(len(self.tickers), self.period[0], self.period[1], self.des))

    def retrieve(self, tickers, period):
        """
        Retrieve sub set data of the portfolio
        :param tickers: list, selected tickers
        :param period: tuple like: (Start date, End date)
        :return: Portfolio Like
        """
        tickers = [ticker for ticker in tickers if ticker in self.tickers]
        cur_ret = self.ret.loc[period[0]: period[1], tickers]
        cur_mv = self.mv.loc[period[0]: period[1], tickers]
        return Portfolio(period, ret=cur_ret, mv=cur_mv)

    def cal_return(self, weight='value'):
        all_stocks_return = self.ret
        all_stocks_return[all_stocks_return.isna()] = 0

        all_stocks_mv = self.mv
        all_stocks_mv[all_stocks_return.isna()] = 0
        if weight == 'value':
            self.portfolio_return = (all_stocks_return * all_stocks_mv).sum(axis=1) / all_stocks_mv.sum(axis=1)
        else:
            self.portfolio_return = all_stocks_return.mean(axis=1)

        return self.portfolio_return


class PanelData(PortfolioBase):
    def __init__(self, period, des=''):
        super().__init__(period, des)
        self.ret = pd.DataFrame(index=self.trade_dates)

    def add_portfolio(self, name, list_of_portfolio, weight='value'):
        portfolio_return = pd.Series()
        trade_dates = []
        for portfolio in list_of_portfolio:
            assert [date for date in trade_dates if date in portfolio.trade_dates] == []
            trade_dates.extend(portfolio.trade_dates)
        assert set(self.trade_dates).issubset(trade_dates)
        for portfolio in list_of_portfolio:
            portfolio_return = portfolio_return.append(portfolio.cal_return(weight))
        portfolio_return = portfolio_return[self.trade_dates]
        self.ret[name] = portfolio_return
        return
