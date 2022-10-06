import pyjokes

def cat(op):
    if op == 1:
        return "neutral"
    if op == 2:
        return "chuck"
    if op == 3:
        return "twister"
    if op == 4:
        return "all"
def lan(op):
    if op == 3:
        return "de"
    elif 1<=op<=2 or op == 4:
        return "en"
        
option = 0
print("MENU\n1. Neutral\n2. Chuck Norris jokes\n3. Twisters(in gerrman)\n4. All\n5. Exit.")
while option != 5:
    try:
        option = int(input("enter option: "))
        My_joke = pyjokes.get_joke(language= lan(option), category= cat(option))
        print(My_joke)
    except pyjokes.pyjokes.LanguageNotFoundError:
        print("successfully exited!")