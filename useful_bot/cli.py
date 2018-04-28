# External
import praw
import time
import sys
# Internal
import datahandler as dh
import logmaker
import main
import botinfo
import downvote


class CommandLineInterface():
    def __init__(self):
        self.logger = logmaker.make_logger("CLI")
        self.logger.debug("Starting CLI")
        # Connect to db.
        dh.create()

        # Start praw object using credentials in data base.
        try:
            if sys.argv[1].lower() == "import":
                self.cred_import()
                return
        except IndexError:
            self.logger.debug("Did not set import")
        self.r = self.start_bot()
        self.run()

    def run(self):
        try:
            main.subreddit_choice = self.fetch_config("subreddit")
        except Exception:
            main.subreddit_choice = botinfo.subreddit
        main.reddit = self.r
        main.subreddit = main.reddit.subreddit(main.subreddit_choice)
        main.logger = logmaker.make_logger("CLI")
        print()
        print("Commands:")
        print("message check")
        print("post reply")
        print("comment reply")
        print("find mentions")
        print("downvote remover")
        print("add -x flag to add a repetition loop with x minutes pause")
        print("all")
        print("exit")
        print()
        print("Extra:")
        print("response add")
        print("response delete")
        print("table search")
        print()
        while True:
            command = input("> ")
            main.comments_replied_to, main.posts_replied_to, main.blacklisted, main.mentions, main.additional_responses = main.getprevious()
            loop = True
            delay = 0
            if "-" in command:
                print("Hit control + C to stop looping")
                delay = int(command.split("-")[1])
            while loop:
                try:
                    if "message check" in command or "all" in command:
                        main.message_check(main.additional_responses)
                    if "post reply" in command or "all" in command:
                        main.post_reply(main.subreddit)
                    if "comment reply" in command or "all" in command:
                        main.comment_reply(main.subreddit)
                    if "find mentions" in command or "all" in command:
                        main.find_mentions()
                    if "downvote remover" in command or "all" in command:
                        downvote.downvoted_remover(main.reddit)
                    if "response add" in command:
                        self.response_add()
                    if "response delete" in command:
                        self.response_delete()
                    if "table search" in command:
                        self.search()
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
            r = praw.Reddit(
                client_id=client_id,
                client_secret=client_secret,
                password=password,
                username=username,
                user_agent=user_agent)
            r.user.me()  # Test authentication.
            self.logger.info("Successfully logged in")
            return r
        except Exception as e:
            self.logger.error("Exception {} occurred on login".format(e))
            main.stopbot(False)

    def fetch_config(self, find):
        try:
            values = dh.fetch("configurations", "value")
            ids = dh.fetch("configurations", "id")
            return values[ids.index(find)]
        except ValueError as ve:
            choice = input(
                "Enter I to import the credential {} from botinfo".format(find)).lower()
            if choice == "i":
                value = getattr(botinfo, find)
                dh.insert("configurations", [[find, value]])
                return value
            else:
                value = input("Enter " + find + ": ")
                dh.insert("configurations", [[find, value]])
                return value
        except Exception as e:
            self.logger.error(
                "There was an error retrieving credentials: {} ".format(e))

    def response_add(self):
        to_add = []
        to_add.append(
            input("Enter what the subject line you want to trigger a response: "))
        to_add.append(input("Enter what you want the reply subject to be: "))
        to_add.append(input("Enter the message for the reply: "))
        print(
            "For the message response template, {0} is the trigger word/phrase. {1} is the response subject and {2} is the response body. \n"
            " Enter Y to conform, R to redo or N to cancel." .format(
                to_add[0],
                to_add[1],
                to_add[2]))
        if input().lower() == "y":
            dh.insert("message_responses", list(to_add))
        elif input().lower() == "r":
            self.response_add()

    def response_delete(self):
        retrieved = dh.fetch("message_responses", "*")
        for i in range(len(retrieved)):
            print(i+1, retrieved[i], "\n")
        try:
            choice = int(input("Enter the number of the response you wish to delete: "))
            print("You have selected ", retrieved[choice - 1], "\n" + "Enter (y)es to delete: ")
        except (ValueError, IndexError):
            print("Enter a valid number")
            self.run()
        confirm = input().lower()
        if confirm.startswith("y"):
            dh.delete("message_responses", "keyword", "\'{keyword}\'".format(keyword=retrieved[choice-1][0]))
            print("Deleted")

    def search(self):
        tables = dh.table_fetch()
        table = input(
            "Available tables are {}. \nEnter the table: ".format(tables))
        if table in tables:
            print("Retrieving {}".format(table))
            retrieved = dh.fetch(table, "*")
            if len(retrieved) == 0:
                print("The table was empty")
            else:
                for i in range(len(retrieved)):
                    print(retrieved[i], "\n")
        else:
            print("Enter a valid table")


    def cred_import(self):
        try:
            for cred in [
                "client_id",
                "client_secret",
                "username",
                "password",
                    "user_agent"]:
                value = getattr(botinfo, cred)
                dh.insert("configurations", [[cred, value]])
            dh.insert("configurations", [["remember", "true"]])
            print("Successfully imported credentials")
        except Exception as e:
            self.logger.error("Error importing: {}".format(e))


if __name__ == "__main__":
    C = CommandLineInterface()
