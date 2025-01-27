import subprocess


def runTest (file, inText):
    if file =="order":
        res = subprocess.run("python " + file + ".py", input=inText, capture_output=True, text=True, shell=True)
        return res.stdout
    
    if file == "pizzaReceipt":
        res = subprocess.run("python -c \"from pizzaReceipt import *; generateReceipt([" +inText+ "])\"", capture_output=True, text=True, shell= True)
        return res.stdout


def equalWithoutSpaces(expected, student):
    expected = expected.replace(" ", "")
    expected = expected.replace("\t", "")
    student = student.replace(" ", "")
    student = student.replace("\t", "")
    return expected == student



# --------------- Test 1 - No Order---------------

inputString = ""
studentOutput = runTest("pizzaReceipt", inputString)
expectedOutput = "You did not order anything\n"

# Compare studentOutput to expectedOutput
if studentOutput == expectedOutput:
    print("Test 1 Passed. (Receipt for empty order)")
else:
    print("Test 1 Failed. (Receipt for empty order)")

#print(studentOutput)

# --------------- Test 2 - List of Orders---------------

inputString = "('L', ['HAM', 'BACON', 'ONION', 'TOMATO']), ('S', ['PEPPERONI', 'SAUSAGE', 'CHICKEN', 'HAM']), ('L', ['BROCCOLI', 'CHICKEN', 'ONION'])"
studentOutput = runTest("pizzaReceipt", inputString)
expectedOutput = "Your order: \nPizza 1: L 				  11.99\n- HAM\n- BACON\n- ONION\n- TOMATO\nExtra Topping (L)		   1.00\n"
expectedOutput += "Pizza 2: S 				   7.99\n- PEPPERONI\n- SAUSAGE\n- CHICKEN\n- HAM\nExtra Topping (S)		   0.50\n"
expectedOutput += "Pizza 3: L 				  11.99\n- BROCCOLI\n- CHICKEN\n- ONION\nTax:					   4.35\nTotal:					  37.82\n"

# Compare studentOutput to expectedOutput
#if studentOutput == expectedOutput:
if equalWithoutSpaces(expectedOutput, studentOutput):
    print("Test 2 Passed. (Receipt for empty order of 3 pizzas)")
else:
    print("Test 2 Failed. (Receipt for empty order of 3 pizzas)")


# --------------- Test 3 - List of Orders---------------

inputString = "('XL', ['GREEN PEPPER', 'HOT PEPPER', 'MUSHROOM', 'ONION', 'SPINACH']), ('L', ['PEPPERONI', 'ONION', 'OLIVE', 'MUSHROOM']), ('L', ['PINEAPPLE', 'HAM']), ('M', ['GROUND BEEF', 'TOMATO', 'ONION', 'SPINACH'])"
studentOutput = runTest("pizzaReceipt", inputString)
expectedOutput = "Your order: \nPizza 1: XL 				  13.99\n- GREEN PEPPER\n- HOT PEPPER\n- MUSHROOM\n- ONION\n- SPINACH\nExtra Topping (XL)		   1.25\n"
expectedOutput += "Extra Topping (XL)		   1.25\nPizza 2: L 				  11.99\n- PEPPERONI\n- ONION\n- OLIVE\n- MUSHROOM\n"
expectedOutput += "Extra Topping (L)		   1.00\nPizza 3: L 				  11.99\n- PINEAPPLE\n- HAM\nPizza 4: M 				   9.99\n"
expectedOutput += "- GROUND BEEF\n- TOMATO\n- ONION\n- SPINACH\nExtra Topping (M)		   0.75\nTax:					   6.79\nTotal:					  59.00\n"

# Compare studentOutput to expectedOutput
if equalWithoutSpaces(expectedOutput, studentOutput):
    print("Test 3 Passed. (Receipt for empty order of 4 pizzas)")
else:
    print("Test 3 Failed. (Receipt for empty order of 4 pizzas)")

# --------------- Test 4 - Find Specific Values in Output ---------------

studentOutput = runTest("order", "Yes\nL\nHAM\nX\nNo\n")

if studentOutput.find("13.55") != -1:
    print("Test 4 Passed. (Ordering system for order of 1 pizza)")
else:
    print("Test 4 Failed. (Ordering system for order of 1 pizza)")

#print(studentOutput)

# --------------- Test 5 - Find Specific Values in Output---------------

studentOutput = runTest("order", "Yes\nmedium\nM\nLIST\npepperoni\nonion\nmushroom\nhot pepper\ntomato\nX\nq\n")

if studentOutput.find("\"X\"\n('") != -1 and studentOutput.count("Choose a size:") == 2 and studentOutput.count("Type in one of our toppings") == 7 and studentOutput.find("1.49") != -1 and studentOutput.find("12.98") != -1:
    print("Test 5 Passed. (Ordering system with typo and use of LIST)")
else:

    print("Test 5 Failed. (Ordering system with typo and use of LIST)")

print()
print(studentOutput.find("\"X\"\n('") != -1)
print(studentOutput.count("Choose a size:") == 2)
print(studentOutput.count("Type in one of our toppings") == 7)
print(studentOutput.find("1.49") != -1)
print(studentOutput.find("12.98") != -1)
print()

# --------------- Find Specific Values in Output ---------------

studentOutput = runTest("order", "y\nm\nsausage\nbacon\nonion\nX\ny\nXl\nchicken\ntomato\nspinach\nmushroom\nx\ny\nm\nolive\nbroccoli\nhot pepper\ngreen pepper\nx\nno\n")

if studentOutput.count("Type in one of our toppings") == 14 and studentOutput.find("4.68") != -1 and studentOutput.find("40.65") != -1:
    print("Test 6 Passed. (Ordering system for order of 3 pizzas)")
else:
    print("Test 6 Failed. (Ordering system for order of 3 pizzas)")
    
# print(studentOutput)
# print(expectedOutput)
# --------------------------------




