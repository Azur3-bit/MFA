import tkinter as tk
from tkinter import simpledialog

def continue_to_next_step():
    username = username_entry.get()
    print("Username entered:", username)

def authenticate_with_password():
    print("User chose password authentication")

def authenticate_with_biometric():
    print("User chose biometric authentication")

def show_authentication_options():
    auth_window = tk.Toplevel(root)
    auth_window.title("Authentication Options")

    # Calculate dimensions for the pop-up window
    pop_up_width = window_width // 2
    pop_up_height = window_height // 2
    pop_up_position_x = window_position_x + (window_width - pop_up_width) // 2
    pop_up_position_y = window_position_y + (window_height - pop_up_height) // 2

    auth_window.geometry(f"{pop_up_width}x{pop_up_height}+{pop_up_position_x}+{pop_up_position_y}")

    auth_window.configure(bg="#f0f0f0")

    password_button = tk.Button(auth_window, text="Password", font=("Arial", 14, "bold"), bg="#007bff", fg="white", command=authenticate_with_password)
    password_button.pack(pady=10)

    biometric_button = tk.Button(auth_window, text="Biometric", font=("Arial", 14, "bold"), bg="#28a745", fg="white", command=authenticate_with_biometric)
    biometric_button.pack(pady=10)

root = tk.Tk()
root.title("User Authentication")

# Set the window size to a constant value
window_width = 400
window_height = 200
window_position_x = (root.winfo_screenwidth() - window_width) // 2
window_position_y = (root.winfo_screenheight() - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{window_position_x}+{window_position_y}")

# Large heading
heading_label = tk.Label(root, text="SRM HACKATHON", font=("Arial", 24, "bold"), bg="#f0f0f0")
heading_label.pack(pady=10)

username_label = tk.Label(root, text="Enter your username:", font=("Arial", 12), bg="#f0f0f0")
username_label.pack()

username_entry = tk.Entry(root, font=("Arial", 12))
username_entry.pack()

continue_button = tk.Button(root, text="Continue", font=("Arial", 12, "bold"), bg="#007bff", fg="white", command=continue_to_next_step)
continue_button.pack(pady=10)

# Button to show authentication options
authentication_options_button = tk.Button(root, text="Authentication Options", font=("Arial", 12, "bold"), bg="#28a745", fg="white", command=show_authentication_options)
authentication_options_button.pack()

root.configure(bg="#f0f0f0")

root.mainloop()
