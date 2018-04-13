## Either default or built in
import praw, re, datetime, os, sys, time
# Local
import datahandler, logmaker, botinfo


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
    try:
        mentions = datahandler.data_fetch("replied_mentions", "id")
    except Exception as e:
        logger.error("Error getting mentions: " + str(e))
        stopbot(False)
    return comments, posts, blacklist, mentions


def start():
    try:
        r = praw.Reddit(client_id=botinfo.client_id, client_secret=botinfo.client_secret, password=botinfo.password,
                        username=botinfo.username, user_agent=botinfo.user_agent)
        r.user.me() # Verify log in, will raise exception if log in failed.
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
            if (re.search("skills", submission.title, re.IGNORECASE)) and (submission.author.name not in blacklisted):
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
                add.append(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                add.append(reply)
                add.append(subreddit_choice)
                comment.reply(reply)
                logger.debug("Bot replying to {0}".format(text))
                toadd.append(add)

    logger.debug("Replied to all comments")
    datahandler.data_insert("Comments", toadd)
    logger.debug("Wrote comment ids")


def blacklist_check():
    logger.info("Checking Messages")
    marked = []
    for x in reddit.inbox.unread():
        subject = x.subject.lower()
        name = x.author.name.lower()
        if (("stop" == subject) or ("blacklist" == subject)) \
                and name not in blacklisted:
            data = [[name, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), x.body]]
            logger.info("Blacklisting user: " + x.author.name)
            message_send(x.author.name, "blacklist add")
            datahandler.data_insert("Blacklist", data)
            marked.append(x)
        elif (("resume" == subject) or ("unblacklist" == subject)) and name in blacklisted:
            datahandler.data_delete("Blacklist", "user", "\'{user}\'".format(user=name))
            logger.info("Unblacklisting " + x.author.name)
            message_send(x.author.name, "blacklist remove")
            marked.append(x)
        else:
            logger.info("Message with subject and body not understood. Subject: {0}   Body: {1}".format(x.subject, x.body))
            message_send(x.author.name, "unknown")
            marked.append(x)
    reddit.inbox.mark_read(marked)


def message_send(user, type):
    logger.info("Sending {0} message to {1}".format(type, user))
    if type == "blacklist add":
        subject = "Successfully blacklisted"
        message = "Hello {user},  \n" \
                  "  This is a message confirming that you have been added to /u/useful_bot's blacklist.  \n" \
                  " If you still receive replies for me please send me a message. ".format(user=user)
    if type == "blacklist remove":
        subject = "Successfully removed from blacklist"
        message = "Hello {user},  \n " \
                  "This message is confirming that you have been removed from /u/useful_bot's blacklist.  \n " \
                  "If you feel that this message was a mistake or you would like to remain on the blacklist then " \
                  "reply stop".format(user=user)
    if type == "unknown":
        subject = "Message Unknown"
        message = "Hello {user},  \n" \
                  "This message is being sent to you because you have sent me a message that I am unsure how to deal with it.  \n " \
                  "Rest assure this has been recorded and a solution should be in progress. Thanks ".format(user=user)
    reddit.redditor(user).message(subject, message)


def find_mentions():
    toadd = []
    for x in reddit.inbox.mentions():
        if str(x) not in mentions:
            logger.info("Found mention {id}. User {user} Body {body}".format(id=x, user=x.author, body=x.body))
            x.reply("Hello, I see you mentioned me. How can I help?")
            marked = [x.id, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
            toadd.append(marked)
    datahandler.data_insert("replied_mentions", toadd)



if __name__ == "__main__":
    datahandler.create()
    logger = logmaker.make_logger("Main")
    logger.debug("Staring up")
    reddit = start()
    subreddit_choice = "usefulbottest"
    subreddit = reddit.subreddit(subreddit_choice)
    stop = False # Will run until this is set to true by user.
    DELAY = 10 # Delay in minutes between runs.
    while not stop:
        comments_replied_to, posts_replied_to, blacklisted, mentions = getprevious()
        blacklist_check()
        post_reply(subreddit)
        comment_reply(subreddit)
        find_mentions()
        # Begin delay.
        logger.debug("Sleeping for {0} minutes\n".format(DELAY))
        print("Hit control+c to stop the bot.") # This does not need to be logged.
        time.sleep(DELAY*60)
    stopbot(True)
