import pyinputplus as pyip

#Input user variables
weight = pyip.inputInt('How much do you weigh in Lbs? ')
height = pyip.inputInt('How tall are you in inches? ')

#Calculate BMI
bmi = (703 * weight) / (height) ** 2
bmi = round(bmi, 1)

#Logic for under/overweight per BMI scale
if bmi < 18.5:
    bmi_category = 'underweight'
elif bmi >= 18.5 and bmi <= 24.9:
    bmi_category = 'normal weight'
elif bmi >= 25 and bmi <= 29.9:
    bmi_category = 'overweight'
elif bmi >= 30:
    bmi_category = 'obese'

print(f'your BMI is {bmi}, you are {bmi_category}.')