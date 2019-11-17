import pandas as pd
import numpy as np
import statsmodels.api as sm


def reg(y, x):
    """
    Regression of panel data on the given factors.
    :param panel: Panel data, data frame of T*N, where T stands for the time length and N is the number of portfolios.
    :param x: Factors, data frame of T*M, where m is the number of factors.(without constant)
    :return:
    """
    names = y.columns.to_list()
    y = np.array(y)
    x = np.array(x)
    x = sm.add_constant(x)
    (T1, N) = y.shape
    (T2, M) = x.shape
    coef = pd.DataFrame()
    t_value = pd.DataFrame()
    p_value = pd.DataFrame()
    adjRsquare = pd.Series()
    try:
        assert T1 == T2
    except AssertionError as e:
        print('The length of Y and X should be equal, got {0} and {1}'.format(T1, T2))
    for i in range(N):
        result = sm.OLS(y[:, i], x).fit()
        port_name = names[i]
        coef[port_name] = result.params
        t_value[port_name] = result.tvalues
        p_value[port_name] = result.pvalues
        adjRsquare[port_name] = result.rsquared_adj
    coef = coef.T
    t_value = t_value.T
    p_value = p_value.T
    return coef, t_value, p_value, adjRsquare


if __name__ == '__main__':
    pass
