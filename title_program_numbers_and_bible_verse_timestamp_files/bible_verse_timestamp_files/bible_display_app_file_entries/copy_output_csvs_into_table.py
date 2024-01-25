import psycopg2
import os

def copy_contents_of_each_csv_in_directory_to_table(
        directory_of_csvs_full_path : str = '',
        host_of_database_cluster : str = '',
        port_of_database_cluster : int = 0,
        database_name_in_database_cluster : str = '',
        tablename_in_database_to_which_to_copy : str = ''
        ) -> None:
    '''
    I have not put any uniqueness contraints on table in database, so
    if any of the runs fail, I should `DELETE FROM tablename;` before beginning again.
    '''
    assert directory_of_csvs_full_path != ''
    assert host_of_database_cluster != ''
    assert port_of_database_cluster != 0
    assert database_name_in_database_cluster != ''
    assert tablename_in_database_to_which_to_copy != ''

    list_of_filenames_for_csvs_to_copy_into_table = os.listdir(directory_of_csvs_full_path)

    with open('password_file.txt') as password_file_object:
        password=password_file_object.read()

    psycopg2_connection = psycopg2.connect(f'dbname={database_name_in_database_cluster} '
                                           f'user=postgres ' # todo: take user as commandline argument?
                                           f'host={host_of_database_cluster} '
                                           f'port={port_of_database_cluster} '
                                           f'password={password} ')
    psycopg2_cursor = psycopg2_connection.cursor()

    for filename_for_csv_to_copy_into_table in list_of_filenames_for_csvs_to_copy_into_table:
        print(f'copying from {filename_for_csv_to_copy_into_table}')
        filename_for_csv_to_copy_into_table_full_path = os.path.join(directory_of_csvs_full_path, filename_for_csv_to_copy_into_table)
        # pass open(filename) b/c documentation says first argument is file-like object
        # psycopg2_cursor.copy_from(open(filename_for_csv_to_copy_into_table_full_path),
        #                           tablename_in_database_to_which_to_copy,
        #                           sep='|',
        #                           columns=('filename',
        #                                    'entry_date',
        #                                    'morning_or_night',
        #                                    'entry_timestamp',
        #                                    'book',
        #                                    'chapter',
        #                                    'verse')) # todo: take these column names as commandline argument?
        # ^ no mention of header or not. will this copy the header line into a row in table?
        # I may replace above call with a use of copy_expert so I can control the parameters like HEADER

        copy_command = f'COPY {tablename_in_database_to_which_to_copy} FROM STDIN WITH (FORMAT CSV, HEADER, DELIMITER \'|\')'
        print(copy_command)
        psycopg2_cursor.copy_expert(copy_command,
                                    open(filename_for_csv_to_copy_into_table_full_path))
        psycopg2_connection.commit() # not sure whether to commit per file or after all files

    #psycopg2_connection.commit()
    psycopg2_connection.close()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_directory_of_csvs_to_read_into_table_full_path')
    parser.add_argument('-w', '--host_on_which_postgres_cluster_running')
    parser.add_argument('-p', '--port_for_postgres_cluster_on_host')
    parser.add_argument('-d', '--database_name_in_postgres_cluster')
    parser.add_argument('-t', '--tablename_for_table_into_which_to_read_csvs')
    commandline_argument_namespace_object = parser.parse_args()
    input_directory_of_csvs_to_read_into_table_full_path = commandline_argument_namespace_object.input_directory_of_csvs_to_read_into_table_full_path
    host_on_which_postgres_cluster_running = commandline_argument_namespace_object.host_on_which_postgres_cluster_running
    port_for_postgres_cluster_on_host = commandline_argument_namespace_object.port_for_postgres_cluster_on_host
    database_name_in_postgres_cluster = commandline_argument_namespace_object.database_name_in_postgres_cluster
    tablename_for_table_into_which_to_read_csvs = commandline_argument_namespace_object.tablename_for_table_into_which_to_read_csvs
    copy_contents_of_each_csv_in_directory_to_table(
        directory_of_csvs_full_path=input_directory_of_csvs_to_read_into_table_full_path,
        host_of_database_cluster=host_on_which_postgres_cluster_running,
        port_of_database_cluster=int(port_for_postgres_cluster_on_host),
        database_name_in_database_cluster=database_name_in_postgres_cluster,
        tablename_in_database_to_which_to_copy=tablename_for_table_into_which_to_read_csvs
        )
