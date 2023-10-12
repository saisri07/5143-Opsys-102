#!/usr/bin/env python
import subprocess
import platform
import os

def pwd(**kwargs):
    """This is my manpage entry for the pwd command
    """
    if "params" in kwargs:
        params = kwargs["params"]
        flags = kwargs["flags"]
        if "--help" in flags:
            help_message = """
            pwd - Print the current working directory
            
            Usage: pwd [OPTIONS]
            
            Options:
              --help     Display this help message and exit.
            
            Examples:
              pwd         # Print the current working directory
            """
            return help_message
    current_directory = os.getcwd()
    return current_directory
    


# if __name__=='__main__':
#     print(pwd())