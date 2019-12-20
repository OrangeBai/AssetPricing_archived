from core.regression import *
from core.adv_utlis import *

result = regress(('1997-01', '2010-04'), 'MV_AdjTover_Pre_55.p', factor_panels=['MV_AdjTover_Pre_23.p'])
gen_latex_table_result(result, (0, 4), '3', 'MV_AdjTover_Pre_55.tex')
result = regress(('2010-04', '2019-07'), 'Saleable_MV_AdjTover_Pre_55.p',
                 factor_panels=['MV_AdjTover_Pre_23.p'])
gen_latex_table_result(result, (0, 4), '3', 'Saleable_MV_AdjTover_Pre_55.tex')
result = regress(('2010-04', '2019-07'), 'Non_Saleable_MV_AdjTover_Pre_55.p',
                 factor_panels=['MV_AdjTover_Pre_23.p'])
gen_latex_table_result(result, (0, 4), '3', 'Non_Saleable_MV_AdjTover_Pre_55.tex')

print(1)
