from core.rolling_windows import *
from core.portfolio import *
from core.allocate import *
from core.adv_utlis import *
#
# # Load the panel data of dependent portfolios
# ret_path = os.path.join(config.extracted_directory, 'DailyRet.csv')
# rets = pd.read_csv(ret_path, index_col=0)
#
# # Load trade dates
# trade_dates = rets.index.to_list()
#
# # Load factor file of market, SMB, HML
# factor_path = os.path.join(config.raw_directory, 'STK_MKT_FivefacDay.txt')
# factors_day = get_factors(factor_path, config.all_period)
# factors = factors_day.iloc[:, [0, 2, 4]]
#
# # Load rf data
# rf_file_path = os.path.join(config.raw_directory, 'TRD_Nrrate.txt')
# rf = get_rf_rate(rf_file_path, config.all_period)
#
#
# month_split = config.month_split
# month_tag = config.month_tag
#
# # Period dictionary: {Month_T: (Month_T-3, Month_T-1)
# period_dict = {}
# for period in month_split:
#     start_id = month_tag.index(period[0])
#     reg_start_id = month_tag[start_id - 3]
#     reg_end_id = month_tag[start_id]
#     period_dict[period[0]] = (reg_start_id, reg_end_id)
#
# # Fama-French regression is performed for each stock for 120 days
# rw = RollingWindow(rets, factors, group_by=period_dict)
# result = rw.regress('group')
#
#
# # Load ssr for each regression
# def get_ssr(reg_res):
#     return reg_res.ssr
#
#
# # read result and save
# res = rw.read_result(get_ssr).T
Sigma_M_path = os.path.join(config.feature_directory, 'M_Sigma.csv')
# res.to_csv(Sigma_M_path)

# Load daily return and market value of all stocks
all_stocks_data_path = os.path.join(config.temp_data_path, 'AllStocksPortfolio.p')
all_stocks_data = Portfolio.load_pickle(all_stocks_data_path)

# Create Allocator Object for monthly adjusted groups
allocator_M_path = os.path.join(config.temp_data_path, 'Allocator_M.p')
allocator_M = update_allocator(allocator_M_path, ('Sigma', Sigma_M_path))

MV_Sigma_23_groups = allocator_M.allocate_stocks_according_to_factors(['MV', 'Sigma'], [(0, 0.5, 1), (0, 0.3, 0.7, 1)])
MV_Sigma_23_panel = generate_panel(all_stocks_data, config.period, MV_Sigma_23_groups)
MV_Sigma_23_panel_path = os.path.join(config.temp_data_path, 'MV_Sigma_23.p')
MV_Sigma_23_panel.to_pickle(MV_Sigma_23_panel_path)
MV_Sigma_23_panel_ret = MV_Sigma_23_panel.ret

Sigma_Factor = (MV_Sigma_23_panel_ret.iloc[:, 0] - MV_Sigma_23_panel_ret.iloc[:, 2] +
                MV_Sigma_23_panel_ret.iloc[:, 3] - MV_Sigma_23_panel_ret.iloc[:, 5]) / 2

Sigma_Factor_path = os.path.join(config.factor_path, 'Sigma.csv')
Sigma_Factor.to_csv(Sigma_Factor_path, header=True)
