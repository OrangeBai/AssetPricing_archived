from core.portfolio import *
from core.rolling_windows import *


def generate_panel(all_stocks, period, groups):
    cur_panel = PanelData(period)
    for name, period_to_tickers in groups.items():
        current_portfolio_list = []
        for period, tickers in period_to_tickers.items():
            current_portfolio_list.append(all_stocks.retrieve(tickers, period))
        cur_panel.add_portfolio(name, current_portfolio_list)
    return cur_panel


def get_rf_rate(path, period, sep='\t', encoding='gbk', mode='d'):
    # Load risk free file
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
            if month_period[0] >= period[0] and month_period[1] < period[1]:
                mask = (rf.index > month_period[0]) & (rf.index < month_period[1])
                rf_month_dict[month_period[0]] = rf.loc[mask, 'Nrrmtdt'].astype('float')[0] / 100
        rf_month = pd.Series(rf_month_dict)
        return rf_month


def get_factors(factor_path, period, market_type='P9709', portfolio='1', mode='d'):
    raw_factors = pd.read_csv(factor_path, sep='\t', encoding='gbk')
    mask = (raw_factors['MarkettypeID'] == market_type) & (raw_factors['Portfolios'] == portfolio)
    A_factor = raw_factors.loc[mask]
    A_factor = A_factor.drop_duplicates(subset='TradingDate', keep='first')
    A_factor.set_index(A_factor['TradingDate'], inplace=True)
    month_split = config.month_split
    if mode == 'd':
        mask = (A_factor.index > period[0]) & (A_factor.index < period[1])
        return A_factor.loc[mask, ['RiskPremium1', 'RiskPremium2', 'SMB1', 'SMB2', 'HML1', 'HML2', 'RMW1', 'RMW2',
                                   'CMA1', 'CMA2']].astype('float')
    else:
        factor_month_dict = {}
        for month_period in month_split:
            if month_period[0] >= period[0] and month_period[1] <= period[1]:
                mask = (A_factor.index > month_period[0]) & (A_factor.index < month_period[1])
                factor_month_dict[month_period[0]] = A_factor.loc[
                    mask, ['RiskPremium1', 'RiskPremium2', 'SMB1', 'SMB2', 'HML1', 'HML2', 'RMW1', 'RMW2', 'CMA1',
                           'CMA2']].astype('float').sum()
        return pd.DataFrame(factor_month_dict).T


def update_allocator(pickle_path, *args):
    """
    Update factors in allocator file.
    :param pickle_path: Pickle path of the original allocator file
    :param args: tuple as (factor_name, factor_path)
    :return: None
    """
    allocator = Allocate.load_pickle(pickle_path)
    for arg in args:
        factor_name = arg[0]
        factor_path = arg[1]
        try:
            allocator.add_factor(factor_name, factor_path)
        except FileExistsError as e:
            print(e)
    allocator.to_pickle(pickle_path)
    return



