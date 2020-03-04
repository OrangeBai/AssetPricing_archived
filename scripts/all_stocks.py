from core.portfolio import *
from core.allocate import *
from core.adv_utlis import *
import config

period = config.all_period
des = 'Return and market value of all stocks from 1997 to 2019'

ret_path = os.path.join(config.extracted_directory, 'DailyRet.csv')
ret = pd.read_csv(ret_path, index_col=0)
ret = ret[period[0]: period[1]]

mv_path = os.path.join(config.extracted_directory, 'CirculateMktValue.csv')
mv = pd.read_csv(mv_path, index_col=0)
mv = mv[period[0]: period[1]]

all_stocks = Portfolio(period, des, ret, mv)
all_stocks.print()
all_stocks_path = os.path.join(config.temp_data_path, 'AllStocksPortfolio.p')
all_stocks.to_pickle(all_stocks_path)

# allocator_M = Allocate(config.A_lists, config.month_split)
# allocator_M_path = os.path.join(config.temp_data_path, 'Allocator_M.p')
# allocator_M.to_pickle(allocator_M_path)

allocator_M_all = Allocate(config.A_lists, config.month_split, exclude_fin=0)
allocator_M_all_path = os.path.join(config.temp_data_path, 'Allocator_M_all.p')
allocator_M_all.to_pickle(allocator_M_all_path)

month_all_path = os.path.join(config.panel_data_directory, 'All_month.p')
month_all_panel = PanelData(('1997-01', '2019-07'), all_stocks, {'all':allocator_M_all.periods_to_tickers})
month_all_panel.to_pickle(month_all_path)
# allocator_Y = Allocate(config.A_lists, config.year_split, num_of_nan=40)
# allocator_Y_path = os.path.join(config.temp_data_path, 'Allocator_Y.p')
# allocator_Y.to_pickle(allocator_Y_path)

allocator_Y_all = Allocate(config.A_lists, config.year_split, num_of_nan=40, exclude_fin=0)
allocator_Y_all_path = os.path.join(config.temp_data_path, 'Allocator_Y_all.p')
allocator_Y_all.to_pickle(allocator_Y_all_path)

year_all_path = os.path.join(config.panel_data_directory, 'All_year.p')
year_all_panel = PanelData(('1997-01', '2020-01'), all_stocks, {'all':allocator_Y_all.periods_to_tickers})
year_all_panel.to_pickle(year_all_path)

print(1)