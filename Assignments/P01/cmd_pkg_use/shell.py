#!/usr/local/bin/python3

"""
This file gives and idea of how to parse commands from the command prompt and
the invoke the proper command function with parameters. 

The functions are examples only that call the built in commands, which is not
acceptable for your project. Again, this file is just an example of parsing a 
command and calling the correct function with params.

It may give you a little insight into organizing your shell code as well.

"""
import threading
import sys
import platform
import subprocess
import readline
from cmd_pkg.cmdMkDir import mkdir
from cmd_pkg.cmdMv import mv
from cmd_pkg.cmdLess import less
from cmd_pkg.cmdCd import cd
from cmd_pkg.cmdGrep import grep
from cmd_pkg.cmdCp import cp
from cmd_pkg.cmdWhoami import whoami
from cmd_pkg.cmdSort import sort 
from cmd_pkg.cmdHead import head
from cmd_pkg.cmdTail import tail
from cmd_pkg.cmdRm_rf import rm
from cmd_pkg.cmdWc import wc
from cmd_pkg.cmdChmod import chmod
from cmd_pkg.cmdCat import cat
from cmd_pkg.cmdHistory import history as custom_history
from cmd_pkg.cmdPwd import pwd as custom_pwd
from cmd_pkg.cmdLs import ls as custom_ls
import signal
from subprocess import call  # FOR DEMO PURPOSES ONLY!




def exit(**kwargs):
    sys.exit()

data = []
class CommandHelper(object):
    def __init__(self):
        self.commands = {}
        self.commands["ls"] = custom_ls
        self.commands["cat"] = cat
        self.commands["pwd"] = custom_pwd
        self.commands["exit"] = exit
        self.commands["mkdir"] = mkdir
        self.commands["cd"] = cd
        self.commands["mv"] = mv
        self.commands["cp"] = cp
        self.commands["rm"] = rm
        self.commands["less"] = less
        self.commands["wc"] = wc
        self.commands["head"] = head
        self.commands["tail"] = tail
        self.commands["grep"] = grep
        self.commands["chmod"] = chmod
        self.commands["sort"] = sort
        self.commands["whoami"] = whoami
        self.history = []
        signal.signal(signal.SIGINT, self.handle_ctrl_c)
        
    def handle_ctrl_c(self, signum, frame):
        sys.exit()
        
    def invoke(self, **kwargs):
        if "cmd" in kwargs:
            cmd = kwargs["cmd"]
        else:
            cmd = ""

        if "params" in kwargs:
            params = kwargs["params"]
        else:
            params = []
            
        if "flags" in kwargs:
            flags = kwargs["flags"]
        else:
            flags = []

        if "thread" in kwargs:
            thread = kwargs["thread"]
        else:
            thread = False
        
        if "stdin" in kwargs:
            stdin = kwargs["stdin"]
            if type(stdin) is not list:
                files =stdin.split(" ")
                for file in files:
                    params.append(file)
            else:
                for out in stdin:
                  params.append(out)
            
            
        else:
            thread = False
            
        
        # One way to invoke using dictionary
        
        self.history.append(cmd)
        
        if not thread:
            return self.commands[cmd](params=params, flags=flags)
        else:
            # Using a thread ****** broken right now *********
            if len(params) > 0:
                c = threading.Thread(target=self.commands[cmd], args=params, kwargs={"flags": flags})
            else:
                c = threading.Thread(target=self.commands[cmd])
                
            c.start()
            c.join()
            return c

    def exists(self, cmd):
        
        return cmd in self.commands
    
    def addHistory(self, cmd, length):
        
        file_object = open(r'/mnt/c/Users/User/Desktop/opsys/History.txt', 'a')
        if  length-1> 0 :
            file_object.write("\n")
        
        file_object.write(f"{length}. {cmd}")
        
    def print_history(self):
        return (tail(params=[r'/mnt/c/Users/User/Desktop/opsys/History.txt', "10"], flags=["-n"]))
        
    
    # def parse_command(self, cmd):
    #     parts = cmd.strip().split()
    #     cmd_name = parts[0]
    #     cmd_params = []
    #     cmd_flags = []
        
    #     for part in parts[1:]:
            
    #         if part.startswith('-'):
    #             # This part is a flag
    #             cmd_flags.append(part)
    #         else:
                
    #             # This part is a parameter
    #             cmd_params.append(part)

    #     return cmd_name, cmd_params, cmd_flags
    
    def parse_command(self, cmd):
        parts = cmd.strip().split()
        cmd_name = parts[0]
        cmd_params = []
        cmd_flags = []
        in_quotes = False  # Variable to track if we are inside double quotes

        for part in parts[1:]:
            if part.startswith('-'):
                # This part is a flag
                cmd_flags.append(part)
            else:
                if part.startswith('"'):
                    # Start of double-quoted parameter
                    in_quotes = True
                    param = part[1:]  # Remove the opening double quote
                elif part.endswith('"'):
                    # End of double-quoted parameter
                    param = part[:-1]  # Remove the closing double quote
                    in_quotes = False
                elif in_quotes:
                    # Inside double quotes, add to the current parameter
                    param += " " + part
                else:
                    # Normal parameter outside of quotes
                    param = part

                cmd_params.append(param)

        return cmd_name, cmd_params, cmd_flags



    def execute_command(self, cmd_str, thread=False, output_file=None):
        # Split the input command string by pipes ('|')
            commands = cmd_str.split('|')

            # Initialize the previous command's output as None
            prev_output = None

            for cmd in commands:
                # Parse the command to extract name, parameters, and flags
                cmd_name, cmd_params, cmd_flags = ch.parse_command(cmd)

                # Check if the command exists
                if cmd.strip() == "history":
                    prev_output = "/mnt/c/Users/User/Desktop/opsys/History.txt"
                else:
                    if ch.exists(cmd_name):
                        # If this is the first command, pass the parameters and flags
                        if prev_output is None:
                            prev_output = ch.invoke(cmd=cmd_name, params=cmd_params, flags=cmd_flags, thread=False)
                            
                        else:
                            # Redirect the output of the previous command to the current command
                            kwargs = {"cmd": cmd_name, "params": cmd_params, "flags": cmd_flags, "thread": False}
                            kwargs["stdin"] = prev_output
                            
                            prev_output = ch.invoke(cmd=cmd_name, params=cmd_params, flags=cmd_flags, stdin=prev_output, thread=False)
                    else:
                        print("Error: Command '{}' doesn't exist.".format(cmd_name))
                        break
                
            if output_file:
                with open(output_file, "w") as file:
                    if type(prev_output) is list:
                        str = '\n'.join(prev_output)
                        file.write(str)
                    else:
                        file.write(prev_output)
                        
            if type(prev_output) is list:
                return " ".join(prev_output)

            return prev_output


