import os
import shutil
import json

def mirrorbackup(sourcemnt,destmnt,mirrorlogdir):
    if os.path.exists(destmnt):
        try: 
            shutil.rmtree(destmnt)
        except Exception as e:
            print(f"Error removing old mirror: {e}")
            return
    
    shutil.copytree(sourcemnt,destmnt,ignore=shutil.ignore_patterns('serverlog.txt','mountlog.txt'),copy_function=shutil.copy2)
    print("Mirrored!")