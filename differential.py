import os
import shutil
import json
import stat
import time
import mirrorbackup
import comparedict

SERVER_PATH = os.environ.get("SERVER_PATH", "/server")
BACKUP_PATH = os.environ.get("BACKUP_PATH", "/backup")
MIRROR_PATH = os.environ.get("MIRROR_PATH", "/mirror")
LOG_DIR = os.environ.get("LOG_DIR", "/logs")

MOUNT_LOG_PATH = os.path.join(LOG_DIR, "mountlog.json")
SERVER_LOG_PATH = os.path.join(LOG_DIR, "serverlog.json")
MIRROR_LOG_PATH = os.path.join(LOG_DIR, "mirrorlog.json")

SKIP_HIDDEN = set()

def explore(path, skipped=None):
    if skipped is None:
        skipped = set()
    skipped = skipped.union(SKIP_HIDDEN)

    directory = {}
    try:
        for item in os.listdir(path):
            if item.startswith('.') or item in skipped:
                continue

            fullpath = os.path.join(path, item)

            if item in ("serverlog.json", "mountlog.json"):
                continue

            try:
                mode = os.stat(fullpath).st_mode
            except PermissionError:
                directory[item] = {"error": "permission denied"}
                continue

            if stat.S_ISSOCK(mode) or stat.S_ISFIFO(mode):
                continue

            if os.path.isdir(fullpath):
                directory[item] = explore(fullpath, skipped)
            else:
                statinfo = os.stat(fullpath)
                directory[item] = {
                    "size": statinfo.st_size,
                    "mtime": int(statinfo.st_mtime)
                }

    except PermissionError:
        return {"error": "permission denied"}

    return directory


def backup(serverpath, backuppath, server_files):
    mount_log = {}

    for name, meta in server_files.items():
        source = os.path.join(serverpath, name)
        destination = os.path.join(backuppath, name)

        if isinstance(meta, dict) and "error" in meta:
            mount_log[name] = meta
            continue

        if isinstance(meta, dict) and "size" not in meta:
            os.makedirs(destination, exist_ok=True)
            mount_log[name] = backup(source, destination, meta)
            continue

        if isinstance(meta, dict) and "size" in meta:
            try:
                mode = os.lstat(source).st_mode
            except Exception:
                continue

            if stat.S_ISSOCK(mode) or stat.S_ISFIFO(mode) or stat.S_ISCHR(mode) or stat.S_ISBLK(mode):
                continue

            copy_required = False
            if not os.path.exists(destination):
                copy_required = True
            else:
                dest_stat = os.stat(destination)
                if dest_stat.st_size != meta["size"] or int(dest_stat.st_mtime) != meta["mtime"]:
                    copy_required = True

            if copy_required:
                try:
                    shutil.copy2(source, destination)
                    mount_log[name] = meta
                except Exception as e:
                    print(f"Failed to copy {source}: {e}")
            else:
                mount_log[name] = meta
    return mount_log


def main():
    os.makedirs(LOG_DIR, exist_ok=True)

    print("Scanning source and backup directories...")
    server_files = explore(SERVER_PATH)

    try:
        mirrorbackup.mirrorbackup(BACKUP_PATH,MIRROR_PATH,MIRROR_LOG_PATH)
        current_mount_log = backup(SERVER_PATH, BACKUP_PATH, server_files)

        with open(MOUNT_LOG_PATH, 'w') as f:
            json.dump(current_mount_log, f)

        with open(SERVER_LOG_PATH, 'w') as f:
            json.dump(server_files, f)

        print("Backup completed successfully.")

        comparedict.run_comparison(
            MOUNT_LOG_PATH,
            BACKUP_PATH, 
            os.path.join(LOG_DIR, "compare_errors.txt")
        )

    except Exception as e:
        print(f"Fatal: {e}")

while True:
    main()
    print("Sleeping for 24 hrs")
    time.sleep(60*60*24)