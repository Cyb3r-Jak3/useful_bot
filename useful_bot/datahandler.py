import sqlite3

from useful_bot import logmaker
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
PRIMARY KEY (user));"""]
    for i in commands:
        cursor.execute(i)


def datainsert(Table, data):
    logger = logmaker.makeLogger("Data")
    if Table == "Blacklist":
        for i in data:
            format_str = """ INSERT OR IGNORE INTO {choice} (user, time, reason) VALUES (?, ?, ?)""".format(
                choice=Table)
            try:
                cursor.execute(format_str, (i[0], i[1], i[2]))
                connection.commit()
            except Exception as e:
                logger.error(e)
    else:
        for i in data:
            format_str = """ INSERT OR IGNORE INTO {choice} (id, time, subreddit, reply) VALUES (?, ?, ?, ?)""".format(
                choice=Table)
            try:
                cursor.execute(format_str, (i[0], i[1], i[2], i[3]))
                connection.commit()
            except Exception as e:
                logger.error(e)




def datafecter(Table, ident):
    cursor.execute("SELECT {ident} FROM {table}".format(table=Table, ident=ident))
    result = list(cursor.fetchall())
    result = "['%s']" % "', '".join([t[0] for t in result])
    return (result)

create()