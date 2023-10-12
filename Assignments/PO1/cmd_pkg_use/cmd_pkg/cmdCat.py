def cat(**kwargs):
    if "params" in kwargs:
        params = kwargs["params"]
        flags = kwargs["flags"]
        if "--help" in flags:
            help_message = """
            cat - Concatenate and display the content of files
            
            Usage: cat [OPTIONS] [file1] [file2] ...
            
            Options:
              --help     Display this help message and exit.
            """
            return help_message
        output =[]
        
        for file_name in params:
            try:
                
            
                with open(file_name, 'r') as file:
                    content = file.read()
                    output.append(content)
            except FileNotFoundError:
                return f"File not found: {file_name}"
            except Exception as e:
                return f"Error reading {file_name}: {str(e)}"
        return output
    else:
        return "Usage: cat [file1] [file2] ..."
