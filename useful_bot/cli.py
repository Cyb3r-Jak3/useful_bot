# External
import praw, time
# Local
import datahandler as dh
import logmaker, main, botinfo, downvote


class CommandLineInterface():
    def __init__(self):
        self.logger = logmaker.make_logger("CLI")
        self.logger.debug("Starting CLI")
        # Connect to db.
        dh.create()
        # Start praw object using credentials in data base.
        self.r = self.start_bot()
        self.run()

    def run(self):
        try:
            main.subreddit_choice = self.fetch_config("subreddit")
        except Exception:
            main.subreddit_choice = botinfo.subreddit
        main.reddit = self.r
        main.subreddit = main.reddit.subreddit(main.subreddit_choice)
        main.logger = logmaker.make_logger("CLI-MAIN")
        print()
        print("commands:")
        print("message check")
        print("post reply")
        print("comment reply")
        print("find mentions")
        print("downvote remover")
        print("all")
        print("import")
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
                    if "import" in command or "all" in command:
                        self.import_creds()
                    if "message check" in command or "all" in command:
                        main.message_check()
                    if "post reply" in command or "all" in command:
                        main.post_reply(main.subreddit)
                    if "comment reply" in command or "all" in command:
                        main.comment_reply(main.subreddit)
                    if "find mentions" in command or "all" in command:
                        main.find_mentions()
                    if "downvote remover" in command or "all" in command:
                        downvote.downvoted_remover(main.reddit)
                    if command == "exit":
                        main.stopbot(True)
                    if "-" not in command:
                        loop = False
                    time.sleep(delay * 60)
                except KeyboardInterrupt:
                    print()
                    loop = False

    def start_bot(self):
        try:
            client_id = self.fetch_config('client_id')
            client_secret = self.fetch_config('client_secret')
            password = self.fetch_config('password')
            username = self.fetch_config('username')
            user_agent = self.fetch_config('user_agent')
            r = praw.Reddit(client_id=client_id, client_secret=client_secret, password=password,
                            username=username, user_agent=user_agent)
            r.user.me()  # Test authentication.
            self.logger.info("Successfully logged in")
            return r
        except Exception as e:
            self.logger.error("Exception {} occurred on login".format(e))
            main.stopbot(False)

    def fetch_config(self, find):
        try:
            values = dh.data_fetch("configurations", "value")
            ids = dh.data_fetch("configurations", "id")
            # Convert strings to proper lists
            values = values.replace("[", "")
            values = values.replace("]", "")
            values = values.replace("'", "")
            values = values.split(", ")
            ids = ids.replace("[", "")
            ids = ids.replace("]", "")
            ids = ids.replace("'", "")
            ids = ids.split(", ")
            return values[ids.index(find)]
        except Exception as e:
            value = input("Enter " + find + ": ")
            dh.data_insert("configurations", [[find, value]])
            return value

    def import_creds(self):
        needed = ['client_id', 'client_secret', 'password', 'username', 'user_agent']
        for i in needed:
            dh.data_insert("configurations", [[i, getattr(botinfo, i)]])
            self.logger.debug("Imported {}".format(i))


if __name__ == "__main__":
    C = CommandLineInterface()
