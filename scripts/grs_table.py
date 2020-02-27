from core.regression import *

grs_statistics = []


def append_list(l, t1, t2):
    l1 = list(t1)
    l2 = list(t2)
    l1.extend(l2)
    l.append(l1)
    return l


res_1 = cal_grs(('1997-01', '2010-04'), 'MV_AdjTover_Cur_55.p')
res_2 = cal_grs(('1997-01', '2010-04'), 'AdjTover_Cur_5.p')
append_list(grs_statistics, res_1, res_2)

res_1 = cal_grs(('2010-04', '2019-07'), 'Non_Saleable_MV_AdjTover_Cur_55.p')
res_2 = cal_grs(('2010-04', '2019-07'), 'Non_Saleable_AdjTover_Cur_5.p')
append_list(grs_statistics, res_1, res_2)

res_1 = cal_grs(('2010-04', '2019-07'), 'Saleable_MV_AdjTover_Cur_55.p')
res_2 = cal_grs(('2010-04', '2019-07'), 'Saleable_AdjTover_Cur_5.p')
append_list(grs_statistics, res_1, res_2)


res_1 = cal_grs(('1997-01', '2010-04'), 'MV_AdjTover_Cur_55.p', factor_panels=['MV_AdjTover_Cur_23.p'])
res_2 = cal_grs(('1997-01', '2010-04'), 'AdjTover_Cur_5.p', factor_panels=['MV_AdjTover_Cur_23.p'])
append_list(grs_statistics, res_1, res_2)

res_1 = cal_grs(('2010-04', '2019-07'), 'Non_Saleable_MV_AdjTover_Cur_55.p', factor_panels=['MV_AdjTover_Cur_23.p'])
res_2 = cal_grs(('2010-04', '2019-07'), 'Non_Saleable_AdjTover_Cur_5.p', factor_panels=['MV_AdjTover_Cur_23.p'])
append_list(grs_statistics, res_1, res_2)

res_1 = cal_grs(('2010-04', '2019-07'), 'Saleable_MV_AdjTover_Cur_55.p', factor_panels=['MV_AdjTover_Cur_23.p'])
res_2 = cal_grs(('2010-04', '2019-07'), 'Saleable_AdjTover_Cur_5.p', factor_panels=['MV_AdjTover_Cur_23.p'])
append_list(grs_statistics, res_1, res_2)

res_1 = cal_grs(('1997-01', '2010-04'), 'MV_AdjTover_Pre_55.p')
res_2 = cal_grs(('1997-01', '2010-04'), 'AdjTover_Pre_5.p')
append_list(grs_statistics, res_1, res_2)

res_1 = cal_grs(('2010-04', '2019-07'), 'Non_Saleable_MV_AdjTover_Pre_55.p')
res_2 = cal_grs(('2010-04', '2019-07'), 'Non_Saleable_AdjTover_Pre_5.p')
append_list(grs_statistics, res_1, res_2)

res_1 = cal_grs(('2010-04', '2019-07'), 'Saleable_MV_AdjTover_Pre_55.p')
res_2 = cal_grs(('2010-04', '2019-07'), 'Saleable_AdjTover_Pre_5.p')
append_list(grs_statistics, res_1, res_2)


res_1 = cal_grs(('1997-01', '2010-04'), 'MV_AdjTover_Pre_55.p', factor_panels=['MV_AdjTover_Pre_23.p'])
res_2 = cal_grs(('1997-01', '2010-04'), 'AdjTover_Pre_5.p', factor_panels=['MV_AdjTover_Pre_23.p'])
append_list(grs_statistics, res_1, res_2)

res_1 = cal_grs(('2010-04', '2019-07'), 'Non_Saleable_MV_AdjTover_Pre_55.p', factor_panels=['MV_AdjTover_Pre_23.p'])
res_2 = cal_grs(('2010-04', '2019-07'), 'Non_Saleable_AdjTover_Pre_5.p', factor_panels=['MV_AdjTover_Pre_23.p'])
append_list(grs_statistics, res_1, res_2)

res_1 = cal_grs(('2010-04', '2019-07'), 'Saleable_MV_AdjTover_Pre_55.p', factor_panels=['MV_AdjTover_Pre_23.p'])
res_2 = cal_grs(('2010-04', '2019-07'), 'Saleable_AdjTover_Pre_5.p', factor_panels=['MV_AdjTover_Pre_23.p'])
append_list(grs_statistics, res_1, res_2)


res_1 = cal_grs(('1997-01', '2010-04'), 'MV_Sigma_Cur_55.p')
res_2 = cal_grs(('1997-01', '2010-04'), 'Sigma_Cur_5.p')
append_list(grs_statistics, res_1, res_2)

