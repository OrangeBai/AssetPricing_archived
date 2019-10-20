import os
import pandas as pd

factor_file = r'/Users/oranbebai/Documents/Data/Finance/Raw/STK_MKT_ThrfacDay.txt'
raw_factors = pd.read_csv(factor_file, sep='\t', encoding='gbk', low_memory=False)
A_factors = raw_factors[raw_factors['MarkettypeID'] == 'P9709']
A_factors = A_factors.set_index(A_factors['TradingDate'])

mkt = A_factors['RiskPremium1'].astype('float')
SMB = A_factors['SMB1'].astype('float')
HML = A_factors['HML1'].astype('float')