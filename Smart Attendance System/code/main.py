from pyzbar.pyzbar import decode
import cv2
from PIL import Image
import csv

cam = cv2.VideoCapture(0)

students = []
RollNumbers = []
with open(r"path of csv","r") as file :
    reader = csv.reader(file)
    for row in reader : 
        students.append(row[1]) 
        RollNumbers.append(row[0])

while True : 
    _,frame = cam.read()
    decodedframe = decode(frame)
    try :
        for qrcode in decodedframe : 
            name = decodedframe[0].data.decode()
            if name in students : 
                RollNumbers.remove(RollNumbers[students.index(name)])
                students.remove(name)
    except:
        print("Error")
    cv2.imshow("Attendace System",frame)
    k = cv2.waitKey(100) & 0xff 
    if k==27: 
        break # press escape to close the loop
print(f"Absent Students Name : {students}.")
print(f"Absent Students Roll No : {RollNumbers}")
