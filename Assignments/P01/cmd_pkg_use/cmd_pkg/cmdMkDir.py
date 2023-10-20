import os

def mkdir(**kwargs):
    if "params" in kwargs:
        params = kwargs["params"]
        flags = kwargs["flags"]
        if "--help" in flags:
            help_message = """
            mkdir - Create directories
            
            Usage: mkdir [OPTIONS] DIRECTORY [DIRECTORY2 ...]
            
            Options:
              --help     Display this help message and exit.
              -p         Create parent directories if they don't exist.
            
            Examples:
              mkdir new_dir            # Create a directory named new_dir
              
            """
            return help_message
        for directory_name in params:
            try:
                os.mkdir(directory_name)
                return f"Directory '{directory_name}' created successfully."
            except FileExistsError:
                return f"Directory '{directory_name}' already exists."
            except Exception as e:
                return f"Error creating directory '{directory_name}': {str(e)}"
    else:
        return "Usage: mkdir [directory_name1] [directory_name2] ..."
