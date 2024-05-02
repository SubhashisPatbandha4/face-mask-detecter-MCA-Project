import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import sys
import subprocess

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Mask Recognition")
        self.root.attributes("-fullscreen", True)  # Make window full-screen

        # Load background image
        self.bg_image = tk.PhotoImage(file="homepagepic.png")
        self.background_label = tk.Label(root, image=self.bg_image)
        self.background_label.place(relwidth=1, relheight=1)  # Use place() instead of grid() for full-screen background

        # Configure style for all buttons
        style = ttk.Style()
        style.configure("TButton", font=('Helvetica', 12, 'bold'), foreground="black", background="#d1d1d1")
        style.map("TButton", foreground=[('active', 'black')], background=[('active', '#cfcfcf')])

        # Buttons
        buttons = [
            ("Detect Mask", self.detect_mask, 0.1, 0.1),
            ("Login", self.open_password_window, 0.1, 0.3),
            # ("Open Terminal", self.open_terminal, 0.1, 0.5),
            ("Exit", self.confirm_exit, 0.1, 0.5)
        ]

        for text, command, relx, rely in buttons:
            button = ttk.Button(root, text=text, command=command, style="TButton")
            button.place(relx=relx, rely=rely, relwidth=0.3, relheight=0.1)

        # Configure grid weights
        root.grid_rowconfigure(0, weight=1)
        root.grid_rowconfigure(1, weight=1)
        root.grid_rowconfigure(2, weight=1)
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)

        # Make window resizable
        root.resizable(True, True)
    # def open_terminal(self):
    #     # Adjust the below command according to your specific Python environment activation script
    #     terminal_command = "cmd.exe /k cd D:\\Web Development\\Face_mask_detection-master\\matching_face & activate"
    #     subprocess.Popen(terminal_command, shell=True)

    def detect_mask(self):
        os.system("python detect_mask_video.py ")

    def open_password_window(self):
        # Create a new window for password entry
        password_window = tk.Toplevel(self.root)
        password_window.title("Enter Password")

        # Set custom theme
        password_window.style = ttk.Style()
        password_window.style.theme_use("clam")  # Choose a theme (e.g., "clam")

        # Add password entry widget
        password_label = ttk.Label(password_window, text="Enter Password:")
        password_label.pack(pady=10)
        password_entry = ttk.Entry(password_window, show="*")
        password_entry.pack(pady=10)
        submit_button = ttk.Button(password_window, text="Submit", command=lambda: self.check_password(password_entry))
        submit_button.pack(pady=10)

        # Position window on the same screen
        password_window.geometry("+{}+{}".format(self.root.winfo_x(), self.root.winfo_y()))

    def check_password(self, password_entry):
        # Check if password is correct
        password = password_entry.get()
        if password == "1":
            self.open_feature_window()
            password_entry.master.destroy()
        else:
            messagebox.showerror("Error", "Incorrect password. Please try again.")

    def open_feature_window(self):
        # Create a new window for feature selection
        feature_window = tk.Toplevel(self.root)
        feature_window.title("Feature Selection")

        # Set custom theme
        feature_window.style = ttk.Style()
        feature_window.style.theme_use("clam")  # Choose a theme (e.g., "clam")

        # Position window on the same screen
        feature_window.geometry("+{}+{}".format(self.root.winfo_x(), self.root.winfo_y()))

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
            "view_database.py",
            "image_similarity_mtcnn.py",
            "view_database_one.py",
            "change_defaultmask_value.py",
            "defaulter_check.py",
            "delete_database.py",
            "add_student_database.py",
            "send_mail_to_defaulter.py"
        ]
        
        for feature, command in zip(features, commands):
            cmd = lambda c=command: subprocess.Popen([sys.executable, os.path.join("D:/Web Development/Face_mask_detection-master", c)])
            button = tk.Button(feature_window, text=feature, command=cmd)
            button.pack(fill="x", padx=20, pady=10)

    def confirm_exit(self):
        # Prompt a message box to confirm exit
        if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
            self.root.destroy()

    def view_database(self):
        os.system(r"python .\matching_face\view_database.py")

if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()
