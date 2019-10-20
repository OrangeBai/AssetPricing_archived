import os
import pandas as pd
import config
from preprocess.CSMAR import *
from core.utils import *

# This script is used for extract daily margin trading information.
# Output is listed in CSV directory and extracted features are listed in Extracted Directory

# Raw data directory, data is downloaded from QuantOS
pre_directory = '/Users/oranbebai/Documents/Data/Finance/pre'
files = os.listdir(pre_directory)
data = pd.DataFrame()
# Aggregate all data in a data frame
for file in files:
    if not os.path.splitext(file)[-1] == '.csv':
        continue
    cur_pd = pd.read_csv(os.path.join(pre_directory, file), index_col=0, converters={'ticker': str})
    data = data.append(cur_pd)

# Retrieve all tickers
tickers = data['ticker'].unique().tolist()

# Create CSV directory
margin_directory = os.path.join(config.csv_directory, 'Margin')
if not os.path.exists(margin_directory):
    os.makedirs(margin_directory)

counter = 0
# for each ticker, retrieve daily trading info
for ticker in tickers:
    counter = counter + 1
    data_ticker = data[data['ticker'] == ticker]
    file_out_path = os.path.join(margin_directory, ticker + '.csv')
    data_ticker.drop_duplicates(keep='first', subset='tradeDate', inplace=True)
    data_ticker.to_csv(file_out_path, mode='w', index=False)
    # print('Reading data of {0} from {1}. Saving to {2}'.format(idx, txt_input_path, file_out_path))
    l1 = counter * 50 // len(tickers)
    print('Reading {0}, Progress Bar: {1:><{len1}}{2:=<{len2}}. {3} of {4}'.format(ticker, '>', '=', counter,
                                                                                   len(tickers),
                                                                                   len1=l1, len2=50 - l1, ))

extract_feature(csv_dir=margin_directory, output_dir=config.extracted_directory, date_col='tradeDate',
                column='finBuyVal', output_file_name='D_FinBuyVal', converters={'ticker': str})

extract_feature(csv_dir=margin_directory, output_dir=config.extracted_directory, date_col='tradeDate',
                column='secSellVol', output_file_name='D_SecSellVol', converters={'ticker': str})

periods = ('2010-04', '2019-07')
month_split, _, _, _, _, _ = get_split(periods)

M_finBuyVal = {}
M_secSellVol = {}
D_finBuyVal = pd.read_csv(os.path.join(config.extracted_directory, 'D_FinBuyVal.csv'), index_col=0)
D_secSellVol = pd.read_csv(os.path.join(config.extracted_directory, 'D_SecSellVol.csv'), index_col=0)
for month in month_split:
    M_finBuyVal[month[1]] = D_finBuyVal.loc[month[0]:month[1], :].sum()
    M_secSellVol[month[1]] = D_secSellVol.loc[month[0]:month[1], :].sum()

M_finBuyVal = pd.DataFrame(M_finBuyVal).fillna(0).T
M_secSellVol = pd.DataFrame(M_secSellVol).fillna(0).T
M_finBuyVal.to_csv(os.path.join(config.feature_directory, 'M_finBuy.csv'))
M_secSellVol.to_csv(os.path.join(config.feature_directory, 'M_secSell.csv'))

