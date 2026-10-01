#Creating variables with different data types
from os import name


student_name = "Emmanuel Dareus"  # String (text)
age = 17                          # Integer (whole number)
target_hourly_rate = 30.0         # Float (decimal number) 
is_ready_to_code = True           # Boolean (True or False)

#Using the Variables Together 
print(student_name) 
print(target_hourly_rate * 40) # Match using Variable

name = "Emmanuel Dareus"
print(f"hello my name is {name}, and I am {age} years old. I am ready to code: {is_ready_to_code}. My target hourly rate is ${target_hourly_rate}.")

#1. Ask for name using input() 
user_name = input("What is your name?")

#2. Ask for hourly rate using input() and convert to float for math
rate_input = input("Enter your target hourly rate: ")
hourly_rate = float(rate_input) 

#3. Calculate weekly earnings (40 hours) and print with an f-string
weekly_earnings = hourly_rate * 40
print(f"User {user_name} will earn ${weekly_earnings} per week at a rate of ${hourly_rate} per hour.")
 