import random
num_questions = int(input("Enter number of questions: "))
q_solutions = dict() # creates an empty dictionary
count = 0 # counts the number of questions asked
for i in range (num_questions):
      question = input("Enter your question: ")
      answer = input("Enter your answer: ")
      q_solutions[question.lower()] = answer.lower() # adding the key-value pair to dictionary
      print("\n")
q_s = list(q_solutions.keys())
while True:
      q = random.choice(q_s) # picks a random key from the question and answer dictionary
      count+=1 # increments the count variable, to indicate that a question has been asked
      print(q)
      ans = input("Enter an answer for the above question: ")
      if ans.lower() == q_solutions[q]:
        print("You're right!")
      else:
        print("You're wrong! \nThe correct answer is:",q_solutions[q])
      q_solutions.pop(q) # removes the question-answer pair that has been asked to prevent repetition
      if count > len(q_solutions):
          print("All questions have been asked.")
          break
      choice = input("\nDo you wish to continue? Enter Y OR N: ")
      print()
      if choice.lower() == 'n':
          break
