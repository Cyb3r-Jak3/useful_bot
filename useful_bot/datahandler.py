# External
import sqlite3
# Internal
import logmaker

connection = sqlite3.connect("data.db")
cursor = connection.cursor()


def create():
    commands = ["""
CREATE TABLE IF NOT EXISTS Posts (
id text NOT NULL DEFAULT '',
time text NOT NULL,
subreddit text,
reply text,
PRIMARY KEY (id)
);""", """
CREATE TABLE IF NOT EXISTS Comments (
id text NOT NULL DEFAULT '',
time text NOT NULL,
subreddit text,
reply text,
PRIMARY KEY (id)); """, """
CREATE TABLE IF NOT EXISTS Blacklist (
user text NOT NULL DEFAULT '',
time text,
reason NULL,
PRIMARY KEY (user));""", """
CREATE TABLE IF NOT EXISTS replied_mentions (
id text NOT NULL DEFAULT '',
time text,
PRIMARY KEY (id));""", """
CREATE TABLE IF NOT EXISTS configurations (
id text NOT NULL DEFAULT '',
value text);""", """
CREATE TABLE IF NOT EXISTS message_responses (
keyword text NOT NULL DEFAULT '',
reply_subject text,
reply_message text);"""]
    for i in commands:
        cursor.execute(i)


def insert(table, data):
    logger = logmaker.make_logger("Data")
    if table == "Blacklist":
        for i in data:
            format_str = """ INSERT OR IGNORE INTO {choice} (user, time, reason) VALUES (?, ?, ?)""".format(
                choice=table)
            try:
                cursor.execute(format_str, (i[0], i[1], i[2]))
                connection.commit()
            except Exception as e:
                logger.error(e)
    elif table == "replied_mentions":
        for i in data:
            format_str = """ INSERT OR IGNORE INTO {choice} (id, time) VALUES (?, ?)""".format(
                choice=table)
            try:
                cursor.execute(format_str, (i[0], i[1]))
                connection.commit()
            except Exception as e:
                logger.error(e)
    elif table == "configurations":
        for i in data:
            format_str = """ INSERT OR IGNORE INTO {choice} (id, value) VALUES (?, ?)""".format(
                choice=table)
            try:
                cursor.execute(format_str, (i[0], i[1]))
                connection.commit()
            except Exception as e:
                logger.error(e)
    elif table == "message_responses":
        for i in data:
            format_str = """ INSERT OR IGNORE INTO {choice} (keyword, reply_subject, reply_message) VALUES (?, ?, ?)""".format(
                choice=table)
            try:
                cursor.execute(format_str, (i[0], i[1], i[2]))
                connection.commit()
            except Exception as e:
                logger.error(e)
    else:
        for i in data:
            format_str = """ INSERT OR IGNORE INTO {choice} (id, time, subreddit, reply) VALUES (?, ?, ?, ?)""".format(
                choice=table)
            try:
                cursor.execute(format_str, (i[0], i[1], i[2], str(i[3])))
                connection.commit()
            except Exception as e:
                logger.error(e)


def fetch(table, ident):
    cursor.execute(
        "SELECT {ident} FROM {table}".format(
            table=table, ident=ident))
    fetched = cursor.fetchall()
    if ident == "*":
        result = fetched
    else:
        result = []
        for i in range(len(fetched)):
            result.append(fetched[i][0])
    return result


def delete(table, choice, ident):
    command = (
        "DELETE FROM {table} WHERE {choice}={ident}".format(
            table=table,
            choice=choice,
            ident=ident))
    cursor.execute(command)
    connection.commit()


def table_fetch():
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    result = []
    for i in range(len(tables)):
        result.append(tables[i][0])
    return result
