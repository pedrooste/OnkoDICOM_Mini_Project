"""This document is to test the CRUD operations on the DB"""
from sqliteconnection import connect, construct_table, insert_setting, get_setting, delete_setting

# Import the test framework (this is a hypothetical module)

# This is a generalized example, not specific to a test framework
def test_connection():
    """ Test connection """
    assert connect("pythonsqlite.db") is not None

def test_droptable():
    """ Test drop table """
    conn = connect("pythonsqlite.db")
    conn.cursor().execute("DROP TABLE SETTINGS")

def test_createtable():
    """ Create Table test """
    conn = connect("pythonsqlite.db")

    table = """CREATE TABLE IF NOT EXISTS SETTINGS (
                                    id integer PRIMARY KEY,
                                    setting text NOT NULL,
                                    state integer NOT NULL
                                );"""

    assert construct_table(conn, table)

def test_insertentry():
    """ Insert Entry Test """
    conn = connect("pythonsqlite.db")

    setting = (1, "Setting one: ", 0)
    setting2 = (1, "Setting one: ", 1)

    assert insert_setting(conn, setting) == 1
    assert insert_setting(conn, setting2) is False

def test_get_setting():
    """ Get Setting Test (single) """
    conn = connect("pythonsqlite.db")

    iden = 1

    assert get_setting(conn, iden) is not None


def test_delete():
    """ Delete setting test """
    conn = connect("pythonsqlite.db")

    assert delete_setting(conn, 1)
