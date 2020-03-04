from core.portfolio import *
from core.rolling_windows import *
from core.utils import *


def allocate(features_file, features, breakpoints, output_file, allocator_file, data_file, period):
    """
    allocate stocks.
    :param features_file: file name of features.
    :param features: name of the features.
    :param breakpoints: breakpoints, {'5*5', '2*3', '5'}.
    :param output_file: file name of output files.
    :param allocator_file: File name of allocator.
    :param data_file: File name of stock Data.
    :param period: period of panel data.
    :return:
    """
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
        assert len(features) == len(features_file)
    except AssertionError as e:
        raise AssertionError('Length of features, features path and split should be equal')

    print("feature: {0}\nbreakpoint:{1}\nfile_path:{2}\n".format(features, split, features_file))

    # Load daily return and market value of all stocks
    all_stocks_data_path = os.path.join(config.temp_data_path, data_file)
    all_stocks_data = Portfolio.load_pickle(all_stocks_data_path)

    # Load features of all stocks
    all_stocks_feature_path = os.path.join(config.temp_data_path, allocator_file)
    all_stocks_feature = Allocate.load_pickle(all_stocks_feature_path)

    feature_path_zip = zip(features, features_file)
    for i in feature_path_zip:
        feature_path = os.path.join(config.feature_directory, i[1])
        all_stocks_feature.add_factor(i[0], feature_path)

    print('Allocation start')
    # allocate all A stocks into 2 * 3 groups to calculate turnover factor
    groups = all_stocks_feature.allocate_stocks_according_to_factors(features, split, sequentially=True)
    panel = PanelData(period, all_stocks_data, groups)
    output_file_path = os.path.join(config.panel_data_directory, output_file)
    panel.to_pickle(output_file_path)

    return panel


def get_rf_rate(period, sep='\t', encoding='gbk', mode='d', path=None):
    # Load risk free file
    if path is None:
        path = os.path.join(config.raw_directory, 'TRD_Nrrate.txt')
    rf_file = pd.read_csv(path, sep='\t', encoding='gbk')
    rf = rf_file[rf_file['Nrr1'] == 'NRI01'].drop_duplicates('Clsdt', keep='first')
    rf.set_index('Clsdt', inplace=True)
    if mode == 'd':
        mask = (rf.index > period[0]) & (rf.index < period[1])
        rf_day = rf.loc[mask, 'Nrrdaydt'].astype('float') / 100
        return rf_day
    else:
        month_split = config.month_split
        rf_month_dict = {}
        for month_period in month_split:
            if month_period[0] >= period[0] and month_period[1] <= period[1]:
                mask = (rf.index > month_period[0]) & (rf.index < month_period[1])
                rf_month_dict[month_period[0]] = rf.loc[mask, 'Nrrmtdt'].astype('float')[0] / 100
        rf_month = pd.Series(rf_month_dict)
        return rf_month


def get_factors(period, market_type='P9709', portfolio='1', factor_path=None):
    if factor_path is None:
        factor_path = os.path.join(config.raw_directory, 'STK_MKT_FivefacDay.txt')
    raw_factors = pd.read_csv(factor_path, sep='\t', encoding='gbk')
    mask = (raw_factors['MarkettypeID'] == market_type) & (raw_factors['Portfolios'] == portfolio)
    A_factor = raw_factors.loc[mask]
    A_factor = A_factor.drop_duplicates(subset='TradingDate', keep='first')
    A_factor.set_index(A_factor['TradingDate'], inplace=True)
    month_split = config.month_split
    mask = (A_factor.index > period[0]) & (A_factor.index < period[1])
    factors = A_factor.loc[mask, ['RiskPremium1', 'RiskPremium2', 'SMB1', 'SMB2', 'HML1', 'HML2', 'RMW1', 'RMW2',
                                  'CMA1', 'CMA2']].astype('float')
    return factors.sort_index()


def period_ret_all(input_df, month_split, period=None):
    ret_all = {}
    start_month = get_month(input_df.index[0])
    end_month = get_month(input_df.index[-1])
    for month_period in [month for month in month_split if start_month <= month[0] <= end_month]:
        # mask = (input_df.index > month_period[0]) & (input_df.index < month_period[1])
        if month_period[0] < period[1]:
            cur_ret = input_df.loc[month_period[0]: month_period[1], :]
            ret_all[month_period[0]] = period_ret(cur_ret)
    return pd.DataFrame(ret_all).T.sort_index()


def period_ret(input_df, max_na=5):
    ret = input_df.sort_index()
    log_ret = (1 + ret).apply(np.log)
    overall_ret = log_ret.sum()
    index = log_ret.isna().sum() > max_na
    overall_ret[index] = np.nan
    return overall_ret


