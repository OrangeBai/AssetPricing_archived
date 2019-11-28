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

# # Set path of features
# adjTover_path = os.path.join(config.feature_directory, 'M_AdjTover.csv')
# mv_path = os.path.join(config.feature_directory, 'M_MktV.csv')
# sigma_path = os.path.join(config.feature_directory, 'M_Sigma.csv')

# Add features to allocator
saleable_allocator_path = os.path.join(config.temp_data_path, 'saleable_allocator.p')
if not os.path.exists(saleable_allocator_path):
    saleable_allocator = Allocate(tickers=config.A_lists, periods=month_split, period_to_tickers=saleable_groups)
    saleable_allocator.to_pickle(saleable_allocator_path)
else:
    saleable_allocator = Allocate.load_pickle(saleable_allocator_path)

non_saleable_allocator_path = os.path.join(config.temp_data_path, 'non_saleable_allocator.p')
if not os.path.exists(non_saleable_allocator_path):
    non_saleable_allocator = Allocate(tickers=config.A_lists, periods=month_split, period_to_tickers=non_saleable_groups)
    non_saleable_allocator.to_pickle(non_saleable_allocator_path)
else:
    non_saleable_allocator = Allocate.load_pickle(non_saleable_allocator_path)

# # Load trade dates
# trd_cale_path = os.path.join(config.raw_directory, 'TRD_Cale.txt')
# trade_dates = get_trade_dates(trd_cale_path, period)
#
# # Load risk free data
# rf_path = os.path.join(config.raw_directory, 'TRD_Nrrate.txt')
# rf_month = get_rf_rate(rf_path, period, mode='m')
#
# # Load 5 factor data
# # Index:    date;
# # Columns: 'RiskPremium1', 'RiskPremium2', 'SMB1', 'SMB2', 'HML1', 'HML2', 'RMW1', 'RMW2', 'CMA1', 'CMA2';
# factor_path = os.path.join(config.raw_directory, 'STK_MKT_FivefacDay.txt')
# factors = get_factors(factor_path, period, mode='d')
# adjTover_factor_path = os.path.join(config.factor_path, 'adjTover.csv')
# adjTOver_factor = pd.read_csv(adjTover_factor_path, index_col=0)
# factors['adjTover'] = adjTOver_factor
#
# input_factor = factors.iloc[:, [0, 2, 4]]
#
# input_factor_m = period_ret_all(input_factor, month_split)
# nonSale_adjTover_5_panel_month = period_ret_all(nonSale_adjTover_5_panel.ret, month_split).subtract(rf_month, axis=0)
# adjTover_5_panel_month = period_ret_all(adjTover_5_panel.ret, month_split).subtract(rf_month, axis=0)
#
#
# coef1, t1, p1, r1 = reg(nonSale_adjTover_5_panel_month, input_factor_m)
# coef2, t2, p2, r2 = reg(adjTover_5_panel_month, input_factor_m)
#
# nonSale_adjTover_MV_55_panel_month = period_ret_all(nonSale_adjTover_MV_55_panel.ret,
#                                                     month_split).subtract(rf_month, axis=0)
# adjTover_MV_55_panel_month = period_ret_all(adjTover_MV_55_panel.ret, month_split).subtract(rf_month, axis=0)
#
# coef3, t3, p3, r3 = reg(nonSale_adjTover_MV_55_panel_month, input_factor_m)
# coef4, t4, p4, r4 = reg(adjTover_MV_55_panel_month, input_factor_m)
#
# print(1)
# # adjTover_5_panel, adjTover_MV_55_panel, nonSale_adjTover_5_panel, nonSale_adjTover_MV_55_panel
# # reg(adjTover_5_panel, x)
