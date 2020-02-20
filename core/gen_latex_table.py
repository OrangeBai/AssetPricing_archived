import config
import os
import pandas as pd
import numpy as np
from core.portfolio import *
from scipy.stats import ttest_1samp
from core.adv_utlis import *

def gen_latex_table_result(ress, data_list, out_dir_name, out_file):
    """
    @param res: regression results. [beta, t-test, p-value, R]
    @param data_list: which data are required
    @param out_dir_name: output_directory name
    @param out_file: out put file name
    @return: None
    """
    res1 = ress[0]
    res2 = ress[1]
    out_dir = config.table_directory + str(out_dir_name)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    group_num_1 = 25
    group_num_2 = 5
    assert group_num_1 == len(res1[3])
    assert group_num_2 == len(res2[3])
    idx = ['Small', '2', '3', '4', 'Big', 'All']
    idx = idx * len(data_list)

    df = pd.DataFrame(index=idx, data=np.zeros((6 * (len(data_list)), 11)))
    df.iloc[:, 5] = np.NaN
    for idx in data_list:
        idx_loc = data_list.index(idx)
        for num in range(group_num_1):
            i = num // 5
            j = num % 5
            if idx == 0:
                df.iloc[i, j] = res1[0].iloc[num, idx] * 100
            else:
                df.iloc[6 * idx_loc + i, j] = res1[0].iloc[num, idx]

            if res1[2].iloc[num, idx] < 0.01:
                df.iloc[6 * idx_loc + i, 6 + j] = '{0:.2f}'.format(res1[1].iloc[num, idx]) + '\si{^{***}}'
            elif 0.05 > res1[2].iloc[num, idx] >= 0.01:
                df.iloc[6 * idx_loc + i, 6 + j] = '{0:.2f}'.format(res1[1].iloc[num, idx]) + '\si{^{**}}'
            elif 0.1 > res1[2].iloc[num, idx] >= 0.05:
                df.iloc[6 * idx_loc + i, 6 + j] = '{0:.2f}'.format(res1[1].iloc[num, idx]) + '\si{^{*}}'
            else:
                df.iloc[6 * idx_loc + i, 6 + j] = res1[1].iloc[num, idx]
            # df.iloc[2 * i, 5 + 5 * idx_loc + j] = res[3].iloc[num]

        for num in range(group_num_2):
            j = num % 5
            if idx == 0:
                df.iloc[5, j] = res2[0].iloc[num, idx] * 100
            else:
                df.iloc[6 * idx_loc + 5, j] = res2[0].iloc[num, idx]

            if res2[2].iloc[num, idx] < 0.01:
                df.iloc[6 * idx_loc + 5, 6 + j] = '{0:.2f}'.format(res2[1].iloc[num, idx]) + '\si{^{***}}'
            elif 0.05 > res2[2].iloc[num, idx] >= 0.01:
                df.iloc[6 * idx_loc + 5, 6 + j] = '{0:.2f}'.format(res2[1].iloc[num, idx]) + '\si{^{**}}'
            elif 0.1 > res2[2].iloc[num, idx] >= 0.05:
                df.iloc[6 * idx_loc + 5, 6 + j] = '{0:.2f}'.format(res2[1].iloc[num, idx]) + '\si{^{*}}'
            else:
                df.iloc[6 * idx_loc + 5, 6 + j] = res2[1].iloc[num, idx]

    out_path = os.path.join(out_dir, out_file)

    latex_str = df.to_latex(None, float_format="{:0.2f}".format, na_rep='')

    latex_str = latex_str.replace(r'\$', '$')
    latex_str = latex_str.replace(r'\{', '{')
    latex_str = latex_str.replace(r'\}', '}')
    latex_str = latex_str.replace(r'\textasciicircum ', '^')
    latex_str = latex_str.replace(r'nan', '')
    latex_str = latex_str.replace(r'\textbackslash ', '\\')
    with open(out_path, 'w') as file:
        file.write(latex_str)
    return


def gen_table_portfolio(file_name_1, file_name_2, weight='ew'):
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

    return out_panel


def gen_latex_portfolios(table, table_path):
    for i in range(len(table.index)):
        if table.iloc[i, 7] < 0.01:
            table.iloc[i, 6] = '{0:.2f}'.format(table.iloc[i, 6]) + '\si{^{***}}'
        elif 0.05 > table.iloc[i, 7] >= 0.01:
            table.iloc[i, 6] = '{0:.2f}'.format(table.iloc[i, 6]) + '\si{^{**}}'
        elif 0.1 > table.iloc[i, 7]:
            table.iloc[i, 6] = '{0:.2f}'.format(table.iloc[i, 6]) + '\si{^{*}}'
        else:
            table.iloc[i, 6] = '{0:.2f}'.format(table.iloc[i, 6])
    latex_str = table.iloc[:, :7].to_latex(None, float_format="{:0.2f}".format, na_rep='')
    latex_str = latex_str.replace(r'\$', '$')
    latex_str = latex_str.replace(r'\{', '{')
    latex_str = latex_str.replace(r'\}', '}')
    latex_str = latex_str.replace(r'\textasciicircum ', '^')
    latex_str = latex_str.replace(r'nan', '')
    latex_str = latex_str.replace(r'\textbackslash ', '\\')

    with open(table_path, 'w') as f:
        f.write(latex_str)
    return latex_str