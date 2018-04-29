# External
import logging

client_id =
client_secret =
password =
username =
author =
user_agent = "/u/" + username + " by /u/" + author
subreddit = "Pick a subreddit"
logging_level = logging.DEBUG  # Levels are DEBUG, INFO, WARNING, ERROR, CRITICAL. Recommended level is INFO
footer = "  \n ---  \n ^(^beep ^boop ^I ^am ^a ^bot ^and ^this ^action ^was ^preformed ^automatically. ^|) [^^Source](https://www.github.com/coolaspie/useful_bot) ^^| " \
         "[^^Blacklist](https://www.reddit.com/message/compose/?to=" + username + "&subject=Blacklist&message=Please+add+a+reason+here) ^^| [^^Contact ^^author]" \
    "(https://www.reddit.com/message/compose/?to=" + author + "&subject=Bot+issue&message=Please+add+a+reason+here)"
    # The footer looks like this because it matches reddit's markdown

# Reply format support:
#   {user} for author's name ie Hello {user} prints Hello (author of comment)
