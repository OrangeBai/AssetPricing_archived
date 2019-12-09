
# Generate Panels of all stocks, from 1997-01 to 2010-03
allocator_file = 'Allocator_M.p'
data_file = 'AllStocksPortfolio.p'
period = ('1997-01', '2010-04')

allocate(['M_MktV.csv', 'M_AdjTover_Cur.csv'], ['MV', 'AdjTover'], '5*5',
         'MV_AdjTover_Cur_55.p', allocator_file, data_file, period)

allocate(['M_MktV.csv', 'M_AdjTover_Pre.csv'], ['MV', 'AdjTover'], '5*5',
         'MV_AdjTover_Pre_55.p', allocator_file, data_file, period)

allocate(['M_AdjTover_Cur.csv'], ['AdjTover'], '5',
         'AdjTover_Cur_5.p', allocator_file, data_file, period)

allocate(['M_AdjTover_Pre.csv'], ['AdjTover'], '5',
         'AdjTover_Pre_5.p', allocator_file, data_file, period)

# Generate Panels of non-saleable stocks, from 2010-04 to 2019-06
data_file = 'AllStocksPortfolio.p'
allocator_file = 'non_saleable_allocator.p'
period = ('2010-04', '2019-07')

allocate(['M_MktV.csv', 'M_AdjTover_Cur.csv'], ['MV', 'AdjTover'], '5*5',
         'Non_Saleable_MV_AdjTover_Cur_55.p', allocator_file, data_file, period)

allocate(['M_MktV.csv', 'M_AdjTover_Pre.csv'], ['MV', 'AdjTover'], '5*5',
         'Non_Saleable_MV_AdjTover_Pre_55.p', allocator_file, data_file, period)

allocate(['M_AdjTover_Cur.csv'], ['AdjTover'], '5',
         'Non_Saleable_AdjTover_Cur_5.p', allocator_file, data_file, period)

allocate(['M_AdjTover_Pre.csv'], ['MV', 'AdjTover'], '5',
         'Non_Saleable_AdjTover_Pre_5.p', allocator_file, data_file, period)

# Generate panels of saleable stocks, from 2010-04 to 2019-06
data_file = 'AllStocksPortfolio.p'
allocator_file = 'saleable_allocator.p'
period = ('2010-04', '2019-07')

# Market Value and Current AdjTover 5*5 groups

allocate(['M_MktV.csv', 'M_AdjTover_Cur.csv'], ['MV', 'AdjTover'], '5*5',
         'Saleable_MV_AdjTover_Cur_55.p', allocator_file, data_file, period)

allocate(['M_MktV.csv', 'M_AdjTover_Pre.csv'], ['MV', 'AdjTover'], '5*5',
         'Saleable_MV_AdjTover_Pre_55.p', allocator_file, data_file, period)

allocate(['M_AdjTover_Cur.csv'], ['AdjTover'], '5',
         'Saleable_AdjTover_Cur_5.p', allocator_file, data_file, period)

allocate(['M_AdjTover_Pre.csv'], ['AdjTover'], '5',
         'Saleable_AdjTover_Pre_5.p', allocator_file, data_file, period)

# Generate Panels of 2*3 groups, from 1997-01 to 2019-06
data_file = 'AllStocksPortfolio.p'
allocator_file = 'Allocator_M.p'
period = config.period

allocate(['M_MktV.csv', 'M_AdjTover_Cur.csv'], ['MV', 'AdjTover'], '2*3',
         'MV_AdjTover_Cur_23.p', allocator_file, data_file, period)

allocate(['M_MktV.csv', 'M_AdjTover_Pre.csv'], ['MV', 'AdjTover'], '2*3',
         'MV_AdjTover_Pre_23.p', allocator_file, data_file, period)
