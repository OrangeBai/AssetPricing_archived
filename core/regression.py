from core.adv_utlis import *
import pandas as df

def reg(y, x):
    """
    Regression of panel data on the given factors.
    :param y: Panel data, data frame of T*N, where T stands for the time length and N is the number of portfolios.
    :param x: Factors, data frame of T*M, where m is the number of factors.(without constant)
    :return:
    """
    names = y.columns.to_list()
    y = np.array(y)
    x = np.array(x)
    (T1, N) = y.shape
    (T2, M) = x.shape
    coef = pd.DataFrame()
    t_value = pd.DataFrame()
    p_value = pd.DataFrame()
    resid = pd.DataFrame()
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
        resid[port_name] = result.resid
        adjRsquare[port_name] = result.rsquared_adj
    coef = coef.T
    t_value = t_value.T
    p_value = p_value.T
    return coef, t_value, p_value, adjRsquare, resid


def GRS(Y, X):
    n = Y.shape[1]
    t = X.shape[0]
    l = X.shape[1] - 1
    res = reg(Y, X)
    alpha = res[0][0]
    sigma = res[4]
    Simga = np.cov(sigma.T, ddof=l+1)
    mu = X.mean(axis=0)[1:]
    F = X[:, 1:]
    omega = np.cov(F.T)
    grs = alpha.dot(np.linalg.inv(Simga)).dot(alpha)/(1+mu.dot(np.linalg.inv(omega)).dot(mu))*(t/n)*((t-n-l)/(t-l-1))
    abs_alpha = np.abs(alpha).mean()
    Y_mean = Y.mean(axis=0)
    adj_Y_mean = Y_mean - Y_mean.mean()
    ret_3 = abs_alpha / abs(Y_mean).mean()
    ret_4 = alpha.var()/Y_mean.var()
    ret_5 = abs_alpha / np.abs(adj_Y_mean).mean()
    return grs, abs_alpha, ret_3, ret_4


def regress(period, y_panel_name, factor_panels=None, factor_names=None):
    HML_path = os.path.join(config.panel_data_directory, 'MV_PB_23.p')
    t = PanelData.load_pickle(HML_path)
    HML = (t.ret.iloc[:, 0] + t.ret.iloc[:, 3] - t.ret.iloc[:, 2] - t.ret.iloc[:, 5])
    SMB = (t.ret.iloc[:, 0] + t.ret.iloc[:, 1] + t.ret.iloc[:, 2] -
           t.ret.iloc[:, 3] - t.ret.iloc[:, 4] - t.ret.iloc[:, 5]) / 3
    Rm_path = os.path.join(config.panel_data_directory, 'All_year.p')
    Rm_panel = PanelData.load_pickle(Rm_path)
    factors = Rm_panel.ret
    factors['HML'] = HML
    factors['SMB'] = SMB
    if factor_names is None:
        factor_names = ['RiskPremium1', 'SMB1', 'HML1']
    rf_month = get_rf_rate(period, mode='m')
    # all_factor = get_factors(period)
    # selected_factors = all_factor.loc[:, factor_names]

    y_panel_path = os.path.join(config.panel_data_directory, y_panel_name)
    y_panel = PanelData.load_pickle(y_panel_path)
    y_panel.set_weight('vw')

    if factor_panels is not None:
        for panel_name in factor_panels:
            panel_path = os.path.join(config.panel_data_directory, panel_name)
            panel = PanelData.load_pickle(panel_path)
            panel.set_weight('vw')
            ret = panel.ret
            factors[panel_name.split(',')[0]] = (ret.iloc[:, 0] + ret.iloc[:, 3] -
                                                          ret.iloc[:, 2] - ret.iloc[:, 5]) / 2

    rets = y_panel.ret
    monthly_rets = period_ret_all(rets, config.month_split, period)
    monthly_factors = period_ret_all(factors, config.month_split, period)
    monthly_factors.loc[:, 'all'] = monthly_factors.loc[:, 'all'].subtract(rf_month)

    Rp_Rf = monthly_rets.subtract(rf_month, axis=0)
    X = np.array(monthly_factors)
    X = sm.add_constant(X)
    return reg(Rp_Rf, X)


def cal_grs(period, y_panel_name, factor_panels=None, factor_names=None):
    if factor_names is None:
        factor_names = ['RiskPremium1', 'SMB1', 'HML1']
    rf_month = get_rf_rate(period, mode='m')
    all_factor = get_factors(period)
    selected_factors = all_factor.loc[:, factor_names]

    y_panel_path = os.path.join(config.panel_data_directory, y_panel_name)
    y_panel = PanelData.load_pickle(y_panel_path)
    y_panel.set_weight('vw')

    if factor_panels is not None:
        for panel_name in factor_panels:
            panel_path = os.path.join(config.panel_data_directory, panel_name)
            panel = PanelData.load_pickle(panel_path)
            panel.set_weight('vw')
            ret = panel.ret
            selected_factors[panel_name.split(',')[0]] = (ret.iloc[:, 0] + ret.iloc[:, 3] -
                                                          ret.iloc[:, 2] - ret.iloc[:, 5]) / 2

    rets = y_panel.ret
    monthly_rets = period_ret_all(rets, config.month_split, period)
    monthly_factors = period_ret_all(selected_factors, config.month_split, period)

    Rp_Rf = monthly_rets.subtract(rf_month, axis=0)
    X = np.array(monthly_factors)
    X = sm.add_constant(X)
    grs = GRS(Rp_Rf, X)
    return grs


def FM_regression(X,Y):
    """
    Fama Macbeth regression
    @param X:
    @param Y:
    @return:
    """


if __name__ == '__main__':
    res_1 = cal_grs(('1997-01', '2010-04'), 'MV_AdjTover_Pre_55.p', factor_panels=['MV_AdjTover_Pre_23.p'])
