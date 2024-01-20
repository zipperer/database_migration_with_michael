import argparse
import re
from typing import Dict
from remove_strong_numbers_except_for_given_word_helpers import remove_strong_numbers_except_after_given_word

def parse_commandline_arguments() -> Dict[str, str]:
    description = '''
    This program:
      1. takes as input a filename (input_filename) for a text file with Strong concordance numbers
      2. takes as input a filename (output_filename) for a text file this program will write
      3. takes as input a word for which the program will keep Strong concordance numbers, discarding the numbers for all
         other words
      4. writes to file with filename output_filename
      5. it writes the text from file with input_filename, discarding the Strong concordance numbers for all words except
         for the given word
    '''
    formatter_class = argparse.RawTextHelpFormatter
    parser = argparse.ArgumentParser(description=description,
                                     formatter_class=formatter_class)
    parser.add_argument('-i', '--input_filename', help='the file with Strong concordance numbers to remove')
    parser.add_argument('-w', '--word_with_numbers_to_keep', help='the word for which we will keep the Strong concordance numbers')
    parser.add_argument('-o', '--output_filename', help='the file with the text from the input file with Strong concordance numbers removed for all words except the given word')
    commandline_argument_namespace_object = parser.parse_args()
    input_filename = commandline_argument_namespace_object.input_filename
    word_for_which_to_keep_strong_numbers = commandline_argument_namespace_object.word_with_numbers_to_keep
    output_filename = commandline_argument_namespace_object.output_filename
    dictionary_to_return = {
        'input_filename' : input_filename,
        'word_for_which_to_keep_strong_numbers' : word_for_which_to_keep_strong_numbers,
        'output_filename' : output_filename
        }
    return dictionary_to_return

def main():
    dictionary_commandline_arguments = parse_commandline_arguments()
    input_filename = dictionary_commandline_arguments['input_filename']
    word_for_which_to_keep_strong_numbers = dictionary_commandline_arguments['word_for_which_to_keep_strong_numbers']
    output_filename = dictionary_commandline_arguments['output_filename']
    with open(input_filename) as input_filename_file_object:
        input_file_contents_as_string = input_filename_file_object.read()
    input_file_contents_as_string_with_strong_numbers_removed_except_after_given_word = remove_strong_numbers_except_after_given_word(input_file_contents_as_string, word_for_which_to_keep_strong_numbers)
    with open(output_filename, 'w') as output_file_object:
        output_file_object.write(input_file_contents_as_string_with_strong_numbers_removed_except_after_given_word)
        
main()
