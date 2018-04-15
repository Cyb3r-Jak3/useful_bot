# Useful bot
## coolaspie

#### Tested in python 3, 3.5, 3.6
---
A reddit bot in python, using praw.

End goal of this project is to have an easy to use reddit bot template

Nice CLI written by [samuellando](https://github.com/samuellando "Author's Github Profile")

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
* Replies to messages
* Be able to blacklist subreddits if contacted
  * Can unblacklist unblacklisting
*  Respond to username mentions
* Additional Responses to messages
* Templete for simlple features

---

#### Issues:

If you find one please submit it in the issues tab

---


##### Future Release Plans
###### These are subject to change without notice
  3.1 - Add cli function to add message responses  
  3.2 - Add ways to format user information in addiontal responses  
  3.3 - Format in proper PEP8 Standards
