
## 16 October 2023
 
## 5143 Filesystem - Implementation of a Virtual Filesystem

## Group Members
- Sai Neeraj Chandragiri
- Sai Teja Sripathi
- Naveen kumar Poka
  
## Introduction
This python project will implement a virtual filesystem. We used Sqlite to create a database for the filesystem's storage. We have inserted some sample files and folders in to the database, we replicated some shell comands on those files and folders.


## Prerequisites

- Python 3.x
- vs code

## Requirements

- humanize
- prettytable
- rich


## Files

|   File   | Description |
| :---: | ----------- | 
|  fileSystem.py  |	File System class where all functions related to file system are implemented.     | 
|   sqliteCRUD.py |	 python file containing class to interact with the sqlite database.     |
|  walkthrough.py  |  file to present an walkthrough of file system functionality implemented.      |



## Commands

|   Command   | Description | Author | 
| :---: | ----------- | ---------------------- |   
|ls|	listing files and directories | Sai Neeraj	|
|mkdir|	Make folder  on current directory or desired location|Sai Teja	|
|cd	|Change the shell working directory |Sai Teja	|
|cd..	|Moving up one directory level |Sai Teja	|
|pwd	|Show current working directory |Sai Neeraj	|
| History  | shows history of commands used in terminal | Sai Neeraj |   
|chmod| chmod is used to change the file permissions | Naveen |
|cp|Copy SOURCE to DEST, or multiple SOURCE(s) to DIRECTORY| Naveen |
|mv| Rename SOURCE to DEST, or move SOURCE(s) to DIRECTORY | Naveen |
|rm|It is used to delete files/directories| Sai Teja |
|Insert|Inserts the file from local to database| Sai Teja |



## Steps to execute

- python3 walkthrough.py
- Hit Enter to continue after each command 
