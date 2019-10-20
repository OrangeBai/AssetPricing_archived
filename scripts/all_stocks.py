from core.portfolio import *
from core.allocate import *
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


allocate = Allocate(config.A_lists, config.month_split)
turnover_path = os.path.join(config.feature_directory, 'M_AdjTover.csv')
mv_path = os.path.join(config.feature_directory, 'M_MktV.csv')
sigma_path = os.path.join(config.feature_directory, 'M_Sigma.csv')
allocate.add_factor('turnover', turnover_path)
allocate.add_factor('mv', mv_path)
allocate.add_factor('sigma', sigma_path)
allocate.to_pickle('AllStocksAllocate')

