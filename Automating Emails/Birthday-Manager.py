import csv
import smtplib, ssl

message="""Hi {fname}, Wish you a very Happy birthday.                 
Hope you had a great time."""

sender_address="forpythonbirthdayproject@gmail.com"
sender_password="qwerty@12345"

context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_address,sender_password)

    with open(r"C:\Users\sriva\OneDrive\Desktop\VS Code\Python\birthday.csv") as file:
        reader=csv.reader(file)
        next(reader)
        for fname,lname,email,dob in reader:
            server.sendmail(
                sender_address,
                email,
                message.format(fname=fname),
            )

add=input(
    """Do you wish to add or remove names to the csv file?
    if you want add names type add
    otherwise if you want remove names type remove
    if you wish to exit, type exit   
    """
)
 
if add=="add":
    new_data=input("Enter data as first name,lastname,email,date of birth: ")
    new_data=new_data.split(",")
    with open(r"C:\Users\sriva\OneDrive\Desktop\VS Code\Python\birthday.csv",'r+') as file:
        writer_object=csv.writer(file)
        next(file)
        writer_object.writerow(new_data)
elif add=="remove":
    lines=[]
    removal=input("Enter the first name of the person to be removed: ")
    with open(r"C:\Users\sriva\OneDrive\Desktop\VS Code\Python\birthday.csv",'r') as file:
        reader=csv.reader(file)
        for row in reader:
            lines.append(row)
        for fields in row:
            if fields==removal:
                lines.remove(row)
    with open(r"C:\Users\sriva\OneDrive\Desktop\VS Code\Python\birthday.csv",'w',newline="") as file:
        writer=csv.writer(file)
        writer.writerows(lines)
    



