# Data modeling and ETL with Postgres

a Postgres database with tables designed to optimize queries on song play analysis.

## Schema for Song Play Analysis

Using the song and log datasets, you'll need to create a star schema optimized for queries on song play analysis. This includes the following tables.

### Fact Table

* **songplays** - records in log data associated with song plays i.e. records with page NextSong
  * songplay_id (PK)
  * start_time (FK)
  * user_id (FK)
  * level
  * song_id (FK)
  * artist_id (FK)
  * session_id (FK)
  * location
  * user_agent

### Dimension Tables

* **users** - users in the app
  * user_id (PK)
  * first_name
  * last_name
  * gender
  * level
* **songs** - songs in music database
  * song_id (PK)
  * title
  * artist_id (FK)
  * year
  * duration
* a**rtists** - artists in music database
  * artist_id (PK)
  * name
  * location
  * lattitude
  * longitude
* **time** - timestamps of records in songplays broken down into specific units
  * start_time (PK)
  * hour
  * day
  * week
  * month
  * year
  * weekday