# Path Backup Automation

This project contains two Python scripts for backing up files from one folder path to another folder path.

It can create a full dated backup, create a dated differential backup folder, preserve the original folder structure, skip selected folders, and write a summary log after each run.

## Scripts

| File | Purpose |
| --- | --- |
| `full_backup.py` | Creates a complete backup of all files from the source folder. |
| `differential_backup.py` | Copies new files into a dated differential backup folder and updates files when the source file is newer than the existing backup file. |

## Features

- Preserves the original folder structure
- Creates backup folders based on the current date
- Supports interactive path input or hardcoded paths
- Copies files from the selected source folder to the selected backup destination
- Skips excluded folders
- Checks whether the source and backup paths exist before starting
- Prints a backup summary in the terminal
- Creates a daily log file with copied, updated, skipped, and failed file counts

## Project Structure

```text
.
|-- README.md
|-- full_backup.py
`-- differential_backup.py
```

## Requirements

- Python 3.12 or newer
- Access to the source folder
- Access to the backup destination, for example an external drive

The scripts only use Python standard library modules:

- `datetime`
- `pathlib`
- `shutil`
- `sys`

## Path Configuration

The scripts can be configured in two ways:

- Use the commented-out `input()` code if you want the script to ask for the paths when it starts.
- Use the uncommented hardcoded code if you always want to back up the same folders.

Only one path setup should be active at the same time. Comment out the block you do not want to use.

By default, the hardcoded path block is active and the interactive input block is commented out.

### Option 1: Interactive Path Input

Use this option if you want the script to ask for the source path and backup path every time it starts.

To use it, remove the `#` from the input block and comment out the hardcoded path block.

```python
def get_path():
    # Use this block if you want to enter the paths when the script starts.
    source = input("Enter source path: ").strip().strip('"').replace("\\", "/")
    backup = input("Enter backup path: ").strip().strip('"').replace("\\", "/")
    source_root = pathlib.Path(source)
    backup_root = pathlib.Path(backup)

    # Use this block if you want to hardcode the paths.
    # source_root = pathlib.Path(r"D:/Icloud/iCloudDrive")
    # backup_root = pathlib.Path(r"E:/")

    return source_root, backup_root
```

This is useful for manual backups or when the source and backup paths change often.

Use normal forward slashes `/` when entering paths:

Example:

```text
C:/Users/YourName/Documents
E:/Backups
```

If a Windows path with backslashes is pasted, the script converts `\` into `/` before creating the `Path`.

### Option 2: Hardcoded Paths

Use this option if you always want to back up the same source folder to the same backup folder.

This is the default setup in the scripts. Keep the input block commented out and edit the hardcoded paths.

```python
def get_path():
    # Use this block if you want to enter the paths when the script starts.
    # source = input("Enter source path: ").strip().strip('"').replace("\\", "/")
    # backup = input("Enter backup path: ").strip().strip('"').replace("\\", "/")
    # source_root = pathlib.Path(source)
    # backup_root = pathlib.Path(backup)

    # Use this block if you want to hardcode the paths.
    source_root = pathlib.Path(r"C:/path/to/source")
    backup_root = pathlib.Path(r"E:/path/to/backup")

    return source_root, backup_root
```

Change `source_root` to the folder you want to back up.

Change `backup_root` to the folder or drive where the backup should be saved.

This is useful when you do not want to enter the same paths every time you run the script.

Both paths can be local folders, external drives, mounted drives, network drives, or cloud-synced folders.

Both paths must already exist. If the source path or backup path does not exist, the script stops.

## Setup Checklist

1. Choose whether you want a full backup or a differential backup.
2. Choose whether you want interactive input or hardcoded paths.
3. Make sure only one `get_path()` version is active.
4. Open a terminal in the project folder.
5. Run the matching script.
6. If you use interactive input, enter the source path and backup path.
7. Make sure both paths exist if the script reports an error.

## Usage

Run a full backup:

```powershell
python full_backup.py
```

Run a differential backup:

```powershell
python differential_backup.py
```

Example terminal input:

```text
Enter source path: C:/Users/YourName/Documents
Enter backup path: E:/Backups
```

## Backup Output

The scripts create folders using the current year, month, and day.

Example:

```text
E:/
|-- 2026/
|   `-- 7/
|       |-- full 12_7_2026/
|       `-- differential 12_7_2026/
`-- Logging data/
    `-- Backup_log_2026_7_12.txt
```

Inside the backup folder, the original folder structure from the source folder is kept.

Example:

```text
source/
|-- Documents/
|   `-- invoice.pdf
`-- School/
    `-- worksheet.pdf
```

becomes:

```text
E:/2026/7/full 12_7_2026/
|-- Documents/
|   `-- invoice.pdf
`-- School/
    `-- worksheet.pdf
```

## Logging

Each run writes a log file to:

```text
<backup_root>/Logging data/
```

The log contains:

- Number of copied files
- Number of updated files
- Number of skipped files
- Number of failed copy or update operations
- Date and time of the backup

The log filename is based on the current date. Running another backup on the same day will replace the previous log file for that date.

## Excluded Paths

The scripts currently skip paths that contain these folder names:

```text
.trash
icloud~is~workflow~my~workflows
```

This prevents selected system, trash, or workflow folders from being copied.

## Notes

- Make sure all files are available locally before running the backup, especially when the source folder is managed by a cloud sync tool.
- Check the entered paths carefully before starting a backup.
- Test the scripts with a small folder first if you change the source or backup location.
- The differential script compares files inside its current dated target folder. It is not a classic differential backup based on the last full backup.

## Author

Created as a practical Python project for automating personal file backups.