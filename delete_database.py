import json
import os

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

# Function to clear the entire database and images folder
def clear_database():
    try:
        with open("student_database.json", "w") as file:
            file.write(json.dumps({}))
        print("Database cleared successfully.")
    except Exception as e:
        print(f"An error occurred while clearing the database: {e}")
        
    try:
        # Clear the images folder
        for filename in os.listdir("student_images"):
            file_path = os.path.join("student_images", filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
        print("Images folder cleared successfully.")
    except Exception as e:
        print(f"An error occurred while clearing the images folder: {e}")

# Function to delete a student record by ID and image
def delete_student_record(student_id):
    student_database = load_database()
    if student_id in student_database:
        # Delete the student's image
        image_path = student_database[student_id]["image_path"]
        try:
            os.remove(image_path)
            print(f"Image for Student ID {student_id} deleted successfully.")
        except FileNotFoundError:
            print(f"Image for Student ID {student_id} not found.")
        except Exception as e:
            print(f"An error occurred while deleting the image: {e}")
        
        # Delete the student record
        del student_database[student_id]
        try:
            with open("student_database.json", "w") as file:
                json.dump(student_database, file)
            print(f"Student record with ID {student_id} deleted successfully.")
        except Exception as e:
            print(f"An error occurred while deleting the student record: {e}")
    else:
        print("Student not found in the database.")

# Function to display all student IDs and names
def display_student_ids_and_names():
    student_database = load_database()
    print("Student ID\tName")
    print("--------------------")
    for student_id, student_info in student_database.items():
        print(f"{student_id}\t\t{student_info['name']}")

# Main function to interact with the user
def main():
    action = input("Enter 'clear' to clear the entire database, 'delete' to delete a student record, or 'display' to show all student IDs and names: ").lower()
    
    if action == 'clear':
        clear_database()
    elif action == 'delete':
        display_student_ids_and_names()  # Display all student IDs and names before asking for deletion
        student_id = input("Enter the student ID to delete the record: ")
        delete_student_record(student_id)
    elif action == 'display':
        display_student_ids_and_names()
    else:
        print("Invalid action. Please enter 'clear', 'delete', or 'display'.")

# Run the main function
if __name__ == "__main__":
    main()
