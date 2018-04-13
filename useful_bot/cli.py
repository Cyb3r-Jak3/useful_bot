# External
import praw,time
# Local
import datahandler as dh
import logmaker, main

class CommandLineInterface():
    def __init__(self):
        self.logger = logmaker.make_logger("CLI")
        self.logger.debug("Straring CLI")
        # Connect to db.
        dh.create()
        # Start praw object useing credentials in data base.
        self.r = self.startBot()
        self.run()

    def run(self):
        main.subreddit_choice = self.fetchConfig("subreddit")
        main.reddit = self.r
        main.subreddit = main.reddit.subreddit(main.subreddit_choice)
        main.logger = logmaker.make_logger("MAIN")
        print()
        print("commands:")
        print("message_check")
        print("post_reply")
        print("comment_reply")
        print("find_mentions")
        print("all")
        print("exit")
        print("add -x flag to add a repetition loop with x minutes pause")
        print()
        while True:
            command = input("> ")
            comments_replied_to, posts_replied_to, blacklisted, mentions = main.getprevious()
            loop = True
            delay = 0
            if "-" in command:
                print("Hit control + C to stop looping")
                delay = int(command.split("-")[1])
            while loop:
                try:
                    if "message_check" in command or "all" in command:
                        main.blacklist_check()
                    if "post_reply" in command or "all" in command:
                        main.post_reply(main.subreddit)
                    if "comment_reply" in command or "all" in command:
                        main.comment_reply(main.subreddit)
                    if "find_mentions" in command or "all" in command:
                        main.find_mentions()
                    if command == "exit":
                        main.stopbot(True)
                    if not "-" in command:
                        loop = False
                    time.sleep(delay*60)
                except KeyboardInterrupt:
                    print()
                    loop = False

    def startBot(self):
        try:
            client_id = self.fetchConfig('client_id')
            client_secret = self.fetchConfig('client_secret')
            password = self.fetchConfig('password')
            username = self.fetchConfig('username')
            user_agent = self.fetchConfig('user_agent')
            r = praw.Reddit(client_id=client_id, client_secret=client_secret, password=password,
                        username=username, user_agent=user_agent)
            r.user.me() # Test authentication.
            self.logger.info("Successfully logged in")
            return r
        except Exception as e:
            self.logger.error("Exception {} occurred on login".format(e))
    
    def fetchConfig(self,find):
        try:
            values = dh.data_fetch("configurations","value")
            ids = dh.data_fetch("configurations","id")
            # Convert strings to proper lists
            values = values.replace("[","")
            values = values.replace("]","")
            values = values.replace("'","")
            values = values.split(", ")
            ids = ids.replace("[","")
            ids = ids.replace("]","")
            ids = ids.replace("'","")
            ids = ids.split(", ")
            return values[ids.index(find)]
        except Exception as e:
            value = input("Enter "+find+": ")
            dh.data_insert("configurations",[[find,value]])
            return value


if __name__ == "__main__":
    C = CommandLineInterface()
