# Day 5/6: Interactive CLI Menu System with JSON Persistence
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
        added_count = 0
        for part in parts:
            part = part.strip()
            if part:
                try:
                    self.grades.append(float(part))
                    added_count += 1
                except ValueError:
                    print(f"⚠️ Skipping invalid input: '{part}'")
        if added_count > 0:
            print(f"✅ Successfully added {added_count} grade(s).")
            self.save_to_file()

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
        except IOError:
            print("❌ Error: Could not save data to file.")

    def load_from_file(self):
        """Loads grades from the JSON file if it exists."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as file:
                    self.grades = json.load(file)
            except (json.JSONDecodeError, IOError):
                print("⚠️ Error reading save file. Starting with an empty grade list.")

    def display_summary(self):
        """Prints out the current summary of grades."""
        if len(self.grades) > 0:
            avg = self.calculate_average()
            letter = self.get_letter_grade(avg)
            print(f"\n--- Grade Summary ---")
            print(f"Total Grades Recorded: {len(self.grades)}")
            print(f"Grades List: {self.grades}")
            print(f"Average Score: {avg:.2f}")
            print(f"Letter Grade: {letter}")
            print(f"---------------------")
        else:
            print("\n📂 No grades on record yet.")

    def clear_grades(self):
        """Clears all grades and deletes the save file."""
        self.grades = []
        if os.path.exists(self.filename):
            os.remove(self.filename)
        print("🗑️ All grades and save data cleared.")


def main():
    """Main execution function featuring an interactive CLI menu loop."""
    my_grades = GradeManager()
    
    while True:
        print("\n=== Grade Management System ===")
        print("1. View Summary")
        print("2. Add Grades")
        print("3. Clear All Data")
        print("4. Exit")
        
        choice = input("Select an option (1-4): ").strip()
        
        if choice == '1':
            my_grades.display_summary()
        elif choice == '2':
            user_input = input("Enter grade(s) (comma-separated): ").strip()
            if user_input:
                my_grades.add_grades(user_input)
        elif choice == '3':
            confirm = input("Are you sure you want to delete all data? (y/n): ").strip().lower()
            if confirm == 'y':
                my_grades.clear_grades()
        elif choice == '4':
            print("Exiting program. Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    main()