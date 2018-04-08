# Either default or built in
import praw, re, datetime, os, sys
from praw.models import Comment

# mine
from useful_bot import datahandler, botinfo, logmaker

def stopbot(Delete):
    logger.info("Shutting down")
    if Delete:
        logger.info("Deleting log file")
        os.remove("bot.log")
    sys.exit(0)


def getprevious():
    try:
        comments = datahandler.datafecter("Comments", "id")
    except Exception as e:
        logger.error("Error getting comment ids " + str(e))
        stopbot(False)
    try:
        posts = datahandler.datafecter("Posts", "id")
    except Exception as e:
        logger.error("Error getting post ids " + str(e))
        stopbot(False)
    try:
        blacklist = datahandler.datafecter("Blacklist", "user")
        blacklist+=(" useful_bot")

    except Exception as e:
        logger.error("Error getting blacklisted users")

    return comments, posts, blacklist


def Start():
    try:
        r = praw.Reddit(client_id=botinfo.client_id, client_secret=botinfo.client_secret, password=botinfo.password,
                        username=botinfo.username, user_agent=botinfo.user_agent)
        logger.info("Successfully logged in")
        return r
    except Exception as e:
        logger.error("Exception {} occurred on login".format(e))
        stopbot(False)


def postReply(subreddit):
    logger.debug("Replying to posts")
    toadd = []
    post_reply = "Useful_bot says that it worked"
    for submission in subreddit.hot(limit=10): # gets submissions from the subreddit. Here it has a limit of 10
        add = []
        if submission.id not in posts_replied_to:
            if (re.search("skills", submission.title, re.IGNORECASE)) and (submission.author not in blacklisted):
                add.append(submission.id)
                submission.reply(post_reply)
                add.append(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                logger.debug("Bot replying to : {0}".format(submission.title))
                add.append(subreddit_choice)
                add.append(post_reply)
                toadd.append(add)
                break

    logger.debug("Replied to posts")
    datahandler.datainsert("Posts", toadd)
    logger.debug("Finished with posts")


def commentReply(subreddit):
    logger.debug("Replying to comments")
    toadd = []
    for post in subreddit.hot(limit=10):
        submission = reddit.submission(post)
        submission.comments.replace_more(limit=50)
        for comment in submission.comments.list():
            add = []
            text = comment.body
            author = comment.author.name
            if ("kidding" in text.lower()) and (comment.id not in comments_replied_to) and \
                    (str(author) not in blacklisted):
                add.append(comment.id)
                comment_reply = "There is no kidding here {0}".format(author)
                add.append(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), comment_reply, subreddit_choice)
                comment.reply(comment_reply)
                logger.debug("Bot replying to {0}".format(text))
                add.append()
                toadd.append(add)
                break

    logger.debug("Replied to all comments")
    datahandler.datainsert("Comments", toadd)
    logger.debug("Wrote comment ids")


def blacklistCheck():
    for x in reddit.inbox.unread(mark_read=True):
        if (("stop" in x.subject.lower()) or ("blacklist" in x.subject.lower())) and x.author.name not in blacklisted:
            data = list([[x.author.name, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), x.body]])
            logger.info("Blacklisting user: " + str(x.author))
            datahandler.datainsert("Blacklist", data)


if __name__ == "__main__":
    datahandler.create()
    logger = logmaker.makeLogger("Main")
    logger.debug("Staring up")
    reddit = Start()
    subreddit_choice = "usefulbottest"
    subreddit = reddit.subreddit(subreddit_choice)
    comments_replied_to, posts_replied_to, blacklisted = getprevious()
    postReply(subreddit)
    commentReply(subreddit)
    blacklistCheck()
    stopbot(True)
