import os
import json

SKIP_HIDDEN = set()

def explore(path, skipped=None):
    if skipped is None:
        skipped = set()
    skipped = skipped.union(SKIP_HIDDEN)

    directory = {}
    try:
        for item in os.listdir(path):
            if item in skipped:
                continue

            fullpath = os.path.join(path, item)

            if fullpath.endswith("serverlog.json") or fullpath.endswith("mountlog.json"):
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


def compare_dicts(old, new, path="", output=None):
    if output is None:
        output = []

    for key in set(old.keys()).union(new.keys()):
        old_val = old.get(key)
        new_val = new.get(key)
        current_path = os.path.join(path, key)

        if old_val is None:
            output.append(f"NEW FILE/FOLDER: {current_path}")
        elif new_val is None:
            output.append(f"MISSING FILE/FOLDER: {current_path}")
        elif isinstance(old_val, dict) and isinstance(new_val, dict):
            compare_dicts(old_val, new_val, current_path, output)
        elif old_val != new_val:
            output.append(f"DIFFERENT METADATA: {current_path}")
            output.append(f"    OLD: {old_val}")
            output.append(f"    NEW: {new_val}")

    return output


def run_comparison(previous_mount_log, current_backup_dir, output_file):
    """Runs the full compare and writes output."""

    if not os.path.exists(previous_mount_log) or os.path.getsize(previous_mount_log) == 0:
        mountold = {}
    else:
        try:
            with open(previous_mount_log, 'r') as f:
                mountold = json.load(f)
        except:
            mountold = {}

    mount_current = explore(current_backup_dir)

    results = compare_dicts(mountold, mount_current)

    with open(output_file, 'w') as f:
        for line in results:
            f.write(line + "\n")

    return results