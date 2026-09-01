# Day 5/6: Object-Oriented Programming with JSON Data Persistence
import json
import os

class GradeManager:
    """A class to manage, calculate, and persistently save student grades."""
    
    def __init__(self, filename="grades.json"):
        self.filename = filename
        self.grades = []
        self.load_from_file()

    def add_grades(self, user_input):
        """Parses single or comma-separated grades and adds them to the instance."""
        parts = user_input.split(',')
        for part in parts:
            part = part.strip()
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
        """Determines the letter grade based on an average score."""
        if average >= 90:
            return 'A'
        elif average >= 80:
            return 'B'
        elif average >= 70:
            return 'C'
        elif average >= 60:
            return 'D'
        else:
            return 'F'

    def save_to_file(self):
        """Saves the current grades list to a JSON file on disk."""
        try:
            with open(self.filename, 'w') as file:
                json.dump(self.grades, file)
            print(f"💾 Successfully saved grades to {self.filename}")
        except IOError:
            print("❌ Error: Could not save data to file.")

    def load_from_file(self):
        """Loads grades from the JSON file if it exists."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as file:
                    self.grades = json.load(file)
                print(f"📂 Loaded {len(self.grades)} existing grades from {self.filename}")
            except (json.JSONDecodeError, IOError):
                print("⚠️ Error reading save file. Starting with an empty grade list.")

    def display_summary(self):
        """Prints out the final summary of grades and saves data."""
        if len(self.grades) > 0:
            avg = self.calculate_average()
            letter = self.get_letter_grade(avg)
            print(f"\nYou have a total of {len(self.grades)} grades on record.")
            print(f"Your average score is: {avg:.2f}")
            print(f"Your letter grade is: {letter}")
            self.save_to_file()
        else:
            print("No grades were entered.")


def main():
    """Main execution function utilizing persistent GradeManager storage."""
    my_grades = GradeManager()
    
    print("\nEnter your grades one by one or separated by commas.")
    print("Type 'done' to finish, or 'clear' to reset your saved data.")
    
    while True:
        user_input = input("Enter grade(s) (or 'done'/'clear'): ").strip()
        
        if user_input.lower() == 'done':
            break
        elif user_input.lower() == 'clear':
            my_grades.grades = []
            if os.path.exists(my_grades.filename):
                os.remove(my_grades.filename)
            print("🗑️ Saved grades cleared.")
            continue
            
        my_grades.add_grades(user_input)
        
    my_grades.display_summary()

if __name__ == "__main__":
    main()