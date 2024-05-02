import json

# Function to load the student database from a file
def load_database():
    try:
        with open("student_database.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {}

# Function to save the student database to a file
def save_database(database):
    try:
        with open("student_database.json", "w") as file:
            json.dump(database, file)
            print("Database updated successfully.")
    except Exception as e:
        print(f"An error occurred while saving the database: {e}")

# Function to change the default mask parameter for a specific student
def change_mask_parameter(database, student_id, new_mask_value):
    student = database.get(student_id)
    if student:
        student['default_mask'] = new_mask_value
        save_database(database)
    else:
        print("Student not found in the database.")

# Function to reset the default mask parameter for all students back to zero
def reset_all_masks(database):
    for student_id, student_info in database.items():
        student_info['default_mask'] = 0
    save_database(database)

# Main function to interact with the user
def main():
    # Load the student database from the file
    student_database = load_database()

    # Display all student IDs and names
    print("Student ID\tName")
    print("--------------------")
    for student_id, student_info in student_database.items():
        print(f"{str(student_id)}\t\t{student_info['name']}")

    # Get input from user for the action to perform
    action = input("\nEnter 'change' to change a specific student's mask parameter or 'reset' to reset all masks to zero: ")

    if action.lower() == 'change':
        # Get input for the student ID and new mask parameter value
        student_id = input("Enter the student ID: ")
        new_mask_value = input("Enter the new mask parameter value: ")
        change_mask_parameter(student_database, student_id, int(new_mask_value))
    elif action.lower() == 'reset':
        reset_all_masks(student_database)
    else:
        print("Invalid action. Please enter 'change' or 'reset'.")

# Run the main function
if __name__ == "__main__":
    main()
