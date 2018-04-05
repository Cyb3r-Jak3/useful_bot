import sqlite3

connection = sqlite3.connect("comments.db")

cursor = connection.cursor()


def create():
    cursor.execute("""
CREATE TABLE IF NOT EXISTS Comments ( 
id char(11) NOT NULL DEFAULT '',
time timestamp NOT NULL,
subreddit text,
reply text,
PRIMARY KEY (id)); """)
    cursor.execute("""
CREATE TABLE IF NOT EXISTS Posts ( 
id char(11) NOT NULL DEFAULT '',
time timestamp NOT NULL,
subreddit text,
reply text
PRIMARY KEY (id)
);""")


def datainsert(choice, data):
    print(choice, "\n")
    print(data)
    for i in data:
        format_str = """ INSERT INTO {choice} (id, time, subreddit, reply) VALUES ({id}, {time}, {subreddit}, {reply}""".format(
            choice=choice, id=i[0], time=i[1], subreddit=i[2], reply=i[3])
        print(format_str)
        #cursor.execute(format_str)
        #connection.commit()


def datafecter(Table):
    cursor.execute("SELECT id FROM {table}".format(table=Table))
    result = cursor.fetchall()
    return list(result)
