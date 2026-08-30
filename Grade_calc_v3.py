def get_user_grades():
    """Collects grades from the user. Supports single numbers or comma-separated lists."""
    grades = []
    print("Enter your grades one by one or separated by commas. Type 'done' when you are finished.")
    while True:
        user_input = input("Enter grade(s) (or 'done' to finish): ").strip()
        
        if user_input.lower() == 'done':
            break
            
        # Split the input by commas in case you typed multiple numbers
        parts = user_input.split(',')
        for part in parts:
            part = part.strip() # Remove any accidental spaces
            if part: # Make sure it's not an empty string
                try:
                    grades.append(float(part))
                except ValueError:
                    print(f"⚠️ Skipping invalid input: '{part}'")
                    
    return grades

def calculate_average(grades):
    """Calculates the average of a list of grades."""
    if len(grades) == 0:
        return None
    return sum(grades) / len(grades)
def get_letter_grade(average):
    """Determines the letter grade based on the average score."""
    if average is None:
        return None
    if average >= 90:
        return "A"
    elif average >= 80:
        return "B"
    elif average >= 70:
        return "C"
    elif average >= 60:
        return "D"
    else:
        return "F"


def main():
    """Main function to run the program."""
    grades = get_user_grades()
    if len(grades) > 0:
        average = calculate_average(grades)
        letter = get_letter_grade(average)
        print(f"\nYou entered {len(grades)} grades.")
        print(f"Your average score is: {average:.2f}")
        print(f"Your letter grade is: {letter}")
    else:
        print("No grades were entered. Cannot calculate average.")


if __name__ == "__main__":
    main()