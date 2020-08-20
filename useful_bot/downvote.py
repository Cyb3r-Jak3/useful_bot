"""Functions that removes negative comments"""
# Internal
import logmaker
import botinfo

logger = logmaker.make_logger("Comment Remover")


def downvoted_remover(reddit_client) -> None:
    """
    Removed all comments that are negative
    Parameters
    ----------
    reddit_client: praw.Reddit
        The reddit client
    """
    logger.info("Starting Downvoted Removal")
    # Gets comments that are most likely to be downvoted
    comments = reddit_client.redditor(botinfo.username).comments.controversial(
        limit=1000
    )

    deleted = 0

    for comment in comments:
        if comment.score <= -1:
            logger.info("Removing comment: %s", comment.id)
            comment.delete()
            deleted += 1
    if deleted == 0:
        logger.debug("No comments were deleted")
    else:
        logger.info("%s comments were deleted", deleted)

    logger.info("Finished Downvote removal")
