import os
import config
import pandas as pd
from core.allocate import *
from core.adv_utlis import *
from core.portfolio import *

pb_path = os.path.join(config.extracted_directory, 'PB.csv')
pb = pd.read_csv(pb_path, index_col=0)

year_tag = config.year_tag

pb_year = {}
for i in range(len(year_tag) - 1):
    try:
        pb_year[year_tag[i + 1]] = pb[year_tag[i]: year_tag[i + 1]].iloc[-1, :]
    except Exception as e:
        print(e)

pb_year = pd.DataFrame(pb_year).T

pb_year_path = os.path.join(config.feature_directory, 'Y_pb.csv')
pb_year.to_csv(pb_year_path)

data_file = 'AllStocksPortfolio.p'
allocator_file = 'Allocator_Y.p'
period = config.period

allocate(['Y_MktV.csv', 'Y_pb.csv'], ['MV', 'PB'], '2*3',
         'MV_PB_23.p', allocator_file, data_file, period)


t = PanelData.load_pickle(r'/Users/oranbebai/Documents/Data/Finance/Panel/MV_PB_23_M.p')

HML = (t.ret.iloc[:, 0] + t.ret.iloc[:, 3] - t.ret.iloc[:, 2] - t.ret.iloc[:, 5])/2
SMB = (t.ret.iloc[:, 0] + t.ret.iloc[:, 1] + t.ret.iloc[:, 2] -
       t.ret.iloc[:, 3] + t.ret.iloc[:, 4] + t.ret.iloc[:, 5]) / 3
