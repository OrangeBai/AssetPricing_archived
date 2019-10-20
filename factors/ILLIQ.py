from core.portfolio import *
import os
import config
import pandas as pd

ret_path = os.path.join(config.data_directory, 'ret.csv')
ret = pd.read_csv(ret_path, index_col=0)

