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
``` 
git clone https://github.com/coolaspie/useful_bot.git  
pip install praw 
```

To run:  
  ```    
  python3 main.py
  ```
or
```
  python3 cli.py
```
---

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

If you find one please submit it in the issues tab

---


##### Future Release Plans
###### These are subject to change without notice
  ~~3.1 - Add cli function to add message responses~~  
     -> 3.2 allows for the main to import credentials from the configurations  
  3.~~2~~3 - Add ways to format user information in addiontal responses  
  3.~~3~~4 - Format in proper PEP8 Standards
