from core.portfolio import *
import pandas as pd
import statsmodels.api as sm
import numpy as np
import config
import time
# Load the panel data of dependent portfolios
panel = PanelData.load_pickle(r'/Users/oranbebai/Code/Finance/Liquidity/temp_data/mv_turnover.p')
rets = panel.ret

# Load trade dates
trade_dates = rets.index.to_list()

# Load factor file of market, SMB, HML
factor_file = r'/Users/oranbebai/Documents/Data/Finance/Raw/STK_MKT_ThrfacDay.txt'
raw_factors = pd.read_csv(factor_file, sep='\t', encoding='gbk', low_memory=False)
A_factors = raw_factors[raw_factors['MarkettypeID'] == 'P9709']
A_factors = A_factors.set_index(A_factors['TradingDate'])

# Load risk free file
rf_file_path = r'/Users/oranbebai/Documents/Data/Finance/Raw/TRD_Nrrate.txt'
rf_file = pd.read_csv(rf_file_path, sep='\t', encoding='gbk')
rf = rf_file[rf_file['Nrr1'] == 'NRI01']
rf = rf.set_index(rf['Clsdt'])
rf_day = rf['Nrrdaydt'].astype('float')
rf_day = rf_day.loc[trade_dates]
rf_month_data = rf['Nrrmtdt'].astype('float')/100

mkt = A_factors['RiskPremium1'].astype('float')  # Set market factor
mkt = mkt.loc[trade_dates]  # Slice market factor
SMB = A_factors['SMB1'].astype('float')  # Set SMB factor
SMB = SMB.loc[trade_dates]  # Slice SMB factor
HML = A_factors['HML1'].astype('float')  # Set HML factor
HML = HML.loc[trade_dates]  # Slice HML factor

# Load turn over factor
cur_panel = PanelData.load_pickle(r'/Users/oranbebai/Code/Finance/Liquidity/temp_data/mv_turn2_3.p')
ret = cur_panel.ret
turnover_factor = (ret.iloc[:, 0] - ret.iloc[:, 2] + ret.iloc[:, 3] - ret.iloc[:, 5]) / 2   # Calculate turnover factor

# Load adjusted turnover factor
cur_panel = PanelData.load_pickle(r'/Users/oranbebai/Code/Finance/Liquidity/temp_data/mv_turnover2_3.p')
ret = cur_panel.ret
adj_turnover_factor = (ret.iloc[:, 0] - ret.iloc[:, 2] + ret.iloc[:, 3] - ret.iloc[:, 5]) / 2
factors_day = pd.concat([mkt, SMB, HML, turnover_factor, adj_turnover_factor], axis=1)

# Set month tags
month_tag = [month_period[0] for month_period in config.month_split]
factors_month = {}
ret_month = {}
rf_month = {}
for month_period in config.month_split:
    factors_month[month_period[0]] = factors_day.loc[month_period[0]: month_period[1], :].sum()
    ret_month[month_period[0]] = rets.loc[month_period[0]: month_period[1], :].sum()
    rf_month_index = rf_month_data.index.to_list()
    loc = [date for date in rf_month_index if month_period[0] < date < month_period[1]]
    rf_month[month_period[0]] = rf_month_data.loc[loc][0]

factors_month = pd.DataFrame(factors_month).T
ret_month = pd.DataFrame(ret_month).T
rf_month = pd.Series(rf_month)

X1 = np.array(factors_month.iloc[:, [0, 1, 2]])
X1 = sm.add_constant(X1)

X2 = np.array(factors_month.iloc[:, [0, 1, 2, 4]])
X2 = sm.add_constant(X2)

Y = factors_month.iloc[:, 3]
results = sm.OLS(Y, X1).fit()
print(results.summary())
turnover_res = results.resid
factors_month['turnover_res'] = turnover_res

X3 = np.array(factors_month.iloc[:, [0, 1, 2, 3, 4]])
X3 = sm.add_constant(X3)

result1 = pd.DataFrame()
result2 = pd.DataFrame()

result1_t = pd.DataFrame()
result2_t = pd.DataFrame()

result3 = pd.DataFrame()
result4 = pd.DataFrame()

result3_t = pd.DataFrame()
result4_t = pd.DataFrame()

result1_p = pd.DataFrame()
result2_p = pd.DataFrame()
result3_p = pd.DataFrame()
st = 12
for i in range(25):
    name = ret_month.columns.to_list()[i]
    print('{0} \n'.format(name))
    start = time.time()
    Y = ret_month.iloc[st:159, i].subtract(rf_month.iloc[st:159])
    results = sm.OLS(Y, X1[st:159, :]).fit()
    result1[name] = results.params
    result1_t[name] = results.tvalues
    result1_p[name] = results.pvalues
    end = time.time()
    print(start-end)

    Y = ret_month.iloc[st:159, i].subtract(rf_month.iloc[st:159])
    results = sm.OLS(Y, X2[st:159, :]).fit()
    result2[name] = results.params
    result2_t[name] = results.tvalues
    result2_p[name] = results.pvalues

    Y = ret_month.iloc[:159, i].subtract(rf_month.iloc[:159])
    results = sm.OLS(Y, X3[:159, :]).fit()
    result3[name] = results.params
    result3_t[name] = results.tvalues
    result3_p[name] = results.pvalues

result1 = result1.T
result2 = result2.T
result3 = result3.T

result1_t = result1_t.T
result2_t = result2_t.T
result3_t = result3_t.T

result1_p = result1_p.T
result2_p = result2_p.T
result3_p = result3_p.T
print(result1)
print(result2)
print(result1_t)
print(result2_t)
