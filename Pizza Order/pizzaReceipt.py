# purpose of pizzaReceipt.py is the back end where the developers create methods and functions to properly format the receipt and its total
def generateReceipt(pizzaOrder):
    # parameter will be placed with pizza_lst = ("M", ["PEPPERONI", "OLIVE"], -----)
    # set initial variables
    size = ""
    additional_price = 0
    price_before_tax = 0
    tax = 1.13
    counter = 1  # pizza number
    size_price = 0
    additional_price_tag = float(0)
    additional_price_tag_format = ""

    # if its an empty list, display this statement
    if len(pizzaOrder) == 0:
        print("You did not order anything")
        exit()

    # beginning of the format of receipt
    print("Your order: ")

    # a for loop which goes through all tuples in the list based on its indices
    for pizza in range(len(pizzaOrder)):
        # cases to determine the sizes selected and its price
        if pizzaOrder[pizza][0] == "S":
            size_price = 7.99
            size = "S"
        elif pizzaOrder[pizza][0] == "M":
            size_price = 9.99
            size = "M"
        elif pizzaOrder[pizza][0] == "L":
            size_price = 11.99
            size = "L"
        elif pizzaOrder[pizza][0] == "XL":
            size_price = 13.99
            size = "XL"

        # add the price of the size to the final price before tax
        price_before_tax += size_price

        # formatting the pizza number and its size beside it and the price on the other side
        if size == "XL":
            print("Pizza", str(counter) + ":", str(size) + "  \t\t\t  " + str(size_price))
        elif size == "L":
            print("Pizza", str(counter) + ":", str(size) + "  \t\t\t  " + str(size_price))
        elif size == "M":
            print("Pizza", str(counter) + ":", str(size) + "  \t\t\t   " + str(size_price))
        elif size == "S":
            print("Pizza", str(counter) + ":", str(size) + "  \t\t\t   " + str(size_price))

        # increment counter variable by one for the pizza number
        counter += 1

        # format the toppings with a dash in front
        for j in range(len(pizzaOrder[pizza][1])):
            print("- " + str(pizzaOrder[pizza][1][j]))

        # if theres more than three toppings, calculate the total additional price and added to the total price before tax
        if len(pizzaOrder[pizza][1]) > 3:
            n = len(pizzaOrder[pizza][1]) - 3
            if size == "S":
                additional_price_tag = 0.50
                additional_price_tag_format = "{:.2f}".format(additional_price_tag)
                additional_price = 0.50 * n
                price_before_tax += additional_price
            elif size == "M":
                additional_price_tag = 0.75
                additional_price = 0.75 * n
                price_before_tax += additional_price
            elif size == "L":
                additional_price_tag = 1.00
                additional_price_tag_format = "{:.2f}".format(additional_price_tag)
                additional_price = 1.00 * n
                price_before_tax += additional_price
            elif size == "XL":
                additional_price_tag = 1.25
                additional_price = 1.25 * n
                price_before_tax += additional_price

        # format the extra topping portion of the receipt with its size and price on the other side
        float_additional_price = float(additional_price)
        format_additional_price = "{:.2f}" .format(float_additional_price)

        for extra in range(len(pizzaOrder[pizza][1])):
            if extra > 2:
                if size == "XL":
                    print("Extra Topping", "(" + size + ")" + "\t\t   " + str(additional_price_tag))
                elif size == "L":
                    print("Extra Topping", "(" + size + ")" + "\t\t   " + str(additional_price_tag_format))
                elif size == "M":
                    print("Extra Topping", "(" + size + ")" + "\t\t   " + str(additional_price_tag))
                elif size == "S":
                    print("Extra Topping", "(" + size + ")" + "\t\t   " + str(additional_price_tag_format))
    # outside of loop begins, calculates the price before tax with the tax value set earlier
    price_final = price_before_tax * tax

    # add the tax price to be added and set it to a float, as well as the final price with tax
    float1 = float(price_before_tax * (13/100))
    float2 = float(price_final)
    formatFloat1 = "{:.2f}" .format(float1)
    formatFloat2 = "{:.2f}" .format(float2)

    # format the price of the tax, and the total with both values on the other side
    print("Tax:" + "\t\t\t\t\t   " + formatFloat1)
    print("Total:" + "\t\t\t\t\t  " + formatFloat2)
