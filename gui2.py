import tkinter as tk
from tkinter import messagebox, filedialog
import os

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Mask Recognition")

        # Load background image
        # self.bg_image = tk.PhotoImage(file=r"C:\Users\subha\OneDrive\Desktop\node-js-g76f85c45d_1280.png")
        self.bg_image = tk.PhotoImage(file="homepagepic.png")
        self.background_label = tk.Label(root, image=self.bg_image)
        self.background_label.grid(row=0, column=1, rowspan=3, sticky="nsew")

        # Buttons
        self.detect_button = tk.Button(root, text="Detect Mask", command=self.detect_mask)
        self.detect_button.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        self.open_password_button = tk.Button(root, text="login", command=self.open_password_window)
        self.open_password_button.grid(row=1, column=0, padx=20, pady=10, sticky="w")

        self.exit_button = tk.Button(root, text="Exit", command=self.confirm_exit)
        self.exit_button.grid(row=2, column=0, padx=20, pady=10, sticky="w")
        
        # self.detect_button = tk.Button(root, text="View Database", command=self.view_database)
        # self.detect_button.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        # Configure grid weights
        root.grid_rowconfigure(0, weight=1)
        root.grid_rowconfigure(1, weight=1)
        root.grid_rowconfigure(2, weight=1)
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)

        # Make window resizable
        root.resizable(True, True)

    def detect_mask(self):
            os.system("python detect_mask_video.py ")

    def open_password_window(self):
        # Create a new window for password entry
        self.password_window = tk.Toplevel(self.root)
        self.password_window.title("Enter Password")

        # Add password entry widget
        self.password_label = tk.Label(self.password_window, text="Enter Password:")
        self.password_label.pack(pady=10)
        self.password_entry = tk.Entry(self.password_window, show="*")
        self.password_entry.pack(pady=10)
        self.submit_button = tk.Button(self.password_window, text="Submit", command=self.check_password)
        self.submit_button.pack(pady=10)

    def check_password(self):
        # Check if password is correct
        password = self.password_entry.get()
        if password == "":
            self.open_feature_window()
            self.password_window.destroy()
        else:
            messagebox.showerror("Error", "Incorrect password. Please try again.")

    def open_feature_window(self):
        # Create a new window for feature selection
        self.feature_window = tk.Toplevel(self.root)
        self.feature_window.title("Feature Selection")

        # Create buttons
        features = [
            "View Database",
            "Image Similarity mtcnn",
            "View Database One",
            "Change defaultmask Value",
            "Defaulter Check",
            "Delete Database",
            "Add Student Database",
            "Send Mail to Defaulter"
            ]
        commands = [
            "python .\matching_face\\view_database.py",
            "python .\matching_face\image_similarity_mtcnn.py",
            "python .\matching_face\\view_database_one.py",
            "python .\matching_face\change_defaultmask_value",
            "python .\matching_face\defaulter_check.py",
            "python .\matching_face\delete_database.py",
            "python .\matching_face\\add_student_database.py",
            "python .\matching_face\send_mail_to_defaulter.py"
            ]

        # for feature in features:
        for feature, command in zip(features, commands):
            cmd = lambda c=command: os.system(c)
            button = tk.Button(self.feature_window, text=feature, command=cmd)
            button.pack(fill="x", padx=20, pady=10)
    def run_feature(self, feature):
        # Run external Python file based on selected feature
        os.system("python {}.py".format(feature.lower().replace(" ", "_")))

    def confirm_exit(self):
        # Prompt a message box to confirm exit
        if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
            self.root.destroy()
            
            
            
    def view_database(self):
        os.system("python .\matching_face\delete_database.py")

if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()