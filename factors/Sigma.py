import config
import os
import pandas as pd
from core.rolling_windows import *

# Load the panel data of dependent portfolios
ret_path = os.path.join(config.extracted_directory, 'DailyRet.csv')
rets = pd.read_csv(ret_path, index_col=0)

# Load trade dates
trade_dates = rets.index.to_list()

# Load factor file of market, SMB, HML
factor_file = os.path.join(config.raw_directory, 'STK_MKT_FivefacDay.txt')
raw_factors = pd.read_csv(factor_file, sep='\t', encoding='gbk', low_memory=False)
A_factors = raw_factors[raw_factors['MarkettypeID'] == 'P9709']
A_factors = A_factors.set_index(A_factors['TradingDate'])

# Load risk free file
rf_file_path = os.path.join(config.raw_directory, 'TRD_Nrrate.txt')
rf_file = pd.read_csv(rf_file_path, sep='\t', encoding='gbk')
rf = rf_file[rf_file['Nrr1'] == 'NRI01']
rf = rf.set_index(rf['Clsdt'])
rf_day = rf['Nrrdaydt'].astype('float') / 100
rf_day = rf_day.loc[trade_dates]
rf_month_data = rf['Nrrmtdt'].astype('float') / 100
rets = rets.subtract(rf_day, axis=0)

mkt = A_factors['RiskPremium1'].astype('float')  # Set market factor
mkt = mkt.loc[trade_dates]  # Slice market factor
SMB = A_factors['SMB1'].astype('float')  # Set SMB factor
SMB = SMB.loc[trade_dates]  # Slice SMB factor
HML = A_factors['HML1'].astype('float')  # Set HML factor
HML = HML.loc[trade_dates]  # Slice HML factor

factors_day = pd.concat([mkt, SMB, HML], axis=1)

month_split = config.month_split
month_tag = config.month_tag

# Period dictionary: {Month_T: (Month_T-3, Month_T-1)
period_dict = {}
for period in config.month_split:
    start_id = month_tag.index(period[0])
    reg_start_id = month_tag[start_id - 3]
    reg_end_id = month_tag[start_id]
    period_dict[period[0]] = (reg_start_id, reg_end_id)

# Fama-French regression is performed for each stock for 120 days
rw = RollingWindow(rets, factors_day, group_by=period_dict)
result = rw.regress('group')


# Load ssr for each regression
def get_ssr(reg_res):
    return reg_res.ssr


res = rw.read_result(get_ssr).T

output_path = os.path.join(config.feature_directory, 'M_Sigma.csv')
res.to_csv(output_path)
