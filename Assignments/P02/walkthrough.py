import time
from rich import print
from rich.table import Table
from rich.box import SIMPLE

from fileSystem import FileSystem

# Create a file system
file_system = FileSystem()

def display_ls(files):
    table = Table(show_header=True, header_style="bold blue", box=SIMPLE)
    for col in files[0]:
        table.add_column(col)

    for data in files[1:]:
        data = [str(item) for item in data]
        table.add_row(*data)

    print(table)

print("[bold blue]Command:[/bold blue] [green]ls[/green]")
ls_result = file_system.list()
file_system.add_history("ls")
display_ls(ls_result)
i=input()

print("[bold blue]Command:[/bold blue] [green]ls -lah[/green]")
ls_result = file_system.list(long=True, all=True, human_readable=True)
file_system.add_history("ls -lah")
display_ls(ls_result)
i=input()

print("[bold blue]Command:[/bold blue] [green]mkdir test[/green]")
mkdir_result = file_system.mkdir(name="test")
file_system.add_history("mkdir test")
print(mkdir_result)
print()
i=input()

print("[bold blue]Command:[/bold blue] [green]ls[/green]")
ls_result = file_system.list()
file_system.add_history("ls")
display_ls(ls_result)
i=input()

print("[bold blue]Command:[/bold blue] [green]cd test[/green]")
cd_result = file_system.cd(name="test")
file_system.add_history("cd test")
print(cd_result)
print()
i=input()

print("[bold blue]Command:[/bold blue] [green]pwd[/green]")
pwd_result = file_system.pwd()
file_system.add_history("pwd")
print(pwd_result)
print()
i=input()


print("[bold blue]Command:[/bold blue] [green]cd ..[/green]")
cd_result = file_system.cd(name="..")
file_system.add_history("cd ..")
print(cd_result)
print()
i=input()

print("[bold blue]Command:[/bold blue] [green]mv Folder3 test[/green]")
mv_result = file_system.mv(source="Folder3", destination="test")
file_system.add_history("mv Folder3 test")
print(mv_result)
print()
i=input()

print("[bold blue]Command:[/bold blue] [green]cd test[/green]")
cd_result = file_system.cd(name="test")
file_system.add_history("cd test")
print(cd_result)
print()
i=input()

print("[bold blue]Command:[/bold blue] [green]ls -l[/green]")
ls_result = file_system.list(long=True)
file_system.add_history("ls -l")
display_ls(ls_result)
i=input()

print("[bold blue]Command:[/bold blue] [green]cd ..[/green]")
cd_result = file_system.cd(name="..")
file_system.add_history("cd ..")
print(cd_result)
print()
i=input()


print("[bold blue]Command:[/bold blue] [green]ls[/green]")
ls_result = file_system.list()
file_system.add_history("ls")
display_ls(ls_result)
i=input()

print("[bold blue]Command:[/bold blue] [green]cp /home/Folder2 test[/green]")
cp_result = file_system.cp(source="/home/Folder2", destination="test")
file_system.add_history("cp /home/Folder2 test")
print(cp_result)
print()
i=input()

print("[bold blue]Command:[/bold blue] [green]cd test[/green]")
cd_result = file_system.cd(name="test")
file_system.add_history("cd test")
print(cd_result)
print()
i=input()

print("[bold blue]Command:[/bold blue] [green]ls[/green]")
ls_result = file_system.list()
file_system.add_history("ls")
display_ls(ls_result)
i=input()

print("[bold blue]Command:[/bold blue] [green]rm Folder2[/green]")
rm_result = file_system.rm(name="Folder2")
file_system.add_history("rm Folder2")
print(rm_result)
print()
i=input()

print("[bold blue]Command:[/bold blue] [green]ls[/green]")
ls_result = file_system.list()
file_system.add_history("ls")
display_ls(ls_result)
i=input()

print("[bold blue]Command:[/bold blue] [green]chmod 777 Folder3[/green]")
chmod_result = file_system.chmod(name="Folder3", permission="777")
file_system.add_history("chmod 777 Folder3")
print(chmod_result)
print()
i=input()

print("[bold blue]Command:[/bold blue] [green]ls -lh[/green]")
ls_result = file_system.list(long=True, human_readable=True)
file_system.add_history("ls -lh")
display_ls(ls_result)
i=input()


print("[bold blue]Command:[/bold blue] [green]insert files/treeout.json[/green]")
touch_result = file_system.touch(name="files/treeout.json")
file_system.add_history("insert files/treeout.json")
print(touch_result)
print()
i=input()

print("[bold blue]Command:[/bold blue] [green]ls -lh[/green]")
ls_result = file_system.list(long=True, human_readable=True)
file_system.add_history("ls -lh")
display_ls(ls_result)
i=input()


print("[bold blue]Command:[/bold blue] [green]history[/green]")
history_result = file_system.get_history()
file_system.add_history("history")
print(history_result)
print()

