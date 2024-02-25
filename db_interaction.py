import sqlite3
import LOGGER

with sqlite3.connect("appdata.db") as adb: cursor = adb.cursor()

def init():
    try:
        cursor.execute(""" CREATE TABLE channels 
                                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                channel_name TEXT,
                                osu_id INTEGER,
                                request_bot INTEGER,
                                rs_command INTEGER)""")

        cursor.execute(""" CREATE TABLE logs 
                                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        date TEXT,
                                        channel TEXT,
                                        author TEXT,
                                        msg TEXT)""")

        LOGGER.log("Channels db created!")
    except sqlite3.OperationalError:
        LOGGER.log("Channels db already exist")


    try:
        cursor.execute(""" CREATE TABLE logs 
                                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        date TEXT,
                                        channel TEXT,
                                        author TEXT,
                                        msg TEXT)""")

        LOGGER.log("Logs db created!")
    except sqlite3.OperationalError:
        LOGGER.log("Logs db already exist")


def add_data(channel_name, osu_id):
    sql = "INSERT INTO channels (channel_name, osu_id) VALUES (?, ?)"
    cursor.execute(sql, [channel_name, osu_id])
    adb.commit()


def add_log(date, channel, author, msg):
    sql = "INSERT INTO logs (date, channel, author, msg) VALUES (?, ?, ?, ?)"
    cursor.execute(sql, [date, channel, author, msg])
    adb.commit()


def get_users():
    cursor.execute("SELECT * FROM channels")
    return cursor.fetchall()
