import os
import hashlib
import json  # Import for generating reports

def get_file_hash(filepath):
    """Return the MD5 hash of a file."""
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def find_duplicates(directory, min_size=0, file_extensions=None):
    """Find duplicate files in a directory, with optional file type filtering."""
    hashes = {}
    duplicates = {}

    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            if file_extensions and not filename.lower().endswith(tuple(file_extensions)):
                continue  # Skip files that don't match the extensions

            filepath = os.path.join(dirpath, filename)
            if os.path.getsize(filepath) >= min_size:
                file_hash = get_file_hash(filepath)
                if file_hash in hashes:
                    duplicates.setdefault(file_hash, []).append(filepath)
                    # Also ensure the original file is in the duplicates list
                    if hashes[file_hash] not in duplicates[file_hash]:
                        duplicates[file_hash].append(hashes[file_hash])
                else:
                    hashes[file_hash] = filepath

    return {k: v for k, v in duplicates.items() if len(v) > 1}

def generate_report(duplicates, report_path):
    """Generate a report of duplicate files in JSON format."""
    with open(report_path, 'w') as report_file:
        json.dump(duplicates, report_file, indent=4)
    print(f"Report generated: {report_path}")

def main():
    directory = input("Enter the directory to scan for duplicates: ")
    min_size = int(input("Enter the minimum file size to consider (in bytes, default is 0): ") or "0")

    file_type_input = input("Enter the file extensions to check (comma-separated, e.g. .jpg,.png), or press Enter to check all: ")
    file_extensions = [ext.strip().lower() for ext in file_type_input.split(",")] if file_type_input else None

    duplicates = find_duplicates(directory, min_size, file_extensions)

    if not duplicates:
        print("No duplicates found.")
        return

    print("\nDuplicates found:")
    for _, paths in duplicates.items():
        for path in paths:
            print(path)
        print("------")

    action = input("\nChoose an action: (D)elete, (M)ove, (R)eport, (N)o action: ").lower()

    if action == "d":
        for _, paths in duplicates.items():
            for path in paths[1:]:  # Keep the first file, delete the rest
                os.remove(path)
                print(f"Deleted {path}")

    elif action == "m":
        target_dir = input("Enter the directory to move duplicates to: ")
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        for _, paths in duplicates.items():
            for path in paths[1:]:  # Keep the first file, move the rest
                target_path = os.path.join(target_dir, os.path.basename(path))
                os.rename(path, target_path)
                print(f"Moved {path} to {target_path}")

    elif action == "r":
        report_path = input("Enter the path to save the report (e.g., duplicates_report.json): ")
        generate_report(duplicates, report_path)

    else:
        print("No action taken.")

if __name__ == "__main__":
    main()
