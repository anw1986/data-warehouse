# Data Warehouse

## Introduction
A music streaming startup, Sparkify, has grown their user base and song database and want to move their processes and data onto the cloud. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

Developed an ETL pipeline that extracts their AWS S3, stages them in Redshift, and transforms data into a set of fact and dimensional tables to perform analytics 

## Main Processing Steps
* A **dwh-sample.cfg** file is provided. After pulling the repo provide the following parameters in config file to run the **create_tables.py** **etl.py** DB_HOST, ARN, AWS Key & Secret.
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