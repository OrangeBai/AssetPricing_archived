from core.allocate import *
from core.utils import *
from core.adv_utlis import *
from core.regression import *

"""
This script is used for testing the difference of return between portfolios formed by short saleable stocks and 
non-short saleable stocks. Fama-french regression is performed for each portfolio with MKT, SMB, HML, adjTover or sigma 
factor. 
"""

# Load daily return and market value of all stocks
all_stocks_data_path = os.path.join(config.temp_data_path, 'AllStocksPortfolio.p')
all_stocks_data = Portfolio.load_pickle(all_stocks_data_path)

# Generate month tags and month split from 2010-04 to 2019-07
period = ('2010-04', '2019-07')
month_split = get_split(period)[0]
month_tag = get_split(period)[3]

# Read short sell target
saleable_target_path = os.path.join(config.extracted_directory, 'ShortSellTarget.csv')
saleable_pd = pd.read_csv(saleable_target_path, index_col=0)

# period_to_tickers dictionary of short sell targets
saleable_groups = {}
for date, row in saleable_pd.iterrows():
    idx = month_tag.index(date)
    key = (month_tag[idx], month_tag[idx + 1])
    saleable_groups[key] = row[row == 1.0].index.tolist()

# period_to_tickers dictionary of non short sell targets
non_saleable_groups = {}
for key, tickers in saleable_groups.items():
    non_tickers = [ticker for ticker in config.A_lists if ticker not in tickers]
    non_saleable_groups[key] = non_tickers

# Add features to allocator
saleable_allocator_path = os.path.join(config.temp_data_path, 'saleable_allocator.p')
saleable_allocator = Allocate(tickers=config.A_lists, periods=month_split, period_to_tickers=saleable_groups)
saleable_allocator.to_pickle(saleable_allocator_path)

non_saleable_allocator_path = os.path.join(config.temp_data_path, 'non_saleable_allocator.p')
non_saleable_allocator = Allocate(tickers=config.A_lists, periods=month_split, period_to_tickers=non_saleable_groups)
non_saleable_allocator.to_pickle(non_saleable_allocator_path)
