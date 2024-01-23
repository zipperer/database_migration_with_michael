import os
import csv

def bible_display_app_filename_to_date(filename: str) -> str:
    '''
    From filename, extract date and format in YYYY-MM-DD.
    >>> bible_display_app_filename_to_date('BDA 2018 8 19.txt')
    '2018-08-19'
    >>> bible_display_app_filename_to_date('BDA 2020 7 04.txt')
    '2020-07-04'
    >>> bible_display_app_filename_to_date('BDA 2021 7 10.txt')
    '2021-07-10'
    '''
    # 'BDA 2018 8 19.txt' -> ('BDA 2018 8 19', '.txt')
    filename_before_extension, dot_txt_extension = os.path.splitext(filename)
    # 'BDA 2018 8 19' -> ('BDA', '2018', '8', '19')
    bda, year, month, day_and_possibly_extra = filename_before_extension.split(' ')
    # e.g. for 'BDA 2017 8 13(1).txt', day_and_possibly_extra is 13(1). 
    # So, to get day, get first two characters.
    day = day_and_possibly_extra[0:2]

    if len(month) == 1:
        month = '0' + month
    year_month_day_joined_with_hyphens = year + '-' + month + '-' + day
    return year_month_day_joined_with_hyphens

def main():
    directory_of_bible_display_app_files = 'bible_verse_timestamp_files_unzipped'
    bible_display_app_filenames = os.listdir(directory_of_bible_display_app_files)
    filename_file_to_write = 'bible_display_app_file_to_date.csv'
    output_csv_column_names = ['filename', 'file_date']
    with open(filename_file_to_write, 'w', newline='') as file_object_file_to_write:
        csv_writer = csv.DictWriter(file_object_file_to_write, fieldnames=output_csv_column_names, delimiter='|')
        csv_writer.writeheader()
        for bible_display_app_filename in bible_display_app_filenames:
            bible_display_app_filename_date = bible_display_app_filename_to_date(bible_display_app_filename)
            dictionary_for_row_to_write = {
                'filename' : bible_display_app_filename, 
                'file_date' : bible_display_app_filename_date
                }
            csv_writer.writerow(dictionary_for_row_to_write)

if __name__ == '__main__':
    main()
