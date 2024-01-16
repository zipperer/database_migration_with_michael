import csv

filename_to_read = 'example_csvs/people.csv'
filename_to_write = 'example_csvs/people_filtered.csv'

fieldnames_to_keep = ['first_name', 'username', 'favorite_color'] # will use this to filter whole columns
color_to_exclude = 'green' # will use this to filter rows

def read_csv_write_csv(csv_filename_to_read : str,
                       csv_filename_to_write : str
                       ) -> None:
    with open(csv_filename_to_write, mode='w', newline='') as csv_fileobject_to_write:
        csv_writer = csv.DictWriter(csv_fileobject_to_write, 
                                    fieldnames=fieldnames_to_keep, 
                                    extrasaction='ignore') # 'raise' or 'ignore' when row-to-write has more fields than specified in fieldnames
        csv_writer.writeheader()
        with open(csv_filename_to_read, mode='r', newline='') as csv_fileobject_to_read:
            csv_reader = csv.DictReader(csv_fileobject_to_read)
            for row in csv_reader:
                if row_satisfies_constraints(row):
                    csv_writer.writerow(row)

def is_substring(substring_candidate : str,
                 string : str) -> bool:
    return substring_candidate in string

def row_satisfies_constraints(row) -> bool:
    return (row_satisfies_constraints_on_color(row) and
            True # put other constraints here
            )

def row_satisfies_constraints_on_color(row) -> bool:
    row_favorite_color = row['favorite_color']
    if is_substring(color_to_exclude,row_favorite_color):
        return False
    return True

read_csv_write_csv(csv_filename_to_read=filename_to_read,
                   csv_filename_to_write=filename_to_write)                  
