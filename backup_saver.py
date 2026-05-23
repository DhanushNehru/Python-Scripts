import os
import shutil
def backup(source,destination):
    if( os.path.exists(source)):
        print("the file has been found")
    else:
        raise FileNotFoundError()

    if (os.path.exists(destination)):
        print("the directory exists")
    else:
        os.mkdir(destination)

    try:
        shutil.copy2(source,destination)
        print("file copied successfully")
    except Exception as e:
        print(f"error during backup {e}")

source1=input("Enter the path of the file you want to save")
destination1=input("Enter the destination directory for the backup")
backup(source1,destination1)


