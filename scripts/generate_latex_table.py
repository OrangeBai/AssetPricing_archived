import os
from core.adv_utlis import *
from core.portfolio import *
from scipy.stats import ttest_1samp

file_name = 'MV_Sigma_Cur_55.p'


def gen_latex(file_name, breakpoints=[5, 5]):
    panel_path = os.path.join(config.panel_data_directory, file_name)
    cur_panel = PanelData.load_pickle(panel_path)
    a = []
    index = ['Small', '2', '3', '4', 'Big']
    columns = ['Low', '2', '3', '4', 'High', '1-5', '(t)']
    out_panel = pd.DataFrame(index=index, columns=columns)
    cur_list = []
    ret = period_ret_all(cur_panel.ret, config.month_split)

    for idx in range(len(cur_panel.group)):
        cur_ret = ret.iloc[:, idx]
        i = idx // 5
        j = idx % 5
        if j == 0:
            cur_list = [cur_ret]
        elif j == 4:
            cur_list.append(cur_ret)
            cur_list.append(cur_list[0] - cur_ret)
            a.append(cur_list)
            out_panel.iloc[i, 5] = cur_list[-1].mean()
            out_panel.iloc[i, 6], _ = ttest_1samp(cur_list[-1], popmean=0)
        else:
            cur_list.append(cur_ret)
        out_panel.iloc[i, j] = cur_ret.mean()


print(1)
