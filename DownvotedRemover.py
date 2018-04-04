import praw, logmaker, botinfo
logger = logmaker.makeLogger("Comment Remover")
try:
    r = praw.Reddit(client_id=botinfo.client_id, client_secret=botinfo.client_secret, password=botinfo.password,
                    username=botinfo.username, user_agent=botinfo.user_agent)
    logger.info("Successfully logged in")
except Exception as e:
    logger.error("Exception {} occurred on login".format(e))

user = r.redditor(botinfo.username)
comments = user.comments.new()

deleted = 0

for comment in comments:
    if(comment.score <= -1):
        logger.warn("Removing comment {}".format(comment.id))
        comment.delete()
        deleted += 1
if deleted == 0:
    logger.info("No comments were deleted")
else:
    logger.info("{0} comments were deleted".format(deleted))

logger.debug("Script ended \n\n")