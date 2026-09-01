# Day 5: Object-Oriented Programming (Classes and Objects)


class GradeManager:
    """A class to manage student grades, calculations, and letter evaluations."""

    def __init__(self):
        # Initialize the empty list of grades when new object is created
        self.grades = []

    def add_grades(self, user_input):
        """Parses single or comma-separated grades from user input and adds them to the instance."""
        parts = user_input.split(',')
        for part in parts:
            part = part.strip()  # Remove any accidental spaces
            if part:
                try:
                    self.grades.append(float(part))
                except ValueError:
                    print(f"⚠️ Skipping invalid input: '{part}'")

    def calculate_average(self):
        """Calculates and returns the average of the stored grades."""
        if len(self.grades) == 0:
            return 0
        return sum(self.grades) / len(self.grades)

    def get_letter_grade(self, average):
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

    def display_summary(self):
        """Prints the final summary of grades."""
        if len(self.grades) > 0:
            average = self.calculate_average()
            letter = self.get_letter_grade(average)
            print(f"\nYou entered {len(self.grades)} grades.")
            print(f"Your average score is: {average:.2f}")
            print(f"Your letter grade is: {letter}")
        else:
            print("No grades were entered. Cannot calculate average.")


def main():
    """Main execution function utilizing the GradeManager class."""
    # Create an instance (object) of the GradeManager class
    my_grades = GradeManager()
    print("Enter your grades one by one or separated by commas. Type 'done' when you are finished.")
    while True:
        user_input = input("Enter grade(s) (or 'done' to finish): ").strip()
        if user_input.lower() == 'done':
            break
        my_grades.add_grades(user_input)
        # Trigger the display method on our object
        my_grades.display_summary()


if __name__ == "__main__":
    main()


