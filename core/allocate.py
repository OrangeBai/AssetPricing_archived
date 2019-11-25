import os
import pandas as pd
import config as config
import dill as pickle
from datetime import datetime
from copy import deepcopy
import numpy as np
from itertools import product


class Allocate:
    """
    This class is used for allocate stocks into different groups according to their features.
    """
    def __init__(self, tickers, periods, period_to_tickers=None, num_of_nan=5, list_limitation='year'):
        """
        initialization method
        :param tickers: list of tickers:['000001','000002',...'600001']
        :param periods: list of tuple: (start_date: yyyy_mm, end_date: yyyy_mm)
        :param period_to_tickers: selected tickers according to features, i.e. newly listed stocks are excluded.
                {
                    (start_date, end_date):[stock_1, stock_2, ..., stock_n]
        :param num_of_nan: maximim nan number of a stock in a period. If stock_i has more than num_of_nan nan data, it should be excluded.
        :param list_limitation: A stock should be on list for at least 'list_limitation' date
        """
        self.tickers = tickers
        self.periods = periods
        self.na_bool = pd.read_csv(os.path.join(config.extracted_directory, 'DailyRet.csv'), index_col=0).isna()
        self.num_of_nan = num_of_nan
        self.list_limitation = list_limitation

        self.periods_to_tickers = period_to_tickers
        self._filter__()

        self.factors = {}
        self.periods_to_factors = {}

    def _filter__(self):
        """
        Filter tickers according to list date and number of nan in the period.
        :return:
        """
        period_to_ticker = {}
        if self.list_limitation == 'month':
            min_diff = 21
        elif self.list_limitation == 'quarter':
            min_diff = 63
        else:
            min_diff = 504

        for period in self.periods:
            # during each period, a stocks are filtered according to their list date as well as number of nan.
            period_start = period[0]
            period_end = period[1]
            tickers = []
            if self.periods_to_tickers is None:
                stock_list = self.tickers
            else:
                stock_list = self.periods_to_tickers[period]
            for stock in stock_list:
                if stock not in config.A_lists or stock not in self.na_bool.columns.to_list():
                    # if stock is not in A list, or there are too many nan data, the ticker is excluded.
                    self.tickers.remove(stock)
                    continue
                if config.co_info.loc[stock, 'Indcd'] == 1:
                    # if stock belongs to Finance related, it should be excluded.
                    self.tickers.remove(stock)
                    continue
                list_date = datetime.strptime(config.co_list_date[stock], '%Y-%m-%d')
                current_date = datetime.strptime(period_start, '%Y-%m')
                diff = current_date - list_date
                if diff.days < min_diff:
                    continue

                if self.na_bool.loc[period_start: period_end, stock].sum() > self.num_of_nan \
                        or self.na_bool.loc[period_start: period_end, stock].shape[0] < 5:
                    continue

                tickers.append(stock)

            period_to_ticker[period] = tickers
            print('{0} : {1} stocks'.format(period_start, len(tickers)))

        self.periods_to_tickers = period_to_ticker

        return period_to_ticker

    def add_factor(self, factor_name, factor_path, replace=False):
        if factor_name in self.factors.keys() and replace is False:
            print('{0} already exist, replacement failed.'.format(factor_name))
            return
        self.factors[factor_name] = pd.read_csv(factor_path, index_col=0)
        print('Adding {0} factor from {1}'.format(factor_name, factor_path))
        return

    @classmethod
    def load_pickle(cls, file_path):
        """
        Load object from pickle file
        :param file_path: path of the pickle file
        :return:
        """
        f = open(file_path, 'rb')
        return pickle.load(f)

    def allocate_stocks_according_to_factors(self, factors, percentage, sequentially=True):
        """
        Allocate stocks by factors. Return a diction like:
            {
                Group_1:{
                            period_1 : tickers
                            period_2 : tickers ...
                        }
                Group_2:{
                            period_1 : tickers
                            period_2 : tickers ...
                        }
            }
            Group is named as : 'Factor1_level_Factor2_level...'
            The group name will be used as the name of panel portfolio.
        :param factors:A list of factors, all factors should be contained in Factor data-frame.
        :param percentage: A tuple whose summation should be 1. (0.3,0.4,0.3)
        :param sequentially: Boolean, if true, stocks are allocated according to their factors one by one.
        :return: Factor
        """
        period_to_group_tickers = {}
        total_periods = len(self.periods)
        counter = 0
        if sequentially:
            for period in self.periods:
                period_to_group_tickers[period] = self.allocate_in_one_period_sequentially(factors, percentage, period)
                counter = counter + 1
                l1 = counter * 50 // total_periods
                print('Progress Bar: {0:><{len1}}{1:=<{len2}}. {2} of {3}'.format('>', '=', counter, total_periods, len1=l1, len2=50 - l1, ))
        else:
            for period in self.periods:
                period_to_group_tickers[period] = self.allocate_in_one_period_mixed(factors, percentage, period)
                counter = counter + 1
                l1 = counter * 50 // total_periods
                print('Progress Bar: {0:><{len1}}{1:=<{len2}}. {2} of {3}'.format('>', '=', counter, total_periods, len1=l1, len2=50 - l1, ))

        group_to_period_to_tickers = {}
        for period, group_to_tickers in period_to_group_tickers.items():
            for group, tickers in group_to_tickers.items():
                if group not in group_to_period_to_tickers.keys():
                    group_to_period_to_tickers[group] = {}
                group_to_period_to_tickers[group][period] = tickers

        return group_to_period_to_tickers

    def allocate_in_one_period_mixed(self, factors, percentages, period):
        """
        Allocate stocks in one period according to assigned factors and their percentages.
        :param factors: Factors based on which the stocks are grouped.
                        Should be a list like: [Factor 1, Factor 2, Factor 3,...]
        :param percentages: Percentage for each stock
        :param period: Selected period for
        :return:
        """
        group_to_factors = {}  # group to factor is a dic object
        tickers = self.periods_to_tickers[period]  # all tickers in different

        factor_df = pd.DataFrame(index=tickers)

        for factor_name in factors:
            factor_df[factor_name] = self.factors[factor_name].loc[period[0]]
            factor_df.drop(factor_df[factor_df[factor_name].isna()].index, inplace=True)

        tagged_factor = deepcopy(factor_df)

        for (factor, percentage) in zip(factors, percentages):
            tagged_factor = self._allocate_one_factor(tagged_factor, factor, percentage)

        group_nums = [list(range(len(percentage) - 1)) for percentage in percentages]

        number_of_factors = len(factors)

        for group in product(*group_nums):
            group_name = ''
            # set group name
            for i in range(number_of_factors):
                group_name = group_name + factors[i] + str(group[i]).zfill(2) + '_'

            group_tickers = self._find_tickers__(tagged_factor, factors, group)
            group_to_factors[group_name] = group_tickers
        return group_to_factors

    def allocate_in_one_period_sequentially(self, factors, percentages, period):

        tickers = self.periods_to_tickers[period]
        factor_df = pd.DataFrame(index=tickers)

        for factor_name in factors:
            try:
                factor_df[factor_name] = self.factors[factor_name].loc[period[0]]
            except ValueError or KeyError:
                factor_df[factor_name] = np.NaN
            factor_df.drop(factor_df[factor_df[factor_name].isna()].index, inplace=True)

        group_to_factors = {}

        number_of_factors = len(factors)
        group_nums = [list(range(len(percentage) - 1)) for percentage in percentages]
        for group in product(*group_nums):
            tagged_factor = deepcopy(factor_df)
            current_tickers = [ticker for ticker in tickers if ticker in tagged_factor.index.to_list()]
            group_name = ''
            for i in range(number_of_factors):
                group_name = group_name + factors[i] + str(group[i]).zfill(2) + '_'
                tagged_factor = self._allocate_one_factor(tagged_factor.loc[current_tickers], factors[i],
                                                          percentages[i])
                current_tickers = tagged_factor[tagged_factor[factors[i]] == float(group[i])].index.to_list()
            group_to_factors[group_name] = current_tickers
        return group_to_factors

    @staticmethod
    def _allocate_one_factor(tagged_factor, factor_name, factor_percentage):
        """
        This function is used for tag all stocks according to the percentage.
        :param tagged_factor:
        :param factor_name:
        :param factor_percentage:
        :return:
        """
        number_of_stocks = tagged_factor.shape[0]
        tagged_factor = tagged_factor.sort_values(by=[factor_name])

        num_of_group = len(factor_percentage) - 1
        for group_num in range(num_of_group):
            start = int(number_of_stocks * factor_percentage[group_num])
            end = int(number_of_stocks * factor_percentage[group_num + 1])
            tagged_factor.iloc[start:end, tagged_factor.columns == factor_name] = int(group_num)
        return tagged_factor

    @staticmethod
    def _find_tickers__(tagged_factor, factors, group):
        """
        This function is used for select tickers from a tagged data_frame structure
        :param tagged_factor:   A tagged data_frame structure
                                columns: ticker, factor_name_1, factor_name_2,..., factor_name_n
        :param factors:         Factors based on which the tickers are selected
        :param group:           Tag numbers of factors, for instance, a group number with [0,1,2] indicates that with
                            factor 0 in group 0, factor _1 in group 1 and factor_2 in group 2
        :return:                selected tickers
        """
        bool_of_tickers = [True] * tagged_factor.shape[0]  # create a bool list for all tickers, default all true
        number_of_factors = len(factors)  # The number of factors
        for i in range(number_of_factors):
            # For each factor, select all tickers in the assigned group
            bool_of_tickers = bool_of_tickers & (tagged_factor[factors[i]] == float(group[i]))
        selected_tickers = tagged_factor[bool_of_tickers].index.to_list()
        # return all tickers that meet the requirement.
        return selected_tickers

    def to_pickle(self, path):
        """
        Save current object to pickle file.
        :param path: File path
        """
        f = open(path, 'wb')
        pickle.dump(self, f)


if __name__ == '__main__':
    pass
    # month_split = [str(i) + '-' + str(j).zfill(2) for i in range(2015, 2016) for j in range(1, 13, 1)]
    # allocate = Allocate(config.A_lists, month_split)
    # allocate.add_factor('turnover', '/Users/oranbebai/Documents/Data/Finance/Features/adjusted_turnover_monthly2.csv')
    # allocate.add_factor('mv', '/Users/oranbebai/Documents/Data/Finance/Features/mv_month2.csv')
    # allocate.allocate_stocks_according_to_factors(['mv', 'turnover'],
    #                                               [(0, 0.2, 0.4, 0.6, 0.8, 1), (0, 0.2, 0.4, 0.6, 0.8, 1)])

