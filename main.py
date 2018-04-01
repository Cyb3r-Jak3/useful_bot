import praw, os, re
from botinfo import Start
from praw.models import MoreComments


if not os.path.isfile("posts_replied_to.txt"): #Checks to see if there is a file
	posts_replied_to = []

else: #just goes through the information from the post that have been replied to
	with open("posts_replied_to.txt", "r") as f:
		posts_replied_to = f.read()
		posts_replied_to = posts_replied_to.split("\n")
		posts_replied_to = list(filter(None, posts_replied_to))


if not os.path.isfile("comments_replied_to.txt"): #again checks to if there a file there
	comments_replied_to = []
else:
	with open("comments_replied_to.txt", "r") as f: # reads the file
		comments_replied_to = f.read()
		comments_replied_to = comments_replied_to.split("\n")
		comments_replied_to = list(filter(None, comments_replied_to))

reddit = Start()
subreddit =  reddit.subreddit("usefulbottest")
#print(comments_replied_to)
#print(posts_replied_to)

for submission in subreddit.hot(limit=10): #gets submissions from the subreddit. Here it has a limit of 5
	if submission.id not in posts_replied_to:
		if  re.search("skills", submission.title, re.IGNORECASE):
			posts_replied_to.append(submission.id)
			submission.reply("Usebot says that it worked")
			print("Bot replying to : ", submission.title)
			break
#print("Finished with the submission replies")#Debugging Steps
with open("posts_replied_to.txt", "w") as f: 
	for post_id in posts_replied_to:
		f.write(post_id + "\n")
#print("Wrote the post_ids") #Debugging Steps


numreplies = 0
debug_num = 0


while True:
	print ("There are ", (len(list(subreddit.hot(limit=10))), "posts"))
	for post in subreddit.hot(limit=10):
		submission = reddit.submission(post)
		submission.comments.replace_more(limit=50)
		print("Commnt list is", str(len(submission.comments.list())))
		for comment in submission.comments.list():
			print(debug_num)
			debug_num += 1
			text = comment.body
			author = comment.author
			#print(author, text)
			if ("kidding" in text.lower()) and (comment.id not in comments_replied_to) and (author != "usefulbot") :
				comments_replied_to.append(comment.id)
				comment.reply ("There is no kidding here %s" % author)
				print("Bot replying to :", text)
				with open("comments_replied_to.txt", "w") as f:
					for comment_id in comments_replied_to:
						f.write(comment_id + "\n")
				break


#print("Finished with replying to comments")#Debugging Steps
with open("comments_replied_to.txt", "w") as f:
	for comment_id in comments_replied_to:
		f.write(comment_id + "\n")
print("end of script")
