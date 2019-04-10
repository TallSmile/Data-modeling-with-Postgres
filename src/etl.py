import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    '''
    Processes provided song JSON file and inserts relevant data into the database.
    '''   
    # open song file
    df = pd.read_json(filepath, lines= True)

    # insert artist record
    artist_data = [ list(row) for row in df.loc[:, ['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']].itertuples(index=False)]
    
    for artist in artist_data:
        cur.execute(artist_table_insert, artist)

    # insert song record
    song_data = [ list(row) for row in df.loc[:, ['song_id', 'title', 'artist_id', 'year', 'duration']].itertuples(index=False)]
    
    for song in song_data:
        cur.execute(song_table_insert, song)
    


def process_log_file(cur, filepath):
    '''
    Processes provided log JSON file and inserts relevant data into the database.
    '''   
    # open log file
    df = pd.read_json(filepath, lines= True)

    # filter by NextSong action
    df = df[df.page == 'NextSong']

    # convert timestamp column to datetime
    t = pd.to_datetime(df["ts"], unit='ms')
    
    # insert time data records
    time_data = time_data = (t, t.dt.hour, t.dt.day, t.dt.weekofyear, t.dt.month, t.dt.year, t.dt.weekday)
    column_labels = ('timestamp', 'hour', 'day', 'week', 'month', 'year', 'weekday')

    time_df = pd.DataFrame(dict(zip(column_labels, time_data))).drop_duplicates()

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df.loc[:, ['userId' ,'firstName', 'lastName', 'gender', 'level']].drop_duplicates()

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        #print("Searching for {}, {}, {}".format(row.song, row.artist, row.length))
        results = cur.execute(song_select, (row.song, row.artist, row.length))
        songid, artistid = results if results else None, None
        # if artistid is not None:
        #     print("Found {}, {}".format(songid,artistid))
        # insert songplay record
        songplay_data = (pd.to_datetime(row['ts'], unit ='ms'), row['userId'], row['level'], songid, artistid, row['sessionId'], row['userAgent'])
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    '''
    Processes all song and log JSON files and inserts relevant data into the database.
    '''   
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    with psycopg2.connect("host=postgresDb dbname=sparkifydb user=student password=student") as conn:
        with conn.cursor() as cur:

            process_data(cur, conn, filepath='/data/song_data', func=process_song_file)
            process_data(cur, conn, filepath='/data/log_data', func=process_log_file)



if __name__ == "__main__":
    main()