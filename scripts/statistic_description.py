from core.adv_utlis import *
from scipy.stats import jarque_bera, skew, kurtosis
import config

names = [('Allocator_M.p', ('1997-01', '2010-04')),
        ('non_saleable_allocator.p', ('2010-04', '2019-07')),
        ('saleable_allocator.p', ('2010-04', '2019-07'))]
data = PanelData.load_pickle(os.path.join(config.temp_data_path, 'AllStocksPortfolio.p'))
pds = []
for name, period in names:
    group = {}
    cur_df = pd.DataFrame(np.zeros((2, 8)))
    a = Allocate.load_pickle(os.path.join(config.temp_data_path, name))

    mn = 99999
    mx = 0
    for periods, value in a.periods_to_tickers.items():
        if len(value) > mx:
            mx = len(value)
        if len(value) < mn:
            mn = len(value)
    cur_df.iloc[0, 0] = mn
    cur_df.iloc[0, 1] = mx

    group[name] = a.periods_to_tickers
    p1 = generate_panel(data, period, group)
    p2 = generate_panel(data, period, group, weight='equal')
    p1_ret = period_ret_all(p1.ret, config.month_split, period)
    p2_ret = period_ret_all(p2.ret, config.month_split, period)
    cur_df.iloc[0, 2] = p1_ret.mean().iloc[0]
    cur_df.iloc[1, 2] = p2_ret.mean().iloc[0]

    cur_df.iloc[0, 3] = p1_ret.var().iloc[0]
    cur_df.iloc[1, 3] = p2_ret.var().iloc[0]

    cur_df.iloc[0, 4] = skew(p1_ret)
    cur_df.iloc[1, 4] = skew(p2_ret)

    cur_df.iloc[0, 5] = kurtosis(p1_ret)
    cur_df.iloc[1, 5] = kurtosis(p2_ret)

    cur_df.iloc[0, 6], cur_df.iloc[0, 7] = jarque_bera(p1_ret)
    cur_df.iloc[1, 6], cur_df.iloc[1, 7] = jarque_bera(p2_ret)

    pds.append(cur_df)

ret = pd.concat(pds, axis=0)
print(1)
