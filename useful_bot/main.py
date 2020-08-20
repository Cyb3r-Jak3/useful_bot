"""Main file that runs the bot"""
#
# © Jacob White 2018 under MIT License
#
# External
import re
import datetime
import os
import sys
from sqlite3 import OperationalError
import praw

# Internal
import datahandler as dh
import logmaker
import botinfo
import downvote


# Ends the script and deletes log files if no errors occurred
def stop_bot(delete=False,) -> None:
    """
    Function that exits the bot
    Parameters
    ----------
    delete: bool
        If set to true it will remove the log file
    """
    logger.info("Shutting down")
    if delete:
        logger.info("Deleting log file")
        os.remove("bot.log")
    sys.exit(0)


def get_previous() -> (str, str, str):
    """
    Gets all the data from the previous run
    Returns
    -------

    """
    try:
        comments = dh.fetch("Comments", "id")
        posts = dh.fetch("Posts", "id")
        blacklist = dh.fetch("Blacklist", "user")
        blacklist.append("useful_bot")
        retrieved_mentions = dh.fetch("replied_mentions", "id")
        message_responses = dh.fetch("message_responses", "*")
        comments_triggers = dh.fetch("comment_responses", "*")
        post_triggers = dh.fetch("post_responses", "*")
    except Exception as err:
        logger.error("Error previous info from database: %s", err)
        stop_bot()
    return (
        comments,
        posts,
        blacklist,
        retrieved_mentions,
        message_responses,
        comments_triggers,
        post_triggers,
    )


def start() -> praw.Reddit():
    """
    Gets the Reddit() class based on botinfo or stored into in the database
    Returns
    -------
        The Reddit class that is used for operations
    """
    try:
        reddit_client = praw.Reddit(
            client_id=botinfo.client_id,
            client_secret=botinfo.client_secret,
            password=botinfo.password,
            username=botinfo.username,
            user_agent=botinfo.user_agent,
        )
        reddit_client.user.me()  # Verify log in, will raise exception if log in failed.
        logger.info("Successfully logged in")
        return reddit_client
    except AttributeError:  # AttributeError will occur if the values of botinfo do not exist
        try:  # Attempts to import credentials from the configurations table
            if dh.fetch("configurations", "remember") == "yes":
                try:
                    reddit_client = praw.Reddit(
                        client_id=dh.fetch("configurations", "client_id"),
                        client_secret=dh.fetch("configurations", "client_secret"),
                        password=dh.fetch("configurations", "password"),
                        username=dh.fetch("configurations", "username"),
                        user_agent=dh.fetch("configurations", "user_agent"),
                    )
                    reddit_client.user.me()
                    logger.info("Successfully logged in using the database")
                    return reddit_client
                except Exception as err:
                    logger.error("Error when trying to import credentials: %s", err)
                    stop_bot()
        except OperationalError:  # OperationalError will occur when nothing exists in the table
            logger.error(
                "There was an error trying to import the credentials."
                "This either means that it was never setup"
                " or there was actually an error.\n"
                "If you want to to be able to import credentials then add them from the cli"
            )
            stop_bot()
        except Exception as err:
            logger.error("There was an error when dealing with credentials: %s", err)
            stop_bot()


def post_reply(sreddit: praw.Reddit().subreddit) -> None:
    """
    Replies to posts in sreddit that meet the criteria
    Parameters
    ----------
    sreddit: str
        Name of the subreddit
    """
    logger.debug("Starting Posts")
    to_add = []
    for submission in sreddit.hot(
        limit=10
    ):  # Gets submissions from the subreddit. Here it has a limit of 10
        if submission.id not in posts_replied_to:
            for response in post_responses:
                if (re.search(response[0], submission.title, re.IGNORECASE)) and (
                    submission.author.name not in ignored
                ):  # If you wanted to have it search the body change submission.title to sub,
                    try:
                        submission.reply(reply_format(response[1], submission.author))
                        logger.debug("Bot replying to : %s", submission.title)
                        add = [
                            submission.id,
                            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            botinfo.subreddit,
                            response[1],
                        ]
                        to_add.append(add)
                        break
                    except Exception as err:
                        logger.warning(err)

    dh.insert("Posts", to_add)  # Adds all the posts that were replied to
    logger.info("Finished Posts")


def comment_reply(
    sreddit: praw.Reddit().subreddit,
) -> None:  # Looks through all comments in a post
    """
    Loops through all comments in a post
    Parameters
    ----------
    sreddit: praw.Reddit.subreddit()
        The subreddit to look through
    """
    logger.info("Starting Comments")
    to_add = []
    for post in sreddit.hot(limit=10):  # Gets the top 10 posts in the subreddit
        submission = reddit.submission(post)
        submission.comments.replace_more(limit=50)  # Gets 50 comments from each post
        for comment in submission.comments.list():
            text = comment.body
            author = comment.author.name
            for response in comment_responses:
                if (
                    (response[0] in text.lower())
                    and (comment.id not in comments_replied_to)
                    and (author.lower() not in ignored)
                ):
                    try:
                        add = [
                            comment.id,
                            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            response[1],
                            botinfo.subreddit,
                        ]
                        comment.reply(reply_format(response[1], author))
                        logger.debug("Bot replying to %s", text)
                        to_add.append(add)
                    except Exception as err:
                        logger.warning(err)

    dh.insert("Comments", to_add)  # Gets all the comments that were replied to
    logger.info("Finished Comments")


