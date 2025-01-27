# purpose of order.py is the front end for users to submit their order
from pizzaReceipt import *  # asks to import all functions found in the pizzaReceipt.py file

# set all initial variables before beginning
size = ""
pizza_lst = []
pizza_lst_current = []
toppings_lst = []  # list to be a parameter for generateReceipt function
list_order_yes = ["Yes", "yes", "Y", "y", "YES"]
list_order_no = ["No", "no", "Q", "NO", "N", "n"]
TOPPINGS = ("ONION", "TOMATO", "GREEN PEPPER", "MUSHROOM", "OLIVE", "SPINACH", "BROCCOLI", "PINEAPPLE",
            "HOT PEPPER", "PEPPERONI", "HAM", "BACON", "GROUND BEEF", "CHICKEN", "SAUSAGE")

# ask user whether they want to order.
order = input("Do you want to order a pizza? ")

# case for when an invalid input is submitted
while (order not in list_order_yes) and (order not in list_order_no):
    order = input("Do you want to order a pizza? ")

# ask for size
if order in list_order_yes:
    size = input("Choose a size: ")
    size.upper()

    # case for when a user inputs invalid size
    while size.upper() not in ["S", "M", "L", "XL"]:
        size = input("Choose a size: ")

# entire loop to repeat if user wants to order more than one pizza
while order in list_order_yes:
    # set empty toppings list as it will show empty each time loop is made
    toppings_lst = []
    # ask user for topping, whether they want to see a list of the toppings, or to finish ordering toppings.
    topping = input('Type in one of our toppings to add it to your pizza. To see the list of toppings, enter "LIST". '
                    'When you are done adding toppings, enter "X" ')

    # cae for when a user places an invalid input for this question
    while (topping.upper() != "X") and (topping.upper() != "LIST") and (topping.upper() not in TOPPINGS):
        topping = input('Type in one of our toppings to add it to your pizza. To see the list of toppings, enter "LIST". '
                        'When you are done adding toppings, enter "X" ')

    print()
    # toppings while loop which ask for toppings selection or list view, multiple times until user enters X
    while topping.upper() != "X":
        TOPPINGS = ("ONION", "TOMATO", "GREEN PEPPER", "MUSHROOM", "OLIVE", "SPINACH", "BROCCOLI", "PINEAPPLE",
                    "HOT PEPPER", "PEPPERONI", "HAM", "BACON", "GROUND BEEF", "CHICKEN", "SAUSAGE")
        if topping.upper() == "LIST":
            print(topping.upper())
            print(TOPPINGS)
            topping = input('Type in one of our toppings to add it to your pizza. To see the list of toppings, enter "LIST". '
                            'When you are done adding toppings, enter "X" \n \n')
        elif topping.upper() in TOPPINGS:
            print(topping.upper())
            print("Added", topping.upper(), "to your pizza")
            toppings_lst.append(topping)
            topping = input('Type in one of our toppings to add it to your pizza. To see the list of toppings, enter "LIST". '
                            'When you are done adding toppings, enter "X" \n \n')

    # add the size and toppings list as a tuple to pizza_lst
    pizza_lst.append((size.upper(), toppings_lst))
    print(pizza_lst)
    # ask whether they want to continue ordering
    order = input("Do you want to continue ordering? ")

    # case for when user types invalid input
    while (order not in list_order_yes) and (order not in list_order_no):
        order = input("Do you want to order a pizza? ")

    # if they say no, break the loop and go through the last line of the code
    if order in list_order_no:
        break
    elif order in list_order_yes:
        size = input("Choose a size: ")  # if they want to order again start by asking size

    # case for when user types invalid input
    while size.upper() not in ["S", "M", "L", "XL"]:
        size = input("Choose a size: ")

generateReceipt(pizza_lst)  # at the end of program, call function using pizza_lst as a parameter
