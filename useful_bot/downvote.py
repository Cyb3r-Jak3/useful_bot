# Internal
import logmaker
import botinfo


def downvoted_remover(r):
    logger = logmaker.make_logger("Comment Remover")
    logger.info("Starting Downvoted Removal")
    # Gets comments that are most likely to be downvoted
    comments = r.redditor(botinfo.username).comments.controversial(limit=1000)

    deleted = 0

    for comment in comments:
        if comment.score <= -1:
            logger.info("Removing comment {}".format(comment.id))
            comment.delete()
            deleted += 1
    if deleted == 0:
        logger.debug("No comments were deleted")
    else:
        logger.info("{0} comments were deleted".format(deleted))

    logger.info("Finished Downvote removal")
