import os
import shutil
import json
import differential

def mirrorbackup(sourcemnt,destmnt,mirrorlogdir):
    if os.path.exists(destmnt):
        try: 
            shutil.rmtree(destmnt)
        except Exception as e:
            print(f"Error removing old mirror: {e}")
            return
    
    shutil.copytree(sourcemnt,destmnt,ignore=shutil.ignore_patterns('serverlog.txt','mountlog.txt'),copy_function=shutil.copy2)

    mirroredfiles = differential.explore(sourcemnt)
    with open(mirrorlogdir,'w') as f:
        json.dump(mirroredfiles,f)

    print("Mirrored!")