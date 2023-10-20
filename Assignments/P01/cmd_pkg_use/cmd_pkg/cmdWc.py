def wc(**kwargs):
    
    if "params" in kwargs:
        params = kwargs["params"]
        
        flags = kwargs["flags"]
        if len(params) < 1:
            return "Usage: wc -w filename or wc -l filename"
        if "--help" in flags:
            help_message = """
            wc - Print newline, word, and byte counts for files
            
            Usage: wc [OPTIONS] [FILE]
            
            Options:
              --help     Display this help message and exit.
              -l         Count lines.
              -w         Count words.
              -c         Count bytes.
            
            Examples:
              wc file.txt         # Display newline, word, and byte counts for file.txt
              wc -l file.txt      # Display line count for file.txt
              wc -w file.txt      # Display word count for file.txt
              
            """
            return help_message
        if flags[0] not in ['-w','-l']:
            return "Usage: wc -w filename or wc -l filename"
        else:
            filename = params[0]
            
            try:
                with open(filename, 'r') as file:
                      # Split on spaces only
                    word_count=0
                    lines = file.readlines()
                    for line in lines:
                        
                        words = line.split(' ')
                        
                        word_count+=len(words)
                    if "l" in flags[0]:
                        return f"Lines count: {len(lines)}"
                    else:
                        return f"words count: {word_count}"
            except FileNotFoundError:
                return f"File not found: {filename}"
    else:
        return "Usage: wc -w [filename]"
