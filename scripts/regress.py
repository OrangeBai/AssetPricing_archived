from core.regression import *
from core.adv_utlis import *
from core.gen_latex_table import *

res_1 = regress(('1997-01', '2010-04'), 'MV_AdjTover_Cur_55.p', factor_panels=['MV_AdjTover_Cur_23.p'])
res_2 = regress(('1997-01', '2010-04'), 'AdjTover_Cur_5.p', factor_panels=['MV_AdjTover_Cur_23.p'])
df1 = gen_regress_table([res_1, res_2], (0, 4))

res_1 = regress(('2010-04', '2019-07'), 'Saleable_MV_AdjTover_Cur_55.p', factor_panels=['MV_AdjTover_Cur_23.p'])
res_2 = regress(('2010-04', '2019-07'), 'Saleable_AdjTover_Cur_5.p', factor_panels=['MV_AdjTover_Cur_23.p'])
df2 = gen_regress_table([res_1, res_2], (0, 4))

res_1 = regress(('2010-04', '2019-07'), 'Non_Saleable_MV_AdjTover_Cur_55.p', factor_panels=['MV_AdjTover_Cur_23.p'])
res_2 = regress(('2010-04', '2019-07'), 'Non_Saleable_AdjTover_Cur_5.p', factor_panels=['MV_AdjTover_Cur_23.p'])
df3 = gen_regress_table([res_1, res_2], (0, 4))

df_out = df.concat([df1, df2, df3], axis=0)


res_1 = regress(('1997-01', '2010-04'), 'MV_AdjTover_Pre_55.p', factor_panels=['MV_AdjTover_Pre_23.p'])
res_2 = regress(('1997-01', '2010-04'), 'AdjTover_Pre_5.p', factor_panels=['MV_AdjTover_Pre_23.p'])
df1 = gen_regress_table([res_1, res_2], (0, 4))

res_1 = regress(('2010-04', '2019-07'), 'Saleable_MV_AdjTover_Pre_55.p', factor_panels=['MV_AdjTover_Pre_23.p'])
res_2 = regress(('2010-04', '2019-07'), 'Saleable_AdjTover_Pre_5.p', factor_panels=['MV_AdjTover_Pre_23.p'])
df2 = gen_regress_table([res_1, res_2], (0, 4))

res_1 = regress(('2010-04', '2019-07'), 'Non_Saleable_MV_AdjTover_Pre_55.p', factor_panels=['MV_AdjTover_Pre_23.p'])
res_2 = regress(('2010-04', '2019-07'), 'Non_Saleable_AdjTover_Pre_5.p', factor_panels=['MV_AdjTover_Pre_23.p'])
df3 = gen_regress_table([res_1, res_2], (0, 4))

res_1 = regress(('1997-01', '2010-04'), 'MV_Sigma_Pre_55.p', factor_panels=['MV_Sigma_Pre_23.p'])
res_2 = regress(('1997-01', '2010-04'), 'Sigma_Pre_5.p', factor_panels=['MV_Sigma_Pre_23.p'])
gen_regress_table([res_1, res_2], (0, 4))

res_1 = regress(('2010-04', '2019-07'), 'Saleable_MV_Sigma_Pre_55.p', factor_panels=['MV_Sigma_Pre_23.p'])
res_2 = regress(('2010-04', '2019-07'), 'Saleable_Sigma_Pre_5.p', factor_panels=['MV_Sigma_Pre_23.p'])
gen_regress_table([res_1, res_2], (0, 4))

res_1 = regress(('2010-04', '2019-07'), 'Non_Saleable_MV_Sigma_Pre_55.p', factor_panels=['MV_Sigma_Pre_23.p'])
res_2 = regress(('2010-04', '2019-07'), 'Non_Saleable_Sigma_Pre_5.p', factor_panels=['MV_Sigma_Pre_23.p'])
gen_regress_table([res_1, res_2], (0, 4))



res_1 = regress(('1997-01', '2010-04'), 'MV_Sigma_Cur_55.p', factor_panels=['MV_Sigma_Cur_23.p'])
res_2 = regress(('1997-01', '2010-04'), 'Sigma_Cur_5.p', factor_panels=['MV_Sigma_Cur_23.p'])
gen_regress_table([res_1, res_2], (0, 4))

