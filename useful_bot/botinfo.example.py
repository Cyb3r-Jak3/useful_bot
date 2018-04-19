# External
import logging

client_id = "Insert Client ID"
client_secret = "Insert Client Secret"
password = "Insert password"
username = "Insert username"
author = "Enter your reddit username"
user_agent = "/u/"+username+" by /u/"+author
subreddit = "Pick a subreddit"
logging_level = logging.DEBUG  # Levels are DEBUG, INFO, WARNING, ERROR, CRITICAL
footer = "  \n ---  \n ^(^beep ^boop ^I ^am ^a ^bot ^and ^this ^action ^was ^preformed ^automatically. ^|) [^^Source](https://www.github.com/coolaspie/useful_bot) ^^| " \
         "[^^Blacklist](https://www.reddit.com/message/compose/?to="+username+"&subject=Blacklist&message=Pleaseadd+a+reason+here) ^^| [^^Contact ^^author]" \
                                                                             "(https://www.reddit.com/message/compose/?to="+author+"&subject=Bot+issue&message=Pleaseadd+a+reason+here)"

comment_text = "What you want the bot to find in the comments"
comment_reply = "What you want the bot to comment when it finds the comment_text"
post_text = "What you want the bot to find in the post"
post_reply = "What you want the bot to comment when it finds the post_text"

# Reply format support:
#   {user} for author's name ie Hello {user} prints Hello (author of comment)
