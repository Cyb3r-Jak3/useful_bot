"""Deals with all database transactions"""
# External
import sqlite3

# Internal
import logmaker

connection = sqlite3.connect("data.db")
cursor = connection.cursor()
logger = logmaker.make_logger("DataHandler")


def create() -> None:
    """
    Creates all the tables in the database.
    Runs every time because tables will not be created if they exist
    """
    tables = [
        """
CREATE TABLE IF NOT EXISTS Posts (
id text NOT NULL DEFAULT '',
time text NOT NULL,
subreddit text,
reply text,
PRIMARY KEY (id)
);""",
        """
CREATE TABLE IF NOT EXISTS Comments (
id text NOT NULL DEFAULT '',
time text NOT NULL,
subreddit text,
reply text,
PRIMARY KEY (id)); """,
        """
CREATE TABLE IF NOT EXISTS ignored (
user text NOT NULL DEFAULT '',
time text,
reason NULL,
PRIMARY KEY (user));""",
        """
CREATE TABLE IF NOT EXISTS replied_mentions (
id text NOT NULL DEFAULT '',
time text,
PRIMARY KEY (id));""",
        """
CREATE TABLE IF NOT EXISTS configurations (
id text NOT NULL DEFAULT '',
value text);""",
        """
CREATE TABLE IF NOT EXISTS message_responses (
keyword text NOT NULL DEFAULT '',
reply_subject text,
reply_message text);""",
        """
CREATE TABLE IF NOT EXISTS comment_responses (
keyword text NOT NULL DEFAULT '',
reply_message text);""",
        """
CREATE TABLE IF NOT EXISTS post_responses (
keyword text NOT NULL DEFAULT '',
reply_message text);""",
    ]
    for table in tables:
        cursor.execute(table)


def insert(table: str, data: list) -> None:
    """
    Add data to the database
    Parameters
    ----------
    table: str
        Name of the table to add data to
    data: list
        List of lists of the data to be added. Each sublist is a new entry

    Returns
    -------
    """
    for item in data:
        if table == "ignored":
            format_str = """ INSERT OR IGNORE INTO ignored (user, time, reason)
                        VALUES (?, ?, ?)"""
        elif table == "replied_mentions":
            format_str = """ INSERT OR IGNORE INTO replied_mentions (id, time)
                VALUES (?, ?)"""
        elif table == "configurations":
            format_str = """ INSERT OR IGNORE INTO configurations (id, value)
             VALUES (?, ?)"""
        elif table == "message_responses":
            format_str = """ INSERT OR IGNORE INTO message_responses
            (keyword, reply_subject, reply_message)
            VALUES (?, ?, ?)"""
        elif table in ["post_responses", "comment_responses"]:
            format_str = """ INSERT OR IGNORE INTO {choice} (keyword, reply_message)
            VALUES (?, ?)""".format(
                choice=table
            )
        else:
            format_str = """ INSERT OR IGNORE INTO {choice}
            (id, time, subreddit, reply) VALUES (?, ?, ?, ?)""".format(
                choice=table
            )
        try:
            cursor.execute(format_str, *item)
            connection.commit()
        except sqlite3.OperationalError as err:
            logger.error(err)


def fetch(table: str, column: str) -> [list]:  # Gets the data from the database
    """
    Gets data from the database
    Parameters
    ----------
    table: str
        Name of the table to query
    column: str
        Name of to get results from

    Returns
    -------
        Returns a list of the contents
    """
    cursor.execute(  # nosec
        "SELECT {ident} FROM {table}".format(table=table, ident=column)
    )
    fetched = cursor.fetchall()
    # This means that you want all the information from the table
    if column == "*":
        result = fetched
    # Stuff like post and comment ids only need the actual id which is the first value stored.
    else:
        result = []
        for i, _ in enumerate(fetched):
            # Gets all the first values and makes them into a list
            result.append(fetched[i][0])
    return result


def delete(table: str, choice: str, ident: str) -> None:
    """
    Deletes a row from the database
    Parameters
    ----------
    table: str
        Table to delete the row from
    choice: str
        The column that will contain the ident value
    ident: str
        The value that will in choice to indicate the row to delete
    """
    command = "DELETE FROM {table} WHERE {choice}={ident}".format(  # nosec
        table=table, choice=choice, ident=ident
    )
    cursor.execute(command)
    connection.commit()


def table_fetch() -> list:
    """
    Gets all the tables in the database
    Returns
    -------
        List that contains the table names
    """
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    result = []
    for i, _ in enumerate(tables):
        result.append(tables[i][0])
    return result
