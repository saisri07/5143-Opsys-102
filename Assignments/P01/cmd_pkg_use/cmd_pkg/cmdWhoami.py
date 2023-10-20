import os
import getpass
def whoami(**kwargs):
    if "params" in kwargs:
        params = kwargs["params"]
        flags = kwargs["flags"]
        if "--help" in flags:
            help_message = """
            whoami - Print the current user's username
            
            Usage: whoami [OPTIONS]
            
            Options:
              --help     Display this help message and exit.
            
            Examples:
              whoami       # Print the current user's username
            """
            return help_message
    username =getpass.getuser()
    return f"Current user: {username}"
