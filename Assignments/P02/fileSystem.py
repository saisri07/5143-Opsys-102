# Filesystem Starter Class

from sqliteCRUD import SQLiteCrud
import humanize
from prettytable import PrettyTable
import datetime

class FileSystem:
    def __init__(self,db_name=None):
        if not db_name:
            self.db_name = "filesystem.sqlite"
        else:
            self.db_name = db_name
        self.crud = SQLiteCrud(self.db_name)

        table_name = "files_data"
        columns = ["id INTEGER PRIMARY KEY", "pid INTEGER NOT NULL", "filename TEXT NOT NULL", "created_date TEXT NOT NULL", "modified_date TEXT NOT NULL", "size REAL NOT NULL","type TEXT NOT NULL","owner TEXT NOT NULL","groop TEXT NOT NULL","permissions TEXT NOT NULL", "content BLOB"]

        data = [
        (1, 0, 'Folder1', str(datetime.datetime.now()), str(datetime.datetime.now()), 0.0, 'folder', 'user1', 'group1', 'drwxr-xr-x', None),
        (2, 1, 'File1.txt', str(datetime.datetime.now()), str(datetime.datetime.now()), 1024.5, 'file', 'user1', 'group1', '-rw-r--r--', None),
        (3, 1, 'File2.txt', str(datetime.datetime.now()), str(datetime.datetime.now()), 512.0, 'file', 'user2', 'group2', '-rw-rw-r--', None),
        (4, 0, 'Folder2', str(datetime.datetime.now()), str(datetime.datetime.now()), 0.0, 'folder', 'user2', 'group2', 'drwxr-xr--', None),
        (5, 4, 'File3.txt', str(datetime.datetime.now()), str(datetime.datetime.now()), 2048.75, 'file', 'user3', 'group3', '-rw-r--r--', None),
        (6, 4, 'File4.txt', str(datetime.datetime.now()), str(datetime.datetime.now()), 4096.0, 'file', 'user3', 'group3', '-rw-r--r--', None),
        (7, 0, 'Folder3', str(datetime.datetime.now()), str(datetime.datetime.now()), 0.0, 'folder', 'user4', 'group4', 'drwxr-x---', None),
        (8, 7, 'File5.txt', str(datetime.datetime.now()), str(datetime.datetime.now()), 8192.0, 'file', 'user4', 'group4', '-rw-------', None),
        (9, 0, 'Folder4', str(datetime.datetime.now()), str(datetime.datetime.now()), 0.0, 'folder', 'user5', 'group5', 'drwxr-xr-x', None),
        (10, 9, 'File6.txt', str(datetime.datetime.now()), str(datetime.datetime.now()), 3072.25, 'file', 'user5', 'group5', '-rwxr-xr--', None),
        (11, 0, 'Sample1.txt', str(datetime.datetime.now()), str(datetime.datetime.now()), 3072.25, 'file', 'user5', 'group5', '-rwxr-xr--', None),
        (12, 0, '.a.txt', str(datetime.datetime.now()), str(datetime.datetime.now()), 5072.25, 'file', 'user5', 'group5', '-rwxr-xr--', None)
        ]

        
        self.crud.drop_table(table_name)
        self.crud.create_table(table_name, columns)

        for row in data:
            self.crud.insert_data(table_name, row)
        
        self.cwd = "home"
        self.cwdid = 0
        self.crud.formatted_print(table_name)
        
        self.history = []
    
    def __del__(self):
        self.crud.close_connection()

    def __getFileId(self,**kwargs):
        """ Find a file id using current location + name
        """
        name = kwargs.get('name', None)
        if name == '.':
            return FileId
        
        if name.startswith("/home") or name.startswith("home"):
            FileId = 0
            name.strip("/")
            name = name.replace("home","")
        else:
            FileId = self.cwdid

        for name_part in name.split("/"):
            if name_part:
                if name_part == ".":
                    continue
                elif name_part == "..":
                    FileId = FileId
                else:
                    query = f"SELECT id FROM files_data WHERE filename = '{name_part}' AND pid = {FileId};"
                    self.crud.cursor.execute(query)
                    result = self.crud.cursor.fetchone()
                    if result:
                        FileId = result[0]
                    else:
                        return None
        if '..' not in name and FileId == self.cwdid:
            return None
        return FileId

    def __delete_directory(self, directory_id):
        # Check if the directory exists
        self.crud.cursor.execute("SELECT id FROM files_data WHERE id = ? AND type = 'folder'", (directory_id,))
        dir_exists = self.crud.cursor.fetchone()

        if dir_exists:
            # List contents of the directory 
            self.crud.cursor.execute("SELECT id, type FROM files_data WHERE pid = ?", (directory_id,))
            contents = self.crud.cursor.fetchall()

            for content_id, content_type in contents:
                if content_type == 'file':
                    # Delete file
                    self.crud.cursor.execute("DELETE FROM files_data WHERE id = ?", (content_id,))
                    self.crud.conn.commit()

                elif content_type == 'folder':
                    # Recursively delete subdirectory
                    self.delete_directory(content_id)

            # Delete the directory itself
            self.crud.cursor.execute("DELETE FROM files_data WHERE id = ?", (directory_id,))
            self.crud.conn.commit()

            return "Directory or file deleted successfully."
        else:
            return "Directory not found."

    def convert_permission(self, triple,folder):
        """
        Convert a triple of numbers (e.g., 644) into the 'rwx' equivalent (e.g., 'rw-r--r--').
        
        Args:
            triple (int): A triple of numbers representing permissions (e.g., 644).

        Returns:
            str: The 'rwx' equivalent representation (e.g., 'rw-r--r--').
        """
        if triple < 0 or triple > 777:
            raise ValueError("Invalid permission triple. Must be between 0 and 777.")

        # Convert each digit of the triple to its 'rwx' equivalent
        owner = self.convert_digit(triple // 100)
        group = self.convert_digit((triple // 10) % 10)
        others = self.convert_digit(triple % 10)
        p=owner + group + others
        if folder:
           return "d"+ p
        return "-"+p

    def convert_digit(self, digit):
        """
        Convert a single digit (0-7) into its 'rwx' equivalent.

        Args:
            digit (int): A single digit (0-7).

        Returns:
            str: The 'rwx' equivalent representation.
        """
        if digit < 0 or digit > 7:
            raise ValueError("Invalid digit. Must be between 0 and 7.")

        permission_map = {
            0: '---',
            1: '--x',
            2: '-w-',
            3: '-wx',
            4: 'r--',
            5: 'r-x',
            6: 'rw-',
            7: 'rwx',
        }

        return permission_map[digit]

    def list(self,**kwargs):
        """ List the files and folders in current directory
        """
        long = kwargs.get('long', False)
        all = kwargs.get('all', False)
        human_readable = kwargs.get('human_readable', False)
        
        cols = ["Filename", "Owner", "Permissions", "Size"]
        query = f"SELECT filename, owner, permissions, size, type FROM files_data WHERE pid = {self.cwdid} AND filename NOT LIKE '.%';"
        if long:
            if all:
                query = f"SELECT filename, created_date, modified_date, size, type, owner, groop, permissions FROM files_data WHERE pid = {self.cwdid};"
            else:
                query = f"SELECT filename, created_date, modified_date, size, type, owner, groop, permissions FROM files_data WHERE pid = {self.cwdid} AND filename NOT LIKE '.%';"
            cols = ["Filename", "Created", "Modified", "Size", "Type", "Owner", "Group", "Permissions"]
        # if all:
        #     query.replace("AND filename LIKE '.%'","")
              
        self.crud.cursor.execute(query)
        results = self.crud.cursor.fetchall()

        data = [cols]
        for row in results:
            row = list(row)
            if human_readable:
                row[3] = humanize.naturalsize(row[3])
            
            # if it is a folder
            if row[4] == 'folder':
                row[3] = '[Dir]'
            if not long:
                row = list(row)[:-1]
            data.append(row)

        return data
    
    def mkdir(self, **kwargs):
        """ Create a new directory
        """
        name = kwargs.get('name', None)
        if name:
            query = f"INSERT INTO files_data (pid, filename, created_date, modified_date, size, type, owner, groop, permissions) VALUES ({self.cwdid}, '{name}', '{datetime.datetime.now()}', '{datetime.datetime.now()}', 0.0, 'folder', 'user1', 'group1', 'drw-r--r--');"
            self.crud.cursor.execute(query)
            self.crud.conn.commit()
            return f"Created directory '{name}'"
        else:
            return "mkdir: missing directory name"

    def cd(self, **kwargs):
        """ Change directory
        """
        name = kwargs.get('name', None)
        for name_part in name.split("/"):
            if name_part:
                if name_part == ".":
                    continue
                elif name_part == "..":
                    query = f"SELECT pid FROM files_data WHERE id = {self.cwdid};"
                    self.crud.cursor.execute(query)
                    result = self.crud.cursor.fetchone()
                    if result:
                        self.cwdid = result[0]
                        self.cwd = "/".join(self.cwd.split("/")[:-1])
                    else:
                        return f"cd: {name}: No such file or directory"
                else:
                    new_cwdid = self.__getFileId(name=name_part)
                    if new_cwdid:
                        self.cwdid = new_cwdid
                        self.cwd = self.cwd + "/" + name_part

                    else:
                        print("tesfsd")
                        return f"cd: {name}: No such file or directory"
        return "current directory: " + self.cwd

    def pwd(self):
        """ Get working directory
        """
        return self.cwd

    def mv(self, **kwargs):
        """ Move file or directory
        """
        source = kwargs.get('source', None)
        destination = kwargs.get('destination', None)

        if source and destination:
            source_id = self.__getFileId(name=source)
            destination_id = self.__getFileId(name=destination)
            if source_id and destination_id:
                query = f"UPDATE files_data SET pid = {destination_id} WHERE id = {source_id};"
                self.crud.cursor.execute(query)
                self.crud.conn.commit()

                return f"Moved '{source}' to '{destination}'"
            else:
                return f"mv: No such file or directory. Please check file or folder paths"
        else:
            return "mv: missing arguments"

    def cp(self, **kwargs):
        """ Copy file or directory
        """
        source = kwargs.get('source', None)
        destination = kwargs.get('destination', None)
        
        # get destination id
        destination_id = self.__getFileId(name=destination)
        if destination_id:
            # if destination is a file, return error
            query = f"SELECT type FROM files_data WHERE id = {destination_id};"
            self.crud.cursor.execute(query)
            result = self.crud.cursor.fetchone()
            if result[0] == "file":
                return "cp: cannot overwrite non-directory with directory"
            else:
                # get source id
                source_id = self.__getFileId(name=source)
                if source_id:
                    # if source is a file, copy file
                    
                    query = f"SELECT * FROM files_data WHERE id = {source_id};"
                    self.crud.cursor.execute(query)
                    result = self.crud.cursor.fetchone()
                    query = f"INSERT INTO files_data (pid, filename, created_date, modified_date, size, type, owner, groop, permissions, content) VALUES ({destination_id}, '{result[2]}', '{str(datetime.datetime.now())}', '{str(datetime.datetime.now())}', {result[5]}, '{result[6]}', '{result[7]}', '{result[8]}', '{result[9]}', '{result[10]}');"
                    self.crud.cursor.execute(query)
                    self.crud.conn.commit()

                    
                    # get the id and filename of copied item
                    query = f"SELECT id, filename FROM files_data WHERE pid = {destination_id} AND filename = '{result[2]}';"
                    self.crud.cursor.execute(query)
                    insertion_result = self.crud.cursor.fetchone()
                    if not insertion_result:
                        return "cp: error copying file"

                    inserted_id, inserted_name = insertion_result[0], insertion_result[1]

                    if result[6] == 'folder':
                        query = f"SELECT * FROM files_data WHERE pid = {source_id};"
                        self.crud.cursor.execute(query)
                        results = self.crud.cursor.fetchall()
                        for row in results:
                            if row[6] == 'folder':
                                self.cp(source=f"{source}/{row[2]}", destination=f"{destination}/{inserted_name}")
                            else:
                                query = f"INSERT INTO files_data (pid, filename, created_date, modified_date, size, type, owner, groop, permissions, content) VALUES ({inserted_id}, '{row[2]}', '{str(datetime.datetime.now())}', '{str(datetime.datetime.now())}', {row[5]}, '{row[6]}', '{row[7]}', '{row[8]}', '{row[9]}', '{row[10]}');"
                                self.crud.cursor.execute(query)
                                self.crud.conn.commit()


                    return f"Copied '{source}' to '{destination}'"
        else:
            return "cp: missing destination file operand"

    def rm(self, **kwargs):
        """ remvoe file or directory
        """
        name = kwargs.get('name', None)
        if name:
            name_id = self.__getFileId(name=name)
            if name_id:
                return self.__delete_directory(name_id)
            else:
                return f"rm: cannot remove '{name}': No such file or directory"
        else:
            return "rm: missing file operand"

    def chmod(self,**kwargs):
        """ Change the permissions of a file
            1) will need the file / folder path/name
            2) select permissions from the table where that id exists
        Params:
            name (string) :  id of file or folder
            permission (string) : +x -x 777 644

            if its a triple just overwrite or update table 

        Example:
            +x 
            p = 'rw-r-----'
            p[2] = x
            p[5] = x
            p[8] = x
        """
        name = kwargs.get("name")
        permission = kwargs.get("permission")
        if (not permission) or (not name):
            return "chmod: missing operand"

        id = self.__getFileId(name=name)
        query = "SELECT type FROM files_data WHERE id = ?;"
        self.crud.cursor.execute(query, (id,))
        result = self.crud.cursor.fetchone()
        folder=False
        if result[0]=="folder":
            folder=True
        if not id:
            return "chmod: cannot access file or folder: No such file or directory"

        if permission.isdigit():
            permission = self.convert_permission(int(permission),folder)
        else:
            current_permissions = self.get_current_permissions(id)
            updated_permissions = self.__process_permission_change(permission, current_permissions)
            if updated_permissions is None:
                return "Invalid permission."

            permission = updated_permissions

        query = f"UPDATE files_data SET permissions = '{permission}' WHERE id = {id};"
        self.crud.cursor.execute(query)
        self.crud.conn.commit()

        
        return "Permissions updated successfully."

    def get_current_permissions(self, id):
        query = "SELECT permissions FROM files_data WHERE id = ?;"
        self.crud.cursor.execute(query, (id,))
        result = self.crud.cursor.fetchone()
        return result[0] if result else None

    def __process_permission_change(self, permission, current_permissions):
        if permission == "+x":
            for i in range(2, 9, 3):
                current_permissions = current_permissions[:i] + 'x' + current_permissions[i+1:]
        elif permission == "-x":
            for i in range(2, 9, 3):
                current_permissions = current_permissions[:i] + '-' + current_permissions[i+1:]
        elif permission == "+r":
            for i in range(0, 9, 3):
                current_permissions = current_permissions[:i] + 'r' + current_permissions[i+1:]
        elif permission == "-r":
            for i in range(0, 9, 3):
                current_permissions = current_permissions[:i] + '-' + current_permissions[i+1:]
        elif permission == "+w":
            for i in range(1, 9, 3):
                current_permissions = current_permissions[:i] + 'w' + current_permissions[i+1:]
        elif permission == "-w":
            for i in range(1, 9, 3):
                current_permissions = current_permissions[:i] + '-' + current_permissions[i+1:]
        else:
            return None
        return current_permissions


    def touch(self, **kwargs):
        """ Create a new file from system directory if not found create an empty file
        
        Params:
            name (string) : name of file
        """
        name = kwargs.get('name', None)
        
        if name:
            try:
                file_content = None
                # check if file exist on file system
                with open(name, 'rb') as f:
                    file_content = f.read()
            except Exception as e:
                file_content = None
            if file_content is None:
                file_size = 0
            else:
                file_size = len(file_content)

            query = "INSERT INTO files_data (pid, filename, created_date, modified_date, size, type, owner, groop, permissions, content) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
            data = (self.cwdid, name.split('/')[-1], datetime.datetime.now(), datetime.datetime.now(), file_size, 'file', 'user1', 'group1', '-rw-r--r--', file_content)
            self.crud.cursor.execute(query, data)
            self.crud.conn.commit()
            return f"Created file '{name}'"

        else:
            return "touch: missing file operand"

    def add_history(self, command):
        self.history.append(command)
    
    def get_history(self):
        return "\n".join(self.history)
    
 
        