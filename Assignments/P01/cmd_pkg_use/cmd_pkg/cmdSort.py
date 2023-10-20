

def sort(**kwargs):
    if "params" in kwargs:
        params = kwargs["params"]
        flags = kwargs["flags"]
        if "--help" in flags:
            help_message = """
            sort - Sort lines of text files
            
            Usage: sort [OPTIONS] [FILE]
            
            Options:
              --help     Display this help message and exit.
              -r         Reverse the sorting order.
            
            Examples:
              sort file.txt         # Sort lines in file.txt in ascending order
              
            """
            return help_message
        if len(params) != 1:
            return "Usage: sort <filename>"
        else:
            filename = params[0]
            try:
                output =""
                with open(filename, 'r') as file:
                    lines = file.readlines()
                    lines.sort()
                    sorted_content = ''.join(lines)
                    output +=sorted_content
                return output
            except FileNotFoundError:
                print(f"File not found: {filename}")
