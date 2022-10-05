import random as rr
import string as ss



"""
ASCII 
A -> Z : 65 -> 90
a -> z : 97 -> 122
"""

characters = ['@', '#', '$', '%', '&', '?']


pass_len = int(input('How lengthy do you want your password to be : '))

tempy, tempz = 0, 0
tempx = rr.randint(2, pass_len-1)                           # alphabets

if tempx != pass_len:
    tempy = rr.randint(1, (pass_len - tempx - 1))           # numbers
    total_nums = tempy

if (tempx + tempy) != pass_len:
    tempz = rr.randint(1, (pass_len-(tempx+tempy)))         # special characters
    total_symbols = tempz

# password : empty string for now
pass_word = ''

# adding alphabets

while tempx:
    x = tempx
    num_cap = rr.randint(0, x)
    num_low = x-num_cap

    total_cap = num_cap
    total_low = num_low

    # capitals in password :
    while num_cap:
        temp = chr(rr.randint(65, 90))
        pass_word = pass_word + str(temp)
        num_cap -= 1

    # lower-case in password :
    while num_low:
        temp = chr(rr.randint(97, 122))
        pass_word = pass_word + str(temp)
        num_low -= 1

    break

# adding numbers to the password
while tempy:
    temp = (rr.randint(0, 9))
    pass_word = pass_word + str(temp)
    tempy -= 1

# adding special characters to the password
while tempz:
    temp = rr.randint(0, len(characters)-1)
    pass_word = pass_word + characters[temp]
    tempz -= 1

#shuffles the string
def shuffle_(alpha):
    str_temp = list(alpha)
    rr.shuffle(str_temp)
    alpha = ''.join(str_temp)
    return alpha

#adds colour to the text
def colored(r, g, b, text):
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)

final_pass =colored(200,200,50, (shuffle_(shuffle_(shuffle_(pass_word)))))


# result & summary
result = """
Generate Password Summary :

Charactor Uppercase : {0}
Charactor Lowercase : {1}
Numbers : {2}
Symbols : {3}

Your computer generated password is :
{4}
""".format(total_cap, total_low, total_nums, total_symbols, final_pass)

print(result)

# print(f"\nYour computer generated password is : {final_pass}\n\n")
