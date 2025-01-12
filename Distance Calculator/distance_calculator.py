# Uses the pythagorean theorem to calculate the distance between two points on a 2D plane.
# The points are represented as tuples of two numbers.
# The function should return a float.

# Sample :- startX = 0, startY = 0, endX = 3, endY = 4. 
# So, according to pythagorean theorem, the distance between these two points is 5.0.

# Hope this helps!
import math

while True:
    startX = input("Enter starting x-coordinate: ")
    if not startX.isdigit():
        print("Error! Input has to be a number!")
        continue
    startY = input("Enter starting y-coordinate: ")
    if not startY.isdigit():
        print("Error! Input has to be a number!")
        continue
    endX = input("Enter ending x-coordinate: ")
    if not endX.isdigit():
        print("Error! Input has to be a number!")
        continue
    endY = input("Enter ending y-coordinate: ")
    if not endY.isdigit():
        print("Error! Input has to be a number!")
        continue

    startX = int(startX)
    startY = int(startY)
    endX = int(endX)
    endY = int(endY)
    distance = math.sqrt(math.pow(startX - endX, 2) + math.pow(startY - endY, 2))
    print(f"The distance between ({startX}, {startY}) and ({endX}, {endY}) is {distance}.")