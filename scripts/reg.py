from core.adv_utlis import *
fr

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

    reg(Rp_Rf, X)

    return


regress(('1997-01', '2010-04'), 'MV_AdjTover_Cur_55.p', factor_panels=['MV_Sigma_Pre_23.p', 'MV_Sigma_Cur_23.p'])
