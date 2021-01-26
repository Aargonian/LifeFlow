import os
import sys
import os.path
import appdirs
import shutil
import datetime

from os.path import join
from pathlib import Path

BASE_LOCATION = appdirs.user_data_dir("LifeFlow", "NyteWorks", "0.1.0")
NOTES_FOLDER = join(BASE_LOCATION, "Notes")

#TODO: In the future, the user will be able to change which folder is the default for QuickNotes
QUICK_NOTES_FOLDER = join(NOTES_FOLDER, "Inbox")

if not os.path.exists(BASE_LOCATION):
    os.makedirs(BASE_LOCATION, exist_ok=True)
if not os.path.exists(NOTES_FOLDER):
    os.makedirs(NOTES_FOLDER, exist_ok=True)
if not os.path.exists(QUICK_NOTES_FOLDER):
    os.makedirs(QUICK_NOTES_FOLDER, exist_ok=True)

current_notebook = "Inbox"
all_notebooks = []
for notebook in os.listdir(NOTES_FOLDER):
    all_notebooks.append(notebook)

def list_notes(args):
    if len(args) == 0:
        print("You have the following notebooks:")
        notebooks = os.listdir(NOTES_FOLDER)
        for notebook in notebooks:
            print("*", notebook)
    else:
        notebook = args[0]
        print("These are the notes in", notebook)
        notes = os.listdir(join(NOTES_FOLDER, notebook))
        for note in notes:
            note = ".".join(note.split(".")[:-1])
            print(note)

def select_notebook(args):
    global all_notebooks
    global current_notebook
    if args[0] in all_notebooks:
        current_notebook = args[0]

def create_notebook(args):
    global all_notebooks
    global current_notebook
    if len(args) < 1:
        print("You need a name for your new notebook!", file=sys.stderr)
        return
    if not os.path.exists(join(NOTES_FOLDER, args[0])):
        os.makedirs(join(NOTES_FOLDER, args[0]), exist_ok=True)
    all_notebooks.append(args[0])
    current_notebook = args[0]

def delete(args):
    global current_notebook
    global all_notebooks
    if len(args) < 1:
        print("Unable to delete nothing.", file=sys.stderr)
        return
    if args[0] == 'notebook':
        if len(args) < 2:
            print("You need to select a notebook to delete.")
        else:
            if args[1] == 'Inbox':
                print("You cannot delete the Inbox.")
                return
            elif args[1] == current_notebook:
                current_notebook = "Inbox"
            path = join(NOTES_FOLDER, args[1])
            if not os.path.exists(path):
                print("That notebook does not exist.")
                return
            print("CHECKING:", path)
            shutil.rmtree(path)
            print("Deleted notebook", args[1])
    else:
        path = join(NOTES_FOLDER, current_notebook, args[0] + ".txt")
        print("CHECKING:", path)
        if not os.path.exists(path):
            print("That note does not exist.")
            return
        os.remove(path)
        print("Deleted", args[0])

def add_note(arguments):
    global current_notebook
    if current_notebook is None:
        current_notebook = "Inbox"
    if len(arguments) == 0:
        filename = '{date:%Y-%m-%d_%H:%M:%S}.txt'.format(date=datetime.datetime.now())
    else:
        #TODO: We need to sanitize this for legal filename
        filename = " ".join(arguments) + ".txt"
    filename = join(NOTES_FOLDER, current_notebook, filename)
    if not os.path.exists(filename):
        filepath = Path(filename)
        filepath.touch()
    os.startfile(join(NOTES_FOLDER, current_notebook, filename))

def run_tui():
    global current_notebook
    valid_commands = {
        "list": list_notes,
        "select": select_notebook,
        "create": create_notebook,
        "delete": delete,
        "add": add_note,
        "quit": exit,
    }
    print("Welcome to LifeFlow Notes")
    print("-------------------------")
    print()
    command = None
    while(command != "quit"):
        if current_notebook is None:
            current_notebook = "Inbox"
        print("You are currently in notebook:", current_notebook)
        command_parts = input("> ").strip().lower().split(" ")
        arguments = command_parts[1:]
        command = command_parts[0]
        if command not in valid_commands:
            print("Invalid command. Please input one of: ", file=sys.stderr)
            for key in valid_commands.keys():
                print("\t", key)
        else:
            valid_commands[command](arguments)
if __name__ == '__main__':
    run_tui()