import os
import shutil

def mv(**kwargs):
    if "params" in kwargs:
        params = kwargs["params"]
        flags = kwargs["flags"]
        if "--help" in flags:
            help_message = """
            mv - Move or rename files and directories
            
            Usage: mv [OPTIONS] SOURCE DEST
            
            Options:
              --help     Display this help message and exit.
            
            Examples:
              mv file.txt newfile.txt       # Rename file.txt to newfile.txt
              mv source_dir/ dest_dir/      # Move source_dir and its contents to dest_dir
            """
            return help_message

        if len(params) == 2:
            source = params[0]
            destination = params[1]
            try:
                shutil.move(source, destination)
                return f"Moved '{source}' to '{destination}'"
            except FileNotFoundError:
                return f"File not found: {source}"
            except Exception as e:
                return f"Error moving '{source}' to '{destination}': {str(e)}"
        else:
            return "Usage: mv [source] [destination]"
    else:
        return "Usage: mv [source] [destination]"
