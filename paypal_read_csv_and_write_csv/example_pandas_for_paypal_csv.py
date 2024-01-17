import pandas as pd
import copy

columns_to_keep_for_processing = [
    'Date',
    'Name', 
    'Gross',
    'Note',
    'Town/City',
    'State/Province/Region/County/Territory/Prefecture/Republic',
    'Country',
    'Type']

# BEGIN don't currently use this to delete the 'Type' 
columns_to_keep_for_writing_out_csv = copy.copy(columns_to_keep_for_processing)
columns_to_keep_for_writing_out_csv.remove('Type')
# END

dataframe_paypal_csv_initial = pd.read_csv('example_csvs/PplTest.csv')
dataframe_paypal_csv_after_filter_columns = dataframe_paypal_csv_initial[columns_to_keep_for_processing]

pandas_boolean_series_type_mobile_payment = dataframe_paypal_csv_after_filter_columns['Type'].str.contains('Mobile Payment')
pandas_boolean_series_type_general_payment = dataframe_paypal_csv_after_filter_columns['Type'].str.contains('General Payment')
pandas_boolean_series_type_donation_payment = dataframe_paypal_csv_after_filter_columns['Type'].str.contains('Donation Payment')
pandas_boolean_series_type_general_currency_conversion = dataframe_paypal_csv_after_filter_columns['Type'].str.contains('General Currency Conversion')
pandas_boolean_series_type_express_checkout_payment = dataframe_paypal_csv_after_filter_columns['Type'].str.contains('Express Checkout Payment')
pandas_boolean_series_type_subscription_payment = dataframe_paypal_csv_after_filter_columns['Type'].str.contains('Subscription Payment')
# add additional transaction types to keep 
pandas_boolean_series_type_transaction_to_keep = (pandas_boolean_series_type_mobile_payment  |
                                                  pandas_boolean_series_type_general_payment |
                                                  pandas_boolean_series_type_donation_payment |
                                                  pandas_boolean_series_type_general_currency_conversion | 
                                                  pandas_boolean_series_type_express_checkout_payment |
                                                  pandas_boolean_series_type_subscription_payment)
#dataframe_with_type_transaction_to_keep = dataframe[pandas_boolean_series_type_transaction_to_keep]

dataframe_paypal_csv_after_filter_columns_and_transaction_types = dataframe_paypal_csv_after_filter_columns[pandas_boolean_series_type_transaction_to_keep]

# new 1
pandas_boolean_series_gross_is_negative = (dataframe_paypal_csv_after_filter_columns_and_transaction_types['Gross'] <= 0)
pandas_boolean_series_gross_is_positive = (~ pandas_boolean_series_gross_is_negative)
dataframe_paypal_csv_after_filter_columns_and_transaction_types_and_negative_values = dataframe_paypal_csv_after_filter_columns_and_transaction_types[pandas_boolean_series_gross_is_positive]

filename_to_write_to='example_csvs/example_output_from_PplTest1.csv'
#dataframe_paypal_csv_after_filter_columns_and_transaction_types.to_csv(filename_to_write_to, index=False)
dataframe_paypal_csv_after_filter_columns_and_transaction_types_and_negative_values.to_csv(filename_to_write_to, index=False)


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
