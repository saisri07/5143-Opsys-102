## 28 Sep 2023

## 5143 Shell Project

## Group Members
- Sai Neeraj Chandragiri
- Sai Teja
- Naveen kumar Poka
  
## Introduction

The Python command-line shell is a simple interactive shell that allows you to execute system commands and some built-in functions. This shell serves as an example of how to parse commands from the command prompt and invoke the corresponding command functions with parameters.

Please note that the built-in commands provided in this shell are for demonstration purposes only. You are encouraged to replace them with your own commands or integrate external commands as needed for your project.

## Features

- Interactive command-line interface.
- Supports executing system commands and built-in functions.
- Basic piping functionality to chain commands together.
- Command history tracking and execution using command numbers.

## Prerequisites

- Python 3.x
- vs code


### Commands:


|   Command   | Description | Author | 
| :---: | ----------- | ---------------------- |   
|ls|	listing files and directories |Sai Neeraj	|
|mkdir|	Make folder  on current directory or desired location|Sai Teja	|
|cd	|Change the shell working directory |Sai Teja	|
|grep	|Search for patterns in a  file |Sai Neeraj	|
|pwd	|Show current working directory |Sai Teja	|
|command > file	| redirect standard output to a file | Sai Neeraj| 
|command1 \| command2	|pipe the output of command1 to the input of command2| Sai Neeraj |
| History  | shows history of commands used in terminal | Sai Neeraj |   
| wc | shows word character and length  in the file | Naveen |  |
|Sort | Sort command will sort the words or numbers depending on flag in terminal | Naveen|
|!x |  executable command is used the use commands from the history |Naveen |
|chmod| chmod is used to change the file permissions |Sai Neeraj |
| whoami | Displays user, group and privileges information for the user who is currently logged | Naveen|
|cat|	 Concatenate FILE(s) to standard output |Naveen|
|less|allows to view and navigate through text files |Naveen|
|head|Print the first 5 lines of each FILE to standard output |Naveen|
|tail|Print the last 5 lines of each FILE to standard output |Sai Teja|
|cp|Copy SOURCE to DEST, or multiple SOURCE(s) to DIRECTORY| Sai Teja |
|mv| Rename SOURCE to DEST, or move SOURCE(s) to DIRECTORY | Sai Teja |
|rm|It is used to delete files/directories|Sai Neeraj|

## Examples

### Running Built-in Commands

To run a built-in command, simply enter the command name followed by any required parameters or flags. For example:

- List files in the current directory:

  bash
  $: ls
  

- Display the contents of a file:

  bash
  $: cat filename.txt
  

- Print the current working directory:

  bash
  $: pwd
  

### Piping Commands

You can chain commands together using the pipe (|) symbol. For example:

- Count the number of lines in a file and then sort the lines:

  bash
  $: wc -l input.txt | sort







### Command History

The shell keeps track of command history. To execute a command from history, prefix the command number with an exclamation mark (!). For example:

- Execute the command from history with number 3:

  bash
  $: !3


