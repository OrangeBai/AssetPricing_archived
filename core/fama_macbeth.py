import pandas as pd
import statsmodels


class FamaMacBeth:
    """
    Fama MacBeth regression
    """
    def __init__(self, dependent, exogenous, first_step_num=252):
        self.dependent = dependent
        self.exogenous = exogenous
        self.first_step_num = first_step_num
        self.betas = {}
        try:
            assert self.dependent.shape[0] == self.exogenous.shape[0]
        except AssertionError:
            print('Shape of dependent variable should be equal to exogenous variable')
        try:
            assert self.dependent.shape[0] > self.first_step_num
        except AssertionError:
            print('Length of dependent variable should be longer than first_step_number')

    def _first_regression(self):
        reg_length = self.dependent.shape[0]
        beta_nums = reg_length - self.first_step_num





