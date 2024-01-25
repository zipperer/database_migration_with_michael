# For each file in
# ~/grace_and_truth_ministries/migrate_database_with_michael/title_program_numbers_and_bible_verse_timestamp_files/bible_verse_timestamp_files/bible_verse_timestamp_files_unzipped/
# 
# make a csv file based on the file.
# make two csvs files based on the file if the file contains entries for both morning session and evening session.
import os
from typing import List, Any, Callable, Optional, Tuple, Dict
import datetime
import csv

def remove_if_not_recursive(input_list : List[Any],
                  predicate : Callable[[Any], bool],
                  verbose : bool = True) -> List[Any]:
    if input_list == list():
        return list()
    elif (not predicate(input_list[0])):
        if verbose:
            print(f'remove_if_not_recursive removed {input_list[0]}, because it failed to match {predicate}')
        return remove_if_not_recursive(input_list[1:], predicate)
    else:
        return [input_list[0]] + remove_if_not_recursive(input_list[1:], predicate)

def remove_if_not(input_list : List[Any],
                  predicate : Callable[[Any], bool],
                  verbose : bool = True) -> List[Any]:
    input_list_with_elements_that_satisfy_predicate = list()
    for element in input_list:
        if predicate(element):
            input_list_with_elements_that_satisfy_predicate.append(element)
    return input_list_with_elements_that_satisfy_predicate
            

def even(x : int) -> bool:
    return (x % 2) == 0

def is_one(x : Any) -> bool:
    return x == 1

def test_remove_if_not():
    assert remove_if_not([1, 2, 3, 4, 5], even) == [2, 4]
    assert remove_if_not([1, 2, 3, 4, 5], is_one) == [1]
    
def line_of_input_text_file_contains_squiggle_brackets(line_of_input_text_file : str) -> bool:
    '''
    '''
    return (('{' in line_of_input_text_file) and
            ('}' in line_of_input_text_file))

def convert_to_one_or_more_csvs(filename_for_file_to_read_full_path : str, 
                                directory_of_files_to_write_full_path : str) -> None:
    '''
    Take content of filename_for_file_to_read_full_path, e.g.
      {"Sun 5 Jan 2014 00:01:49", "Romans", 8, 29}
      ...
      {"Sun 5 Jan 2014 01:31:00", "2Corinthians", 10, 16}
      ...
      {"Sun 5 Jan 2014 00:04:45", "1Timothy", 4, 1}
      ...
      {"Sun 5 Jan 2014 01:33:49", "Titus", 3, 4}

    Convert content of file into a csv or two csvs.

    Make two csvs when the content of the file contains a restart from 12am, e.g. in example above
      see {"Sun 5 Jan 2014 01:31:00", "2Corinthians", 10, 16} followed by 
          {"Sun 5 Jan 2014 00:04:45", "1Timothy", 4, 1}.


    Each output csv will have form
    filename                  | filename_date | morning_or_night | entry_timestamp     | book        | chapter | verse
    BDA_2014_1_05_morning.csv | 2014-01-05    | morning          | 2014-01-05 00:01:49 | Romans      | 8       | 29
    ...
    BDA_2014_1_05_morning.csv | 2014-01-05    | morning          | 2014-01-05 01:31:00"| 2Corinthians| 10      | 16

    
    The method stores the output csv files in os.path.join(directory_of_files_to_write_full_path, filename_for_csv.csv)
    '''
    # read lines of file
    # separate lines into (a) morning session and (b) night session.
    # if there is no restart at 12am, then all lines are night session.
    # if there is a restart, then lines before restart are morning session and lines after are night.
    # write all morning lines to filename_morning.csv -- where morning_or_night = 'morning'
    # write all night lines to filename_night.csv -- where morning_or_night == 'night'
    with open(filename_for_file_to_read_full_path) as file_object_filename_for_file_to_read_full_path:
        lines_of_input_file = file_object_filename_for_file_to_read_full_path.readlines()

    # remove any line that does not contain both '{' and '}'. Protect against stray newlines.
    lines_of_input_file = remove_if_not(lines_of_input_file, line_of_input_text_file_contains_squiggle_brackets)

    lines_of_input_file_separated_by_session = separate_lines_of_input_file_by_session(lines_of_input_file)

    lines_of_input_file_for_night_session, lines_of_input_file_for_morning_session = lines_of_input_file_separated_by_session

    filename_for_file_to_read = os.path.basename(filename_for_file_to_read_full_path)
    filename_for_file_to_read_without_extension, txt_extension = os.path.splitext(filename_for_file_to_read)
    filename_for_file_to_read_without_extension_with_underscores_for_spaces = filename_for_file_to_read_without_extension.replace(' ', '_')
    
    if lines_of_input_file_for_morning_session:
        # write csv file for morning session
        filename_csv_file_for_entries_from_morning_session = filename_for_file_to_read_without_extension_with_underscores_for_spaces + '_morning' + '.csv'
        filename_csv_file_for_entries_from_morning_session_full_path = os.path.join(directory_of_files_to_write_full_path, filename_csv_file_for_entries_from_morning_session)
        write_entries_csv_for_lines_from_input_entries_file(filename_csv_file_for_entries_from_morning_session_full_path, lines_of_input_file_for_morning_session)

    # write csv file for night session
    filename_csv_file_for_entries_from_night_session = filename_for_file_to_read_without_extension_with_underscores_for_spaces + '_night' + '.csv'
    filename_csv_file_for_entries_from_night_session_full_path = os.path.join(directory_of_files_to_write_full_path, filename_csv_file_for_entries_from_night_session)
    write_entries_csv_for_lines_from_input_entries_file(filename_csv_file_for_entries_from_night_session_full_path, lines_of_input_file_for_night_session)

