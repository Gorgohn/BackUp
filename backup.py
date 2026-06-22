import datetime 
import pathlib
import shutil
import sys

source_icloud = pathlib.Path(r"D:/iCloudDrive")
backup_root = pathlib.Path(r"E:/")

today = datetime.date.today()
year = today.year
month = today.month

target = backup_root / str(year) / str(month)

if not source_icloud.is_dir():
    print("Icloud not found")
    sys.exit(1)

if not backup_root.is_dir():
    print("Backup not found")
    sys.exit(1)

print("Icloud found")
print("Backup found")

def run_backup():
    copied_files = 0
    skipped_files = 0
    updated_files = 0

    for new_file in source_icloud.rglob("*"):

        if new_file.is_file():
            relative_path = new_file.relative_to(source_icloud)
            destination_file = target / relative_path

            destination_file.parent.mkdir(parents=True, exist_ok=True)

            if destination_file.exists():
                icloud_file_time = new_file.stat().st_mtime
                backup_file_time = destination_file.stat().st_mtime

                if icloud_file_time > backup_file_time:
                    shutil.copy2(new_file, destination_file)
                    updated_files += 1

                else:
                    skipped_files += 1

            else:
                shutil.copy2(new_file, destination_file)
                copied_files += 1

    return copied_files, updated_files, skipped_files

copied_files, updated_files, skipped_files = run_backup()

print(f"Backup finished. Copied files: {copied_files}. Updated files: {updated_files}. Skipped files: {skipped_files}.")