import datetime 
import pathlib


source_icloud = pathlib.Path(r"C:/Users/amd/iCloudDrive")
backup_root = pathlib.Path(r"E:/")

year = datetime.date.today().year
month = datetime.date.today().month

target = backup_root / str(year) / str(7)

target.mkdir(parents=True, exist_ok=True)

print(target)