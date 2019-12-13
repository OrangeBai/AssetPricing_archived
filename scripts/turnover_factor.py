from core.allocate import *
from core.portfolio import *
from core.utils import *
from core.adv_utlis import *
import config
import os

# Load daily return and market value of all stocks
all_stocks_data_path = os.path.join(config.temp_data_path, 'AllStocksPortfolio.p')
all_stocks_data = Portfolio.load_pickle(all_stocks_data_path)

# Load features of all stocks
all_stocks_feature_path = os.path.join(config.temp_data_path, 'AllStocksAllocate.p')
all_stocks_feature = Allocate.load_pickle(all_stocks_feature_path)
all_stocks_feature.add_factor('turn', '/Users/oranbebai/Documents/Data/Finance/Features/turnover_month.csv')

# allocate all A stocks into 2 * 3 groups to calculate turnover factor
groups = all_stocks_feature.allocate_stocks_according_to_factors(['mv', 'adj_turnover'],
                                                                 [(0, 0.5, 1), (0, 0.3, 0.7, 1)])
cur_panel = PanelData(config.period, all_stocks_data, groups)
ret = cur_panel.ret
turnover_factor = (ret.iloc[:, 0] - ret.iloc[:, 2] + ret.iloc[:, 3] - ret.iloc[:, 5]) / 2
cur_panel.to_pickle('mv_turnover_2_3')

# allocate all A stocks into 5 * 5 groups according to market value and turnover to calculate portfolio return
groups = all_stocks_feature.allocate_stocks_according_to_factors(['mv', 'adj_turnover'],
                                                                 [(0, 0.2, 0.4, 0.6, 0.8, 1),
                                                                  (0, 0.2, 0.4, 0.6, 0.8, 1)])
cur_panel = PanelData(config.period, all_stocks_data, groups)
cur_panel.to_pickle('mv_adj_turnover_5_5')