res_1 = cal_grs(('2010-04', '2019-07'), 'Non_Saleable_MV_Sigma_Cur_55.p')
res_2 = cal_grs(('2010-04', '2019-07'), 'Non_Saleable_Sigma_Cur_5.p')
append_list(grs_statistics, res_1, res_2)

res_1 = cal_grs(('2010-04', '2019-07'), 'Saleable_MV_Sigma_Cur_55.p')
res_2 = cal_grs(('2010-04', '2019-07'), 'Saleable_Sigma_Cur_5.p')
append_list(grs_statistics, res_1, res_2)


res_1 = cal_grs(('1997-01', '2010-04'), 'MV_Sigma_Cur_55.p', factor_panels=['MV_Sigma_Cur_23.p'])
res_2 = cal_grs(('1997-01', '2010-04'), 'Sigma_Cur_5.p', factor_panels=['MV_Sigma_Cur_23.p'])
append_list(grs_statistics, res_1, res_2)

res_1 = cal_grs(('2010-04', '2019-07'), 'Non_Saleable_MV_Sigma_Cur_55.p', factor_panels=['MV_Sigma_Cur_23.p'])
res_2 = cal_grs(('2010-04', '2019-07'), 'Non_Saleable_Sigma_Cur_5.p', factor_panels=['MV_Sigma_Cur_23.p'])
append_list(grs_statistics, res_1, res_2)

res_1 = cal_grs(('2010-04', '2019-07'), 'Saleable_MV_Sigma_Cur_55.p', factor_panels=['MV_Sigma_Cur_23.p'])
res_2 = cal_grs(('2010-04', '2019-07'), 'Saleable_Sigma_Cur_5.p', factor_panels=['MV_Sigma_Cur_23.p'])
append_list(grs_statistics, res_1, res_2)


res_1 = cal_grs(('1997-01', '2010-04'), 'MV_Sigma_Pre_55.p')
res_2 = cal_grs(('1997-01', '2010-04'), 'Sigma_Pre_5.p')
append_list(grs_statistics, res_1, res_2)

res_1 = cal_grs(('2010-04', '2019-07'), 'Non_Saleable_MV_Sigma_Pre_55.p')
res_2 = cal_grs(('2010-04', '2019-07'), 'Non_Saleable_Sigma_Pre_5.p')
append_list(grs_statistics, res_1, res_2)

res_1 = cal_grs(('2010-04', '2019-07'), 'Saleable_MV_Sigma_Pre_55.p')
res_2 = cal_grs(('2010-04', '2019-07'), 'Saleable_Sigma_Pre_5.p')
append_list(grs_statistics, res_1, res_2)


res_1 = cal_grs(('1997-01', '2010-04'), 'MV_Sigma_Pre_55.p', factor_panels=['MV_Sigma_Pre_23.p'])
res_2 = cal_grs(('1997-01', '2010-04'), 'Sigma_Pre_5.p', factor_panels=['MV_Sigma_Pre_23.p'])
append_list(grs_statistics, res_1, res_2)

res_1 = cal_grs(('2010-04', '2019-07'), 'Non_Saleable_MV_Sigma_Pre_55.p', factor_panels=['MV_Sigma_Pre_23.p'])
res_2 = cal_grs(('2010-04', '2019-07'), 'Non_Saleable_Sigma_Pre_5.p', factor_panels=['MV_Sigma_Pre_23.p'])
append_list(grs_statistics, res_1, res_2)

res_1 = cal_grs(('2010-04', '2019-07'), 'Saleable_MV_Sigma_Pre_55.p', factor_panels=['MV_Sigma_Pre_23.p'])
res_2 = cal_grs(('2010-04', '2019-07'), 'Saleable_Sigma_Pre_5.p', factor_panels=['MV_Sigma_Pre_23.p'])
append_list(grs_statistics, res_1, res_2)

df = pd.DataFrame(grs_statistics)
df.iloc[:, 1] = df.iloc[:, 1] * 100
df.iloc[:, 5] = df.iloc[:, 5] * 100

df.index = 8 * ['\si{Short sale orbidden set}', '\si{Non-shortable set}', '\si{Shortable set}']
latex_str = df.to_latex(None, float_format="{:0.2f}".format)
latex_str = latex_str.replace(r'\$', '$')
latex_str = latex_str.replace(r'\{', '{')
latex_str = latex_str.replace(r'\}', '}')
latex_str = latex_str.replace(r'\textasciicircum ', '^')
latex_str = latex_str.replace(r'nan', '')
latex_str = latex_str.replace(r'\textbackslash ', '\\')
out_path = r'/Users/oranbebai/PHD/Finance/Papers/ShortSellContrain/table/grs.tex'
with open(out_path, 'w') as file:
    file.write(latex_str)

print(1)
