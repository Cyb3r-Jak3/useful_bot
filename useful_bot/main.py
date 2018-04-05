# Either default or built in
import praw, os, re, datetime

# mine
import botinfo, logmaker, datahandler

comments_replied_to = datahandler.datafecter("Comments")

posts_replied_to = datahandler.datafecter("Posts")

"""if not os.path.isfile("posts_replied_to.txt"):  # Checks to see if there is a file
    posts_replied_to = []

else:  # just goes through the information from the post that have been replied to
    with open("posts_replied_to.txt", "r") as f:
        posts_replied_to = f.read()
        posts_replied_to = posts_replied_to.split("\n")
        posts_replied_to = list(filter(None, posts_replied_to))

if not os.path.isfile("comments_replied_to.txt"):  # again checks to if there a file there
    comments_replied_to = []
else:
    with open("comments_replied_to.txt", "r") as f:  # reads the file
        comments_replied_to = f.read()
        comments_replied_to = comments_replied_to.split("\n")
        comments_replied_to = list(filter(None, comments_replied_to))"""


def Start():
    try:
        r = praw.Reddit(client_id=botinfo.client_id, client_secret=botinfo.client_secret, password=botinfo.password,
                        username=botinfo.username, user_agent=botinfo.user_agent)
        logger.info("Successfully logged in")
        return r
    except Exception as e:
        logger.error("Exception {} occurred on login".format(e))





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
                add.append(datetime.datetime.now().strftime('%Y-%m-$d %H:%M:%S'))
                logger.debug("Bot replying to : {0}".format(submission.title))
                add.append(subreddit_choice)
                add.append(post_reply)
                toadd.append(add)
                break

    #print(toadd)
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
                add.append(datetime.datetime.now().strftime('%Y-%m-$d $H:%M:%S'))
                comment.reply(comment_reply)
                logger.debug("Bot replying to {0}".format(text))
                add.append(comment_reply)
                add.append(subreddit_choice)
                toadd.append(add)
                break

    logger.debug("Replied to all comments")
    datahandler.datainsert("Comments", toadd)
    logger.debug("Wrote comment ids")


logger = logmaker.makeLogger("Main")
logger.debug("Staring up")
reddit = Start()
subreddit_choice = "usefulbottest"
subreddit = reddit.subreddit(subreddit_choice)


postReply(subreddit)

commentReply(subreddit)

logger.debug("end of script \n \n")
