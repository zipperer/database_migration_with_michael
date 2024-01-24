import os
import datetime
from typing import List, Any

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

def list_remove_all(input_list : List[Any],
                    element_to_remove : Any) -> List[Any]:
    if input_list == list():
        return list()
    elif input_list[0] == element_to_remove:
        return list_remove_all(input_list[1:], element_to_remove)
    else:
        return [input_list[0]] + list_remove_all(input_list[1:], element_to_remove)

def main(filename_file_to_read : str) -> None:
    # At first, assume it is possible to have two sessions: morning and night
    # Default to there is only one block. Change this if encounter second session.
    file_contains_entries_for_morning_session_and_night_session = False
    # ^ to generalize this, make a counter
    # if this is False (/ counter is 0), then don't write new files
    with open(filename_file_to_read) as file_object_file_to_read:
        lines_in_file = file_object_file_to_read.readlines()
    lines_in_file_no_empty_lines = list_remove_all(lines_in_file, '\n')
    count_non_empty_lines_in_file = len(lines_in_file_no_empty_lines)
    dates_one_per_line_in_file = list(map(line_to_datetime, lines_in_file_no_empty_lines))

    # we will be checking list[i] and list[i+1]. This last index prevents us from checking the next element for the last element.
    last_index_to_check_whether_element_at_next_index_is_a_date_before_element_at_current_index = count_non_empty_lines_in_file - 1

    last_index_of_first_session = None

    for index in range(last_index_to_check_whether_element_at_next_index_is_a_date_before_element_at_current_index):
        date_at_current_index = dates_one_per_line_in_file[index]
        date_at_next_index = dates_one_per_line_in_file[index + 1]
        if date_at_current_index > date_at_next_index:
            file_contains_entries_for_morning_session_and_night_session = True
            last_index_of_first_session = index
            break

    if (file_contains_entries_for_morning_session_and_night_session and
        last_index_of_first_session is not None):
        # write files for separate sessions
        subdirectory_into_which_to_store_files_for_morning_and_night = 'files_separated_into_morning_and_night'
        suffix_for_first_session = '_session1'
        suffix_for_second_session = '_session2'
        # /Users/andrew/.../FILENAME_BEFORE_EXTENSION.txt -> (FILENAME_BEFORE_EXTENSION, '.txt')
        filename_file_to_read_without_txt, txt_extension = os.path.splitext(os.path.basename(filename_file_to_read))
        filename_for_first_session = filename_file_to_read_without_txt + suffix_for_first_session + txt_extension
        filename_for_second_session = filename_file_to_read_without_txt + suffix_for_second_session + txt_extension
        relative_path_for_file_for_first_session = subdirectory_into_which_to_store_files_for_morning_and_night + '/' + filename_for_first_session
        relative_path_for_file_for_second_session = subdirectory_into_which_to_store_files_for_morning_and_night + '/' + filename_for_second_session
        lines_in_first_session = lines_in_file_no_empty_lines[:last_index_of_first_session + 1]
        lines_in_second_session = lines_in_file_no_empty_lines[last_index_of_first_session + 1:]
        with open(relative_path_for_file_for_first_session, mode='w') as file_object_file_for_first_session:
            for line in lines_in_first_session:
                file_object_file_for_first_session.write(line)
        with open(relative_path_for_file_for_second_session, mode='w') as file_object_file_for_second_session:
            for line in lines_in_second_session:
                file_object_file_for_second_session.write(line)
    # want to:
    # - read initial file
    # - get list of lines
    # - map line_to_datetime over list
    # - search in mapped list for a place where list_of_datetimes[i] > list_of_datetimes[i+1]
    # - record i as last index of morning session
    # - divide original list of lines into entries (a) up to (and not including) index i+1 and (b) start at i+1 to end
    # - in subdirectory, write two new files:
    # -- FILENAME_WITHOUT_TXT_EXTENSION_morning.txt
    # -- FILENAME_WITHOUT_TXT_EXTENSION_night.txt

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_filename_file_to_read', help='filename for file to read and possibly split into morning and evening')
    commandline_argument_namespace_object = parser.parse_args()
    filename_file_to_read = commandline_argument_namespace_object.input_filename_file_to_read
    main(filename_file_to_read)
