import psycopg2
import os

#app_user is login info for normal user, they can only select, insert, delete rows from table
host = 'localhost' #172.16.37.250 - for ramy
dbname = 'postgres'
user = 'postgres' #, postgres
port = 5432

def connection(password):
    try:
        conn = psycopg2.connect(
            host = host,
            dbname = dbname,
            user = user,
            password = password,
            port = port
        )

        # this low diffs the error: 
        # current transaction is aborted, commands ignored until end of transaction block
        conn.autocommit = True 
        
        return conn

    except Exception as error:
        print(error)
        return None

