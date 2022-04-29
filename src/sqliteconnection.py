import sqlite3
from sqlite3 import Error

def connect(db_file):
    """ create database connection to SQLite database """
    connection = None
    try:
        connection = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)

    return connection
    
def construct_table(connection, construct_table_sql):
    #create a table from the create_table_sql statement
    try:
        c = connection.cursor()
        c.execute(construct_table_sql)
    except Error as e:
        print(e)



