import datetime 
import pathlib
import shutil

source_icloud = pathlib.Path(r"C:/Users/amd/iCloudDrive")
backup_root = pathlib.Path(r"E:/")

today = datetime.date.today()
year = today.year
month = today.month

target = backup_root / str(year) / str(month)

if source_icloud.is_dir():
    print("Source found")

    target.mkdir(parents=True, exist_ok=True)
    print(target)

    test_path = source_icloud / "test.txt"


    if test_path.is_file():
        print("File found")

        destination_file = target / test_path.name
        print(destination_file)
        
        shutil.copy2(test_path, destination_file)
        print("copied")
    else:
        print("File not found")
else:
    print("source not found")