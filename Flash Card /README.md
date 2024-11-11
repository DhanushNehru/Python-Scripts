## Prerequisites
+ Python 3.x
+ Import of random module

## Workings of Code
+ Imports random module --> Selective import can be done of random.choice() only
+ 
+ The code uses both for and while loops
+ 
+ The while loop is infinite, and option to exit the program is given to user
+ 
+ User enters question and answer which is accepted via an input()
+ 
+ These input question-answers are stored in a dictionary as key-value pairs (key = question, value = answer)
+ 
+ After input by the user, stored questions are randomly asked to user using random.choice() from random module
+ 
+ Answers are verified by calling the question stored in the dictionary
+
+ Code ends when user inputs "n" to indicate that they wish to exit, or when every question has been asked.
