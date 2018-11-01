#
# © Jacob White 2018 under MIT License
#
# External
import praw
import re
import datetime
import os
import sys
from sqlite3 import OperationalError
# Internal
import datahandler as dh
import logmaker
import botinfo
import downvote


def stopbot(delete=False):  # Ends the script and deletes log files if no errors occurred
    logger.info("Shutting down")
    if delete:
        logger.info("Deleting log file")
        os.remove("bot.log")
    sys.exit(0)


def getprevious():  # This just goes through and get all the data
    try:
        comments = dh.fetch("Comments", "id")
    except Exception as e:
        logger.error("Error getting comment ids: {}".format(e))
        stopbot()
    try:
        posts = dh.fetch("Posts", "id")
    except Exception as e:
        logger.error("Error getting post ids: {}".format(e))
        stopbot()
    try:
        blacklist = dh.fetch("Blacklist", "user")
        blacklist.append("useful_bot")
    except Exception as e:
        logger.error("Error getting blacklisted users: ".format(e))
        stopbot()
    try:
        retrieved_mentions = dh.fetch("replied_mentions", "id")
    except Exception as e:
        logger.error("Error getting mentions: ".format(e))
        stopbot()
    try:
        message_responses = dh.fetch("message_responses", "*")
    except Exception as e:
        logger.error("Error getting message responses: {}".format(e))
        stopbot()
    try:
        comments_triggers = dh.fetch("comment_responses", "*")
    except Exception as e:
        logger.error("Error getting comment responses: {}".format(e))
    try:
        post_triggers = dh.fetch("post_responses", "*")
    except Exception as e:
        logger.error("Error getting post responses: {}".format(e))

    # If using Pycharm says references before assignment but the script will
    # stop before that
    return comments, posts, blacklist, retrieved_mentions, message_responses, comments_triggers, post_triggers


def start():  # Logging in
    try:
        r = praw.Reddit(
            client_id=botinfo.client_id,
            client_secret=botinfo.client_secret,
            password=botinfo.password,
            username=botinfo.username,
            user_agent=botinfo.user_agent)
        r.user.me()  # Verify log in, will raise exception if log in failed.
        logger.info("Successfully logged in")
        return r
    except AttributeError as ae:  # AttributeError will occur if the values of botinfo do not exist
        try:  # Attempts to import credentials from the configurations table
            if dh.fetch("configurations", "remember") == "yes":
                needed = [
                    "client_id",
                    "client_secret",
                    "password",
                    "username",
                    "user_agent"]
                imports = []
                for i in needed:
                    imports.append(dh.fetch("configurations", i))
                try:
                    r = praw.Reddit(
                        client_id=imports[0],
                        client_secret=imports[1],
                        password=imports[2],
                        username=imports[3],
                        user_agent=imports[4])
                    r.user.me()
                    logger.info("Successfully logged in")
                except Exception as e:
                    logger.error(
                        "Error when trying to import credentials: {}".format(e))
                    stopbot()
        except OperationalError as oe:  # OperationalError will occur when nothing exists in the table
            logger.error(
                "There was an error trying to import the credentials. This either means that it was never setup"
                " or there was actually an error.\nIf you want to to be able to import credentials then add them from the cli")
            stopbot()
        except Exception as e:  # General Exception
            logger.error(
                "There was an error when dealing with credentials: {}".format(e))
            stopbot()


# Replies to posts that have the words in the title.
def post_reply(subreddit):
    logger.info("Starting Posts")
    toadd = []
    for submission in subreddit.hot(
            limit=10):  # Gets submissions from the subreddit. Here it has a limit of 10
        if submission.id not in posts_replied_to:
            for response in post_responses:
                if (re.search(response[0], submission.title, re.IGNORECASE)) and (
                        submission.author.name not in blacklisted):  # If you wanted to have it search the body change submission.title to sub,
                    try:
                        submission.reply(
                            reply_format(
                                response[1],
                                submission.author))
                        add.append(
                            )
                        logger.debug(
                            "Bot replying to : {0}".format(
                                submission.title))
                        add = [submission.id, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), botinfo.subreddit, response[1]]
                        toadd.append(add)
                        break
                    except Exception as e:
                        logger.warn(e)

    dh.insert("Posts", toadd)  # Adds all the posts that were replied to
    logger.info("Finished Posts")


def comment_reply(subreddit):  # Looks through all comments in a post
    logger.info("Starting Comments")
    toadd = []
    for post in subreddit.hot(
            limit=10):  # Gets the top 10 posts in the subreddit
        submission = reddit.submission(post)
        submission.comments.replace_more(
            limit=50)  # Gets 50 comments from each post
        for comment in submission.comments.list():
            text = comment.body
            author = comment.author.name
            for response in comment_responses:
                if (response[0] in text.lower()) and (
                        comment.id not in comments_replied_to) and (author.lower() not in blacklisted):
                    try:
                        add = [comment.id, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), response[1], botinfo.subreddit]
                        comment.reply(reply_format(response[1], author))
                        logger.debug("Bot replying to {0}".format(text))
                        toadd.append(add)
                    except Exception as e:
                        logger.warn(e)

    dh.insert("Comments", toadd)  # Gets all the comments that were replied to
    logger.info("Finished Comments")


