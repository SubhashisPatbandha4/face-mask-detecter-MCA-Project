import os
import shutil
import json
import tkinter as tk
from tkinter import filedialog

DATABASE_FILE = "student_database.json"

# Function to load the student database from a file
def load_database():
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, "r") as file:
            return json.load(file)
    else:
        return {}

# Function to save the student database to a file
def save_database(database):
    with open(DATABASE_FILE, "w") as file:
        json.dump(database, file)

# Function to create a new student entry
def add_student(database, name, email, image_path):
    try:
        # Check if the "student_images" directory exists, if not, create it
        if not os.path.exists("student_images"):
            os.makedirs("student_images")

        # Find the maximum student ID in the current database
        max_student_id = max(database.keys()) if database else 0

        # Generate a unique student ID
        student_id = max_student_id + 1
        
        # Extract the file extension from the image path
        file_extension = os.path.splitext(image_path)[1]
        
        # Construct the new image path with student ID and name
        new_image_path = f"student_images/{str(student_id)}_{name.replace(' ', '_')}{file_extension}"
        # new_image_path = f"student_images/"+{str(student_id)}+"_"+{name.replace(' ', '_')}+(file_extension)

        # Copy the image to the student_images folder with the new path
        shutil.copy(image_path, new_image_path)

        # Add the student's information to the database
        database[student_id] = {
            "name": name,
            "email": email,
            "image_path": new_image_path,
            "default_mask": 0
        }

        # Save the database to the file
        save_database(database)
    except FileNotFoundError:
        print("Error: The specified image path does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Function to handle choosing an image file from the system
def choose_image_file():
    root = tk.Tk()
    root.attributes("-topmost", True)  # Force the window to be on top

    root.withdraw()  # Hide the main window
    
    file_path = filedialog.askopenfilename(title="Choose an image file",
                                            filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif")])
    return file_path

# Main function to interact with the user
def main():
    # Load the student database from the file
    student_database = load_database()

    while True:
        # Get student's name and email from the user
        name = input("Enter student's name (or type 'quit' to exit): ")
        if name.lower() == 'quit':
            break
        email = input("Enter student's email: ")

        # Choose the image file from the system
        image_path = choose_image_file()
        if not image_path:
            print("No image selected. Please try again.")
            continue

        # Add the student to the database
        add_student(student_database, name, email, image_path)

        print("Student added successfully!\n")

    print("Student Database:")
    print(student_database)

# Run the main function
if __name__ == "__main__":
    main()
