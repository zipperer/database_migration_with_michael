import pandas as pd
from typing import List

csv_dataframe_initial = pd.read_csv('example_csvs/people.csv')

def filter_to_columns(dataframe : pd.DataFrame,
                    columns : List[str]) -> pd.DataFrame:
    return dataframe[columns]

def reorder_columns(dataframe : pd.DataFrame,
                    columns_in_new_order : List[str]) -> pd.DataFrame:
    return dataframe[columns_in_new_order]

csv_dataframe_with_filtered_columns = filter_to_columns(csv_dataframe_initial,
                                                        ['first_name', 'username', 'favorite_color'])
# i.e. csv_dataframe_initial[['first_name', 'username', 'favorite_color']]

print(csv_dataframe_with_filtered_columns)

csv_dataframe_with_reordered_columns = reorder_columns(csv_dataframe_initial, 
                                                       ['username', 'first_name', 'favorite_color'])
# i.e. csv_dataframe_initial[['username', 'first_name', 'favorite_color']]
print(csv_dataframe_with_reordered_columns)

csv_boolean_series_favorite_color_variety_of_green = csv_dataframe_initial['favorite_color'].str.contains('green')
csv_dataframe_with_filtered_rows_favorite_color_green = csv_dataframe_initial[csv_boolean_series_favorite_color_variety_of_green]
print(csv_dataframe_with_filtered_rows_favorite_color_green)

csv_boolean_series_favorite_color_not_a_variety_of_green = (~ csv_boolean_series_favorite_color_variety_of_green)
csv_dataframe_with_filtered_rows_favorite_color_not_green = csv_dataframe_initial[csv_boolean_series_favorite_color_not_a_variety_of_green]
print(csv_dataframe_with_filtered_rows_favorite_color_not_green)

csv_dataframe_with_filtered_rows_favorite_color_not_green_and_filtered_columns = filter_to_columns(csv_dataframe_with_filtered_rows_favorite_color_not_green, ['first_name', 'username', 'favorite_color'])
print(csv_dataframe_with_filtered_rows_favorite_color_not_green_and_filtered_columns)

csv_boolean_series_favorite_color_variety_of_red = csv_dataframe_initial['favorite_color'].str.contains('red')
csv_boolean_series_favorite_color_variety_of_red_or_green = (csv_boolean_series_favorite_color_variety_of_red | csv_boolean_series_favorite_color_variety_of_green)
csv_dataframe_with_filtered_rows_favorite_color_red_or_green =  csv_dataframe_initial[csv_boolean_series_favorite_color_variety_of_red_or_green]
print(csv_dataframe_with_filtered_rows_favorite_color_red_or_green)

#csv_dataframe_with_filtered_rows_favorite_color_red_or_green.to_csv('example_csvs/people_filtered_pandas.csv')
# ^ writes out column with autoincrementing ints that pandas creates and that is not in original csv
# https://pandas.pydata.org/docs/user_guide/io.html#io-store-in-csv
csv_dataframe_with_filtered_rows_favorite_color_red_or_green.to_csv('example_csvs/people_filtered_pandas1.csv', index=False)
