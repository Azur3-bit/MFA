import tkinter as tk
from tkinter import simpledialog
from UipaymentGateways import open_payment_gateway_global

# Constant password
CORRECT_PASSWORD = "123"

def authenticate_with_password(root):  # Add root as an argument
    password = simpledialog.askstring("Password Authentication", "Enter your password:")
    if password == CORRECT_PASSWORD:
        print("Password entered:", password)
        # Open payment gateway layout
        open_payment_gateway_global(root)  # Pass root as an argument
    else:
        print("Incorrect password")

root = tk.Tk()  # Define root here
root.title("User Authentication")

# Set the window size to a constant value
window_width = 400
window_height = 250
window_position_x = (root.winfo_screenwidth() - window_width) // 2
window_position_y = (root.winfo_screenheight() - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{window_position_x}+{window_position_y}")

# Large heading
heading_label = tk.Label(root, text="SRM HACKATHON", font=("Arial", 24, "bold"))
heading_label.pack(pady=10)

# Input username text box
username_frame = tk.Frame(root)
username_frame.pack()

username_label = tk.Label(username_frame, text="Enter your username:", font=("Arial", 12))
username_label.pack(side=tk.LEFT)

username_entry = tk.Entry(username_frame)
username_entry.pack(side=tk.LEFT, padx=5)

# Frame to hold authentication buttons
auth_frame = tk.Frame(root)
auth_frame.pack()

password_button = tk.Button(auth_frame, text="Authenticate", font=("Arial", 12, "bold"), bg="#28a745", fg="white", command=lambda: authenticate_with_password(root))
password_button.grid(row=0, column=0, padx=5, pady=5)

biometric_button = tk.Button(auth_frame, text="Biometric", font=("Arial", 12, "bold"), bg="#007bff", fg="white", command=lambda: authenticate_with_biometric(root))
biometric_button.grid(row=0, column=1, padx=5, pady=5)

root.mainloop()
