import os
import config
import pandas as pd
import config
import time


def txt_to_csv(txt_input_path, csv_output_path, column, index_col, converters=None, decoding='gbk', encoding='utf8'):
    """
    Split txt files downloaded from CSMAR into csv files according to tickers, this fun can be applied to return files,
    price files
    :param index_col:
    :param converters:
    :param txt_input_path: file path of a txt file
    :param csv_output_path: directory path of output files
    :param column: split according to which key
    :param decoding: input file encoding type
    :param encoding: output file encoding type
    :return: None
    """
    if not os.path.exists(csv_output_path):
        os.makedirs(csv_output_path)
    data = pd.read_csv(txt_input_path, sep='\t', encoding=decoding, low_memory=False, converters=converters).set_index(
        index_col)
    index = data[column].unique().tolist()
    counter = 0
    print('Reading data from {0} to {1}'.format(txt_input_path, csv_output_path))
    for idx in index:
        counter = counter + 1
        if idx == column:
            continue
        data_ticker = data[data[column] == idx]
        file_out_path = os.path.join(csv_output_path, idx + '.csv')
        data_ticker.to_csv(file_out_path, encoding=encoding, mode='w', index=True)
        # print('Reading data of {0} from {1}. Saving to {2}'.format(idx, txt_input_path, file_out_path))
        l1 = counter * 50 // len(index)
        print('Reading {0}, Progress Bar: {1:><{len1}}{2:=<{len2}}. {3} of {4}'.format(idx, '>', '=', counter, len(index),
                                                                                     len1=l1, len2=50 - l1, ))
    return


def extract_feature(csv_dir, output_dir, date_col, column, output_file_name, converters=None):
    print('Extracting {0} from CSVs located at {1}'.format(column, csv_dir))
    files = os.listdir(csv_dir)
    df = pd.DataFrame(index=config.all_trade_dates)
    for file in files:
        file_name = os.path.splitext(file)[0]
        if file_name not in config.A_lists:
            continue
        cur_path = os.path.join(csv_dir, file)
        cur_df = pd.read_csv(cur_path, converters=converters)
        cur_df = cur_df.set_index(cur_df[date_col])
        cur_series = cur_df[column]
        print('Inserting {0} to DataFrame'.format(file_name))
        df[file_name] = cur_series
    output_path = os.path.join(output_dir, output_file_name + '.csv')
    df.to_csv(output_path)
    print('File exported to {0}'.format(output_dir))
    return


def extract_feature2(csv_dir, output_dir, date_col, column, output_file_name, converters=None):
    print('Extracting {0} from CSVs located at {1}'.format(column, csv_dir))
    files = os.listdir(csv_dir)
    df = {}
    for file in files:
        file_name = os.path.splitext(file)[0]
        if file_name not in config.A_lists:
            continue
        cur_path = os.path.join(csv_dir, file)
        cur_df = pd.read_csv(cur_path, converters=converters)
        cur_df = cur_df.set_index(cur_df[date_col])
        cur_series = cur_df[column]
        print('Inserting {0} to DataFrame'.format(file_name))
        df[file_name] = cur_series
    output_path = os.path.join(output_dir, output_file_name + '.csv')
    df = pd.DataFrame(df)
    df.to_csv(output_path)
    print('File exported to {0}'.format(output_dir))
    return


def append_csv(csv_dir, append_path, column, date_column, new_file_dir=None, append_encoding='utf-16', converters=None):
    append_file = pd.read_csv(append_path, sep='\t', encoding=append_encoding, converters=converters)
    if new_file_dir is None:
        new_file_dir = csv_dir
    else:
        if not os.path.exists(new_file_dir):
            os.makedirs(new_file_dir)
    index = append_file[column].unique().tolist()
    counter = 0
    for idx in index:
        if idx == column:
            continue
        cur_file_path = os.path.join(csv_dir, idx + '.csv')
        new_file_path = os.path.join(new_file_dir, idx + '.csv')
        if os.path.exists(cur_file_path):
            cur_file = pd.read_csv(cur_file_path, converters=converters, index_col=0)
            cur_dates = cur_file.index.tolist()
            append_data = append_file[append_file[column] == idx]
            append_dates = append_data[date_column].to_list()
            union = [date for date in cur_dates if date in append_dates]
            new_date = [date for date in append_dates if date not in cur_dates]
            append = append_data[append_data[date_column].isin(new_date)]
            append.set_index(date_column, inplace=True)
            cur_file_new = cur_file.append(append)
            try:
                assert union == []
            except AssertionError as e:
                print('Current data and new data should have no intersection')
                cur_file_new.drop_duplicates(date_column, 'first', inplace=True)
            cur_file_new.to_csv(new_file_path, mode='w')
            print('Append data from of {0} to {1}'.format(idx, new_file_path))
        else:
            data_ticker = append_file[append_file[column] == idx]
            data_ticker.to_csv(new_file_path, mode='w')
            print('Reading data of new listed stock {0}. Saving to {1}'.format(idx, new_file_path))

        counter = counter + 1
        l1 = counter * 50 // len(index)
        print(
            'Reading {0}, Progress Bar: {1:><{len1}}{2:=<{len2}}. {3} of {4}'.format(idx, '>', '=', counter, len(index),
                                                                                     len1=l1, len2=50 - l1, ))

    return
