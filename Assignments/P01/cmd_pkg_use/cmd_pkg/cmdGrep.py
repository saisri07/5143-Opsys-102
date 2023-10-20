# cmd_pkg/cmdGrepL.py

def grep(**kwargs):
    if "params" in kwargs:
        params = kwargs["params"]
        flags = kwargs["flags"]
        if "--help" in flags:
            help_message = """
            grep - Search for text patterns in files
            
            Usage: grep [OPTIONS] PATTERN FILE
            
            Options:
              --help     Display this help message and exit.
              -i         Ignore case while searching.
              -n         Show line numbers.
            
            Examples:
              grep "pattern" file.txt       # Search for "pattern" in file.txt
              grep -l "pattern" file.txt    # Search files
              
            """
            return help_message
        if len(flags) != 0:
            for f in flags:
                if f not in ["-l"]:
                    return "Usage: grep  pattern filename or grep -l pattern filename"
        if len(params) < 2:
            return "Usage: grep -l pattern filename"
        else:
            pattern= params[0].strip('\'"')
            files=params[1:]
            try:
                output =[]
                matching_files = []
                for filename in files:
                    with open(filename, 'r') as file:
                        for line in file:
                            if pattern in line:
                                output.append(f"{line}")
                                matching_files.append(filename)
                                
                                  # Break after the first match is found

                if matching_files:
                    if len(flags) != 0:
                        if flags[0] == "-l":
                          return matching_files
                    return output
            except FileNotFoundError:
                return f"File not found: {filename}"