res_1 = regress(('2010-04', '2019-07'), 'Saleable_MV_Sigma_Cur_55.p', factor_panels=['MV_Sigma_Cur_23.p'])
res_2 = regress(('2010-04', '2019-07'), 'Saleable_Sigma_Cur_5.p', factor_panels=['MV_Sigma_Cur_23.p'])
gen_regress_table([res_1, res_2], (0, 4))

res_1 = regress(('2010-04', '2019-07'), 'Non_Saleable_MV_Sigma_Cur_55.p', factor_panels=['MV_Sigma_Cur_23.p'])
res_2 = regress(('2010-04', '2019-07'), 'Non_Saleable_Sigma_Cur_5.p', factor_panels=['MV_Sigma_Cur_23.p'])
gen_regress_table([res_1, res_2], (0, 4))

res_1 = regress(('1997-01', '2010-04'), 'MV_AdjTover_Pre_55.p')
res_2 = regress(('1997-01', '2010-04'), 'AdjTover_Pre_5.p')
gen_regress_table([res_1, res_2], (0,))

res_1 = regress(('2010-04', '2019-07'), 'Saleable_MV_AdjTover_Pre_55.p')
res_2 = regress(('2010-04', '2019-07'), 'Saleable_AdjTover_Pre_5.p')
gen_regress_table([res_1, res_2], (0,))

res_1 = regress(('2010-04', '2019-07'), 'Non_Saleable_MV_AdjTover_Pre_55.p')
res_2 = regress(('2010-04', '2019-07'), 'Non_Saleable_AdjTover_Pre_5.p')
gen_regress_table([res_1, res_2], (0,))


res_1 = regress(('1997-01', '2010-04'), 'MV_Sigma_Pre_55.p')
res_2 = regress(('1997-01', '2010-04'), 'Sigma_Pre_5.p')
gen_regress_table([res_1, res_2], (0,))

res_1 = regress(('2010-04', '2019-07'), 'Saleable_MV_Sigma_Pre_55.p')
res_2 = regress(('2010-04', '2019-07'), 'Saleable_Sigma_Pre_5.p')
gen_regress_table([res_1, res_2], (0,))

res_1 = regress(('2010-04', '2019-07'), 'Non_Saleable_MV_Sigma_Pre_55.p')
res_2 = regress(('2010-04', '2019-07'), 'Non_Saleable_Sigma_Pre_5.p')
gen_regress_table([res_1, res_2], (0,))


res_1 = regress(('1997-01', '2010-04'), 'MV_AdjTover_Cur_55.p')
res_2 = regress(('1997-01', '2010-04'), 'AdjTover_Cur_5.p')
gen_regress_table([res_1, res_2], (0,))

res_1 = regress(('2010-04', '2019-07'), 'Saleable_MV_AdjTover_Cur_55.p')
res_2 = regress(('2010-04', '2019-07'), 'Saleable_AdjTover_Cur_5.p')
gen_regress_table([res_1, res_2], (0,))

res_1 = regress(('2010-04', '2019-07'), 'Non_Saleable_MV_AdjTover_Cur_55.p')
res_2 = regress(('2010-04', '2019-07'), 'Non_Saleable_AdjTover_Cur_5.p')
gen_regress_table([res_1, res_2], (0,))


res_1 = regress(('1997-01', '2010-04'), 'MV_Sigma_Cur_55.p')
res_2 = regress(('1997-01', '2010-04'), 'Sigma_Cur_5.p')
gen_regress_table([res_1, res_2], (0,))

res_1 = regress(('2010-04', '2019-07'), 'Saleable_MV_Sigma_Cur_55.p')
res_2 = regress(('2010-04', '2019-07'), 'Saleable_Sigma_Cur_5.p')
gen_regress_table([res_1, res_2], (0,))

res_1 = regress(('2010-04', '2019-07'), 'Non_Saleable_MV_Sigma_Cur_55.p')
res_2 = regress(('2010-04', '2019-07'), 'Non_Saleable_Sigma_Cur_5.p')
gen_regress_table([res_1, res_2], (0,))

print(1)
