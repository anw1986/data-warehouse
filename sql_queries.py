import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events_log"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplay_table"
user_table_drop = "DROP TABLE IF EXISTS user_table"
song_table_drop = "DROP TABLE IF EXISTS song_table"
artist_table_drop = "DROP TABLE IF EXISTS artist_table"
time_table_drop = "DROP TABLE IF EXISTS time_table"

# CREATE TABLES

staging_events_table_create= ("""
    CREATE TABLE staging_events_log(
    artist                  VARCHAR,
    auth                    VARCHAR,
    firstName               VARCHAR,              
    gender                  VARCHAR,
    itemInSession           INTEGER,
    lastName                VARCHAR,
    length                  FLOAT,
    level                   VARCHAR,
    location                VARCHAR,
    method                  VARCHAR,
    page                    VARCHAR,
    registration            FLOAT,
    sessionId               INTEGER,
    song                    VARCHAR,
    status                  INTEGER,
    ts                      TIMESTAMP,
    userAgent               VARCHAR,
    userId                  INTEGER
);
""")

staging_songs_table_create = ("""
    CREATE TABLE staging_songs(
        num_songs           INTEGER,
        artist_id           VARCHAR,
        artist_latitude     FLOAT,
        artist_longitude    FLOAT,
        artist_location     VARCHAR,
        artist_name         VARCHAR,
        song_id             VARCHAR,
        title               VARCHAR,
        duration            FLOAT,
        year                INTEGER
    );
""")

songplay_table_create = ("""
    CREATE TABLE songplay_table(
        songplay_id     INT IDENTITY(0,1) PRIMARY KEY, 
        start_time      VARCHAR, 
        user_id         INTEGER, 
        level           VARCHAR, 
        song_id         VARCHAR, 
        artist_id       VARCHAR, 
        session_id      INTEGER, 
        location        VARCHAR, 
        user_agent      VARCHAR
    );
""")

user_table_create = ("""
    CREATE TABLE user_table(
        user_id     INTEGER PRIMARY KEY, 
        first_name  VARCHAR, 
        last_name   VARCHAR, 
        gender      VARCHAR, 
        level       VARCHAR
    );
""")

song_table_create = ("""
    CREATE TABLE song_table(
        song_id     VARCHAR PRIMARY KEY, 
        title       VARCHAR, 
        artist_id   VARCHAR, 
        year        INT,
        duration    FLOAT
    );
""")

artist_table_create = ("""
    CREATE TABLE artist_table(
        artist_id   VARCHAR PRIMARY KEY,
        name        VARCHAR, 
        location    VARCHAR, 
        latitude    FLOAT, 
        longitude   FLOAT
    );
""")

time_table_create = ("""
    CREATE TABLE time_table(
        start_time      TIMESTAMP PRIMARY KEY,
        time_hour       INTEGER, 
        time_day        INTEGER, 
        time_week       INTEGER, 
        time_month      INTEGER, 
        time_year       INTEGER, 
        time_weekday    INTEGER
    );
""")

# STAGING TABLES

staging_events_copy = ("""
    copy staging_events_log 
    from {} \
    iam_role {}\
    FORMAT AS json {}\
    TIMEFORMAT 'epochmillisecs';
""").format(config['S3']['LOG_DATA'],config['IAM_ROLE']['ARN'],config['S3']['LOG_JSONPATH'])

staging_songs_copy = ("""
    copy staging_songs 
    from {} \
    iam_role {}
    json 'auto';
""").format(config['S3']['SONG_DATA'],config['IAM_ROLE']['ARN'])

# FINAL TABLES

songplay_table_insert = ("""
    INSERT INTO songplay_table (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent) SELECT ts, userId, level, song_id, artist_id, sessionId, location, userAgent FROM staging_events_log se, staging_songs ss 
    WHERE se.page='NextSong' 
    AND se.song = ss.title
    AND se.artist = ss.artist_name
    AND se.length = ss.duration
""")

user_table_insert = ("""
    INSERT INTO user_table SELECT DISTICT userId, firstName, lastName, gender, level FROM staging_events_log
""")

song_table_insert = ("""
    INSERT INTO song_table SELECT DISTICT song_id, title, artist_id, year, duration FROM staging_songs
""")

artist_table_insert = ("""
    INSERT INTO artist_table SELECT DISTICT artist_id, artist_name, artist_location, artist_latitude, artist_longitude FROM staging_songs
""")

time_table_insert = ("""
    INSERT INTO time_table SELECT DISTICT ts, EXTRACT(HOUR FROM ts), EXTRACT(DAY FROM ts), EXTRACT(WEEK FROM ts), EXTRACT(MONTH FROM ts), EXTRACT(YEAR FROM ts), EXTRACT(dayofweek FROM ts) FROM staging_events_log
""")

# QUERY LISTS
# Create and Drop table queries are imported in create_tables.py file
create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]

# these queries are imported in the etl.py file
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
