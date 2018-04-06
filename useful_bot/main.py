# Either default or built in
import praw, re, datetime, os, sys

# mine
import botinfo, logmaker, datahandler


def stopbot(Delete):
    logger.info("Shutting down")
    if Delete:
        logger.info("Deleting log file")
        os.remove("bot.log")
    sys.exit(0)


def getprevious():
    try:
        comments = datahandler.datafecter("Comments")
    except Exception as e:
        logger.error("Error getting comment ids " + str(e))
        stopbot(False)
    try:
        posts = datahandler.datafecter("Posts")
    except Exception as e:
        logger.error("Error getting post ids " + str(e))
        stopbot(False)
    return comments, posts


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
            if re.search("skills", submission.title, re.IGNORECASE):
                add.append(submission.id)
                submission.reply(post_reply)
                add.append(datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))
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
            author = comment.author
            if ("kidding" in text.lower()) and (comment.id not in comments_replied_to) and (author != "useful_bot"):
                add.append(comment.id)
                comment_reply = "There is no kidding here {0}".format(author)
                add.append(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                comment.reply(comment_reply)
                logger.debug("Bot replying to {0}".format(text))
                add.append(comment_reply)
                add.append(subreddit_choice)
                toadd.append(add)
                break

    logger.debug("Replied to all comments")
    datahandler.datainsert("Comments", toadd)
    logger.debug("Wrote comment ids")


if __name__ == "__main__":
    if not os.path.isfile("data.db"):
        datahandler.create()

    logger = logmaker.makeLogger("Main")
    logger.debug("Staring up")
    reddit = Start()
    subreddit_choice = "usefulbottest"
    subreddit = reddit.subreddit(subreddit_choice)
    get = getprevious()
    posts_replied_to = get[1]
    comments_replied_to = get[0]
    postReply(subreddit)
    commentReply(subreddit)
    logger.debug("end of script \n \n")
    stopbot(True)
