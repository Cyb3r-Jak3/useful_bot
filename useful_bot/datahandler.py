import sqlite3, string

import logmaker
connection = sqlite3.connect("data.db")

cursor = connection.cursor()


def create():

    command = """
CREATE TABLE IF NOT EXISTS Posts ( 
id text NOT NULL DEFAULT '',
time text NOT NULL,
subreddit text,
reply text,
PRIMARY KEY (id)
);"""
    cursor.execute(command)
    command = """
CREATE TABLE IF NOT EXISTS Comments ( 
id text NOT NULL DEFAULT '',
time text NOT NULL,
subreddit text,
reply text,
PRIMARY KEY (id)); """
    cursor.execute(command)


def datainsert(choice, data):
    logger = logmaker.makeLogger("Data")
    for i in data:
        # logger.debug(choice, str(data))
        format_str = """ INSERT OR IGNORE INTO {choice} (id, time, subreddit, reply) VALUES (?, ?, ?, ?)""".format(
            choice=choice)
        #logger.debug(format_str)
        try:
            cursor.execute(format_str, (i[0], i[1], i[2], i[3]))
            connection.commit()
        except Exception as e:
            logger.error(e)




def datafecter(Table):
    cursor.execute("SELECT id FROM {table}".format(table=Table))
    result = list(cursor.fetchall())
    result = "['%s']" % "', '".join([t[0] for t in result])
    return (result)

create()