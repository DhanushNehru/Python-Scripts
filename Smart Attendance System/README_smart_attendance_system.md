### Prerequisites

Before you begin, ensure you have met the following requirements:

* [Git](https://git-scm.com/downloads "Download Git") must be installed on your operating system.

### Installation 

1. Clone this repo.

To run **Smart Attendance System**, run this command on your git bash:

Linux and macOS:

```bash
sudo git clone https://github.com/raj-mistry-01/Computer-Vision.git
```

Windows:

```bash
git clone https://github.com/raj-mistry-01/Computer-Vision.git
```

2. Navigate to Smart Attendance Folder
   
3. Install required python packages

```bash
pip install -r requirements
```

## What Is It (You can also read it in .idea folder)
Now first we should have the students's data
We have name and roll number of the students stored in a data.csv
We will encode the each student's name(a string) into a qrcode

In main.py
    first we will read the data.csv and make a list of name and their rollnumber
    By cv2 , If a student is present it will give his or her code to camera , we will 
    decode it and by decoding it we will get his or her name after that we will remove 
    his or her name from name list
    Which names are left in list ,simple logic they are absent


## Avoid A Comman Mistake : 
In ```main.py``` the path of csv should be according your ```system```

### A Question In Your Mind (I know) :
If one student has all qrcode than it can also presents his all friends , but soon this ```code``` is going to be integretad by ```Face Recognization```

## Languages Used : 
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
