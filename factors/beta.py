from core.rolling_windows import *
from core.portfolio import *
from core.allocate import *
from core.adv_utlis import *

# Load the panel data of dependent portfolios
ret_path = os.path.join(config.extracted_directory, 'DailyRet.csv')
rets = pd.read_csv(ret_path, index_col=0)
rets_month = period_ret_all(rets, config.month_split_all)
month_ret_path = os.path.join(config.feature_directory, 'M_Return.csv')
# Load trade dates
trade_dates = rets.index.to_list()

# Load factor file of market, SMB, HML
factor_path = os.path.join(config.raw_directory, 'STK_MKT_FivefacDay.txt')
factors_day = get_factors(config.all_period)
factors_month = period_ret_all(factors_day, config.month_split_all)
factors = factors_month.iloc[:, [0]]

# Load rf data
rf_file_path = os.path.join(config.raw_directory, 'TRD_Nrrate.txt')
rf = get_rf_rate(config.all_period, mode='m')

month_split = config.month_split
month_tag = config.month_tag

# Period dictionary: {Month_T: (Month_T-1, Month_T-1)
period_dict = {}
for period in month_split:
    start_id = month_tag.index(period[0])
    reg_start_id = month_tag[start_id - 36]
    reg_end_id = month_tag[start_id]
    period_dict[period[0]] = (reg_start_id, reg_end_id)

period_dict[month_split[-1][1]] = (month_split[-1][0], month_split[-1][1])
# Fama-French regression is performed for each stock for 120 days
rw = RollingWindow(rets_month, factors, group_by=period_dict, nan_num=5)
result = rw.regress('group')