def reply_format(unformatted: str, author: str):
    """
    Adds the footer and formats the author name if in the unformatted text
    Parameters
    ----------
    unformatted: str
        The string to post
    author: str
        The author of the post or comment
    Returns
    -------
        String with footer added
    """
    if "{user}" in unformatted:
        unformatted = unformatted.format(user=author)
    formatted = unformatted + botinfo.footer
    return formatted


def message_check(additional: list):
    """
    Checks messages received
    Parameters
    ----------
    additional: list
        List of customer message triggers and responses
    """
    logger.info("Starting Messages")
    marked = []
    for message in reddit.inbox.unread():  # Gets all unread messages
        to_break = False
        received_subject = message.subject.lower()
        name = message.author.name.lower()
        if received_subject in ["stop", "ignore", "ignored"] and name not in ignored:
            data = [
                [
                    name,
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    message.body,
                ]
            ]
            logger.info("Ignoring user: %s", message.author.name)
            message_send(message.author.name, "Ignored add")
            dh.insert("ignored", data)
            marked.append(message)
        elif received_subject in ["resume", "unignore"] and name in ignored:
            dh.delete("ignored", "user", name)
            logger.info("Unignoring %s", message.author.name)
            message_send(message.author.name, "ignore remove")
            marked.append(message)
        for i, _ in enumerate(additional):  # Looks
            if additional[i][0] == received_subject:
                global ADDITIONAL_CHOICE  # pylint: disable=global-statement
                ADDITIONAL_CHOICE = i
                message_send(message.author.name, "additional")
                to_break = True
                marked.append(message)
        if to_break:
            break
        # Username mentions appear in the inbox so this filters them out
        if received_subject != "username mention":
            logger.warning(
                "Message with subject and body not understood. Subject: %s Body: %s",
                message.subject,
                message.body,
            )
            message_send(message.author.name, "unknown")
            marked.append(message)
    reddit.inbox.mark_read(marked)
    logger.info("Finished Messages")


def message_send(user: str, kind: str) -> None:
    """
    Sends messages to users
    Parameters
    ----------
    user: str
        The name of the user who the message will be sent to
    kind: str
        The type of message to be sent
    """
    # pylint: disable=line-too-long
    logger.debug("Sending %s message to %s", kind, user)
    if kind == "Ignored add":
        subject = "Successfully ignored"
        message = (
            "Hello {user},  \n"
            "  This is a message confirming that you have been added to /u/useful_bot's ignore list.  \n"
            " If you still receive replies for me please send me a message. ".format(
                user=user
            )
        )
    elif kind == "Ignored remove":
        subject = "Successfully removed from ignored list"
        message = (
            "Hello {user},  \n "
            "This message is confirming that you have been removed from /u/useful_bot's ignored list.  \n "
            "If you feel that this message was a mistake or you would like to remain on the ignored list then "
            "reply stop".format(user=user)
        )
    elif kind == "additional":
        subject = additional_responses[ADDITIONAL_CHOICE][1]
        message = additional_responses[ADDITIONAL_CHOICE][2]
    else:
        subject = "Message Unknown"
        message = (
            "Hello {user},  \n"
            "This message is being sent to you because you have sent me a message that I am unsure how to deal with it. "
            " \nRest assure this has been recorded and a solution should be in progress. Thanks ".format(
                user=user
            )
        )
    reddit.redditor(user).message(subject, message)


def find_mentions() -> None:
    """
    Find bot name mentions and responds with a comment
    """
    logger.info("Starting Mentions")
    to_add = []
    for message in reddit.inbox.mentions():
        # Needs the mentions database because I was unable to mark them as read
        # with praw
        if str(message) not in mentions:
            try:
                logger.debug(
                    "Found mention %s, User: %s, Body: %s",
                    message,
                    message.author,
                    message.body,
                )
                message.reply("Hello, I see you mentioned me. How can I help?")
                logger.debug("Replying to %s", message)
                marked = [
                    message.id,
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                ]
                to_add.append(marked)
            except Exception as err:
                logger.warning(err)
    dh.insert("replied_mentions", to_add)
    logger.info("Finished mentions")


if __name__ == "__main__":
    logger = logmaker.make_logger("Main")
    dh.create()
    logger.info("Starting up")
    reddit = start()
    SUBREDDIT_CHOICE = botinfo.subreddit
    subreddit = reddit.subreddit(botinfo.subreddit)
    # Gets all the data from the database
    (
        comments_replied_to,
        posts_replied_to,
        ignored,
        mentions,
        additional_responses,
        comment_responses,
        post_responses,
    ) = get_previous()
    ADDITIONAL_CHOICE = None
    message_check(additional_responses)
    post_reply(subreddit)
    comment_reply(subreddit)
    find_mentions()
    downvote.downvoted_remover(reddit)
    stop_bot(True)
