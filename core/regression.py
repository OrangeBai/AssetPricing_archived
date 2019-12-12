from core.adv_utlis import *


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


def regress(period, y_panel_name, factor_panels=None, factor_names=None):
    if factor_names is None:
        factor_names = ['RiskPremium1', 'SMB1', 'HML1']
    rf_month = get_rf_rate(period, mode='m')
    all_factor = get_factors(period)
    selected_factors = all_factor.loc[:, factor_names]

    y_panel_path = os.path.join(config.panel_data_directory, y_panel_name)
    y_panel = PanelData.load_pickle(y_panel_path)

    if factor_panels is not None:
        for panel_name in factor_panels:
            panel_path = os.path.join(config.panel_data_directory, panel_name)
            panel = PanelData.load_pickle(panel_path)
            ret = panel.ret
            selected_factors[panel_name.split(',')[0]] = (ret.iloc[:, 0] + ret.iloc[:, 3] -
                                                          ret.iloc[:, 2] - ret.iloc[:, 5]) / 2

    rets = y_panel.ret
    monthly_rets = period_ret_all(rets, config.month_split, period)
    monthly_factors = period_ret_all(selected_factors, config.month_split, period)

    Rp_Rf = monthly_rets.subtract(rf_month, axis=0)
    X = np.array(monthly_factors)
    X = sm.add_constant(X)

    return reg(Rp_Rf, X)


if __name__ == '__main__':
    a = regress(('1997-01', '2010-04'), 'MV_AdjTover_Pre_55.p', factor_panels=['MV_Sigma_Pre_23.p'])
    b = regress(('2010-04', '2019-07'), 'Saleable_MV_AdjTover_Pre_55.p',
                factor_panels=['MV_Sigma_Pre_23.p'])
    c = regress(('2010-04', '2019-07'), 'Non_Saleable_MV_AdjTover_Pre_55.p',
                factor_panels=['MV_Sigma_Pre_23.p'])
    print(1)
