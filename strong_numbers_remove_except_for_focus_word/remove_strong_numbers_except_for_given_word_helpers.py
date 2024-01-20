import re
from typing import Tuple

WORD_FOLLOWED_BY_LEFT_CORNER_BRACKET_NUMBERS_RIGHT_CORNER_BRACKET_RAW_STRING_PATTERN = r'\w+\s+<\d+>'
WORD_FOLLOWED_BY_LEFT_CORNER_BRACKET_NUMBERS_RIGHT_CORNER_BRACKET_PATTERN = re.compile(WORD_FOLLOWED_BY_LEFT_CORNER_BRACKET_NUMBERS_RIGHT_CORNER_BRACKET_RAW_STRING_PATTERN)

WHITESPACE_RAW_STRING_PATTERN = r'\s+'
WHITESPACE_PATTERN = re.compile(WHITESPACE_RAW_STRING_PATTERN) 

def split_on_first_whitespace(input_string : str) -> Tuple[str,str]:
    # https://docs.python.org/3/library/re.html#re.Pattern.split
    section_before_first_occurrence_whitespace_and_section_after_first_occurrence_of_whitespace = WHITESPACE_PATTERN.split(input_string, maxsplit=1)
    section_before_first_occurrence_whitespace = section_before_first_occurrence_whitespace_and_section_after_first_occurrence_of_whitespace[0]
    section_after_first_occurrence_of_whitespace = section_before_first_occurrence_whitespace_and_section_after_first_occurrence_of_whitespace[1]
    return section_before_first_occurrence_whitespace, section_after_first_occurrence_of_whitespace

def remove_strong_numbers_except_after_given_word(input_file_contents_as_string : str, 
                                                  word_for_which_to_keep_strong_numbers : str
                                                  ) -> str:

    # find each string in input_file_contents_as_string that matches r'\w+\s+<\d+>', e.g. 'rich <124>'.
    # return a list of these matches, e.g. ['rich <124>', 'beyond <321>', 'brethren <9991>']
    matches_for_pattern_in_input_file_contents_as_string = WORD_FOLLOWED_BY_LEFT_CORNER_BRACKET_NUMBERS_RIGHT_CORNER_BRACKET_PATTERN.findall(input_file_contents_as_string)

    # initialize string in which we will replace. e.g. will replace 'brethren <9991>' with 'brethren'
    string_with_extra_strong_numbers_removed = input_file_contents_as_string

    # pattern for word for which to keep Strong numbers. pattern is case-insensitive 
    word_for_which_to_keep_strong_numbers_pattern = re.compile(word_for_which_to_keep_strong_numbers, re.IGNORECASE)

    # for any match like 'brethren <9991>', replace 'brethren <9991>' with 'brethren'
    for match_for_pattern in matches_for_pattern_in_input_file_contents_as_string:
        # split 'brethren <9991>' into ('brethren', '<9991>')
        match_for_pattern_word_before_whitespace, match_for_pattern_remainder_after_whitespace = split_on_first_whitespace(match_for_pattern)
        # get 'brethren'
        word = match_for_pattern_word_before_whitespace
        # if 'brethren' does not match 'rich' (i.e. if the word does not match the word for which we are keeping the Strong numbers)
        if (not word_for_which_to_keep_strong_numbers_pattern.match(word)):
            # replace 'brethren <9991>' with 'brethren'
            string_with_extra_strong_numbers_removed = string_with_extra_strong_numbers_removed.replace(match_for_pattern, word)
    return string_with_extra_strong_numbers_removed

def test_pattern_to_detect_word_then_strong_numbers():
    assert WORD_FOLLOWED_BY_LEFT_CORNER_BRACKET_NUMBERS_RIGHT_CORNER_BRACKET_PATTERN.match('hello <123>') != None
    assert WORD_FOLLOWED_BY_LEFT_CORNER_BRACKET_NUMBERS_RIGHT_CORNER_BRACKET_PATTERN.match('rich <345>') != None
    assert WORD_FOLLOWED_BY_LEFT_CORNER_BRACKET_NUMBERS_RIGHT_CORNER_BRACKET_PATTERN.match('beyond <321>') != None
    assert WORD_FOLLOWED_BY_LEFT_CORNER_BRACKET_NUMBERS_RIGHT_CORNER_BRACKET_PATTERN.match('measure <55>') != None
    assert WORD_FOLLOWED_BY_LEFT_CORNER_BRACKET_NUMBERS_RIGHT_CORNER_BRACKET_PATTERN.match('never <32>') != None
    assert WORD_FOLLOWED_BY_LEFT_CORNER_BRACKET_NUMBERS_RIGHT_CORNER_BRACKET_PATTERN.match('brethren <9991>') != None
    assert WORD_FOLLOWED_BY_LEFT_CORNER_BRACKET_NUMBERS_RIGHT_CORNER_BRACKET_PATTERN.match('rich <1024>') != None
    assert WORD_FOLLOWED_BY_LEFT_CORNER_BRACKET_NUMBERS_RIGHT_CORNER_BRACKET_PATTERN.match('rich beyond') == None

def test_remove_strong_numbers_except_after_given_word():
    assert remove_strong_numbers_except_after_given_word('hello <123> rich <134> bye <135>', 'rich') == 'hello rich <134> bye'
    assert remove_strong_numbers_except_after_given_word('hello <123> rich <134> bye <135>', 'hello') == 'hello <123> rich bye'
    assert remove_strong_numbers_except_after_given_word('hello <123> rich <134> bye <135>', 'bye') == 'hello rich bye <135>'

def test_split_on_first_whitespace():
    assert split_on_first_whitespace('a b') == ('a', 'b')
    assert split_on_first_whitespace('a\nb') == ('a', 'b')
    assert split_on_first_whitespace('a\tb') == ('a', 'b')
    assert split_on_first_whitespace('a\n\nb') == ('a', 'b')
    assert split_on_first_whitespace('a\n\nb\n') == ('a', 'b\n')
    assert split_on_first_whitespace('a b c') == ('a', 'b c')
