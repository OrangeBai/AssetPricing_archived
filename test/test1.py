from core.portfolio import *
import pandas as pd
import statsmodels.api as sm
import numpy as np
import config
import time

period = ('2010-04', '2019-07')

cur_panel = PanelData.load_pickle(r'/Users/oranbebai/Code/Finance/Liquidity/temp_data/mv_turn2_3.p')
ret = cur_panel.ret
turnover_factor = (ret.iloc[:, 0] - ret.iloc[:, 2] + ret.iloc[:, 3] - ret.iloc[:, 5]) / 2

print(1)
