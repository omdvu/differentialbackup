import os
import shutil
import json

def mirrorbackup(sourcemnt, destmnt):
    for item in os.listdir(destmnt):
        item_path = os.path.join(destmnt, item)
        try:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.unlink(item_path)
            else:
                shutil.rmtree(item_path)
        except Exception as e:
            print(f"Error removing {item_path}: {e}")
            return

    shutil.copytree(
        sourcemnt,
        destmnt,
        dirs_exist_ok=True,
        ignore=shutil.ignore_patterns("serverlog.txt", "mountlog.txt","mnt"),
        copy_function=shutil.copy2
    )

    print("Mirrored!")