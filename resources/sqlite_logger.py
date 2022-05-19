from __future__ import absolute_import, division, print_function, unicode_literals

import sqlite3
import logging
import time


INIT_SQL = """CREATE TABLE IF NOT EXISTS log(
                    TimeStamp TEXT,
                    Source TEXT,
                    LogLevel INT,
                    LogLevelName TEXT,
                    Message TEXT,
                    Args TEXT,
                    Module TEXT,
                    FuncName TEXT,
                    LineNo INT,
                    Exception TEXT,
                    Process INT,
                    Thread TEXT,
                    ThreadName TEXT
               )"""

INSERT_SQL = """INSERT INTO log(
                    TimeStamp,
                    Source,
                    LogLevel,
                    LogLevelName,
                    Message,
                    Args,
                    Module,
                    FuncName,
                    LineNo,
                    Exception,
                    Process,
                    Thread,
                    ThreadName
               )
               VALUES (
                    '%(dbtime)s',
                    '%(name)s',
                    %(levelno)d,
                    '%(levelname)s',
                    '%(msg)s',
                    '%(args)s',
                    '%(module)s',
                    '%(funcName)s',
                    %(lineno)d,
                    '%(exc_text)s',
                    %(process)d,
                    '%(thread)s',
                    '%(threadName)s'
               );
               """

def getLogLevel():
            f = open("log-level.txt", "r")
            firstline = f.readline().rstrip()
            if firstline == "INFO = False":
                #print("False")
                return False
            #print("True")
            return True

class SQLiteHandler(logging.Handler):
    """
    Thread-safe logging handler for SQLite.
    """

    def __init__(self, database='app.db'):
        logging.Handler.__init__(self)
        self.database = database
        conn = sqlite3.connect(self.database)
        conn.execute(INIT_SQL)
        conn.commit()

    def format_time(self, record):
        """
        Create a time stamp
        """
        record.dbtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(record.created))

    def emit(self, record):
        self.format(record)
        self.format_time(record)
        if record.exc_info:  # for exceptions
            record.exc_text = logging._defaultFormatter.formatException(record.exc_info)
            record.exc_text = record.exc_text.replace("'",'"')         ## added for fixing quotes causing error
        else:
            record.exc_text = ""

        # Insert the log record
        sql = INSERT_SQL % record.__dict__
        conn = sqlite3.connect(self.database)
        conn.execute(sql)
        conn.commit()  # not efficient, but hopefully thread-safe
        
def main():
    """ Main Method """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # sqlite handler
    

    # test
    logging.info('Start')
    logging.info('End')
    logging.error("Application error")