from core.rolling_windows import *
from core.portfolio import *
from core.allocate import *
from core.adv_utlis import *

# set the regression period
period = ('1997-01', '2019-06')

# Load rf data
rf_file_path = os.path.join(config.raw_directory, 'TRD_Nrrate.txt')
rf = get_rf_rate(config.all_period, mode='m')

# Load the panel data of dependent portfolios
month_ret_path = os.path.join(config.feature_directory, 'M_Return.csv')
rets = pd.read_csv(month_ret_path, index_col=0).loc[period[0]:period[1], :]
rets = rets.subtract(rf, axis=0)

# Load factor file of market, SMB, HML
factor_path = os.path.join(config.raw_directory, 'STK_MKT_FivefacDay.txt')
factors_day = get_factors(config.all_period)
factors_month = period_ret_all(factors_day, config.month_split_all)
factors = factors_month.iloc[:, [0]]
factors = factors.loc[period[0]:period[1], :]

# Fama-French regression is performed for each stock for 120 days
rw = RollingWindow(rets, factors, windows_length=36, nan_num=5)
result = rw.regress('window')


def get_beta(reg_res):
    return reg_res.params[1]

res = rw.read_result(get_beta)
res = res.T

beta_path = os.path.join(config.feature_directory, 'M_beta.csv')
res.to_csv(beta_path)
print(1)
