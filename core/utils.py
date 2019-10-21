from pathlib import Path
from datetime import datetime
import pandas as pd


def get_project_root():
    """
    Get project root path
    :return: Project root path
    """
    return Path(__file__).parent.parent


def get_trade_dates(file_path, period, sep='\t', encoding='gbk'):
    dates = pd.read_csv(file_path, sep=sep, encoding=encoding)
    open_dates = dates[dates['State'] == 'O']
    open_dates = open_dates['Clddt'].unique().tolist()
    for date in open_dates:
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except Exception as e:
            print(e)
            open_dates.rempve(date)
    required_trade_dates = [date for date in open_dates if period[0] < date < period[1]]
    return required_trade_dates


def get_split(period):
    start_year = 1990
    end_year = 2022
    year_tag = [str(i) + '-01' for i in range(start_year, end_year + 1)]
    year_split = [(year_tag[i], year_tag[i+1]) for i in range(len(year_tag)-1) if period[0] <= year_tag[i] < period[1]]

    quarter_tag = [str(i) + '-' + str(j).zfill(2) for i in range(start_year, end_year) for j in range(1, 13, 3)]
    quarter_split = [month for month in quarter_tag if period[0] <= month <= period[1]]

    month_tag = [str(i) + '-' + str(j).zfill(2) for i in range(start_year, end_year) for j in range(1, 13, 1)]
    month_split = [(month_tag[i], month_tag[i + 1]) for i in range(len(month_tag) - 1) if
                   period[0] <= month_tag[i] < period[1]]

    return month_split, quarter_split, year_split, month_tag, quarter_tag, year_tag


