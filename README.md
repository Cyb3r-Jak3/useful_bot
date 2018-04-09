# Useful bot
## coolaspie

A reddit bot in python, using praw.

End goal of this project is to have an easy to use reddit bot template

---

##### To use:
The only requirement that you should have to download is praw
   `pip3 install praw`
All the other modules should already be installed but if they are not use
`pip3 install sqlite3 logging`
make sure you have your own api credentials. If you do not head [here](https://www.reddit.com/prefs/apps "reddit apps") and click create application -> script.
Once you have those credentials add them to botinfo.example.py and rename the file to botinfo.py.
To run:
`python3 main.py`

---

##### Currently:  
* Replies to posts
* Replies to comments
* Reads messages and adds users who request blacklist

---  
  
##### Issues:
* ~~Adding to blacklist does not actually stop replies~~

If you find one please submit it in the issues tab
  
---

#####  Future Features for a Release V2:
- [ ] Reply to messages
- [x] Be able to blacklist subreddits if contacted
  - [x] Request unblacklisting
- [ ] Respond to username mentions
