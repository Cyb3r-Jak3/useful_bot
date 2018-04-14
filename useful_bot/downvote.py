# Global
import praw
# Local
import logmaker, main, botinfo


def downvoted_remover(r):
    logger = logmaker.make_logger("Comment Remover")
    logger.info("Starting Downvoted Removal")

    comments = r.redditor(botinfo.username).comments.controversial()

    deleted = 0

    for comment in comments:
        if comment.score <= -1:
            logger.info("Removing comment {}".format(comment.id))
            comment.delete()
            deleted += 1
    if deleted == 0:
        logger.info("No comments were deleted")
    else:
        logger.info("{0} comments were deleted".format(deleted))

    logger.info("Finished Downvote removal")
