import datetime
import pathlib
import shutil
import sys

def get_path():
    # Use this block to set the source and backup paths directly in the code
    source_root = pathlib.Path(r"D:/") # Need to be changed into the source path
    backup_root = pathlib.Path(r"E:/") # Need to be changed into the target path

    # Use this block to get the source and backup paths from user input
    # source = input("Enter the source path: ").strip().strip('"').replace("\\", "/")
    # source_root = pathlib.Path(source) # Path to the source directory, e.g. D:/path/to/source
    # backup = input("Enter the backup path: ").strip().strip('"').replace("\\", "/")
    # backup_root = pathlib.Path(backup) # Path to the backup directory, e.g. E:/path/to/backup

    return source_root, backup_root

def get_time():
    today = datetime.date.today()
    year = today.year
    month = today.month
    day = today.day
    current_time = datetime.datetime.now()
    return today, year, month, day, current_time

today, year, month, day, current_time = get_time()

def set_target(backup_root):
    target = backup_root / str(year) / str(month) / f"full {day}_{month}_{year}" # Backup directory name changeable e.g. backup_root / "full_backup" / ... or backup_root / "full_backup_2024_06_15" / ...
    return target

def set_logging_dir(backup_root):
    logging_dir = backup_root / "Logging data" # Backup directory name changeable e.g. backup_root / "Loggings" / ... or backup_root / "Logging data_2024_06_15" / ...
    logging_dir.mkdir(parents=True, exist_ok=True)
    return logging_dir

def check_is_dir(source_root, backup_root):
    if not source_root.is_dir():
        print("Source not found\n")
        sys.exit(1)
    else:
        print("Source found\n")

    if not backup_root.is_dir():
        print("Backup not found\n")
        sys.exit(1)
    else:
        print("Backup found\n")

def create_logging_file(backup_root, copied_files, copied_files_list, failed_copy_files):
    logging_dir = set_logging_dir(backup_root)
    log_file_path = logging_dir / f"Backup_log_{year}_{month}_{day}.txt" # Backup log file name changeable e.g. logging_dir / "Backup_log.txt" / ... or logging_dir / "Backup_log_2024_06_15.txt" / ...
    with open(log_file_path, "w") as log_file:
        log_file.write(f"Full Backup finished.\n\n\nCopied files: {copied_files}\n{copied_files_list}.\n\nFailed copy files: {failed_copy_files}.\n\nDate: {current_time.strftime("%x")} {current_time.strftime("%X")}")
    print("Backup log created\n")

def run_full_backup():
    source_root, backup_root = get_path()

    target = set_target(backup_root)

    copied_files = 0
    copied_files_list = []

    failed_copy_files= 0
    excluded_path_parts = {} # Add the excluded path parts here, e.g. {"excluded_folder", "excluded_file.txt"}

    check_is_dir(source_root, backup_root)

    for new_file in source_root.rglob("*"):
        relative_path = new_file.relative_to(source_root)

        if any(part.lower() in excluded_path_parts for part in relative_path.parts):
            continue

        if new_file.is_file():
            destination_file = target / relative_path
            destination_file.parent.mkdir(parents=True, exist_ok=True)
            try:
                shutil.copy2(new_file, destination_file)
                copied_files += 1
                copied_files_list.append(relative_path.name)
            except OSError:
                failed_copy_files += 1
    
    create_logging_file(backup_root, copied_files, copied_files_list, failed_copy_files)

    return copied_files, copied_files_list, failed_copy_files, new_file

copied_files, copied_files_list, failed_copy_files, new_file = run_full_backup()

print(f"Full Backup finished.\n\n\nCopied files: {copied_files}\n{copied_files_list}.\n\nFailed copy files: {failed_copy_files}.\n\nDate: {current_time.strftime("%x")} {current_time.strftime("%X")}")
