import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    """Drops table in the data base"""
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """Create tables in the database"""
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    The main function calls the create_tables and drop_tables function
    The database parameters are in the config file and are used to connect to the database
    The connection (conn) and cursor (cur) are passed as parameters to the drop_table and create_table
    
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)
    
    conn.close()


if __name__ == "__main__":
    main()