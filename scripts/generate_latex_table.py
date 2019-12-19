import os
from core.adv_utlis import *
from core.portfolio import *
from scipy.stats import ttest_1samp, jarque_bera

# file_name = 'MV_Sigma_Cur_55.p'
data = PanelData.load_pickle(os.path.join(config.temp_data_path, 'AllStocksPortfolio.p'))
#
#
def gen_latex(file_name_1, file_name_2, out_path=None, weight='ew'):
    panel_path_1 = os.path.join(config.panel_data_directory, file_name_1)
    panel_path_2 = os.path.join(config.panel_data_directory, file_name_2)
    cur_panel_1 = PanelData.load_pickle(panel_path_1)
    cur_panel_2 = PanelData.load_pickle(panel_path_2)
    index = ['Small', '2', '3', '4', 'Big', 'All']
    columns = ['Low', '2', '3', '4', 'High', '1-5', '(t)', '(p)']
    out_panel = pd.DataFrame(index=index, columns=columns)
    cur_list = []
    if weight == 'vw':
        ret_1 = period_ret_all(cur_panel_1.ret_vw, config.month_split)
        ret_2 = period_ret_all(cur_panel_2.ret_vw, config.month_split)
    else:
        ret_1 = period_ret_all(cur_panel_1.ret_ew, config.month_split)
        ret_2 = period_ret_all(cur_panel_2.ret_ew, config.month_split)

    for idx in range(len(cur_panel_1.group) + len(cur_panel_2.group)):
        if idx < len(cur_panel_1.group):
            ret = ret_1
            ret_idx = idx
        else:
            ret = ret_2
            ret_idx = idx - len(cur_panel_1.group)
        cur_ret = ret.iloc[:, ret_idx]
        i = idx // 5
        j = idx % 5
        if j == 0:
            cur_list = [cur_ret]
        elif j == 4:
            cur_list.append(cur_ret)
            cur_list.append(cur_list[0] - cur_ret)
            out_panel.iloc[i, 5] = cur_list[-1].mean() * 100
            out_panel.iloc[i, 6], out_panel.iloc[i, 7] = ttest_1samp(cur_list[-1], popmean=0)
        else:
            cur_list.append(cur_ret)
        out_panel.iloc[i, j] = cur_ret.mean() * 100
    if out_path is not None:
        out_panel.to_latex(out_path, float_format="{:0.2f}".format)
    print(out_path)
    print(out_panel)
    return out_panel


dir = '/Users/oranbebai/PHD/Finance/Papers/ShortSellContrain/Tables'
dir2 = "F:\PHD\Finance\Papers\ShortSellContrain\\table3"

gen_latex('MV_Sigma_Cur_55.p', 'Sigma_Cur_5.p', os.path.join(dir2, 'Sigma_Cur.tex'))
gen_latex('MV_Sigma_Pre_55.p', 'Sigma_Pre_5.p', os.path.join(dir2, 'Sigma_Pre.tex'))

gen_latex('Non_Saleable_MV_Sigma_Cur_55.p', 'Non_Saleable_Sigma_Cur_5.p', os.path.join(dir2, 'Non_Sigma_Cur.tex'))
gen_latex('Non_Saleable_MV_Sigma_Pre_55.p', 'Non_Saleable_Sigma_Pre_5.p', os.path.join(dir2, 'Non_Sigma_Pre.tex'))

gen_latex('Saleable_MV_Sigma_Cur_55.p', 'Saleable_Sigma_Cur_5.p', os.path.join(dir2, 'S_Sigma_Cur.tex'))
gen_latex('Saleable_MV_Sigma_Pre_55.p', 'Saleable_Sigma_Pre_5.p', os.path.join(dir2, 'S_Sigma_Pre.tex'))


gen_latex('MV_AdjTover_Cur_55.p', 'AdjTover_Cur_5.p', os.path.join(dir2, 'AdjTover_Cur.tex'))
gen_latex('MV_AdjTover_Pre_55.p', 'AdjTover_Pre_5.p', os.path.join(dir2, 'AdjTover_Pre.tex'))

gen_latex('Non_Saleable_MV_AdjTover_Cur_55.p', 'Non_Saleable_AdjTover_Cur_5.p', os.path.join(dir2, 'Non_AdjTover_Cur.tex'))
gen_latex('Non_Saleable_MV_AdjTover_Pre_55.p', 'Non_Saleable_AdjTover_Pre_5.p', os.path.join(dir2, 'Non_AdjTover_Pre.tex'))

gen_latex('Saleable_MV_AdjTover_Cur_55.p', 'Saleable_AdjTover_Cur_5.p', os.path.join(dir2, 'S_AdjTover_Cur.tex'))
gen_latex('Saleable_MV_AdjTover_Pre_55.p', 'Saleable_AdjTover_Pre_5.p', os.path.join(dir2, 'S_AdjTover_Pre.tex'))


# def gen_latex(panels, splits):
#     assert len(panels) == len(splits)
#     for panel in panels:


def gen_latex_table_result(res, data_list, dir, out_file):
    """
    @param res: regression results. [beta, t-test, p-value, R]
    @param data_list: which data are required
    @param dir: output_directory name
    @param out_file: out put file name
    @return: None
    """
    out_dir = config.table_directory + str(dir)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    group_num = 25
    assert group_num == len(res[3])
    df = pd.DataFrame()
    for idx in data_list:
        cur_df = pd.DataFrame(np.zeros((16, 6)))
        for num in range(group_num):
            i = num // 5
            j = num % 5
            cur_df.iloc[1 + 2 * i, 1 + j] = res[0].iloc[idx, data] * 100
            cur_df.iloc[2 + 2 * i, 1 + j] = res[1].iloc[idx, data]
            cur_df.iloc[11 + i, 1 + j] = res[2].iloc[idx, data]
            cur_df.iloc[16 + i, 1 + j] = res[3].iloc[idx, data]
        pd.concat([df, cur_df], axis=0)
    out_path = os.path.join(out_dir, out_file)
    pd.to_latex(out_path, float_format="{:0.2f}".format)
    return








print(1)
