# PyOS

A simple proof-of-concept command-line operating system simulator written in Python. PyOS provides a virtual filesystem with basic file and directory operations. I made this because I'm actively learning Python.

## Features

- Virtual filesystem with directories and files
- Create, read, and edit files
- Navigate between directories
- Clear screen functionality
- Uses real files

## Available Commands

| Command | Description |
|---------|-------------|
| `ls` | List files in current directory |
| `cd <dir>` | Change directory |
| `cd --root` | Return to root directory |
| `cd --host-os` | Go to host OS root (e.g., `C:\` on Windows) |
| `cd ..` | Go to parent directory |
| `cat <file>` | View file contents |
| `edit <file>` | Edit or create a file |
| `mkdir <dir>` | Create new directory |
| `rm <file/dir>` | Remove file or directory |
| `clear` | Clear the screen |
| `help` | Show available commands |
| `exit` | Exit SimpleOS |

## Usage

Run the script with Python:

```bash
python PyOS.py
```

## Example Session

```
/> ls

Files in /:
  readme.txt
  notes.txt
  documents/

/> cd documents/
/documents/> ls

Files in /documents/:
  file1.txt
  file2.txt
Both of these are empty
/documents/> cat file1.txt

Contents of /documents/file1.txt:
Content of file 1

/documents/> mkdir newfolder/
Directory 'newfolder/' created

/documents/> cd --root
/>
```

## Requirements

- Python 3.x
- No external dependencies required
