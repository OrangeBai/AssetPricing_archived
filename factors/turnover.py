from core.adv_utlis import *
from core.portfolio import *
from core.allocate import *
import config

# Load Feature
turnover_path = os.path.join(config.extracted_directory, 'DailyTurnover.csv')
turnover = pd.read_csv(turnover_path, index_col=0)

stock_nums = turnover.shape[1]  # Number of stocks, M
dates_nums = turnover.shape[0]  # Number of trade dates, N

# Load month tags
month_tags = config.month_tag

# Calculate daily average turnover of all stocks
average_turnover = turnover.mean(axis=1)

# Calculate average turnover of calender month
turnover_month = {}
for i in range(len(month_tags) - 1):
    turnover_month[month_tags[i + 1]] = turnover[month_tags[i]: month_tags[i + 1]].mean()
turnover_month = pd.DataFrame(turnover_month).T
turnover_monthly_path = os.path.join(config.feature_directory, 'M_Tover.csv')
turnover_month.to_csv(turnover_monthly_path)

# Daily turnover subtract daily average turnover
reduced_turnover = turnover.subtract(average_turnover, axis='index')

# For each trading day T, calculate the average turnover of T-125 to T-5
adjTover_daily = {}
for i in range(dates_nums):
    # Idiosyncratic turnover of each stock subtract mean of idiosyncratic turnover from T-125 to T-5
    if i < 125:
        continue
    date = reduced_turnover.index[i]
    adjTover_daily[date] = reduced_turnover.iloc[i] - reduced_turnover.iloc[i - 125:i - 5, :].mean()

# Adjusted daily turnover.DataFrame looks like (N-125) * M
average_of_120_days = pd.DataFrame(adjTover_daily).T
turnover_daily_path = os.path.join(config.feature_directory, 'D_AdjTover.csv')
average_of_120_days.to_csv(turnover_daily_path)

adjTove_month = {}
for i in range(len(month_tags) - 1):
    adjTove_month[month_tags[i + 1]] = average_of_120_days[month_tags[i]: month_tags[i + 1]].mean()
adjusted_monthly = pd.DataFrame(adjTove_month).T
adjTove_monthly_path = os.path.join(config.feature_directory, 'M_AdjTover_Pre.csv')
adjusted_monthly.to_csv(adjTove_monthly_path)

adjTove_month_C = {}
for i in range(len(month_tags) - 1):
    adjTove_month_C[month_tags[i]] = average_of_120_days[month_tags[i]: month_tags[i + 1]].mean()
adjusted_month_C = pd.DataFrame(adjTove_month_C).T
adjTove_month_path_C = os.path.join(config.feature_directory, 'M_AdjTover_Cur.csv')
adjusted_month_C.to_csv(adjTove_month_path_C)
# """
# Once the adjusted turnover is calculated, stocks can be allocated into different groups according to their features.
# 2*3 groups and 5*5 groups are formed so that the adjTover factor can be calculated.
# """
# # Load daily return and market value of all stocks
# all_stocks_data_path = os.path.join(config.temp_data_path, 'AllStocksPortfolio.p')
# all_stocks_data = Portfolio.load_pickle(all_stocks_data_path)
#
# # Create Allocator Object
# allocator_path = os.path.join(config.temp_data_path, 'Allocator_M.p')
# allocator = Allocate.load_pickle(allocator_path)
#
# # Add features.
# allocator.add_factor('adjTover', adjTove_monthly_path)
# allocator.add_factor('adjTover_C', adjTove_month_path_C)
# MV_monthly_path = os.path.join(config.feature_directory, 'M_MktV.csv')
# allocator.add_factor('MV', MV_monthly_path)

# # allocate all A stocks into 2 * 3 groups to calculate turnover factor
# MV_Adj_23_groups = allocator.allocate_stocks_according_to_factors(['MV', 'adjTover'],
#                                                                   [(0, 0.5, 1), (0, 0.3, 0.7, 1)])
# MV_Adj_23_groups_C = allocator.allocate_stocks_according_to_factors(['MV', 'adjTover_C'],
#                                                                     [(0, 0.5, 1), (0, 0.3, 0.7, 1)])
#
# MV_Adj_23_panel = generate_panel(all_stocks_data, config.period, MV_Adj_23_groups)
# MV_Adj_23_panel_path = os.path.join(config.temp_data_path, 'MV_AdjTover_23')
# MV_Adj_23_panel.to_pickle(MV_Adj_23_panel_path)
# MV_Adj_23_panel_ret = MV_Adj_23_panel.ret
# adjTover_factor = (MV_Adj_23_panel_ret.iloc[:, 0] - MV_Adj_23_panel_ret.iloc[:, 2] +
#                    MV_Adj_23_panel_ret.iloc[:, 3] - MV_Adj_23_panel_ret.iloc[:, 5]) / 2
#
# MV_Adj_23_panel_C = generate_panel(all_stocks_data, config.period, MV_Adj_23_groups_C)
# MV_Adj_23_panel_path_C = os.path.join(config.temp_data_path, 'MV_AdjTover_23_C')
# MV_Adj_23_panel_C.to_pickle(MV_Adj_23_panel_path_C)
# MV_Adj_23_panel_ret_C = MV_Adj_23_panel_C.ret
# adjTover_C_factor = (MV_Adj_23_panel_ret_C.iloc[:, 0] - MV_Adj_23_panel_ret_C.iloc[:, 2] +
#                      MV_Adj_23_panel_ret_C.iloc[:, 3] - MV_Adj_23_panel_ret_C.iloc[:, 5]) / 2
#
# adjTover_factor_path = os.path.join(config.factor_path, 'adjTover.csv')
# adjTover_factor.to_csv(adjTover_factor_path, header=True)
#
# adjTover_factor_C_path = os.path.join(config.factor_path, 'adjTover_C.csv')
# adjTover_C_factor.to_csv(adjTover_factor_C_path, header=True)
# print(1)
