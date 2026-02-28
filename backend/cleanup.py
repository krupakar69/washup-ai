import shutil
import os

folders = [
    os.path.expanduser("~\\AppData\\Local\\Temp"),
]

for folder in folders:
    for item in os.listdir(folder):
        item_path = os.path.join(folder, item)
        try:
            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
        except:
            pass

print("✅ Temp files cleaned!")