from core.adv_utlis import *
"""
This script is used to extract circulated market value of all stocks in all period.
"""

# Config mv path and read data
mv_path = os.path.join(config.extracted_directory, r'CirculateMktValue.csv')
mv = pd.read_csv(mv_path, index_col=0)

# read month tags
month_tags = config.month_tag_all
mv_monthly = {month_tags[0]: np.NaN}
for i in range(len(month_tags) - 1):
    # Since the mv data is often used for allocate stocks and predict, MV of month N is record with tag N+1 for further use
    mv_monthly[month_tags[i + 1]] = mv[month_tags[i]: month_tags[i + 1]].mean()

mv_monthly = pd.DataFrame(mv_monthly).T
mv_monthly_path = os.path.join(config.feature_directory, 'M_MktV.csv')
mv_monthly.to_csv(mv_monthly_path)

# read year data
year_tags = config.year_tag_all
mv_year = {year_tags[0]: np.NaN}
for i in range(len(year_tags)-1):
    # Since the mv data is often used for allocate stocks and predict, MV of month N is record with tag N+1 for further use
    year_select = mv.loc[year_tags[i]: year_tags[i+1]]
    mv_year[year_tags[i+1]] = year_select.mean()

mv_year = pd.DataFrame(mv_year).T
mv_year_path = os.path.join(config.feature_directory, 'Y_MktV.csv')
mv_year.to_csv(mv_year_path)

# # Load daily return and market value of all stocks
# all_stocks_data_path = os.path.join(config.temp_data_path, 'AllStocksPortfolio.p')
# all_stocks_data = Portfolio.load_pickle(all_stocks_data_path)
#
# # Create Allocator Object for monthly adjusted groups
# allocator_M_path = os.path.join(config.temp_data_path, 'Allocator_M.p')
# allocator_M = update_allocator(allocator_M_path, ('MV', mv_monthly_path))
#
# # Create Allocator Object for monthly adjusted groups
# allocator_Y_path = os.path.join(config.temp_data_path, 'Allocator_Y.p')
# allocator_Y = update_allocator(allocator_Y_path, ('MV', mv_year_path))
#
# # Allocate stocks in to 2*3 groups according to mv
# MV_Y_23_groups = allocator_Y.allocate_stocks_according_to_factors(['MV'], [(0, 0.3, 0.7, 1)])
# MV_M_23_groups = allocator_M.allocate_stocks_according_to_factors(['MV'], [(0, 0.3, 0.7, 1)])
#
# MV_Y_23_panel = generate_panel(all_stocks_data, config.period, MV_Y_23_groups)
# MV_Y_23_panel_path = os.path.join(config.temp_data_path, 'MV_Y_23.p')
# MV_Y_23_panel.to_pickle(MV_Y_23_panel_path)
# MV_Y_23_panel_ret = MV_Y_23_panel.ret
# MV_Y = MV_Y_23_panel_ret.iloc[:, 0] - MV_Y_23_panel_ret.iloc[:, 2]
#
# MV_M_23_panel = generate_panel(all_stocks_data, config.period, MV_Y_23_groups)
# MV_M_23_panel_path = os.path.join(config.temp_data_path, 'MV_Y_23.p')
# MV_M_23_panel.to_pickle(MV_Y_23_panel_path)
# MV_M23_panel_ret = MV_Y_23_panel.ret
# MV_M = MV_M23_panel_ret.iloc[:, 0] - MV_M23_panel_ret.iloc[:, 2]
#
# MV_Y_day_path = os.path.join(config.factor_path, 'MV_Y_day.csv')
# MV_Y.to_csv(MV_Y_day_path, header=True)
#
# MV_M_day_path = os.path.join(config.factor_path, 'MV_M_day.csv')
# MV_M.to_csv(MV_M_day_path, header=True)
#
# print(1)
