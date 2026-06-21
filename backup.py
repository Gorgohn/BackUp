import datetime 
import pathlib


source_icloud = pathlib.Path(r"C:/Users/amd/iCloudDrive")
backup_root = pathlib.Path(r"E:/")

today = datetime.date.today()
year = today.year
month = today.month

target = backup_root / str(year) / str(month)

if source_icloud.exists():
    print("Quelle gefunden")
    target.mkdir(parents=True, exist_ok=True)
    print(target)
else:
    print("Quelle nicht gefunden")