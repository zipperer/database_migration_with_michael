import psycopg2
# argparse ... to get id

ID_VALUE_TO_USE_IN_QUERY = '3192'
database_name_in_database_cluster = 'postgres'
host_of_database_cluster = 'localhost'
port_of_database_cluster = 5433
password = 'hello'

psycopg2_connection = psycopg2.connect(f'dbname={database_name_in_database_cluster} '
                                       f'user=postgres '
                                       f'host={host_of_database_cluster} '
                                       f'port={port_of_database_cluster} '
                                       f'password={password} ')
psycopg2_cursor = psycopg2_connection.cursor()

psycopg2_cursor.execute('''
SELECT id, entry.entry_timestamp, entry.book, entry.chapter, entry.verse 
FROM presentations_decoded_date
JOIN bible_display_app_file_entries_with_morning_or_night as entry ON presentations_decoded_date.presentation_date = entry.entry_date
WHERE presentations_decoded_date.morning_or_night = entry.morning_or_night AND
      id = %s 
ORDER BY entry_timestamp;''', (ID_VALUE_TO_USE_IN_QUERY,))

results = psycopg2_cursor.fetchall()
for result in results:
    print(result) # output needs to be formatted

# example output
# ...
# (3192, datetime.datetime(2014, 1, 5, 0, 1, 49), 'Romans', '8', '29')
# (3192, datetime.datetime(2014, 1, 5, 0, 1, 50), 'Romans', '8', '29')
# ...

psycopg2_connection.close()

