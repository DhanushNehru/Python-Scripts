import os
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--path', type=str, required=True, help='Path to the directory containing images and labels')
args = parser.parse_args()
path = args.path

allFiles = os.listdir(path)



#Delete images without labels
def check_labels(path,allFiles):

    missing = []
    for file in allFiles:
        if file.lower().endswith('.jpg') or file.lower().endswith('.jpeg') or file.lower().endswith('.png'):
            label_file = file.rsplit('.', 1)[0] + '.txt'
            if not os.path.exists(os.path.join(path,label_file)):
                missing.append(file)
                print(f"Label file missing for image: {file}")

    print('Would you like to delete these images? (y/n)')

    user_input = input().strip().lower()
    if user_input == 'y':
        for file in missing:
            os.remove(os.path.join(path,file))
            missing.pop()
            print(f"Deleted image: {file}")

#delete empty labels

def check_missing_labels(path,allFiles):
    missing = []
    for file in allFiles:
        if file.lower().endswith('.txt'):
            with open(os.path.join(path,file), 'r') as f:
                content = f.read().strip()
                if not content:
                    missing.append(file)
                    print(f"Label file is empty: {file}")

    print('Would you like to delete these label files? (y/n)')

    user_input = input().strip().lower()
    if user_input == 'y':
        for file in missing:
            os.remove(os.path.join(path,file))
            missing.pop()
            print(f"Deleted label file: {file}")

#delete labels without images

def check_missing_images(path,allFiles):
    missing=[]
    for file in allFiles:
        if file.lower().endswith('.txt'):
            image_file_jpg = file.rsplit('.', 1)[0] + '.jpg'
            image_file_png = file.rsplit('.', 1)[0] + '.png'
            image_file_jpeg = file.rsplit('.', 1)[0] + '.jpeg'
            if not (os.path.exists(os.path.join(path,image_file_jpg)) or os.path.exists(os.path.join(path,image_file_png)) or os.path.exists(os.path.join(path,image_file_jpeg))):
                missing.append(file)
                print(f"Image file missing for label: {file}")

    print('Would you like to delete these label files? (y/n)')

    user_input = input().strip().lower()
    if user_input == 'y':
        for file in missing:
            os.remove(os.path.join(path,file))
            print(f"Deleted label file: {file}")

print('check images without labels [1] \ncheck for missing labels [2] \ncheck missing labels [3]')
user_choice = input().strip()
if user_choice == '1':
    check_labels(path,allFiles)
    sys.exit(0)
elif user_choice == '2':
    check_missing_labels(path,allFiles)
    sys.exit(0)

elif user_choice == '3':
    check_missing_images(path,allFiles)
    sys.exit(0)
else:
    print('Invalid choice. Exiting.')
    sys.exit(0)