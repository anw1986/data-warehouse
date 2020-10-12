# Data Warehouse

## Introduction
A music streaming startup, Sparkify, has grown their user base and song database and want to move their processes and data onto the cloud. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

Developed an ETL pipeline that extracts their AWS S3, stages them in Redshift, and transforms data into a set of fact and dimensional tables to perform analytics 

## Main Processing Steps
* A **dwh-sample.cfg** file is provided. After pulling the repo, provide the following parameters in config file to run the **create_tables.py** **etl.py** : DB_HOST, ARN, AWS Key & Secret.
* Extract data from S3
* Stage them in Redshift
* Transform data into a set of dimensional tables (star schema) 

## Database Design
The database is designed using the Star Schema. The data after loading into the staging table is injested from the staging table to the target Fact and Dimension tables

| Fact Table | Dimension Table | 
|   :---:      |     :---:      |
| songplay_table   | song_table     |
|              | artist_table       |
|              | user_table       |
|              | time_table       | 

### Fact tables

It contains all the primary keys of the dimension and associated facts or measures(is a property on which calculations can be made) like quantity sold, amount sold and average sales.

#### Songplays

Records in log data associated with song plays .

|   Column    |  Type   |
| ----------- | --------|
| songplay_id | INT     |
| start_time  | VARCHAR |
| user_id     | INT     |
| level       | VARCHAR |
| song_id     | INT     |
| artist_id   | INT     | 
| session_id  | INT     |
| location    | VARCHAR | 
| user_agent  | VARCHAR | 

Primary key: songplay_id

### Dimension tables

Dimension tables provides descriptive information for all the measurements recorded in fact table.

#### Users

Users in the app.

|   Column   |  Type   | 
| ---------- | ------- | 
| user_id    | INT     | 
| first_name | VARCHAR | 
| last_name  | VARCHAR | 
| gender     | VARCHAR | 
| level      | VARCHAR | 

Primary key: user_id

#### Songs

Songs in music database.

|  Column   |  Type   | 
| --------- | ------- | 
| song_id   | VARCHAR | 
| title     | VARCHAR | 
| artist_id | VARCHAR | 
| year      | INT     | 
| duration  | FLOAT   | 

Primary key: song_id

#### Artists

Artists in music database.

|  Column   |  Type      |  
| --------- | ---------- | 
| artist_id | VARCHAR    | 
| name      | VARCHAR    | 
| location  | VARCHAR    | 
| latitude  | FLOAT      | 
| longitude | FLOAT      | 

Primary key: artist_id

#### Time

Timestamps of records in songplays broken down into specific units.

|   Column   |  Type     | 
| ---------- | --------- | 
| start_time | VARCHAR   | 
| hour       | VARCHAR   | 
| day        | VARCHAR   | 
| week       | VARCHAR   | 
| month      | VARCHAR   | 
| year       | VARCHAR   | 
| weekday    | VARCHAR   | 

## Running

To run the project locally, use pipenv to activate the virtual environment:

``` sh
pipenv shell
```

And run the scripts to create database tables. This creates both the staging and target tables:

``` sh
./create_tables.py
```

and populate data into staging and final tables:

``` sh
./etl.py
```

Data can be verified using the provided `etl-result.ipynb` jupyter notebook:

``` sh
etl-result.ipynb
```