import os
from core.adv_utlis import *
from core.portfolio import *
from scipy.stats import ttest_1samp, jarque_bera
from core.gen_latex_table import *
# file_name = 'MV_Sigma_Cur_55.p'
data = PanelData.load_pickle(os.path.join(config.temp_data_path, 'AllStocksPortfolio.p'))

dir = '/Users/oranbebai/PHD/Finance/Papers/ShortSellContrain/table'

table_1_path = os.path.join(dir, 'table_portfolios_S.tex')
table_2_path = os.path.join(dir, 'table_portfolios_T.tex')

table_1 = pd.DataFrame()
table_2 = pd.DataFrame()
table_1 = pd.concat([table_1, gen_table_portfolio('MV_Sigma_Cur_55.p', 'Sigma_Cur_5.p')])
table_1 = pd.concat([table_1, gen_table_portfolio('Non_Saleable_MV_Sigma_Cur_55.p', 'Non_Saleable_Sigma_Cur_5.p')])
table_1 = pd.concat([table_1, gen_table_portfolio('Saleable_MV_Sigma_Cur_55.p', 'Saleable_Sigma_Cur_5.p')])

table_1 = pd.concat([table_1, gen_table_portfolio('MV_Sigma_Pre_55.p', 'Sigma_Pre_5.p')])
table_1 = pd.concat([table_1, gen_table_portfolio('Non_Saleable_MV_Sigma_Pre_55.p', 'Non_Saleable_Sigma_Pre_5.p')])
table_1 = pd.concat([table_1, gen_table_portfolio('Saleable_MV_Sigma_Pre_55.p', 'Saleable_Sigma_Pre_5.p')])

gen_latex_portfolios(table_1, table_1_path)


table_2 = pd.concat([table_2, gen_table_portfolio('MV_AdjTover_Cur_55.p', 'AdjTover_Cur_5.p')])
table_2 = pd.concat([table_2, gen_table_portfolio('Non_Saleable_MV_AdjTover_Cur_55.p', 'Non_Saleable_AdjTover_Cur_5.p')])
table_2 = pd.concat([table_2, gen_table_portfolio('Saleable_MV_AdjTover_Cur_55.p', 'Saleable_AdjTover_Cur_5.p')])

table_2 = pd.concat([table_2, gen_table_portfolio('MV_AdjTover_Pre_55.p', 'AdjTover_Pre_5.p')])
table_2 = pd.concat([table_2, gen_table_portfolio('Non_Saleable_MV_AdjTover_Pre_55.p', 'Non_Saleable_AdjTover_Pre_5.p')])
table_2 = pd.concat([table_2, gen_table_portfolio('Saleable_MV_AdjTover_Pre_55.p', 'Saleable_AdjTover_Pre_5.p')])

gen_latex_portfolios(table_2, table_2_path)

print(1)
