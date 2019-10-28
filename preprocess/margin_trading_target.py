from core.portfolio import *
import config
import pandas as pd
import os
from core.utils import *

start_time = '2010-04'
end_time = '2019-07'
month, _, _, _, _, _ = get_split((start_time, end_time))

margin_target_path = r'/Users/oranbebai/Documents/Data/Finance/Raw/rzrq_target.csv'
margin_target = pd.read_csv(margin_target_path, index_col=0)

Margin_Buy = {}
Sell_Out = {}
rz_file = margin_target[margin_target['targetType'] == 10]
rq_file = margin_target[margin_target['targetType'] == 20]

for num, row in rz_file.iterrows():
    ticker = row['secID'].split('.')[0]
    Margin_Buy[ticker] = {}
    targetType = row['targetType']
    date = row['intoDate']
    month_split = month[0][0]
    for month_split in month:
        if month_split[0] < date:
            continue
        Margin_Buy[ticker][month_split[0]] = 1.0

for num, row in rq_file.iterrows():
    ticker = row['secID'].split('.')[0]
    Sell_Out[ticker] = {}
    targetType = row['targetType']
    date = row['intoDate']
    month_split = month[0][0]
    for month_split in month:
        if month_split[0] < date:
            continue
        Sell_Out[ticker][month_split[0]] = 1.0

margin_target = pd.DataFrame(Margin_Buy).fillna(0)
short_target = pd.DataFrame(Sell_Out).fillna(0)

margin_target_path = os.path.join(config.feature_directory, 'MarginTradingTarget.csv')
short_target_path = os.path.join(config.feature_directory, 'ShortSellTarget.csv')

margin_target.to_csv(margin_target_path)
short_target.to_csv(short_target_path)