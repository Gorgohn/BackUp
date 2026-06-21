import datetime 
import pathlib
import shutil

source_icloud = pathlib.Path(r"D:/test_dir")
backup_root = pathlib.Path(r"E:/")

today = datetime.date.today()
year = today.year
month = today.month

target = backup_root / str(year) / str(month)

if source_icloud.is_dir():
    print("Source found")

    for doc in source_icloud.rglob("*"):
        if doc.is_file():
            relative_path = doc.relative_to(source_icloud)
            destination_file = target / relative_path
            print(relative_path)
            print(destination_file)
            print(destination_file.parent)
            destination_file.parent.mkdir(parents=True, exist_ok=True)
else:
    print("source not found")