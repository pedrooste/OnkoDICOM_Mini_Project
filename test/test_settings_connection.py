"""This document is to test the CRUD operations on the DB Settings"""
from resources.settings import Settings
from resources.settings_connection import connect, construct_table, SettingsConnection


def test_connection():
    """ Test connection to DB """
    assert connect("pythonsqlite.db") is not None


def test_droptable():
    """ Test drop table Settings """
    conn = SettingsConnection()
    conn.connection.cursor().execute("DROP TABLE SETTINGS")


def test_createtable():
    """ Create Table Settings test """
    conn = SettingsConnection()

    table = """CREATE TABLE IF NOT EXISTS SETTINGS (
                                   user_id integer PRIMARY KEY,
                                   window_x integer,
                                   window_y integer,
                                   force_open bool,
                                   dicom_path varchar
                               );"""

    assert construct_table(conn.connection, table)


def test_insert_and_update_entry():
    """ Insert settings Test """
    conn = SettingsConnection()

    setting = Settings(1, 500, 600, True, 'path')
    setting2 = Settings(1, 700, 800, False, 'path2')

    assert conn.insert_or_update_setting(setting) == 1
    conn.insert_or_update_setting(setting2)
    assert conn.get_setting(1) == (1, 700, 800, False, 'path2')


def test_get_setting():
    """ Get Setting Test """
    conn = SettingsConnection()
    assert conn.get_setting(1) == (1, 700, 800, False, 'path2')
    assert conn.get_setting(2) is None


def test_delete():
    """ Delete setting test """
    conn = SettingsConnection()

    assert conn.delete_setting(1)
    assert conn.get_setting(1) is None