output_csv_fieldnames = ['filename', 'entry_date', 'morning_or_night', 'entry_timestamp', 'book', 'chapter', 'verse']

def write_entries_csv_for_lines_from_input_entries_file(filename_csv_file_for_entries_from_session_full_path : str,
                                                        lines_of_input_file_for_session : List[str]) -> None:

    filename_csv_file_for_entries_from_session = os.path.basename(filename_csv_file_for_entries_from_session_full_path)
    
    if 'morning' in filename_csv_file_for_entries_from_session:
        session_morning_or_night = 'morning'
    else:
        session_morning_or_night = 'night'

    with open(filename_csv_file_for_entries_from_session_full_path, mode='w', newline='') as file_object_output_csv:
        # ^ newline='' comes from csv module documentation
        csv_writer = csv.DictWriter(file_object_output_csv, fieldnames=output_csv_fieldnames, delimiter='|')
        csv_writer.writeheader()
        for line_of_input_file_for_session in lines_of_input_file_for_session:
            dictionary_to_write_for_line = line_from_file_to_dictionary_to_write_for_line(filename_csv_file_for_entries_from_session,
                                                                                          line_of_input_file_for_session)
            dictionary_to_write_for_line['morning_or_night'] = session_morning_or_night
            csv_writer.writerow(dictionary_to_write_for_line)


