# Useful bot
## coolaspie

#### Tested in python 3, 3.5, 3.6
---
A reddit bot in python, using praw.

End goal of this project is to have an easy to use reddit bot template

---

### To use:
The only requirement that you should have to download is praw. All the other modules that are used come with python3.  
You need to have your own api credentials. If you do not head [here](https://www.reddit.com/prefs/apps "reddit apps") and click create application -> script.
Once you have those credentials add them to botinfo.example.py and rename the file to botinfo.py.  
To run:  
  `python3 main.py`

---

#### Currently:
* Replies to posts
* Replies to comments
* Reads messages and adds users who request blacklist or remove from blacklist

---

#### Issues:
* ~~Adding to blacklist does not actually stop replies~~
* ~~Does not mark previous read messages as such~~
  * ~~Does not mark mentions are read~~
* ~~[#1](https://github.com/coolaspie/useful_bot/issues/1 "Issue #1") Issue with imports~~

If you find one please submit it in the issues tab

---

#### Features for a Release V2: (Messaging)
- [x] Reply to messages
- [x] Be able to blacklist subreddits if contacted
  - [x] Request unblacklisting
- [x] Respond to username mentions

#### Future Features for Release V3: (Assistance)
- [ ] Easier template layout.
- [ ] Easier customization.
- [ ] Easier to add functions
- [ ] More execption handling
- [ ] Make it loop better than currently @samuellando
