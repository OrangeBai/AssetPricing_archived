from core.adv_utlis import *


def regress(period, y_panel, factor_panels=None, factor_names=None):
    if factor_names is None:
        factor_names = ['RiskPremium1', 'SMB1', 'HML1']
    rf_month = get_rf_rate(period, mode='m')
    all_factor = get_factors(period)
    selected_factors = all_factor.loc[:, factor_names]

    if factor_panels is not None:
        for panel_name in factor_panels:
            panel_path = os.path.join(config.panel_data_directory, panel_name)
            panel = PanelData.load_pickle(panel_path)
            ret = panel.ret
            selected_factors[panel_name.split(',')[0]] = (ret.iloc[:, 0] + ret.iloc[:, 3] -
                                                          ret.iloc[:, 2] - ret.iloc[:, 5]) / 2

    return


regress(('1997-01', '2010-04'), 'a', factor_panels=['MV_Sigma_Pre_55.p', 'MV_Sigma_Cur_55.p'])
