import tkinter as tk
from tkinter import simpledialog, messagebox
from UipaymentGateways import open_payment_gateway_global

# Constant password
CORRECT_PASSWORD = "123"


def authenticate_with_password(root):  # Add root as an argument
    username = username_entry.get()  # Retrieve username from the entry widget
    password = simpledialog.askstring("Password Authentication", "Enter your password:")
    if password == CORRECT_PASSWORD:
        print("Username:", username)  # Log the username
        print("Password entered:", password)
        # Open payment gateway layout
        open_payment_gateway_global(root, username)  # Pass root as an argument
    else:
        messagebox.showinfo(
            "Incorrect Password", "The password you entered is incorrect."
        )


def fingerPrint_connection(root):
    print(" **** finger print option selected \n")

    from fingerprint import FingerPrint 
    
    
    username = username_entry.get()
    myfingerPrint = FingerPrint()
    
    try:
        myfingerPrint.open()
        print("hey there ! now place your finger on scanner please :)\n")
        if myfingerPrint.verify():
            print("hey authenicated user \n");
            open_payment_gateway_global(root,username)
        else:
            print("there always a second chance for everything \n")
    finally:
        print("closing connectin with FingerPrint scanner\n")
        myfingerPrint.close() 






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

username_label = tk.Label(
    username_frame, text="Enter your username:", font=("Arial", 12)
)
username_label.pack(side=tk.LEFT)

username_entry = tk.Entry(username_frame)
username_entry.pack(side=tk.LEFT, padx=5)

# Frame to hold authentication buttons
auth_frame = tk.Frame(root)
auth_frame.pack()

password_button = tk.Button(
    auth_frame,
    text="Password",
    font=("Arial", 12, "bold"),
    bg="#28a745",
    fg="white",
    command=lambda: authenticate_with_password(root),
)
password_button.grid(row=0, column=0, padx=5, pady=5)

biometric_button = tk.Button(
    auth_frame,
    text="Biometric",
    font=("Arial", 12, "bold"),
    bg="#007bff",
    fg="white",
    command=lambda: fingerPrint_connection(root),
)
biometric_button.grid(row=0, column=1, padx=5, pady=5)

root.mainloop()
