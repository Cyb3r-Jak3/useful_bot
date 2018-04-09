# Either default or built in
import praw, re, datetime, os, sys
# Local
from useful_bot import datahandler, botinfo, logmaker


def stopbot(delete):
    logger.info("Shutting down")
    if delete:
        logger.info("Deleting log file")
        os.remove("bot.log")
    sys.exit(0)


def getprevious():
    try:
        comments = datahandler.data_fetch("Comments", "id")
    except Exception as e:
        logger.error("Error getting comment ids: " + str(e))
        stopbot(False)
    try:
        posts = datahandler.data_fetch("Posts", "id")
    except Exception as e:
        logger.error("Error getting post ids: " + str(e))
        stopbot(False)
    try:
        blacklist = datahandler.data_fetch("Blacklist", "user")
        blacklist += " useful_bot"
    except Exception as e:
        logger.error("Error getting blacklisted users: " + str(e))
        stopbot(False)
    return comments, posts, blacklist


def start():
    try:
        r = praw.Reddit(client_id=botinfo.client_id, client_secret=botinfo.client_secret, password=botinfo.password,
                        username=botinfo.username, user_agent=botinfo.user_agent)
        logger.info("Successfully logged in")
        return r
    except Exception as e:
        logger.error("Exception {} occurred on login".format(e))
        stopbot(False)


def post_reply(subreddit):
    logger.debug("Replying to posts")
    toadd = []
    reply = "Useful_bot says that it worked"
    for submission in subreddit.hot(limit=10):  # Gets submissions from the subreddit. Here it has a limit of 10
        add = []
        if submission.id not in posts_replied_to:
            if (re.search("skills", submission.title, re.IGNORECASE)) and (submission.author not in blacklisted):
                add.append(submission.id)
                submission.reply(reply)
                add.append(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                logger.debug("Bot replying to : {0}".format(submission.title))
                add.append(subreddit_choice)
                add.append(post_reply)
                toadd.append(add)
                break

    logger.debug("Replied to posts")
    datahandler.data_insert("Posts", toadd)
    logger.debug("Finished with posts")


def comment_reply(subreddit):
    logger.debug("Replying to comments")
    toadd = []
    for post in subreddit.hot(limit=10):  # Gets the top 10 posts in the subreddit
        submission = reddit.submission(post)
        submission.comments.replace_more(limit=50)  # Gets 50 comments from each post
        for comment in submission.comments.list():
            add = []
            text = comment.body
            author = comment.author.name
            if ("kidding" in text.lower()) and (comment.id not in comments_replied_to) and \
                    (str(author) not in blacklisted):
                add.append(comment.id)
                reply = "There is no kidding here {0}".format(author)
                add.append(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), reply, subreddit_choice)
                comment.reply(reply)
                logger.debug("Bot replying to {0}".format(text))
                toadd.append(add)

    logger.debug("Replied to all comments")
    datahandler.data_insert("Comments", toadd)
    logger.debug("Wrote comment ids")


def blacklist_check():
    logger.info("Checking Messages")
    for x in reddit.inbox.unread(mark_read=True):
        if (("stop" in x.subject.lower()) or ("blacklist" in x.subject.lower())) and x.author.name.lower() not in blacklisted:
            data = [[x.author.name.lower(), datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), x.body]]
            logger.info("Blacklisting user: " + str(x.author))
            message_send(x.author.name, "blacklist add")
            datahandler.data_insert("Blacklist", data)
        elif (("resume" in x.subject.lower()) or ("unblacklist" in x.subject.lower())) and x.author.name.lower() in blacklisted:
            datahandler.data_delete("Blacklist", "user", "\'{user}\'".format(user=x.author.name.lower()))
            logger.info("Unblacklisting " + x.author.name)
            message_send(x.author.name, "blacklist remove")


def message_send(user, type):
    logger.info("Sending {0} message to {1}".format(type, user))
    if type == "blacklist add":
        subject = "Successfully blacklisted"
        message = "Hello {user}," \
                  "  \n This is a message confirming that you have been added to /u/useful_bot's blacklist.  \n" \
                  " If you still receive replies for me please send me a message. ".format(user=user)
    if type == "blacklist remove":
        subject = "Successfully removed from blacklist"
        message = ("Hello {user},  \n "
                   "This message is confirming that you have been removed from /u/useful_bot's blacklist.  \n "
                   "If you feel that this message was a mistake or you would like to remain on the blacklist then "
                   "reply stop".format(user=user))
    reddit.redditor(user).message(subject, message)


if __name__ == "__main__":
    datahandler.create()
    logger = logmaker.make_logger("Main")
    logger.debug("Staring up")
    reddit = start()
    subreddit_choice = "usefulbottest"
    subreddit = reddit.subreddit(subreddit_choice)
    comments_replied_to, posts_replied_to, blacklisted = getprevious()
    post_reply(subreddit)
    comment_reply(subreddit)
    blacklist_check()
    stopbot(True)
