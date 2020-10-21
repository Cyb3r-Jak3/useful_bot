"""Command CLI for useful_bot"""
# External
import sys
import time
import praw

# Internal
import datahandler as dh
import logmaker
import main
import botinfo  # pylint: disable=import-error
import downvote


def search() -> None:
    """
    Find all data in the tables
    """
    tables = dh.table_fetch()
    table = input("Available tables are {}. \nEnter the table: ".format(tables))
    if table in tables:
        print("Retrieving {}".format(table))
        retrieved = dh.fetch(table, "*")
        if len(retrieved) == 0:
            print("The table was empty")
        else:
            for _, row in enumerate(retrieved):
                print(retrieved[row], "\n")
    else:
        print("Enter a valid table")


class CommandLineInterface:
    """ "
    Class that handles the command line interactions
    """

    def __init__(self):
        self.logger = logmaker.make_logger("CLI")
        self.logger.debug("Starting CLI")
        # Connect to db.
        dh.create()
        # Imports the credentials
        try:
            if sys.argv[1].lower() == "import":
                self.cred_import()
                return
        except IndexError:
            self.logger.debug("Did not set import")
        # Start praw object using credentials in data base.
        self.reddit = self.setup_praw()
        self.run()

    def run(self) -> None:
        # pylint: disable=too-many-branches,too-many-statements
        """
        Main Menu that calls all the sub-functions
        """
        try:
            main.SUBREDDIT_CHOICE = self.fetch_config("subreddit")
        except ValueError:
            main.SUBREDDIT_CHOICE = botinfo.subreddit
        main.reddit = self.reddit
        main.subreddit = main.reddit.subreddit(main.SUBREDDIT_CHOICE)
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
        print("change subreddit")
        print()
        while True:
            command = input("> ").lower()
            (
                main.comments_replied_to,
                main.posts_replied_to,
                main.ignored,
                main.mentions,
                main.additional_responses,
                main.comment_responses,
                main.post_responses,
            ) = main.get_previous()
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
                        search()
                    if "change subreddit" in command:
                        self.replace_subreddit()
                    if command == "exit":
                        main.stop_bot(True)
                    if "-" not in command:
                        loop = False
                    time.sleep(delay * 60)
                except KeyboardInterrupt:
                    print()
                    loop = False

    def setup_praw(
        self,
    ) -> praw.Reddit:
        """
        Completed the same process as in the main.py file just
        auto uses credentials from the configuration table
        Returns
        -------
            Praw client that is used to complete actions
        """
        try:
            client_id = self.fetch_config("client_id")
            client_secret = self.fetch_config("client_secret")
            password = self.fetch_config("password")
            username = self.fetch_config("username")
            user_agent = self.fetch_config("user_agent")
            reddit_client = praw.Reddit(
                client_id=client_id,
                client_secret=client_secret,
                password=password,
                username=username,
                user_agent=user_agent,
            )
            reddit_client.user.me()  # Test authentication.
            self.logger.info("Successfully logged in")
            return reddit_client
        except Exception as err:
            self.logger.error("Exception %s occurred on login", err)
            main.stop_bot(False)

    def fetch_config(self, find) -> str:  # Fetches the values needed to run the bot
        """
        Fetches the value `find` and returns the string for the needed value
        Parameters
        ----------
        find: str
            configuration value needed
        Returns
        -------
            The value that is mapped to find
        """
        try:
            values = dh.fetch("configurations", "value")
            ids = dh.fetch("configurations", "id")
            return values[ids.index(find)]
        # The exception is called if there are no values in configurations table
        except ValueError:
            value = input("Enter " + find + ": ")
            dh.insert("configurations", [[find, value]])
            return value
        except Exception as err:
            self.logger.error("There was an error retrieving credentials: %s ", err)
            main.stop_bot()

    def response_add(self) -> None:
        """
        Creates addition response for messages, comments, or posts
        """
        to_add = []
        choice = input(
            "What kind of response do you want to set; Comment, Post, or Message: "
        ).lower()
        if choice.startswith("c"):
            table = "comment_responses"
        elif choice.startswith("p"):
            table = "post_responses"
        elif choice.startswith("m"):
            table = "message_responses"
        else:
            print("Exiting: no valid selection")
            self.run()
        to_add.append(input("Enter what the keyword you want to trigger a response: "))
        if table == "message_responses":
            to_add.append(input("Enter what you want the reply subject to be: "))
        to_add.append(input("Enter the message for the reply: "))
        if table == "message_responses":
            print(
                "For the message response, \n' {0} ' is the trigger word/phrase."
                "' {1} ' is the response subject and ' {2} ' is the response body. \n"
                "Enter Y to conform, R to redo or N to cancel.".format(
                    to_add[0], to_add[1], to_add[2]
                )
            )
        else:
            print(
                "For the comment/post response, \n' "
                "{0} ' is the trigger word/phrase. The response body is ' {1} ' \n"
                "Enter Y to confirm, R to redo or N to cancel.".format(
                    to_add[0], to_add[1]
                )
            )
        if input().lower() == "y":
            dh.insert(table, [to_add])
        elif input().lower() == "r":
            self.response_add()

    def response_delete(self) -> None:
        """
        Deletes unwanted responses from the database
        Returns
        -------

        """
        choice = input(
            "Enter the response type you want to remove: Comment, Post, or Message\n"
        ).lower()
        if choice.startswith("c"):
            table = "comment_responses"
        elif choice.startswith("p"):
            table = "post_responses"
        elif choice.startswith("m"):
            table = "message_responses"
        else:
            print("No valid table selected")
            self.run()
        retrieved = dh.fetch(table, "*")
        for item, _ in enumerate(retrieved):
            print(item + 1, retrieved[item], "\n")
        try:
            choice = int(input("Enter the number of the response you wish to delete: "))
            print(
                "You have selected ",
                retrieved[choice - 1],
                "\n" + "Enter (y)es to delete: ",
            )
        except (ValueError, IndexError):
            print("Enter a valid number")
            self.run()
        confirm = input().lower()
        if confirm.startswith("y"):
            dh.delete(
                "message_responses",
                "keyword",
                "'{keyword}'".format(keyword=retrieved[choice - 1][0]),
            )
            print("Deleted")

    def cred_import(self) -> None:  # Imports credentials from the botinfo
        """
        Imports the credentials from botinfo.py to the database.
        """
        try:
            for cred in [
                "client_id",
                "client_secret",
                "username",
                "password",
                "user_agent",
            ]:
                try:
                    value = getattr(botinfo, cred)
                    dh.insert("configurations", [[cred, value]])
                except ValueError:
                    self.fetch_config(cred)
            dh.insert("configurations", [["remember", "true"]])
            print("Successfully imported credentials")

        except Exception as err:
            self.logger.error("Error importing: %s", err)

    def replace_subreddit(self) -> None:
        """
        Sets the new subreddit to monitor
        """
        new = input("Enter the new subreddit: ")
        dh.delete("configurations", "id", "'subreddit'")
        dh.insert("configurations", [["subreddit", new]])
        print("Subreddit changed to: {}".format(self.fetch_config("subreddit")))


if __name__ == "__main__":
    C = CommandLineInterface()