def line_from_file_to_dictionary_to_write_for_line(filename_file_to_write : str,
                                                   line : str) -> Dict:
    '''
    '{"Mon 4 Nov 2013 23:21:49", "2Samuel", 3, 22}\n' ->
    {
      'filename' : FILENAME, 
      'entry_date' : ENTRY_DATE, # plan to have postgres cast this from timestamp to date
      'entry_timestamp' : ENTRY_TIMESTAMP, # first item from input
      'book' : BOOK, # str() -- second item from input
      'chapter' : CHAPTER, # int() -- third item from input
      'verse' : VERSE # int() -- fourth item from input]
    }
    '''
    # remove whitespace from left (if any) and from right (e.g. trailing newline), i.e.
    # '{"Mon 4 Nov 2013 23:21:49", "2Samuel", 3, 22}\n' -> '{"Mon 4 Nov 2013 23:21:49", "2Samuel", 3, 22}'
    line_without_whitespace_at_ends = line.strip()
    #line_without_brackets = line_without_whitespace_at_ends.removeprefix('{').removesuffix('}')
    # '{"Mon 4 Nov 2013 23:21:49", "2Samuel", 3, 22}' -> '"Mon 4 Nov 2013 23:21:49", "2Samuel", 3, 22'
    line_without_brackets = line_without_whitespace_at_ends.replace('{', '').replace('}', '')
    # '"Mon 4 Nov 2013 23:21:49", "2Samuel", 3, 22' -> ["Mon 4 Nov 2013 23:21:49", "2Samuel", 3, 22]
    line_split_on_comma_space = line_without_brackets.split(', ')
    # ["Mon 4 Nov 2013 23:21:49", "2Samuel", 3, 22] -> '"Mon 4 Nov 2013 23:21:49"'
    entry_timestamp_with_quotes = line_split_on_comma_space[0]
    # '"Mon 4 Nov 2013 23:21:49"' -> 'Mon 4 Nov 2013 23:21:49'
    entry_timestamp = entry_timestamp_with_quotes.replace('"', '')
    # ["Mon 4 Nov 2013 23:21:49", "2Samuel", 3, 22] -> '"2Samuel"'
    entry_book_with_quotes = line_split_on_comma_space[1]
    # '"2Samuel"' -> '2Samuel'
    entry_book = entry_book_with_quotes.replace('"', '')
    #entry_chapter_with_quotes = line_split_on_comma_space[2]
    #entry_chapter = entry_chapter_with_quotes.replace('"', '')
    #^ commented out two lines above, because I claim the chapter will not have extra quotes
    entry_chapter = line_split_on_comma_space[2]
    entry_verse = line_split_on_comma_space[3]
    dictionary_to_write_for_line = {
        'filename' : filename_file_to_write, 
        'entry_date' : entry_timestamp, # intentionally using timestamp here for date. postgres will cast the type from timestamp to date
        'entry_timestamp' : entry_timestamp,
        'book' : entry_book, 
        'chapter' : entry_chapter,
        'verse' : entry_verse
    }
    return dictionary_to_write_for_line        

month_three_letter_abbreviation_to_number_dictionary = {
    'Jan' : 1,
    'Feb' : 2,
    'Mar' : 3,
    'Apr' : 4,
    'May' : 5,
    'Jun' : 6,
    'Jul' : 7,
    'Aug' : 8,
    'Sep' : 9,
    'Oct' : 10,
    'Nov' : 11,
    'Dec' : 12
    }

def month_three_letter_abbreviation_to_number(month_as_string_three_letter_abbreviation : str) -> int:
    '''
    'Jan' -> 1
    ...
    'Dec' -> 12
    '''
    return month_three_letter_abbreviation_to_number_dictionary[month_as_string_three_letter_abbreviation]

