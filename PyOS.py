import os
import sys
import time

def clear_screen():
    # Windows
    if os.name == 'nt':
        _ = os.system('cls')
    # macOS/Linux
    else:
        _ = os.system('clear')

def set_title(title):
    sys.stdout.write(f"\x1b]2;{title}\x07")
    sys.stdout.flush()

# basic setup
set_title("PyOS Terminal")
time.sleep(1.5)
clear_screen()

class PyOS:
    def __init__(self, root_dir="root-sys"):
        self.root_path = os.path.abspath(root_dir)

        # Create the folder if it doesn't exist
        if not os.path.exists(self.root_path):
            os.makedirs(self.root_path)

        # track relative path internally (starting at root)
        self.current_rel_path = ""
        self.running = True

    def get_full_path(self, target=""):
        """Helper to combine root_path with current position and target filename"""
        return os.path.normpath(os.path.join(self.root_path, self.current_rel_path, target))

    def list_files(self):
        full_path = self.get_full_path()
        print(f"\nFiles in /{self.current_rel_path.replace('\\', '/')}:")
        try:
            items = os.listdir(full_path)
            for item in items:
                suffix = "/" if os.path.isdir(os.path.join(full_path, item)) else ""
                print(f"  {item}{suffix}")
        except FileNotFoundError:
            print("Directory not found.")

    def change_directory(self, target):
        if target == "..":
            if self.current_rel_path != "" and self.current_rel_path != ".":
                self.current_rel_path = os.path.dirname(self.current_rel_path)
            else:
                self.current_rel_path = ""
            return

        if target == "--root" or target == "/":
            self.current_rel_path = ""
            return

        if target == "--host":
            # Change to host OS root (e.g., C:\ on Windows, / on Unix)
            self.current_rel_path = os.path.abspath(os.sep)
            return

        new_potential_path = os.path.join(self.current_rel_path, target)
        full_path = os.path.join(self.root_path, new_potential_path)

        if os.path.isdir(full_path):
            self.current_rel_path = new_potential_path
        else:
            print("Directory not found.")

    def read_file(self, filename):
        full_path = self.get_full_path(filename)
        if os.path.isfile(full_path):
            print(f"\nContents of {filename}:")
            try:
                with open(full_path, "r") as f:
                    print(f.read())
            except UnicodeDecodeError:
                print("File is not a text file or cannot be decoded.")
        else:
            print("File not found.")

    def make_directory(self, dirname):
        full_path = self.get_full_path(dirname)
        if os.path.exists(full_path):
            print("Directory already exists.")
        else:
            try:
                os.makedirs(full_path)
                print(f"Directory '{dirname}' created.")
            except OSError as e:
                print(f"Error creating directory: {e}")

    def remove(self, target):
        full_path = self.get_full_path(target)
        if not os.path.exists(full_path):
            print("File or directory not found.")
            return
        
        if os.path.isfile(full_path):
            try:
                os.remove(full_path)
                print(f"File '{target}' removed.")
            except OSError as e:
                print(f"Error removing file: {e}")
        elif os.path.isdir(full_path):
            try:
                os.rmdir(full_path)
                print(f"Directory '{target}' removed.")
            except OSError:
                print("Directory not empty. Remove contents first.")

    def edit_file(self, filename):
        full_path = self.get_full_path(filename)
        if os.path.isdir(full_path):
            print("Cannot edit directories.")
            return

        if os.path.isfile(full_path):
            print(f"Editing {filename} (Enter new content, type 'SAVE' on a new line to finish):")
            content = []
            while True:
                line = input()
                if line == "SAVE":
                    break
                content.append(line)
            with open(full_path, "w") as f:
                f.write("\n".join(content))
            print("File saved!")
        else:
            # Create new file
            print(f"Creating new file {filename} (Enter content, type 'SAVE' on a new line to finish):")
            content = []
            while True:
                line = input()
                if line == "SAVE":
                    break
                content.append(line)
            with open(full_path, "w") as f:
                f.write("\n".join(content))
            print("File created and saved!")

    def clear_screen(self):
        if os.name == 'nt':
            _ = os.system('cls')
        else:
            _ = os.system('clear')
        print("PyOS v1.5 - Type 'help' for commands.\n")

    def run(self):
        print("PyOS v1.5 - Type 'help' for commands.\n")
        while self.running:
            display_path = "/" + self.current_rel_path.replace("\\", "/")
            if display_path == "//":
                display_path = "/"

            cmd = input(f"{display_path}> ").strip().split()
            if not cmd:
                continue

            # lowercase the commands but not the arguments (like file names)
            command = cmd[0].lower()
            args = cmd[1:] if len(cmd) > 1 else []

            # Handle commands
            if command == "ls":
                self.list_files()
            elif command == "cd":
                if args:
                    self.change_directory(args[0])
                else:
                    print("Usage: cd <dir>")
            elif command == "cat":
                if args:
                    self.read_file(args[0])
                else:
                    print("Usage: cat <file>")
            elif command == "edit":
                if args:
                    self.edit_file(args[0])
                else:
                    print("Usage: edit <file>")
            elif command == "mkdir":
                if args:
                    self.make_directory(args[0])
                else:
                    print("Usage: mkdir <directory>")
            elif command == "rm":
                if args:
                    self.remove(args[0])
                else:
                    print("Usage: rm <file|dir>")
            elif command == "exit":
                self.running = False
            elif command == "clear":
                self.clear_screen()
            elif command == "help":
                print("\nCommands:")
                print("  ls          - List files/folders")
                print("  cd <dir>    - Change directory (use '..' to go up, '--root' or '/' for root, '--host' for host OS root)")
                print("  cat <file>  - View file contents")
                print("  edit <file> - Edit/create file")
                print("  mkdir <dir> - Create new directory")
                print("  rm <file|dir> - Remove file or directory")
                print("  clear       - Clear the screen")
                print("  exit        - Exit PyOS")
            elif command == "note":
                print("- To get to the root, type 'cd /' or 'cd --root'. 'cd' alone will not work.\n- Text files are the only supported file type for viewing/editing.")
            else:
                print("Unknown command. Type 'help' for a list of commands.")

def start_system():
    os_instance = PyOS(root_dir="root-sys")
    os_instance.run()

if __name__ == "__main__":
    start_system()
