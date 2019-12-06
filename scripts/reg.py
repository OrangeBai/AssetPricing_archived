from core.adv_utlis import *


def regress(period, y_panel, factor_panels, factor_names=None):
    if factor_names is None:
        factor_names = ['RiskPremium1', 'SMB1', 'HML1']
    rf_month = get_rf_rate(period, mode='m')
    all_factor = get_factors(period)

    if factor_panels is not None:
        for panel in factor_panels:
            panel_path = os.path.join(config.panel_data_directory, panel)
    adjTover_factor_path = os.path.join(config.factor_path, 'adjTover.csv')
    adjTOver_factor = pd.read_csv(adjTover_factor_path, index_col=0)
    factors['adjTover'] = adjTOver_factor