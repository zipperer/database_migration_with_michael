#!/usr/bin/env bash

# example use: $ ./program_name.sh 3192

id=$1

NAME_OF_DOCKER_CONTAINER_RUNNING_POSTGRES=az_postgres_ubuntu1

docker exec $NAME_OF_DOCKER_CONTAINER_RUNNING_POSTGRES psql --username postgres --host localhost --port 5432 --dbname postgres --command "SELECT id, entry.entry_timestamp, entry.book, entry.chapter, entry.verse
FROM presentations_decoded_date
JOIN bible_display_app_file_entries_with_morning_or_night as entry ON presentations_decoded_date.presentation_date = entry.entry_date
WHERE presentations_decoded_date.morning_or_night = entry.morning_or_night AND
      id = ${id}
ORDER BY entry_timestamp;"


# example output:
# ./program_name.sh 3192
#  id  |   entry_timestamp   |      book      | chapter | verse 
#------+---------------------+----------------+---------+-------
# 3192 | 2014-01-05 00:01:49 | Romans         | 8       | 29
# 3192 | 2014-01-05 00:01:50 | Romans         | 8       | 29
# 3192 | 2014-01-05 00:01:54 | Romans         | 8       | 29
# 3192 | 2014-01-05 00:01:59 | Isaiah         | 46      | 10
