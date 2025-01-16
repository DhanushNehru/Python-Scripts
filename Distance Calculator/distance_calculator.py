# Uses the pythagorean theorem to calculate the distance between two points on a 2D plane.
# The points are represented as tuples of two numbers.
# The function should return a float.

# Sample :- startX = 0, startY = 0, endX = 3, endY = 4. 
# So, according to pythagorean theorem, the distance between these two points is 5.0.

# Hope this helps!
import math

while True:
    que=input("Do you want to calculate the distance between two points? (yes/no): ")
    if que.lower() == "yes":
        pass
    elif que.lower() == "no":
        print("Thank you for using the distance calculator!")
        quit()
    else:
        print("Invalid input! Please enter 'yes' or 'no'.")
        continue    

    startX = input("Enter starting x-coordinate: ")
    if startX.isalpha():
        print("Error! Input has to be a number!")
        continue
    startY = input("Enter starting y-coordinate: ")
    if startY.isalpha():
        print("Error! Input has to be a number!")
        continue
    endX = input("Enter ending x-coordinate: ")
    if endX.isalpha():
        print("Error! Input has to be a number!")
        continue
    endY = input("Enter ending y-coordinate: ")
    if endY.isalpha():
        print("Error! Input has to be a number!")
        continue

    startX = float(startX)
    startY = float(startY)
    endX = float(endX)
    endY = float(endY)
    distance = math.sqrt(math.pow(startX - endX, 2) + math.pow(startY - endY, 2))
    print(f"The distance between ({startX}, {startY}) and ({endX}, {endY}) is {distance}.")
