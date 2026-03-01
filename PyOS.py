import os

def clear_screen():
 # Windows
    if os.name == 'nt':
         _ = os.system('cls')
# macOS/Linux
    else:
         _ = os.system('clear')
    print("PyOS v1.1 - Type 'help' for commands")
    

class PyOS:
    clear_screen()
    def __init__(self):
        self.current_directory = "/"
        self.files = {
            "/": ["readme.txt", "notes.txt", "documents/"],
            "/documents/": ["file1.txt", "file2.txt"]
        }
        self.file_contents = {
            "/readme.txt": "Welcome to PyOS\nThis is a basic text file.",
            "/notes.txt": "",
            "/documents/file1.txt": "Content of file 1",
            "/documents/file2.txt": "Content of file 2"
        }
        self.running = True

    def list_files(self):
        path = self.current_directory
        if path in self.files:
            print("\nFiles in", path + ":")
            for item in self.files[path]:
                print("  " + item)
        else:
            print("Directory not found")

    def change_directory(self, target):
        if target == "--root":
            self.current_directory = "/"
            return

        if target == "..":
            if self.current_directory != "/":
                parts = self.current_directory.strip("/").split("/")
                new_path = "/" + "/".join(parts[:-1]) + "/"
                if new_path == "//": new_path = "/"
                self.current_directory = new_path
            return

        new_path = self.current_directory + target
        if new_path.endswith("/") or target in [d for d in self.files.get(self.current_directory, []) if d.endswith("/")]:
            if new_path in self.files:
                self.current_directory = new_path
            else:
                print("Directory not found")
        else:
            print("Not a directory")

    def read_file(self, filename):
        path = self.current_directory + filename
        if path in self.file_contents:
            print("\nContents of", path + ":")
            print(self.file_contents[path])
        else:
            print("File not found")

    def make_directory(self, dirname):
        if not dirname.endswith("/"):
            dirname += "/"
        new_path = self.current_directory + dirname
        if new_path in self.files:
            print("Directory already exists")
        elif self.current_directory not in self.files:
            print("Parent directory not found")
        else:
            self.files[new_path] = []
            self.files[self.current_directory].append(dirname)
            print(f"Directory '{dirname}' created")

    def edit_file(self, filename):
        path = self.current_directory + filename
        if path in self.file_contents:
            print(f"Editing {path} (Enter new content, type 'SAVE' on a new line to finish):")
            content = []
            while True:
                line = input()
                if line == "SAVE":
                    break
                content.append(line)
            self.file_contents[path] = "\n".join(content)
            print("File saved!")
        elif self.current_directory in self.files and filename in self.files[self.current_directory]:
            print("Cannot edit directories")
        else:
            # Create new file
            self.file_contents[path] = ""
            self.files[self.current_directory].append(filename)
            self.edit_file(filename)

    def run(self):
        while self.running:
            cmd = input(f"\n{self.current_directory}> ").strip().split()
            if not cmd:
                continue
            command = cmd[0].lower()

            if command == "ls":
                self.list_files()
            elif command == "cd":
                if len(cmd) > 1:
                    self.change_directory(cmd[1])
                else:
                    self.change_directory("")
            elif command == "cat":
                if len(cmd) > 1:
                    self.read_file(cmd[1])
                else:
                    print("Usage: cat <filename>")
            elif command == "edit":
                if len(cmd) > 1:
                    self.edit_file(cmd[1])
                else:
                    print("Usage: edit <filename>")
            elif command == "mkdir":
                if len(cmd) > 1:
                    self.make_directory(cmd[1])
                else:
                    print("Usage: mkdir <directory>")
            elif command == "help":
                print("\nCommands:")
                print("  ls          - List files in current directory")
                print("  cd <dir>    - Change directory (use '--root' for root directory)")
                print("  cat <file>  - View file contents")
                print("  edit <file> - Edit/create file")
                print("  mkdir <dir> - Create new directory")
                print("  clear       - Clear the screen")
                print("  exit        - Exit PyOS")
            elif command == "exit":
                self.running = False
            elif command == "clear":
                clear_screen()
            else:
                print("Unknown command. Type 'help' for available commands.")

if __name__ == "__main__":
    app = PyOS() 
    app.run()