# todo: factor
def line_to_datetime(line : str) -> datetime.datetime:
    '''
    '{"Sun 5 Jan 2014 00:01:49", "Romans", 8, 29}\n'
    ->
    datetime.datetime(year=2014, month=1, day=5, hour=0, minute=1, second=49)
    '''
    #breakpoint()
    # '{"Sun 5 Jan 2014 00:01:49", "Romans", 8, 29}\n' -> '{"Sun 5 Jan 2014 00:01:49", "Romans", 8, 29}'
    line_stripped = line.strip()

    # '{"Sun 5 Jan 2014 00:01:49", "Romans", 8, 29}' -> '"Sun 5 Jan 2014 00:01:49", "Romans", 8, 29'
    line_stripped_no_brackets = line_stripped.replace('{', '').replace('}', '')

    # '"Sun 5 Jan 2014 00:01:49", "Romans", 8, 29' -> ['"Sun 5 Jan 2014 00:01:49"', '"Romans", 8, 29'] # list with two strings
    line_stripped_no_brackets_split_on_comma_space_once = line_stripped_no_brackets.split(', ', maxsplit=1)

    # ['"Sun 5 Jan 2014 00:01:49"', '"Romans", 8, 29'] -> '"Sun 5 Jan 2014 00:01:49"'
    date_as_string = line_stripped_no_brackets_split_on_comma_space_once[0]

    # '"Sun 5 Jan 2014 00:01:49"' -> 'Sun 5 Jan 2014 00:01:49'
    date_as_string_remove_internal_quotes = date_as_string.replace('"', '')

    # 'Sun 5 Jan 2014 00:01:49' -> ['Sun', '5', 'Jan', '2014' ,'00:01:49']
    date_components_as_strings_and_time_as_string = date_as_string_remove_internal_quotes.split(' ')

    # ['Sun', '5', 'Jan', '2014' ,'00:01:49'] -> '5'
    day_number_as_string = date_components_as_strings_and_time_as_string[1]
    #                                         -> 'Jan'
    month_as_string = date_components_as_strings_and_time_as_string[2]
    #                                         -> '2014'
    year_as_string = date_components_as_strings_and_time_as_string[3]
    #                                         -> '00:01:49'
    time_as_string = date_components_as_strings_and_time_as_string[4]

    # '00:01:49' -> ['00', '01', '49']
    time_as_string_split = time_as_string.split(':')
    # ['00', '01', '49'] -> '00'
    hours_as_string = time_as_string_split[0]
    #                    -> '01'
    minutes_as_string = time_as_string_split[1]
    #                    -> '49'
    seconds_as_string = time_as_string_split[2]

    # '5' -> 5
    day_number = int(day_number_as_string)

    # 'Jan' -> 1
    month_number = month_three_letter_abbreviation_to_number(month_as_string)

    # '2014' -> 2014
    year_number = int(year_as_string)

    # '00' -> 0
    hour_number = int(hours_as_string)

    # '01' -> 1
    minute_number = int(minutes_as_string)

    # '49' -> 49
    second_number = int(seconds_as_string)

    return datetime.datetime(year=year_number,
                             month=month_number,
                             day=day_number,
                             hour=hour_number,
                             minute=minute_number,
                             second=second_number)

def test_line_to_datetime():
    assert line_to_datetime('{"Sun 5 Jan 2014 00:01:49", "Romans", 8, 29}\n') == datetime.datetime(year=2014,
                                                                                                   month=1,
                                                                                                   day=5,
                                                                                                   hour=0,
                                                                                                   minute=1,
                                                                                                   second=49)

    assert line_to_datetime('{"Sun 5 Jan 2014 07:34:20", "2Corinthians", 10, 16}\n') == datetime.datetime(year=2014,
                                                                                                          month=1,
                                                                                                          day=5,
                                                                                                          hour=7,
                                                                                                          minute=34,
                                                                                                          second=20)

    assert line_to_datetime('{"Sun 5 Jan 2014 00:04:45", "1Timothy", 4, 1}\n') == datetime.datetime(year=2014,
                                                                                                    month=1,
                                                                                                    day=5,
                                                                                                    hour=0,
                                                                                                    minute=4,
                                                                                                    second=45)


def separate_lines_of_input_file_by_session(lines_of_input_file : List[str]) -> Tuple[List[str], Optional[List[str]]]:
    '''
    Look for line for which the date in current line occurs AFTER date in next line.
    If this occurs, return lines up to and including current line as lines for morning session
    and return lines after this as lines for night session.
    If this does not occur, return all lines as lines for night session.    
    '''
    file_contains_entries_for_morning_session_and_night_session = False
    index_in_lines_of_input_file_for_last_entry_of_morning_session = None
    index_in_lines_of_input_file_last_possible_index = len(lines_of_input_file) - 1

    # Make new list from lines_of_input_file: the list of dates from each line. Each date is a datetime.datetime.
    lines_of_input_file_as_lines_of_dates = list(map(line_to_datetime, lines_of_input_file))
    # ^ Since this list of dates is the result of list(map(function, lines_of_input_file)),
    # the list of dates has the same length as lines_of_input_file. An index for lines_of_input_file
    # is an index for the corresponding element in the list of dates.

    # range(x) goes from 0 through x - 1, so range(index_in_lines_of_input_file_last_possible_index)
    # will exclude index_in_lines_of_input_file_last_possible_index, which is what we want.
    # The last index i for which we want to check whether date_in_line[i] > date_in_line[i+1] is
    # index_in_lines_of_input_file_last_possible_index - 1.
    for index_in_lines_of_input_file in range(index_in_lines_of_input_file_last_possible_index):
        date_for_current_line = lines_of_input_file_as_lines_of_dates[index_in_lines_of_input_file]
        date_for_next_line = lines_of_input_file_as_lines_of_dates[index_in_lines_of_input_file + 1]
        if date_for_current_line > date_for_next_line:
            file_contains_entries_for_morning_session_and_night_session = True
            index_in_lines_of_input_file_for_last_entry_of_morning_session = index_in_lines_of_input_file
            break

    lines_of_input_file_for_morning_session = None

    if (file_contains_entries_for_morning_session_and_night_session and
        (index_in_lines_of_input_file_for_last_entry_of_morning_session is not None)):
        lines_of_input_file_for_morning_session = lines_of_input_file[:index_in_lines_of_input_file_for_last_entry_of_morning_session + 1]
        lines_of_input_file_for_night_session = lines_of_input_file[index_in_lines_of_input_file_for_last_entry_of_morning_session + 1:]
    else:
        lines_of_input_file_for_night_session = lines_of_input_file

    tuple_lines_of_input_for_night_session_and_morning_session = (lines_of_input_file_for_night_session, lines_of_input_file_for_morning_session)

    return tuple_lines_of_input_for_night_session_and_morning_session


