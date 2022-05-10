""" SQL Connection """
import sqlite3
from sqlite3 import Error

def connect(db_file):
    """ create database connection to SQLite database """
    connection = None
    try:
        connection = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as err:
        print(err)
        return None

    return connection

def construct_table(connection, construct_table_sql):
    """ CREATE TABLE function """
    #create a table from the create_table_sql statement
    try:
        conn = connection.cursor()
        conn.execute(construct_table_sql)
        print("Success")
    except Error as err:
        print("ERORR: ")
        print(err)
        return False

    return True

def insert_setting(conn, setting):
    """ Insert setting """
    sql = ''' INSERT INTO SETTINGS(id,setting,state)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    try:
        cur.execute(sql, setting)
    except Error as err:
        print(err)
        return False

    conn.commit()

    return cur.lastrowid


def get_setting(conn, iden):
    """ get setting """
    sql = '''SELECT * FROM SETTINGS where id = ?'''
    cur = conn.cursor()
    ret = None
    try:
        ret = cur.execute(sql, (iden,))
    except Error as err:
        print(err)
        return False

    return ret


def delete_setting(conn, iden):
    """ delete setting """
    sql = '''DELETE FROM SETTINGS WHERE id = ?'''

    cursor = conn.cursor()

    try:
        cursor.execute(sql, (iden,))
    except Error as err:
        print(err)
        return False

    return True
