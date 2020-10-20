import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    """Function used to injest data in the staging table"""
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    """Function used to injest data into the fact and dimension table from the staging table"""
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    The main function calls the load_staging_tables and insert_tables function
    The database parameters are in the config file and are used to connect to the database
    The connection (conn) and cursor (cur) are passed as parameters to the load_staging_tables and insert_tables function
    Data is then populated into the staging tables and then the target tables

    """

    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()