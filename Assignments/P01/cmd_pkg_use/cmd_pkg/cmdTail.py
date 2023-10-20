# Define the "head" command function
def tail(**kwargs):
    if "params" in kwargs:
        params = kwargs["params"]
        flags = kwargs["flags"]
        if "--help" in flags:
            help_message = """
            tail - Display the end of a file
            
            Usage: tail [OPTIONS] [FILE]
            
            Options:
              --help     Display this help message and exit.
              -n NUM     Display the last NUM lines (default is 10).
            
            Examples:
              
              tail -n 20 file.txt   # Display the last 20 lines
            """
            return help_message
        if "-n" in flags:
            try:
                if ".txt" in params[0]:
                    length =len(params)
                    n = int(params[length-1])
                    file_names = params[:length-1]
                else:
                    n = int(params[0])
                    file_names = params[1:]
                    
                for file_name in file_names:
                    lis =[]
                    try:
                        with open(file_name, 'r') as file:
                            lines = file.readlines()
                            for line in lines[-n:]:
                                lis.append(line.rstrip('\n'))
                    except FileNotFoundError:
                        lis.append(f"File not found: {file_name}")
                    except Exception as e:
                        lis.append(f"Error reading {file_name}: {str(e)}")
                    return '\n'.join(lis)
            except Exception as e :
                return "Usage: tail -n [number] [file1] [file2] ..."
        else:
            return "Usage: tail -n [number] [file1] [file2] ..."
    else:
        return "Usage: tail -n [number] [file1] [file2] ..."
