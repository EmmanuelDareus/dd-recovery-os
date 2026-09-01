# Day 5/6: Named Assignments with Dictionaries and JSON Persistence
import json
import os

class GradeManager:
    """A class to manage named assignments, calculate averages, and save persistently."""
    
    def __init__(self, filename="grades_v8.json"):
        self.filename = filename
        self.records = {}
        self.load_from_file()

    def add_assignment(self, name, score):
        """Adds a named assignment and its score to the records."""
        try:
            numeric_score = float(score)
            self.records[name] = numeric_score
            print(f"✅ Successfully added '{name}': {numeric_score}")
            self.save_to_file()
        except ValueError:
            print(f"❌ Error: Score must be a valid number, got '{score}'.")

    def remove_assignment(self, name):
        """Removes an assignment by name if it exists."""
        if name in self.records:
            del self.records[name]
            print(f"🗑️ Removed assignment: '{name}'")
            self.save_to_file()
        else:
            print(f"⚠️ Assignment '{name}' not found.")

    def calculate_average(self):
        """Calculates and returns the average of all recorded scores."""
        if len(self.records) == 0:
            return 0
        return sum(self.records.values()) / len(self.records)

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
        """Saves the records dictionary to a JSON file on disk."""
        try:
            with open(self.filename, 'w') as file:
                json.dump(self.records, file)
        except IOError:
            print("❌ Error: Could not save data to file.")

    def load_from_file(self):
        """Loads records from the JSON file if it exists."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as file:
                    self.records = json.load(file)
            except (json.JSONDecodeError, IOError):
                print("⚠️ Error reading save file. Starting with empty records.")

    def display_detailed_summary(self):
        """Prints out all assignments, scores, average, and letter grade."""
        if len(self.records) > 0:
            print(f"\n--- Grade Breakdown ---")
            for name, score in self.records.items():
                print(f"  • {name}: {score}")
            
            avg = self.calculate_average()
            letter = self.get_letter_grade(avg)
            print(f"-----------------------")
            print(f"Total Assignments: {len(self.records)}")
            print(f"Overall Average: {avg:.2f}")
            print(f"Overall Letter Grade: {letter}")
            print(f"-----------------------")
        else:
            print("\n📂 No assignments on record yet.")

    def clear_all(self):
        """Clears all records and deletes the save file."""
        self.records = {}
        if os.path.exists(self.filename):
            os.remove(self.filename)
        print("🗑️ All records and save data cleared.")


def main():
    """Main execution function featuring an expanded interactive menu."""
    my_grades = GradeManager()
    
    while True:
        print("\n=== Advanced Grade Book ===")
        print("1. View Grade Summary")
        print("2. Add Assignment & Score")
        print("3. Delete an Assignment")
        print("4. Clear All Data")
        print("5. Exit")
        
        choice = input("Select an option (1-5): ").strip()
        
        if choice == '1':
            my_grades.display_detailed_summary()
        elif choice == '2':
            name = input("Enter assignment name (e.g., 'Math Quiz 1'): ").strip()
            if name:
                score = input(f"Enter score for '{name}': ").strip()
                my_grades.add_assignment(name, score)
            else:
                print("❌ Assignment name cannot be empty.")
        elif choice == '3':
            name = input("Enter the exact name of the assignment to remove: ").strip()
            if name:
                my_grades.remove_assignment(name)
        elif choice == '4':
            confirm = input("Are you sure you want to delete all records? (y/n): ").strip().lower()
            if confirm == 'y':
                my_grades.clear_all()
        elif choice == '5':
            print("Exiting program. Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()