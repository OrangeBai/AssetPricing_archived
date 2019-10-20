from core.portfolio import *
from core.allocate import *
from core.adv_utlis import *
import config


period = ('1997-01', '2019-07')
des = 'Return and market value of all stocks from 1997 to 2019'

ret_path = os.path.join(config.extracted_directory, 'DailyRet.csv')
ret = pd.read_csv(ret_path, index_col=0)
ret = ret[period[0]: period[1]]

mv_path = os.path.join(config.extracted_directory, 'CirculateMktValue.csv')
mv = pd.read_csv(mv_path, index_col=0)
mv = mv[period[0]: period[1]]

all_stocks = Portfolio(period, des, ret, mv)
all_stocks.print()
all_stocks.to_pickle('AllStocksPortfolio')


allocator_M = Allocate(config.A_lists, config.month_split_all)
allocator_M_path = os.path.join(config.temp_data_path, 'Allocator_M.p')
allocator_M.to_pickle(allocator_M_path)


adjTover_path = os.path.join(config.feature_directory, 'M_AdjTover.csv')
mktValue_path = os.path.join(config.feature_directory, 'M_MktV.csv')
sigma_path = os.path.join(config.feature_directory, 'M_Sigma.csv')
update_allocator(allocator_M_path, ('adjTover', adjTover_path), ('MV', mktValue_path), ('sigma', sigma_path))

allocator_Y = Allocate(config.A_lists, config.year_split_all)
allocator_Y_path = os.path.join(config.temp_data_path, 'Allocator_Y.p')
allocator_Y.to_pickle(allocator_Y_path)



