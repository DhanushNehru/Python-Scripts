from shutil import move
from os import path
import os


directory = {
    'Programming Files': set(['ipynb', 'py', 'java', 'cs', 'js', 'vsix', 'jar', 'cc', 'ccc', 'html', 'xml', 'kt']),
    'Music':  set(['mp3', 'wav', 'wma', 'mpa', 'ram', 'ra', 'aac', 'aif', 'm4a', 'tsa']),
    'Videos':  set(['mp4', 'webm', 'mkv', 'MPG', 'MP2', 'MPEG', 'MPE', 'MPV', 'OGG', 'M4P', 'M4V', 'WMV', 'MOV', 'QT', 'FLV', 'SWF', 'AVCHD', 'avi', 'mpg', 'mpe', 'mpeg', 'asf', 'wmv', 'mov', 'qt', 'rm']),
    'Pictures':  set(['jpeg', 'jpg', 'png', 'gif', 'tiff', 'raw', 'webp', 'jfif', 'ico', 'psd', 'svg', 'ai']),
    'Applications': set(['exe', 'msi', 'deb', 'rpm']),
    'Compressed': set(['zip', 'rar', 'arj', 'gz', 'sit', 'sitx', 'sea', 'ace', 'bz2', '7z']),
    'Documents': set(['txt', 'pdf', 'doc', 'xlsx', 'pdf', 'ppt', 'pps', 'docx', 'pptx']),
    'Other': set([])
}


def create_folders():

    for dir_ in directory:
        try:
            os.mkdir(dir_)
            print(f'{dir_:20} Created')
        except OSError:
            print(f'{dir_:20} Already Exists')


def get_folder(ext):
    
    for f, ex in directory.items():
        if ext in ex:
            return f
    return 'Other'


def start():
    for filename in os.listdir():
        if filename != __file__ and filename[0] != '.' and '.' in filename:
            ext = os.path.basename(filename).split('.')[-1]
            folder = get_folder(ext)
            if not os.path.isfile(os.path.join(folder, filename)):
                move(filename, folder)


if __name__ == '__main__':
    create_folders()
    start()
