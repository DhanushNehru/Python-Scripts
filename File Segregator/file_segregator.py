import os

path = input("Enter the base path: ")

os.chdir(path)

# getting all files

all_files = os.listdir()

# declaring list for different type


# list of extention with different file types

audio = [".mp3", ".wav", ".m4a", ".wma", ".aac"]

video = [".mp4", ".wmv", ".mov", ".mkv", ".mpd"]

pdf = [".pdf", ".PDF"]

doc = [".doc", ".txt", ".dox", ".ppt", ".pptx", ".pptm", ".xls", ".xlsx", ".csv", ".docx"]

comp = [".zip", ".rar", ".tar", ".7z"]

app = [".exe", ".msi"]

image = [".png", ".jpg", ".jpeg", ".gif", ".jfif"]

web = [".html", ".svg"]

prog = [".py", "ipynb", ".c", ".cpp", ".r", ".asm", ".db", ".json", ".ipynb"]

all_types = [
    (image, "images"), 
    (doc, "documents"), 
    (pdf, "pdfs"),
    (app, "applications"), 
    (audio, "audios"), 
    (video, "videos"), 
    (prog, "programs"), 
    (web, "WEB"), 
    (comp, "devices")
    ]


for type in all_types:
    os.makedirs(type[1], exist_ok=True)
# creating folders for moving folders if not existing

# loop through all file names
for file_name in all_files:
    # getting extention
    name, extention = os.path.splitext(file_name)
    for type in all_types:
        if extention in type[0]:
            # adding file according to extention
            os.rename(file_name, f"{type[1]}/{file_name}")
            break
