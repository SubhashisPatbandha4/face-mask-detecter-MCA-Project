import json
import tkinter as tk
from PIL import Image, ImageTk

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

# Function to display student information by ID
def display_student_info(database, student_id):
    student = database.get(student_id)
    if student:
        # Create a Tkinter window
        root = tk.Tk()
        root.title(f"Student Information - ID: {student_id}")

        # Set window dimensions
        root.geometry("400x300")

        # Display student name
        label_name = tk.Label(root, text=f"Name: {student['name']}")
        label_name.pack()

        # Display default mask
        label_default_mask = tk.Label(root, text=f"Default Mask: {student['default_mask']}")
        label_default_mask.pack()

        # Load and resize the image to fit the window
        image = Image.open(student['image_path'])
        image = image.resize((350, 200), Image.BILINEAR)  # Resize image to fit the window
        photo = ImageTk.PhotoImage(image)
        label_image = tk.Label(root, image=photo)
        label_image.image = photo  # Keep a reference to prevent garbage collection
        label_image.pack()

        # Run the Tkinter event loop
        root.mainloop()
    else:
        print("Student not found in the database.")


# Main function to interact with the user
def main():
    # Load the student database from the file
    student_database = load_database()

    # Display all student IDs and names
    print("Student ID\tName")
    print("--------------------")
    for student_id, student_info in student_database.items():
        print(f"{str(student_id)}\t\t{student_info['name']}")

    # Get input from user for the student ID to view details
    student_id = input("\nEnter the student ID to view details (or 'quit' to exit): ")

    while student_id.lower() != 'quit':
        # Validate input and display student information if valid
        if student_id in student_database:
            display_student_info(student_database, student_id)
        else:
            print("Student not found in the database.")

        # Get next input from user
        student_id = input("\nEnter the student ID to view details (or 'quit' to exit): ")

    print("Exiting...")


# Run the main function
if __name__ == "__main__":
    main()
