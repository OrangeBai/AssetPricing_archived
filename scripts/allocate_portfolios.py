import argparse
from core.allocate import *
from core.portfolio import *
from core.adv_utlis import *
import config
import os

parser = argparse.ArgumentParser(description='Allocate some stocks')
parser.add_argument('-f', '--features', nargs='+')
parser.add_argument('-b', '--breakpoint')
parser.add_argument('-fp', '--feature-file-name', nargs='+')
parser.add_argument('-o', '--out-put-name')
parser.add_argument('-ol', '--output_latex_file')
args = parser.parse_args()


features_path = [os.path.join(config.feature_directory, name) for name in args.feature_file_name]
features = args.features
breakpoints = args.breakpoint
output_file = os.path.join(config.temp_data_path, args.out_put_name+'.p')

if breakpoints == '5*5':
    split = [(0, 0.2, 0.4, 0.6, 0.8, 1.0), (0, 0.2, 0.4, 0.6, 0.8, 1.0)]
elif breakpoints == '2*3':
    split = [(0, 0.5, 1), (0, 0.3, 0.7, 1)]
elif breakpoints == '5':
    split = [(0, 0.2, 0.4, 0.6, 0.8, 1.0)]
else:
    raise ValueError('Invalid input')

try:
    assert len(features) == len(split)
    assert len(features) == len(features_path)
except AssertionError as e:
    raise AssertionError('Length of features, features path and split should be equal')

print("feature: {0}\nbreakpoint:{1}\nfile_path:{2}".format(features, split, features_path))


# Load daily return and market value of all stocks
all_stocks_data_path = os.path.join(config.temp_data_path, 'AllStocksPortfolio.p')
all_stocks_data = Portfolio.load_pickle(all_stocks_data_path)

# Load features of all stocks
all_stocks_feature_path = os.path.join(config.temp_data_path, 'Allocator_M.p')
all_stocks_feature = Allocate.load_pickle(all_stocks_feature_path)

feature_path_zip = zip(features, features_path)
for i in feature_path_zip:
    all_stocks_feature.add_factor(i[0], i[1])

print('Allocation start')
# allocate all A stocks into 2 * 3 groups to calculate turnover factor
groups = all_stocks_feature.allocate_stocks_according_to_factors(features, split)
panel = generate_panel(all_stocks_data, config.period, groups)
panel.to_pickle(output_file)

rets = panel.ret
rets.to_latex()