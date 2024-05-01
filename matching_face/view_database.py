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

# Function to display student information
def display_student_info(label_id, label_name, label_image, label_default_mask):
    student = student_database[student_keys[student_index]]
    label_id.config(text=f"ID: {student_keys[student_index]}")
    label_name.config(text=f"Name: {student['name']}")
    label_default_mask.config(text=f"Default Mask: {student['default_mask']}")

    # Load image
    image = Image.open(student['image_path'])
    image.thumbnail((200, 200))  # Resize image
    photo = ImageTk.PhotoImage(image)

    # Update label with image
    label_image.config(image=photo)
    label_image.image = photo  # Keep a reference to prevent garbage collection

# Function to handle navigation buttons
def navigate(direction, label_id, label_name, label_image, label_default_mask):
    global student_index
    if direction == "next":
        student_index = (student_index + 1) % len(student_keys)
    elif direction == "prev":
        student_index = (student_index - 1) % len(student_keys)
    display_student_info(label_id, label_name, label_image, label_default_mask)

# Main function to interact with the user
def main():
    global student_database, student_keys, student_index
    # Load the student database from the file
    student_database = load_database()
    student_keys = list(student_database.keys())
    student_index = 0

    # Create main window
    root = tk.Tk()
    root.title("Student Database Viewer")

    # Create widgets
    label_student_info = tk.Label(root, text="Student Information:")
    label_student_info.grid(row=0, column=0, columnspan=2)

    label_id = tk.Label(root, text="")
    label_id.grid(row=1, column=0, columnspan=2)

    label_name = tk.Label(root, text="")
    label_name.grid(row=2, column=0, columnspan=2)

    label_image = tk.Label(root)
    label_image.grid(row=3, column=0, columnspan=2)

    label_default_mask = tk.Label(root, text="")
    label_default_mask.grid(row=4, column=0, columnspan=2)

    button_prev = tk.Button(root, text="Previous", command=lambda: navigate("prev", label_id, label_name, label_image, label_default_mask))
    button_prev.grid(row=5, column=0)

    button_next = tk.Button(root, text="Next", command=lambda: navigate("next", label_id, label_name, label_image, label_default_mask))
    button_next.grid(row=5, column=1)

    display_student_info(label_id, label_name, label_image, label_default_mask)  # Display initial student information

    # Run the application
    root.mainloop()

# Run the main function
if __name__ == "__main__":
    main()
