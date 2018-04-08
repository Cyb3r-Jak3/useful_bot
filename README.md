# Useful bot
## coolaspie

A reddit bot in python, using praw.

---

##### To use:
The only requirement that you should have to download is praw
   `pip3 install praw`
All the other modules should already be installed but if they are not use
`pip3 install sqlite3 logging`
make sure you have your own api credentials. If you do not head [here](https://www.reddit.com/prefs/apps "here") and click create application -> script.
Once you have those credentials add them to botinfo.example.py and rename the file to botinfo.py.
To run:
`python3 main.py`

---

##### Currently:  
* Replies to posts
* Replies to comments

---  
  
##### Issues:  
* Adding to blacklist does not actually stop replies

If you find one please submit it in the issues tab
  
---

#####  Future Features for a Release V2:
- [ ] Reply to messages
- [x] Be able to blacklist subreddits if contacted. (The data gets added and pulled from table in the database but it does not actually do anything
- [ ] Respond to username mentions
