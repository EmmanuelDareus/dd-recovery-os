Grade = [] 
print("Enter your grades one by one. Type 'done' when you are finished. ")
while True:
    user_input = input("Enter grade (or 'done' to finish): ")
    if user_input.lower() == 'done':
        break
    try:
        grade = float(user_input)
        Grade.append(grade)
    except ValueError:
        print("Please enter a valid grade or 'done' to finish.")

if len(Grade) > 0:
    average = sum(Grade) / len(Grade)
    if average >= 90:
        letter = "A"
    elif average >= 80:
        letter = "B"
    elif average >= 70:
        letter = "C"
    elif average >= 60:
        letter = "D"
    else:
        letter = "F"

    print(f"\nYour average score is: {average:.2f}")
    print(f"Your letter grade is: {letter}")
else:
    print("No grades were entered. Cannot calculate average.")