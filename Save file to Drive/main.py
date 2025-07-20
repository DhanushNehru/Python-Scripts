from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

# Authenticate
gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

# === Prompt for target folder ===
target_folder_name = input("Enter the name of the target folder in Google Drive: ").strip()

def get_or_create_drive_folder(folder_name, parent_id='root'):
    """Get Drive folder ID by name or create it under given parent"""
    query = (
        f"title='{folder_name}' and "
        f"mimeType='application/vnd.google-apps.folder' and "
        f"'{parent_id}' in parents and trashed=false"
    )
    file_list = drive.ListFile({'q': query}).GetList()
    if file_list:
        print(f"Folder '{folder_name}' found in Google Drive.")
        return file_list[0]['id']
    else:
        print(f"Folder '{folder_name}' not found. Creating it...")
        folder_metadata = {
            'title': folder_name,
            'parents': [{'id': parent_id}],
            'mimeType': 'application/vnd.google-apps.folder'
        }
        folder = drive.CreateFile(folder_metadata)
        folder.Upload()
        return folder['id']

# === Configuration ===
local_root = r"drive"  # Your local folder name
drive_root_id = get_or_create_drive_folder(target_folder_name)

# Folder mapping cache
folder_mapping = {local_root: drive_root_id}

# Recursively walk and upload
for root, dirs, files in os.walk(local_root):
    rel_path = os.path.relpath(root, local_root)
    
    if rel_path == '.':
        parent_id = drive_root_id
    else:
        parent_local = os.path.dirname(root)
        parent_id = folder_mapping.get(parent_local, drive_root_id)

        folder_name = os.path.basename(root)
        folder_id = get_or_create_drive_folder(folder_name, parent_id)
        folder_mapping[root] = folder_id

    for file_name in files:
        file_path = os.path.join(root, file_name)

        # === Check if file already exists in this Drive folder ===
        query = (
            f"title='{file_name}' and "
            f"'{folder_mapping[root]}' in parents and "
            f"trashed=false"
        )
        existing_files = drive.ListFile({'q': query}).GetList()
        if existing_files:
            print(f"⏩ File '{file_name}' already exists in '{rel_path}', skipping.")
            continue

        print(f"⬆️ Uploading '{file_name}' to '{rel_path}'...")
        file_drive = drive.CreateFile({
            'title': file_name,
            'parents': [{'id': folder_mapping[root]}]
        })
        file_drive.SetContentFile(file_path)
        file_drive.Upload()
        file_drive = None
