""" Maintains and returns settings functionality """
import os
import logging
import sqlite3
from sqlite3 import Error

LOG_FILES_DIR = 'logs'
if not os.path.isdir(LOG_FILES_DIR):
    os.makedirs(LOG_FILES_DIR)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s.%(msecs)03d %(levelname)s:%(name)s:%(message)s')
file_handler = logging.FileHandler('logs/settings_connection.log', mode='w')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def connect(db_file):
    """ create database connection to SQLite database """
    connection = None
    try:
        connection = sqlite3.connect(db_file)
        logger.info(sqlite3.version)
    except Error as err:
        logger.warning("Cannot connect to DB: %s", err)
        return None

    return connection


def construct_table(connection, construct_table_sql):
    """ CREATE TABLE function """
    # create a table from the create_table_sql statement
    try:
        conn = connection.cursor()
        conn.execute(construct_table_sql)
        logger.info("Settings table constructed")
    except Error as err:
        logger.warning("Could not construct settings table: %s", err)
        return False

    return True


class SettingsConnection:
    """Maintains DB conection and actions for settings"""

    def __init__(self):
        self.connection = connect("pythonsqlite.db")

        # constructing settings
        construct_table(self.connection,
                        """CREATE TABLE IF NOT EXISTS SETTINGS (
                                   user_id integer PRIMARY KEY,
                                   window_x integer,
                                   window_y integer,
                                   force_open bool,
                                   dicom_path varchar
                               );""")

    def insert_setting(self, settings):
        """ Insert setting """
        sql = '''INSERT INTO SETTINGS(user_id,window_x,window_y,force_open,dicom_path)VALUES(?,?,?,?,?)'''
        cur = self.connection.cursor()
        try:
            cur.execute(sql,
                        [settings.user_id, settings.window_x, settings.window_y, settings.force_open,
                         settings.dicom_path])
        except Error as err:
            logger.warning("Could not insert settings: %s", err)
            return False

        self.connection.commit()

        return cur.lastrowid

    def get_setting(self, user_id):
        """ get setting """
        sql = '''SELECT * FROM SETTINGS where user_id = ?'''
        cur = self.connection.cursor()
        try:
            ret = cur.execute(sql, (user_id,)).fetchone()
        except Error as err:
            logger.warning("Could not get settings: %s", err)
            return False

        return ret

    def delete_setting(self, iden):
        """ delete setting """
        sql = '''DELETE FROM SETTINGS WHERE user_id = ?'''

        cursor = self.connection.cursor()

        try:
            cursor.execute(sql, (iden,))
        except Error as err:
            logger.warning("Could not delete settings: %s", err)
            return False

        self.connection.commit()
        return True
