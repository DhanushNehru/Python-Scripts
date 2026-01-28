import pyinputplus as pyip

#User input variables for calculating compound interest
time = pyip.inputInt('How many years will you be saving? Enter amount: ')
principal = pyip.inputFloat('How much money is currently in your account? Enter amount: ')
monthly_invest = pyip.inputFloat('How much money do you plan on investing monthly? Enter amount: ')
interest_percent = pyip.inputFloat('''What do you estimate will be the yearly interest of this investment?\n
Enter rate as percent (%): ''')

#Interest conversion
rate = interest_percent/100

#Calculate final amount after investing and accruing interest:
balance = principal

for year in range(time):
    balance = balance * (1 + rate)
    balance += monthly_invest * 12

#Print final result
print(f"This is how much money you would have in your account after {time} years: ${balance:,.2f}")
