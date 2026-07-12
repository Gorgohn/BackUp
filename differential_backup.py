import datetime
import pathlib
import shutil
import sys

def get_path():
    source_root = pathlib.Path(r"D:/") # Need to be changed into the source path
    backup_root = pathlib.Path(r"E:/") # Need to be changed into the target path
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
    target = backup_root / str(year) / str(month) / f"differential {day}_{month}_{year}" # Backup directory name changeable e.g. backup_root / "differential_backup" / ... or backup_root / "differential_backup_2024_06_15" / ...
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

def create_logging_file(backup_root, copied_files, copied_files_list, skipped_files, updated_files, updated_files_list, failed_update_files, failed_copy_files):
    logging_dir = set_logging_dir(backup_root)
    log_file_path = logging_dir / f"Backup_log_{year}_{month}_{day}.txt" # Backup log file name changeable e.g. logging_dir / "Backup_log.txt" / ... or logging_dir / "Backup_log_2024_06_15.txt" / ...
    with open(log_file_path, "w") as log_file:
        log_file.write(f"Differential Backup finished.\n\n\nCopied files: {copied_files}\n{copied_files_list}.\n\nUpdated files: {updated_files}\n{updated_files_list}.\n\nSkipped files: {skipped_files}.\n\nFailed update files: {failed_update_files}.\n\nFailed copy files: {failed_copy_files}.\n\nDate: {current_time.strftime("%x")} {current_time.strftime("%X")}")
    print("Backup logging data created\n")

def run_backup():
    source_root, backup_root = get_path()

    target = set_target(backup_root)

    copied_files = 0
    copied_files_list = []

    skipped_files = 0

    updated_files = 0
    updated_files_list = []

    failed_update_files= 0
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
            if destination_file.exists():
                icloud_file_time = new_file.stat().st_mtime
                backup_file_time = destination_file.stat().st_mtime
                try:
                    if icloud_file_time > backup_file_time:
                        shutil.copy2(new_file, destination_file)
                        updated_files += 1
                        updated_files_list.append(relative_path.name)
                    else:
                        skipped_files += 1
                except OSError:
                    failed_update_files += 1
            else:
                try:
                    shutil.copy2(new_file, destination_file)
                    copied_files += 1
                    copied_files_list.append(relative_path.name)
                except OSError:
                    failed_copy_files += 1
    
    create_logging_file(backup_root, copied_files, copied_files_list, skipped_files, updated_files, updated_files_list, failed_update_files, failed_copy_files)
    
    return copied_files, copied_files_list, skipped_files, updated_files, updated_files_list, failed_update_files, failed_copy_files, new_file

copied_files, copied_files_list, skipped_files, updated_files, updated_files_list, failed_update_files, failed_copy_files, new_file = run_backup()

print(f"Differential Backup finished.\n\n\nCopied files: {copied_files}\n{copied_files_list}.\n\nUpdated files: {updated_files}\n{updated_files_list}.\n\nSkipped files: {skipped_files}.\n\nFailed update files: {failed_update_files}.\n\nFailed copy files: {failed_copy_files}.\n\nDate: {current_time.strftime("%x")} {current_time.strftime("%X")}")