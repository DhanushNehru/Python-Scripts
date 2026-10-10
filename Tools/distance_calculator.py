# Uses the pythagorean theorem to calculate the distance between two points on a 2D plane.
# The points are represented as tuples of two numbers.
# The function should return a float.

# Sample :- startX = 0, startY = 0, endX = 3, endY = 4. 
# So, according to pythagorean theorem, the distance between these two points is 5.0.

# Hope this helps!

# Importing module(s)
import math

# Main loop
while True:
    use_program=input("Do you want to calculate the distance between two points? (yes/no): ")
    if use_program.lower() == "yes":
        pass
    elif use_program.lower() == "no":
        print("Thank you for using the distance calculator!")
        quit()
    else:
        print("Invalid input! Please enter 'yes' or 'no'.")
        continue    

    # Input validation for startX, startY, endX, endY

    # startX
    while True:
        startX = input("Enter starting x-coordinate: ")
        if not startX.isnumeric():
            print("Error! Input has to be a number!")
            continue
        else:
            break
    
    # startY
    while True:
        startY = input("Enter starting y-coordinate: ")
        if not startY.isnumeric():
            print("Error! Input has to be a number!")
            continue
        else:
            break

    # endX
    while True:
        endX = input("Enter ending x-coordinate: ")
        if not endX.isnumeric():
            print("Error! Input has to be a number!")
            continue
        else:
            break

    # endY    
    while True:
        endY = input("Enter ending y-coordinate: ")
        if not endY.isnumeric():
            print("Error! Input has to be a number!")
            continue
        else:
            break

    # Converting the values to floats
    startX = float(startX)
    startY = float(startY)
    endX = float(endX)
    endY = float(endY)

    # The calculation
    distance = math.sqrt(math.pow(startX - endX, 2) + math.pow(startY - endY, 2))
    print(f"The distance between ({startX}, {startY}) and ({endX}, {endY}) is {distance} units.")
