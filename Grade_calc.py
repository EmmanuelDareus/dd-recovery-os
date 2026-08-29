print("---Welcome to the Grade Calculator---")
grade = []
for i in range(3):
    score = float(input("Enter score for subject {}: ".format(i + 1)))
    grade.append(score)

average = sum(grade) / len(grade)

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