# Adds the footer and formats author name if needed
def reply_format(unformatted, author):
    if "{user}" in unformatted:
        unformatted = unformatted.format(user=author)
    formatted = unformatted + botinfo.footer
    return formatted


def message_check(additional):  # Checks to see if there are messages
    logger.info("Starting Messages")
    marked = []
    for x in reddit.inbox.unread():  # Gets all unread messages
        to_break = False
        received_subject = x.subject.lower()
        name = x.author.name.lower()
        if (("stop" == received_subject) or ("blacklist" ==
                                             received_subject)) and name not in blacklisted:
            data = [[name, datetime.datetime.now().strftime(
                '%Y-%m-%d %H:%M:%S'), x.body]]
            logger.info("Blacklisting user: " + x.author.name)
            message_send(x.author.name, "blacklist add")
            dh.insert("Blacklist", data)
            marked.append(x)
        elif (("resume" == received_subject) or ("unblacklist" == received_subject)) and name in blacklisted:
            dh.delete(
                "Blacklist",
                "user",
                "\'{user}\'".format(
                    user=name))
            logger.info("Unblacklisting " + x.author.name)
            message_send(x.author.name, "blacklist remove")
            marked.append(x)
        for i in range(len(additional)):  # Looks
            if additional[i][0] == received_subject:
                global additional_choice
                additional_choice = i
                message_send(x.author.name, "additional")
                to_break = True
                marked.append(x)
                break
        if to_break:
            break
        # Username mentions appear in the inbox so this filters them out
        elif received_subject != "username mention":
            logger.info(
                "Message with subject and body not understood. Subject: {0}   Body: {1}".format(
                    x.subject, x.body))
            message_send(x.author.name, "unknown")
            marked.append(x)
    reddit.inbox.mark_read(marked)
    logger.info("Finished Messages")


def message_send(user, kind):  # Sends messages to users
    logger.info("Sending {0} message to {1}".format(kind, user))
    if kind == "blacklist add":
        subject = "Successfully blacklisted"
        message = "Hello {user},  \n" \
                  "  This is a message confirming that you have been added to /u/useful_bot's blacklist.  \n" \
                  " If you still receive replies for me please send me a message. ".format(
                      user=user)
    if kind == "blacklist remove":
        subject = "Successfully removed from blacklist"
        message = "Hello {user},  \n " \
                  "This message is confirming that you have been removed from /u/useful_bot's blacklist.  \n " \
                  "If you feel that this message was a mistake or you would like to remain on the blacklist then " \
                  "reply stop".format(user=user)
    if kind == "additional":
        subject = additional_responses[additional_choice][1]
        message = additional_responses[additional_choice][2]
    if kind == "unknown":
        subject = "Message Unknown"
        message = "Hello {user},  \n" \
                  "This message is being sent to you because you have sent me a message that I am unsure how to deal with it. " \
                  " \nRest assure this has been recorded and a solution should be in progress. Thanks ".format(
                      user=user)
    reddit.redditor(user).message(subject, message)


def find_mentions():  # Finds anytime there is a username mention
    logger.info("Starting Mentions")
    toadd = []
    for x in reddit.inbox.mentions():
        # Needs the mentions database because I was unable to mark them as read
        # with praw
        if str(x) not in mentions:
            try:
                logger.debug(
                    "Found mention {id}, User: {user}, Body: {body}".format(
                        id=x, user=x.author, body=x.body))
                x.reply("Hello, I see you mentioned me. How can I help?")
                logger.debug("Replying to {}".format(x))
                marked = [
                    x.id, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
                toadd.append(marked)
            except Exception as e:
                logger.warn(e)
    dh.insert("replied_mentions", toadd)
    logger.info("Finished mentions")


if __name__ == "__main__":
    logger = logmaker.make_logger("Main")
    dh.create()
    logger.info("Starting up")
    reddit = start()
    subreddit_choice = botinfo.subreddit
    subreddit = reddit.subreddit(botinfo.subreddit)
    # Gets all the data from the database
    comments_replied_to, posts_replied_to, blacklisted, mentions, additional_responses, comment_responses, post_responses = getprevious()
    additional_choice = None
    message_check(additional_responses)
    post_reply(subreddit)
    comment_reply(subreddit)
    find_mentions()
    downvote.downvoted_remover(reddit)
    stopbot(True)
