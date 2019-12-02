import argparse
from core.allocate import *
from core.portfolio import *
from core.adv_utlis import *
import config
import os

# parser = argparse.ArgumentParser(description='Allocate some stocks')
# parser.add_argument('-f', '--features', nargs='+')
# parser.add_argument('-fp', '--feature-files', nargs='+')
# parser.add_argument('-b', '--breakpoint')
# parser.add_argument('-o', '--output-name')
# parser.add_argument('-a', '--allocator_file', default='Allocator_M.p')
# parser.add_argument('-d', '--data_file', default='AllStocksPortfolio.p')
# parser.add_argument('-p', '--period', default=config.period)
# args = parser.parse_args()
#
# features = args.features
# feature_files = args.feature_files
# breakpoints = args.breakpoint
# output_file = args.output_name
# allocator_file = args.allocator_file
# data_file = args.data_file
# period = args.period

allocator_file = 'Allocator_M.p'
data_file = 'AllStocksPortfolio.p'
period = config.period

feature_files = ['M_MktV.csv', 'M_Sigma_Cur.csv']
features = ['MV', 'Sigma']
breakpoints = '5*5'
output_file = 'MV_Sigma_Cur_55.p'

allocate(feature_files, features, breakpoints, output_file, allocator_file, data_file, period)

feature_files = ['M_MktV.csv', 'M_Sigma_Pre.csv']
features = ['MV', 'Sigma']
breakpoints = '5*5'
output_file = 'MV_Sigma_Pre_55.p'

allocate(feature_files, features, breakpoints, output_file, allocator_file, data_file, period)
