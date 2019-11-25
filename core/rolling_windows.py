from core.allocate import *
import pandas as pd
import os
import statsmodels.api as sm
import numpy as np
import time


class RollingWindow:
    def __init__(self, dependent, exogenous, windows_length=252, group_by=None, nan_num=15):
        """

        :param dependent: DataFrame, dependent variable
        :param exogenous: DataFrame, exogenous variable, shoule have the same length and index with dependent variable
        :param windows_length:
        :param group_by: Dictionary, should be
                        {
                            result_index_1: (start_index1, end_index1),
                            result_index_2: (start_index2, end_index2),
                            ...
                        }
                        Indicator of how to group variables.
        """
        self.dependent = dependent
        self.exogenous = exogenous
        self.windows_length = windows_length
        self.group_by = group_by
        self.nan_num = nan_num
        self.result = {}
        try:
            assert self.dependent.shape[0] == self.exogenous.shape[0]
        except AssertionError:
            print('Length of depend variable should be equal to length of exogenous variable')

    def regress(self, method='window'):
        try:
            assert method in ['window', 'group']
        except AssertionError:
            print('Regression method should be \'window\' or \'group\'')
        portfolio_num = self.dependent.shape[1]
        portfolio_names = self.dependent.columns.to_list()
        dates = self.dependent.index.to_list()
        results = {}
        if method == 'window':
            try:
                assert self.dependent.shape[0] > self.windows_length
            except AssertionError:
                print('Length of dependent variable should be longer than first_step_number')
            # How many regression will be performed for one stock
            reg_num = self.dependent.shape[0] - self.windows_length
            for i in range(reg_num):
                start_time = time.time()
                cur_dependent = self.dependent.iloc[i: i + self.windows_length]
                cur_exogenous = self.exogenous.iloc[i: i + self.windows_length]
                cur_result = {}

                # Number of stocks
                for j in range(portfolio_num):
                    Y = cur_dependent.iloc[:, j]
                    if sum(Y.isna()) > self.nan_num:
                        continue
                    X = np.array(cur_exogenous)
                    X = sm.add_constant(X)
                    reg_result = sm.OLS(Y, X, missing='drop').fit()
                    cur_result[portfolio_names[j]] = reg_result

                end_time = time.time()

                results[dates[i + self.windows_length]] = cur_result
                print('Regression {0:03d} of {1:03d}, time:{2}'.format(i, reg_num, end_time-start_time))
        else:
            reg_num = len(self.group_by)
            counter = 0
            for output_index, input_boundry in self.group_by.items():
                counter = counter + 1
                start_time = time.time()
                cur_dependent = self.dependent.loc[input_boundry[0]: input_boundry[1]]
                cur_exogenous = self.exogenous.loc[input_boundry[0]: input_boundry[1]]
                cur_result = {}

                for j in range(portfolio_num):
                    Y = cur_dependent.iloc[:, j]
                    if sum(Y.isna()) > self.nan_num:
                        continue
                    X = np.array(cur_exogenous)
                    X = sm.add_constant(X)
                    reg_result = sm.OLS(Y, X, missing='drop').fit()
                    cur_result[portfolio_names[j]] = reg_result

                end_time = time.time()
                results[output_index] = cur_result
                print('Regression {0:03d} of {1:03d}, time:{2}'.format(counter, reg_num, end_time - start_time))

        self.result = results
        return results

    def read_result(self, fun):
        output_dict = {}
        counter = 0
        for key_date, date_dict in self.result.items():
            start_time = time.time()
            counter = counter+1
            cur_dict = {}
            for ticker, cur_result in date_dict.items():
                try:
                    output_data = fun(cur_result)
                    cur_dict[ticker] = output_data
                except ValueError:
                    print('The passed function handle is invalid')
            output_dict[key_date] = cur_dict
            end_time = time.time()
            print('Load {0:03d} of {1:03d}, time{2}'.format(counter, len(self.result), end_time-start_time))

        return pd.DataFrame(output_dict)

    def to_pickle(self, name):
        """
        Save current object to pickle file for further use.
        The save folder is set to be default : ~/Root/Data/
        :param name: File name
        """
        path = os.path.join(config.temp_data_path, name + '.p')
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


# Load ssr for each regression
def get_ssr(reg_res):
    return reg_res.ssr
