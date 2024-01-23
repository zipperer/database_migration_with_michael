import csv

filename_file_to_read = 'program_number_and_title.csv'
with open(filename_file_to_read) as file_object_file_to_read:
    file_lines_file_to_read = file_object_file_to_read.readlines()
filename_file_to_write = 'program_number_and_title_pipe_separated_quote_none.csv'
fieldnames_for_input_file=['program_id', 'program_code', 'program_title']
with open(filename_file_to_write, 'w', newline='') as file_object_file_to_write:
    csv_writer = csv.DictWriter(file_object_file_to_write, fieldnames=fieldnames_for_input_file, delimiter='|', escapechar='\\', quoting=csv.QUOTE_NONE)
    csv_writer.writeheader()
    for file_line in file_lines_file_to_read:
        file_line_split_into_three_fields = file_line.split(sep=' ', maxsplit=2)
        program_id = file_line_split_into_three_fields[0]
        program_code = file_line_split_into_three_fields[1]
        program_title = file_line_split_into_three_fields[2]
        program_title_no_whitespace_at_ends = program_title.strip()
        dictionary_of_values_to_write = {
            'program_id' : program_id,
            'program_code' : program_code,
            'program_title' : program_title_no_whitespace_at_ends
            }
#        print(file_line_split_into_three_fields)
#        print(dictionary_of_values_to_write)
        csv_writer.writerow(dictionary_of_values_to_write)
