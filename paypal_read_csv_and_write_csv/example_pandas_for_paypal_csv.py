import pandas as pd
import copy
import argparse

columns_to_keep_for_processing = [
    'Date',
    'Name', 
    'Gross',
    'Note',
    'Town/City',
    'State/Province/Region/County/Territory/Prefecture/Republic',
    'Country',
    'Type']

transaction_types_to_keep = ['Mobile Payment',
                             'General Payment',
                             'Donation Payment',
                             'General Currency Conversion',
                             'Express Checkout Payment',
                             'Subscription Payment'
                             ]

def remove_columns_given_column_names_to_keep_for_processing(dataframe : pd.DataFrame) -> pd.DataFrame:
    return dataframe[columns_to_keep_for_processing]

def filter_rows_given_transaction_types_to_keep(dataframe : pd.DataFrame) -> pd.DataFrame:
    # https://pandas.pydata.org/docs/reference/api/pandas.Series.isin.html#pandas.Series.isin
    pandas_boolean_series_type_transaction_to_keep = dataframe['Type'].isin(transaction_types_to_keep)
    return dataframe[pandas_boolean_series_type_transaction_to_keep]
        
def filter_rows_due_to_negative_values(dataframe : pd.DataFrame) -> pd.DataFrame:
    pandas_boolean_series_gross_is_negative = (dataframe['Gross'] <= 0)
    pandas_boolean_series_gross_is_positive = (~ pandas_boolean_series_gross_is_negative)
    return dataframe[pandas_boolean_series_gross_is_positive]

def write_dataframe_to_output_file(dataframe : pd.DataFrame,
                                   filename : str) -> None:
    write_pandas_autoincrementing_int_index = False
    remove_type_column_when_write_new_csv = False
    if remove_type_column_when_write_new_csv:
        columns_to_keep_for_writing_out_csv = copy.copy(columns_to_keep_for_processing)
        columns_to_keep_for_writing_out_csv.remove('Type')
        dataframe_to_write_to_csv = dataframe[columns_to_keep_for_writing_out_csv]
        dataframe_to_write_to_csv.to_csv(filename, index=write_pandas_autoincrementing_int_index)
    else:
        dataframe.to_csv(filename, index=write_pandas_autoincrementing_int_index)

def parse_commandline_arguments():
    commandline_arguments_help_description='''
    This program:
      1. takes csv exported from paypal, and 
      2. writes new csv file containing only those rows and columns pastor uses'''
    parser = argparse.ArgumentParser(description=commandline_arguments_help_description,
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', '--input_paypal_csv', help='the filename for the csv file we exported from paypal', required=True)
    parser.add_argument('-o', '--output_csv', help='the filename for the csv file this program will write', required=True)
    args = parser.parse_args()
    return args.input_paypal_csv, args.output_csv
    

def main():
    #breakpoint()
    
    filename_to_read_from, filename_to_write_to = parse_commandline_arguments()

    dataframe_paypal_csv_initial = pd.read_csv(filename_to_read_from)
        
    dataframe_paypal_csv_after_filter_columns = remove_columns_given_column_names_to_keep_for_processing(dataframe_paypal_csv_initial)
    
    dataframe_paypal_csv_after_filter_columns_and_transaction_types = filter_rows_given_transaction_types_to_keep(dataframe_paypal_csv_after_filter_columns)

    dataframe_paypal_csv_after_filter_columns_and_transaction_types_and_negative_values = filter_rows_due_to_negative_values(dataframe_paypal_csv_after_filter_columns_and_transaction_types)

    write_dataframe_to_output_file(dataframe_paypal_csv_after_filter_columns_and_transaction_types_and_negative_values,
                                   filename_to_write_to)

main()

# future features:
# 1.
# rows with currency conversion type
# - if 'Donation Payment' and currency is not USD, then get rid of it
# - if currency is USD then keep it
# overall idea:
# don't want currency conversion lines
# do want the final USD amount
# 2.
# 'General Payment' that has negative value -- can get rid of
# ^ this is taken care of by removing all negative values
# 3.
# 'Express Checkout Payment' that has negative value -- can get rid of
# ^ this is taken care of by removing all negative values

# I ran this script locally with
# $ python3 example_pandas_for_paypal_csv.py -i 'example_csvs/PplTest.csv' -o 'example_csvs/example_output_from_PplTest2.csv'
