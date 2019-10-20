from preprocess.CSMAR import *
import config
import os

TRD_DailyRet_path = os.path.join(config.raw_directory, r'TRD_Dalyr.txt')
TRD_DailyRet_csv_path = os.path.join(config.csv_directory, 'DailyRet')
# txt_to_csv(TRD_DailyRet_path, TRD_DailyRet_csv_path, column='Stkcd', index_col='Trddt', decoding='gbk',
#            converters={'Stdcd': str})
#
extracted_path = config.extracted_directory
extract_feature(TRD_DailyRet_csv_path, extracted_path, 'Trddt', 'Dretnd', 'DailyRet', converters={'Stdcd': str})
#
output_directory = r'/Users/oranbebai/Documents/Data/Finance/Extracted'
extract_feature(TRD_DailyRet_csv_path, extracted_path, 'Trddt', 'Dsmvosd', 'CirculateMktValue', converters={'Stdcd': str})
#
# STK_MKT_Daily = os.path.join(config.raw_directory, r'STK_MKT_Dalyr.txt')
STK_MKT_Daily_csv_path = os.path.join(config.csv_directory, 'DailyIndicator')
# txt_to_csv(STK_MKT_Daily, STK_MKT_Daily_csv_path, 'Symbol', index_col='TradingDate',decoding='gbk', converters={'Symbol': str})
#
# append_path = r'/Users/oranbebai/Documents/Data/Finance/Append/2019-01-25/STK_MKT_Dalyr.txt'
# append_csv(STK_MKT_Daily_csv_path, append_path,
#            new_file_dir='/Users/oranbebai/Documents/Data/Finance/CSV/DailyIndicator2',
#            column='Symbol', date_column='TradingDate', converters={'Symbol': str})
extract_feature(STK_MKT_Daily_csv_path, extracted_path, date_col='TradingDate', column='Turnover',
                output_file_name='DailyTurnover', converters={'Symbol': str})

extract_feature(STK_MKT_Daily_csv_path, extracted_path, date_col='TradingDate', column='PB',
                output_file_name='PB', converters={'Symbol': str})

extract_feature(STK_MKT_Daily_csv_path, extracted_path, date_col='TradingDate', column='Liquidility',
                output_file_name='Liquidity', converters={'Symbol': str})

extract_feature(STK_MKT_Daily_csv_path, extracted_path, date_col='TradingDate', column='Amount',
                output_file_name='Amount', converters={'Symbol': str})
