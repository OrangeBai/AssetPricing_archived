from core.adv_utlis import *
from scipy.stats import jarque_bera, skew, kurtosis, norm
import config
import matplotlib.pyplot as plt
import seaborn as sns

names = [('Allocator_M.p', ('1997-01', '2010-04')),
         ('non_saleable_allocator.p', ('2010-04', '2019-07')),
         ('saleable_allocator.p', ('2010-04', '2019-07'))]
# data = PanelData.load_pickle(os.path.join(config.temp_data_path, 'AllStocksPortfolio.p'))
# pds = []
# rets_1 = []
# rets_2 = []
# retss_1 = []
# retss_2 = []
# for name, period in names:
#     group = {}
#     cur_df = pd.DataFrame(np.zeros((2, 8)))
#     a = Allocate.load_pickle(os.path.join(config.temp_data_path, name))
#
#     mn = 99999
#     mx = 0
#     for periods, value in a.periods_to_tickers.items():
#         if len(value) > mx:
#             mx = len(value)
#         if len(value) < mn:
#             mn = len(value)
#     cur_df.iloc[0, 0] = mn
#     cur_df.iloc[0, 1] = mx
#
#     group[name] = a.periods_to_tickers
#     p1 = generate_panel(data, period, group)
#     p2 = generate_panel(data, period, group, weight='equal')
#     rets_1.append(p1.ret)
#     rets_2.append(p2.ret)
#
#     p1_ret = period_ret_all(p1.ret, config.month_split, period)
#     p2_ret = period_ret_all(p2.ret, config.month_split, period)
#
#     retss_1.append(p1_ret)
#     retss_2.append(p2_ret)
#
#     cur_df.iloc[0, 2] = p1_ret.mean().iloc[0]
#     cur_df.iloc[1, 2] = p2_ret.mean().iloc[0]
#
#     cur_df.iloc[0, 3] = p1_ret.var().iloc[0]
#     cur_df.iloc[1, 3] = p2_ret.var().iloc[0]
#
#     cur_df.iloc[0, 4] = skew(p1_ret)
#     cur_df.iloc[1, 4] = skew(p2_ret)
#
#     cur_df.iloc[0, 5] = kurtosis(p1_ret)
#     cur_df.iloc[1, 5] = kurtosis(p2_ret)
#
#     cur_df.iloc[0, 6], cur_df.iloc[0, 7] = jarque_bera(p1_ret)
#     cur_df.iloc[1, 6], cur_df.iloc[1, 7] = jarque_bera(p2_ret)
#
#     pds.append(cur_df)
#
#
# ret = pd.concat(pds, axis=0)
# print(1)
#
# a = retss_1[0]
# temp0 = (a - a.mean())/a.std()
# a = retss_1[1]
# temp1 = (a - a.mean())/a.std()
# a = retss_1[2]
# temp2 = (a - a.mean())/a.std()
#
# sns.distplot(temp0, color='b', fit=norm, label='Period 1', hist=False)
# sns.distplot(temp1, color='g', label='Period 2', hist=False)
# sns.distplot(temp2, color='y', label='Period 3', hist=False)
#
# files = ['M_Sigma_Cur.csv', 'M_Sigma_Pre.csv', 'M_AdjTover_Cur.csv', 'M_AdjTover_Cur.csv', 'M_MktV.csv']
# sts = []
# for name, period in names:
#     a = Allocate.load_pickle(os.path.join(config.temp_data_path, name))
#     periods_to_tickers = a.periods_to_tickers
#     st = []
#     for file in files:
#         feature = pd.read_csv(os.path.join(config.feature_directory, file), index_col=0)
#         cur_st = []
#         for month, tickers in periods_to_tickers.items():
#             cur_st.append(feature.loc[month[0], tickers].mean())
#         st.append(np.array(cur_st).mean())
#     sts.append(st)
# print(1)

files = ['M_Sigma_Cur.csv', 'M_Sigma_Pre.csv', 'M_AdjTover_Cur.csv', 'M_AdjTover_Cur.csv', 'M_MktV.csv']
sts = []
files2 = ['MV_Sigma_Cur_55.p', 'Non_Saleable_MV_Sigma_Cur_55.p', 'Saleable_MV_Sigma_Cur_55.p', 'Saleable_Sigma_Cur_5.p']
# for name, period in names:
#     a = Allocate.load_pickle(os.path.join(config.temp_data_path, name))
#     periods_to_tickers = a.periods_to_tickers
#     st = []
#     for file in files:
#         feature = pd.read_csv(os.path.join(config.feature_directory, file), index_col=0)
#         cur_st = []
#         for month, tickers in periods_to_tickers.items():
#             cur_st.append(feature.loc[month[0], tickers].mean())
#         st.append(np.array(cur_st).mean())
#     sts.append(st)
# print(1)

mv = pd.read_csv(os.path.join(config.feature_directory, 'M_MktV.csv'), index_col=0)
st = {}
for file in files2:
    panel = PanelData.load_pickle(os.path.join(config.panel_data_directory, file))
    cur_st = {}
    for key, periods_to_tickers in panel.group.items():
        cur_stt = []
        a = [month for month in periods_to_tickers.keys()]
        # a.sort()
        # month = a[-1]
        # tickers = periods_to_tickers[month]
        # cur_stt.append(mv.loc[month[0], tickers].mean())
        for month, tickers in periods_to_tickers.items():
            cur_stt.append(mv.loc[month[0], tickers].mean())
        cur_st[key] = np.array(cur_stt).mean()
    st[file] = cur_st

print(1)