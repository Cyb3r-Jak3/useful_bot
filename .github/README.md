# Useful bot
## coolaspie

#### Tested in python 3, 3.5, 3.6
---
A reddit bot in python, using praw.  

End goal of this project is to have an easy to use reddit bot template for anyone who wants one.

----------------------------------------------------------------------


### To use:
You need to have your own api credentials. If you do not head [here](https://www.reddit.com/prefs/apps "reddit apps") and click create application -> script.
Currently recommended that you enter the credtinals in botinfo.example.py and rename the file to. It is the recommended approach because you can run the cli and import the credtinals from the botinfo file but you can not currently run the main.py off the database credtinals.
Fully tested releases are [here](https://github.com/coolaspie/useful_bot/releases "useful bot releases")   
``` 
pip install praw  
git clone https://github.com/coolaspie/useful_bot.git  
```

To run:  
```    
python3 main.py
```
or
```
python3 cli.py
```
If you want to import the credentials for easier use
``` python
python3.6 cli.py import
```
---
#### Versions


Number | Date | Download Link
---|---|---
Version 3.5 | April 21th, 2018 | [Link](https://github.com/coolaspie/useful_bot/releases/download/v3.4/useful_bot-master.zip)
Version 3 | April 15th, 2018 | [Link](https://github.com/coolaspie/useful_bot/releases/download/V3/useful_bot-master.zip)
Version 2 | April 13th, 2018 | [Link](https://github.com/coolaspie/useful_bot/releases/download/v2.0/useful_bot.zip)
Version 1 | April 5th, 2018 | [Link](https://github.com/coolaspie/useful_bot/releases/tag/v1.0)


#### Currently:
* Replies to posts
* Replies to comments
* Reads messages and adds users who request blacklist or remove from blacklist
* Replies to messages
* Be able to blacklist subreddits if contacted
  * Can request unblacklisting
*  Respond to username mentions
* Additional Responses to messages
* Templete for simlple features

---

#### Issues:
* running either main.py or cli.py out of folder creates the db file there

If you find one please submit it in the issues tab

---
#### Possible Future Features
