from typing import Tuple
import csv

filename_file_to_read = 'program_number_and_title_pipe_separated.csv'
filename_file_to_write = 'program_number_and_title_pipe_separated_with_columns_for_day_and_date.csv'
dict_reader_fieldnames = ['program_id', 'program_code', 'program_title']
dict_writer_fieldnames = ['program_id', 'program_code', 'program_day', 'program_morning_or_night', 'program_date', 'program_title']

decode_day_dictionary = {
    'S' : 'Sunday',
    'W' : 'Wednesday'
    }

def decode_day(day_code : str) -> str:
    '''
    >>> decode_day('S')
    'Sunday'
    >>> decode_day('W')
    'Wednesday'
    For other inputs, announce it for now then handle it later.
    '''
    if day_code in decode_day_dictionary:
        return decode_day_dictionary[day_code]
    else:
        print(f'decode_day unhandled input {day_code}')
        return day_code

decode_morning_or_night_dictionary = {
    'M' : 'morning',
    'N' : 'night'
    }

def decode_morning_or_night(morning_or_night_code : str) -> str:
    '''
    >>> decode_morning_or_night('M')
    'morning'
    >>> decode_morning_or_night('N')
    'night'
    For other inputs, announce it for now then handle it later.
    '''
    if morning_or_night_code in decode_morning_or_night_dictionary:
        return decode_morning_or_night_dictionary[morning_or_night_code]
    else:
        print(f'decode_morning_or_night unhandled input {morning_or_night_code}')
        return morning_or_night_code

def decode_date(date_encoded : str) -> str:
    '''
    >>> decode_date('090901')
    '2001-09-09'
    >>> decode_date('091601')
    '2001-09-16'
    >>> decode_date('091901')
    '2001-09-19'
    '''
    month = date_encoded[0:2]
    day = date_encoded[2:4]
    year = date_encoded[4:]
    year_with_20_prefix = '20' + year
    date_decoded = year_with_20_prefix + '-' + month + '-' + day
    return date_decoded

def parse_program_date_code(date_code : str) -> Tuple[str, str, str]:
    '''
    e.g. 
    >>> parse_program_date_code('SN090901')
    ('Sunday', 'night', '2001-09-09')
    >>> parse_program_date_code('SM091601')
    ('Sunday, 'morning', '2001-09-16')
    >>> parse_program_date_code('WN091901')
    ('Wednesday', 'night', '2001-09-19')
    '''
    day_encoded = date_code[0]
    morning_or_night_encoded = date_code[1]
    date_encoded = date_code[2:]
    day_decoded = decode_day(day_encoded)
    morning_or_night_decoded = decode_morning_or_night(morning_or_night_encoded)
    date_decoded = decode_date(date_encoded)
    return (day_decoded, morning_or_night_decoded, date_decoded)


with open(filename_file_to_write, 'w', newline='') as output_csv:
    csv_writer = csv.DictWriter(output_csv, dict_writer_fieldnames, delimiter='|')
    csv_writer.writeheader()
    with open(filename_file_to_read, newline='') as input_csv:
        csv_reader = csv.DictReader(input_csv, delimiter='|')
        # next(csv_reader) # skip header?
        for row_as_dictionary in csv_reader:
            id = row_as_dictionary['program_id']
            date_code = row_as_dictionary['program_code']
            title = row_as_dictionary['program_title']
            day, morning_or_night, date = parse_program_date_code(date_code)
            dictionary_to_write = {
                'program_id' : id,
                'program_code' : date_code,
                'program_day' : day,
                'program_morning_or_night' : morning_or_night,
                'program_date' : date,
                'program_title' : title
                }
            csv_writer.writerow(dictionary_to_write)
