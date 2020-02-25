from core.adv_utlis import *

ret_path = os.path.join(config.extracted_directory, 'DailyRet.csv')
rets = pd.read_csv(ret_path, index_col=0)
rets_month = period_ret_all(rets, config.month_split_all)
month_ret_path = os.path.join(config.feature_directory, 'M_Return.csv')
rets_month.to_csv(month_ret_path)

month_tags = rets_month.index.to_list()

pre_month = {}
for i in range(len(month_tags)):
    if i > 0:
        pre_month[month_tags[i]] = rets_month.loc[month_tags[i-1], :]
pre_month = pd.DataFrame(pre_month).T
pre_month_ret_path = os.path.join(config.feature_directory, 'M_Return_Pre.csv')
pre_month.to_csv(pre_month_ret_path)

pre_11_month = {}
for i in range(len(month_tags)):
    if i > 11:
        pre_11_month[month_tags[i]] = rets_month.loc[month_tags[i-12]: month_tags[i-1], :].sum()
pre_11_month = pd.DataFrame(pre_11_month).T
pre_11_month_ret_path = os.path.join(config.feature_directory, 'M_Return_Pre_11.csv')

pre_11_month.to_csv(pre_11_month_ret_path)