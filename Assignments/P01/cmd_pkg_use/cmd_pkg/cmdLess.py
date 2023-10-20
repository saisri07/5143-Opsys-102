def less(**kwargs):
    if "params" in kwargs:
        params = kwargs["params"]
        flags = kwargs["flags"]
        if "--help" in flags:
            help_message = """
            less - Display text files with paging
            
            Usage: less [OPTIONS] [FILE]
            
            Options:
              --help     Display this help message and exit.
            
            Examples:
              less file.txt         # Display the contents of file.txt
            """
            return help_message
        for file_name in params:
            try:
                with open(file_name, 'r') as file:
                    lines = file.readlines()
                    page_size = 10  # Number of lines to display at a time
                    start_line = 0

                    while start_line < len(lines):
                        end_line = min(start_line + page_size, len(lines))
                        page = lines[start_line:end_line]
                        
                        output=""
                        for line in page:
                            output += line
                        print(output)
                        
                        user_input = input("\nPress 'q' to quit, 'n' for the next page: ")
                        
                        if user_input == 'q':
                            
                            return "bye"
                        elif user_input == 'n':
                            start_line += page_size
                        else:
                            return "Invalid input. Press 'q' to quit, 'n' for the next page."
            except FileNotFoundError:
                return f"File '{file_name}' not found."
    else:
        return "Usage: less [directory_path]"

if __name__ == "__main__":
    file_name = input("Enter the file name: ")
    less(file_name)
