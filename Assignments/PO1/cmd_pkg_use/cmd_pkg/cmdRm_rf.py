import os
import shutil

def rm(**kwargs):
    if "params" in kwargs:
        params = kwargs["params"]
        
        if "--help" in kwargs["flags"]:
            help_message = """
            rm - Remove files or directories
            
            Usage: rm [OPTIONS] FILE [FILE2 ...]
            
            Options:
              --help     Display this help message and exit.
              -r         Remove directories and their contents recursively.
              -f         Forcefully remove files or directories.
            
            Examples:
              
              rm -rf dir/         # Forcefully remove directory dir and its contents
            """
            return help_message
        if "-rf" in  kwargs["flags"]:
            for item in params:
                try:
                    if os.path.isdir(item):
                        shutil.rmtree(item)
                        return f"Removed directory and its contents: {item}"
                    elif os.path.isfile(item):
                        os.remove(item)
                        return f"Removed file: {item}"
                    else:
                        return f"Not found: {item}"
                except Exception as e:
                    return f"Error removing '{item}': {str(e)}"
        else:
            return "Usage: rm -rf [file_or_directory1] [file_or_directory2] ..."
    else:
        return "Usage: rm -rf [file_or_directory1] [file_or_directory2] ..."
