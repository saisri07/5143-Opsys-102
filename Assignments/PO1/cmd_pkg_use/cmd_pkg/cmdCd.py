import os

def cd(**kwargs):
    if "params" in kwargs:
        params = kwargs["params"]
        flags = kwargs["flags"]
        if "--help" in flags:
            help_message = """
            cd - Change the current working directory
            
            Usage: cd [DIRECTORY]
            
            Options:
              --help     Display this help message and exit.
            """
            return help_message
        if len(params) > 0:
            try:
                if params[0] == "~":
                    os.chdir(os.path.expanduser("~"))  # Change to the user's home directory
                elif params[0] == "run":
                    path = r"/mnt/c/Users/User/Desktop/opsys/5143-Opsys102/Assignments/P01/cmd_pkg_use"
                    os.chdir(path)
                elif params[0] == "opsys":
                    path = r"/mnt/c/Users/User/Desktop/opsys"
                    os.chdir(path)
                else:
                    os.chdir(params[0])
                return f"Current directory changed to: {os.getcwd()}"
            except FileNotFoundError:
                return f"Directory not found: {params[0]}"
            except Exception as e:
                return f"Error changing directory: {str(e)}"
        else:
            return "Usage: cd [directory_path]"
    else:
        return "Usage: cd [directory_path]"
        
