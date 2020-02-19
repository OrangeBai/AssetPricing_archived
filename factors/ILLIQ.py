from core.portfolio import *
import os
import config
import pandas as pd
import numpy

ret_path = os.path.join(config.extracted_directory, 'DailyRet.csv')
ret = pd.read_csv(ret_path, index_col=0)

volumn_path = os.path.join(config.extracted_directory, 'Amount.csv')
volumn = pd.read_csv(volumn_path, index_col=0)

daily_ILLIQ = abs(ret.loc[:, volumn.columns.to_list()]) / volumn * 10e8

month_tags = config.month_tag

ILLIQ = {}
for i in range(len(month_tags) - 1):
    ILLIQ[month_tags[i + 1]] = daily_ILLIQ[month_tags[i]: month_tags[i + 1]].mean()

ILLIQ = pd.DataFrame(ILLIQ).T

ILLIQ_path = os.path.join(config.feature_directory, 'M_ILLIQ.csv')
ILLIQ.to_csv(ILLIQ_path)