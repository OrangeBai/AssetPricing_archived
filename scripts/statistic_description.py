from core.adv_utlis import *
from scipy.stats import jarque_bera, skew, kurtosis, ttest_1samp
import config
import numpy as np

period_all = ('1997-01', '2019-06')
period_1 = ('1997-01', '2010-03')
period_2 = ('2010-04', '2019-06')

names = [('Allocator_M.p', ('1997-01', '2010-04')),
         ('non_saleable_allocator.p', ('2010-04', '2019-07')),
         ('saleable_allocator.p', ('2010-04', '2019-07'))]
data = PanelData.load_pickle(os.path.join(config.temp_data_path, 'AllStocksPortfolio.p'))

time_series_list = []

for name, period in names:
    group = {}
    cur_df = pd.DataFrame(np.zeros((2, 8)))
    a = Allocate.load_pickle(os.path.join(config.temp_data_path, name))

    group[name] = a.periods_to_tickers
    p1 = PanelData(period, data, group)

    p1_ret = period_ret_all(p1.ret_vw, config.month_split, period)

    time_series_list.append(p1_ret)

factor_names = ['RiskPremium1', 'SMB1', 'HML1']
rf_month = get_rf_rate(period_all, mode='m')
all_factor = get_factors(period_all)
selected_factors = all_factor.loc[:, factor_names]

factor_panels = ['MV_Sigma_Cur_23.p', 'MV_Sigma_Pre_23.p', 'MV_AdjTover_Cur_23.p', 'MV_AdjTover_Pre_23.p']
if factor_panels is not None:
    for panel_name in factor_panels:
        panel_path = os.path.join(config.panel_data_directory, panel_name)
        panel = PanelData.load_pickle(panel_path)
        panel.set_weight('vw')
        ret = panel.ret
        selected_factors[panel_name.split(',')[0]] = (ret.iloc[:, 0] + ret.iloc[:, 3] -
                                                      ret.iloc[:, 2] - ret.iloc[:, 5]) / 2

selected_monthly = period_ret_all(selected_factors, config.month_split, period_all)

df_1 = selected_monthly.loc[period_1[0]: period_1[1]]
df_1['all'] = time_series_list[0]

df_2 = selected_monthly.loc[period_2[0]: period_2[1]]
df_2['Non'] = time_series_list[1]
df_2['short'] = time_series_list[2]


def cal_table_features(df):
    """
    Calculate statistical features of df
    @param df: input df
    @return:    [mean, var, skewness, kurtosis, 25th, 75th, t-statistics]
                [covariance]
    """
    df_feature = {}
    for idx in df.columns:
        s = df.loc[:, idx] * 100
        temp_list = [s.mean(), np.std(s), skew(s), kurtosis(s),
                     np.percentile(s, 25), np.percentile(s, 75), ttest_1samp(s, 0)[0], ttest_1samp(s, 0)[1]]
        df_feature[idx] = temp_list
    df_feature = pd.DataFrame(df_feature).T
    df_feature.columns = ['mean', 'std', 'skewness', 'kurtosis', '25th', '75th', 't-statistics', 'p-value']

    df_cov = np.corrcoef(df.T.iloc[:,:7])
    df_cov = pd.DataFrame(df_cov, index=df.columns, columns=df.columns)
    df_cov.columns = df.columns
    df_cov.index = df.columns
    return df_feature, df_cov


f1, cov1 = cal_table_features(df_1)
f2, cov2 = cal_table_features(df_2)

print(1)