if __name__ == "__main__":
    ch = CommandHelper()

    while True:
        # Get input from the terminal
        cmd = input("$: ")
        readline.add_history(cmd)
        x=(wc(params=[r"/mnt/c/Users/User/Desktop/opsys/History.txt"], flags=["-l"])).split(":")
        
        length= (int)(x[1].strip())
        ch.addHistory(cmd, length+1)

        if cmd.startswith("!"):
            try:
                # Extract the command number (x)
                history_number = int(cmd[1:])
                
                if history_number > 0 and history_number <= length+1:
                    # Get the corresponding command from history
                    with open(r"/mnt/c/Users/User/Desktop/opsys/History.txt", 'r') as file:
                      # Split on spaces only
                    
                        lines = file.readlines()
                        line = lines[history_number - 1]
                        str =line.split(".")
                        cmd=str[1].strip()
                    
                    print(f"Executing: {cmd}")
                else:
                    print("Error: Invalid history number.")
            except ValueError:
                print("Error: Invalid history format.")

        params = []
        
        if '>' in cmd:
            cmd_parts = cmd.split('>')
            cmd = cmd_parts[0].strip()
            output_file = cmd_parts[1].strip()
            print(f"Redirecting output to: {output_file}")
            print(ch.execute_command(cmd, output_file=output_file))

        # Handle command piping
        else:
            if '|' in cmd:
                print(ch.execute_command(cmd))
            else:
                # If no piping, execute a single command
                cmd_name, cmd_params, cmd_flags = ch.parse_command(cmd)
                if cmd.strip() == "history":
                    print(ch.print_history())
                
                elif ch.exists(cmd_name):
                    # Handle commands with parameters and flags
                    
                    # if cmd_name == "cd":
                    #     # Handle flags and parameters for the 'cd' command
                    #     directory = cmd_params[0] if cmd_params else "~"
                    #     if "-l" in cmd_flags:
                    #         # Handle the '-l' flag
                    #         print(f"Changing directory to {directory} (with -l flag)")
                    #     else:
                    #         print(f"Changing directory to {directory}")
                    #     # Execute the 'cd' command
                    #     output=(ch.invoke(cmd=cmd_name, params=[directory], thread=False))
                    #     if type(output) is list:
                    #         print(" ".join(output))
                    #     else:
                    #         print(output)
                    # # ... (other commands with parameters and flags)
                    # else:
                    output=(ch.invoke(cmd=cmd_name, params=cmd_params, flags=cmd_flags, thread=False))
                    if type(output) is list:
                        print(" ".join(output))
                    else:
                        print(output)
                else:
                    print("Error: command %s doesn't exist." % (cmd))


