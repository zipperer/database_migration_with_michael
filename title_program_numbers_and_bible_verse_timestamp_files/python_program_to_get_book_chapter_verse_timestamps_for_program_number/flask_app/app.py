from flask import Flask, render_template

app = Flask(__name__)

def message_id_title(message_id):
    import psycopg2
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
    psycopg2_cursor.execute('''SELECT title FROM presentations_decoded_date WHERE id = %s;''', (message_id,))
    results = psycopg2_cursor.fetchall()
    result = results[0] # should be only one result
    title = result[0] # should be only one entry in tuple
    return title

def message_id_timestamped_verses(message_id):
    import psycopg2
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
    ORDER BY entry_timestamp;''', (message_id,))
    results = psycopg2_cursor.fetchall()
    psycopg2_connection.close()
    return results

@app.route('/timestamped_verses/table/<int:message_id>', methods=['GET'])
def get_timestamped_verses_table(message_id):
    message_title = message_id_title(message_id)
    results = message_id_timestamped_verses(message_id)
    return render_template('timestamp_verse_table.html', message_id=message_id, message_title=message_title, results=results)
