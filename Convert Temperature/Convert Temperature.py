import math

def from_cel(x):    
    y = input("You want to convert it into: \n (a)fahrenheit (b)Kelvin ")
    
    if y == 'a':
        final = (x*(9/5)) + 32
        print(f"The temperature is: {final} °F")

    else:
        final = x + 273.15
        print(f"The temperature is: {final} K")

        

def from_fah(x):
    y = input("You want to convert it into: \n (a)celsius (b)Kelvin ")
    
    if y == 'a':
        final = (x - 32)*(5/9)
        print(f"The temperature is: {final} °C")


    else:
        final = (x - 32)*(5/9) + 273.15
        print(f"The temperature is: {final} K")


def from_Kel(x):
    y = input("You want to convert it into: \n (a)celsius (b)fahrenheit ")
    
    if y == 'a':
        final = x - 273.15
        print(f"The temperature is: {final} °C")

    else:
        final = (x - 273.15)*(5/9) + 32
        print(f"The temperature is: {final} °F")




def get_temp():
    global t
    t = input("What would you like to convert from? (input no.): \n (1)Celsius (2)fahrenheit (3)Kelvin ")

get_temp()

x = float(input("Enter Temperature: ")) 

if t == "1":
    from_cel(x)

elif t == '2':
    from_fah(x)

elif t == '3':
    from_Kel(x)

else:
    print("please enter a correct input")
    get_temp()




