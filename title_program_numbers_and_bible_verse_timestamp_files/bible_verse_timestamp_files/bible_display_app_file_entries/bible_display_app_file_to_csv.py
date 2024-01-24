import csv
import os
from typing import Dict

def txt_filename_to_csv_filename(txt_filename : str) -> str:
    '''
    'BDA 2014 1 01.txt' -> 'BDA 2014 1 01.csv'
    '''
    filename_before_extension, extension = os.path.splitext(txt_filename)
    csv_filename = filename_before_extension + '.csv'
    return csv_filename

def test_txt_filename_to_csv_filename():
    assert txt_filename_to_csv_filename('BDA 2014 1 01.txt') == 'BDA 2014 1 01.csv'

def line_from_file_to_dictionary_to_write_for_line(filename_file_to_read : str,
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
    entry_timestamp_with_quotes = line_split_on_comma_space[0]
    entry_timestamp = entry_timestamp_with_quotes.replace('"', '')
    entry_book_with_quotes = line_split_on_comma_space[1]
    entry_book = entry_book_with_quotes.replace('"', '')
    entry_chapter_with_quotes = line_split_on_comma_space[2]
    entry_chapter = entry_chapter_with_quotes.replace('"', '')
    entry_verse = line_split_on_comma_space[3]
    dictionary_to_write_for_line = {
        'filename' : filename_file_to_read,
        'entry_date' : entry_timestamp, # intentionally using timestamp here for date. postgres will cast the type from timestamp to date
        'entry_timestamp' : entry_timestamp,
        'book' : entry_book, 
        'chapter' : entry_chapter,
        'verse' : entry_verse
    }
    return dictionary_to_write_for_line

def line_appears_to_contain_timestamp_entry(line : str) -> bool:
    '''
    confirm line non-empty, in case input file has newlines at bottom
    '''
    if ('{' in line) and ('}' in line):
        return True
    else:
        return False

def write_entries_from_file_to_file(filename_file_to_read : str, 
                                    filename_file_to_write : str) -> None:
    with open(filename_file_to_read) as file_object_file_to_read:
        file_to_read_lines = file_object_file_to_read.readlines()

    # '/Users/andrew/.../BDA 2014 1 01.txt' -> 'BDA 2014 1 01.txt'
    filename_file_to_read_no_path = os.path.basename(filename_file_to_read)

    fieldnames_to_write = ['filename', 'entry_date', 'entry_timestamp', 'book', 'chapter', 'verse']
    with open(filename_file_to_write, 'w', newline='') as file_object_file_to_write:
        csv_writer = csv.DictWriter(file_object_file_to_write, fieldnames=fieldnames_to_write, delimiter='|')
        csv_writer.writeheader()
        for line in file_to_read_lines:
                if line_appears_to_contain_timestamp_entry(line):
                    dictionary_to_write_for_line = line_from_file_to_dictionary_to_write_for_line(filename_file_to_read_no_path, line)
                    csv_writer.writerow(dictionary_to_write_for_line)

def main():
    filename_file_to_read_full_path = '/Users/andrew/grace_and_truth_ministries/migrate_database_with_michael/title_program_numbers_and_bible_verse_timestamp_files/bible_verse_timestamp_files/bible_verse_timestamp_files_unzipped/BDA 2014 1 01.txt'
    #filename_file_to_read = 'BDA 2014 1 01.txt' i.e. os.path.basename(filename_file_to_read_full_path)
    #'BDA 2014 10 05.txt'
    #'BDA 2015 8 12.txt'
    filename_file_to_read_no_path = os.path.basename(filename_file_to_read_full_path)
    filename_file_to_write = txt_filename_to_csv_filename(filename_file_to_read_no_path)
    write_entries_from_file_to_file(filename_file_to_read_full_path, filename_file_to_write)

if __name__ == '__main__':
    main()
