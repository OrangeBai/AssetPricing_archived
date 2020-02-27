from core.rolling_windows import *
from core.portfolio import *
from core.allocate import *
from core.adv_utlis import *

# Load the panel data of dependent portfolios
ret_path = os.path.join(config.extracted_directory, 'DailyRet.csv')
rets = pd.read_csv(ret_path, index_col=0)

# Load trade dates
trade_dates = rets.index.to_list()

# Load factor file of market, SMB, HML
factor_path = os.path.join(config.raw_directory, 'STK_MKT_FivefacDay.txt')
factors_day = get_factors(config.all_period)
factors = factors_day.iloc[:, [0, 2, 4]]

# Load rf data
rf_file_path = os.path.join(config.raw_directory, 'TRD_Nrrate.txt')
rf = get_rf_rate(rf_file_path, config.all_period)

month_split = config.month_split
month_tag = config.month_tag

# Period dictionary: {Month_T: (Month_T-1, Month_T-1)
period_dict = {}
for period in month_split:
    start_id = month_tag.index(period[0])
    reg_start_id = month_tag[start_id - 1]
    reg_end_id = month_tag[start_id]
    period_dict[period[0]] = (reg_start_id, reg_end_id)

period_dict[month_split[-1][1]] = (month_split[-1][0], month_split[-1][1])
# Fama-French regression is performed for each stock for 120 days
rw = RollingWindow(rets, factors, group_by=period_dict, nan_num=5)
result = rw.regress('group')

# read result and save
res = rw.read_result(get_ssr).T

# Create cur_sigma and one-month-lag Sigma DataFrame
new_df = res.iloc[1:]   # Current Sigma
new_idx = res.index.to_list()[:-1]
new_df.index = new_idx

res = res.iloc[:-1, :]  # One-month-lag

Sigma_M_Cur_path = os.path.join(config.feature_directory, 'M_Sigma_Cur.csv')
Sigma_M_Pre_path = os.path.join(config.feature_directory, 'M_Sigma_Pre.csv')

res.to_csv(Sigma_M_Pre_path)
new_df.to_csv(Sigma_M_Cur_path)