def read_files_from_directory_and_write_files_to_directory(directory_of_files_to_read_full_path : str,
                                                           directory_of_files_to_write_full_path : str) -> None:
    '''
    directory_of_files_to_read_full_path contains .txt files with entries of form
      {"Sun 5 Jan 2014 00:01:49", "Romans", 8, 29}
    directory_of_files_to_write_full_path is a directory to which this function will write files.

    Each file written will be a csv like
      filename                  | filename_date | morning_or_night | entry_timestamp     | book        | chapter | verse
      BDA_2014_1_05_morning.csv | 2014-01-05    | morning          | 2014-01-05 00:01:49 | Romans      | 8       | 29
      ...
      BDA_2014_1_05_morning.csv | 2014-01-05    | morning          | 2014-01-05 01:31:00"| 2Corinthians| 10      | 16

    The default value for morning_or_night is 'night'. A file will have 'morning' if the file contains
     - entries that start at 12am
     - entries that continue after this
     - after above, entries that start at 12 am
    That is, a file will have 'morning' if it contains the list of entries like that that occur before the restart at 12am.
    When an input file has that pattern (start at 12am, proceed, start again at 12am), then there will be two csvs 
    in directory_of_files_to_write_full_path that correspond to that input file. One output csv will have value 'morning'
    in the morning_or_night column. The other output csv will have value 'night'.

    The correspondence between the filenames will be:
    - input filename: 'BDA YYYY (M)M DD.txt' -- the (M) is because single digit days do not have 0 padding, e.g. 'BDA 2014 1 05.txt'
    - output csvs: 'BDA_YYYY_MM_DD_night.csv' and 'BDA_YYYY_MM_DD_morning.csv' (where there is a night and morning)
    '''
    # iterate through input directory (directory_of_files_to_read_full_path)
    # for each file, translate to one or more csvs and save in output directory (directory_of_files_to_write_full_path)

    list_of_files_to_read_and_convert_to_csvs = os.listdir(directory_of_files_to_read_full_path)
    for filename_for_file_to_read in list_of_files_to_read_and_convert_to_csvs:
        filename_for_file_to_read_full_path = os.path.join(directory_of_files_to_read_full_path, filename_for_file_to_read)
        print(f'working on {filename_for_file_to_read_full_path}')
        convert_to_one_or_more_csvs(filename_for_file_to_read_full_path, directory_of_files_to_write_full_path)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--directory_of_files_to_read_full_path', help='directory of files for which to make csvs')
    parser.add_argument('-o', '--directory_of_files_to_write_full_path', help='directory of files where csvs will go')
    commandline_argument_namespace_object = parser.parse_args()
    directory_of_files_to_read_full_path = commandline_argument_namespace_object.directory_of_files_to_read_full_path
    directory_of_files_to_write_full_path = commandline_argument_namespace_object.directory_of_files_to_write_full_path
    read_files_from_directory_and_write_files_to_directory(directory_of_files_to_read_full_path,
                                                           directory_of_files_to_write_full_path)
