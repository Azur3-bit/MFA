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




# def fingerPrint_connection(root):
#     print("**** [option selected] Finger print option selected \n")
#     root = tk.Tk()
#     root.withdraw()  # Hide the main window

#     # Create the pop-up window for fingerprint scanning
#     scan_popup = tk.Toplevel()
#     scan_popup.title("Fingerprint Scanner")
#     scan_popup.geometry("300x150")

#     # Add a label to the pop-up window
#     label = tk.Label(scan_popup, text="Please place your finger on the scanner.")
#     label.pack(pady=20)

#     myfingerPrint = FingerPrint()
    
#     try:
#         print(" [Block notification] Entered try block\n")
#         # root.mainloop()
#         print("[Finger print device] Finger print device connected \n")
#         myfingerPrint.open()
#         print("[User-Notice] Now place your finger on the scanner, please :)\n")
        
#         if myfingerPrint.verify():
#             print("[User-Notice] Authenticated user\n")
#             scan_popup.destroy()  # Close the pop-up window
#             messagebox.showinfo(
#                 "Fingerprint Matched", "FingerPrint matched, User Authenticated."
#             )
#             open_payment_gateway_global(root)
#         else:
#             print("[User-Notice] Incorrect Fingerprint", "The fingerprint is incorrect.\n")
#             messagebox.showinfo(
#                 "Incorrect Fingerprint", "The fingerprint is incorrect."
#             )
#             scan_popup.destroy()  # Close the pop-up window
#     finally:
#         print("[User-Notice] Closing connection with the fingerprint scanner\n")
#         myfingerPrint.close()



def fingerPrint_connection(root):
    from fingerprint import FingerPrint
    print("**** [option selected] Finger print option selected \n")
    root.withdraw()  # Hide the main window

    myfingerPrint = FingerPrint()

    def scan_fingerprint():
        try:
            print(" [Block notification] Entered try block\n")
            print("[Finger print device] Finger print device connected \n")
            myfingerPrint.open()
            print("[User-Notice] Now place your finger on the scanner, please :)\n")

            if myfingerPrint.verify():
                print("[User-Notice] Authenticated user\n")
                scan_popup.destroy()  # Close the pop-up window
                messagebox.showinfo("Fingerprint Matched", "Fingerprint matched, User Authenticated.")
                open_payment_gateway_global(root)
            else:
                print("[User-Notice] Incorrect Fingerprint", "The fingerprint is incorrect.\n")
                messagebox.showinfo("Incorrect Fingerprint", "The fingerprint is incorrect. Please try again.")
                scan_popup.lift()  # Bring the pop-up window to the front
        finally:
            print("[User-Notice] Closing connection with the fingerprint scanner\n")
            myfingerPrint.close()

    # Create the pop-up window for fingerprint scanning
    scan_popup = tk.Toplevel()
    scan_popup.title("Fingerprint Scanner")
    scan_popup.geometry("300x150")

    # Add a label to the pop-up window
    label = tk.Label(scan_popup, text="Please place your finger on the scanner.")
    label.pack(pady=20)


    scan_fingerprint()
    # Button to start scanning the fingerprint
    # scan_button = tk.Button(scan_popup, text="Scan Fingerprint", command=scan_fingerprint)
    # scan_button.pack(pady=10)

    # # Bind the return key to start scanning the fingerprint
    # scan_popup.bind('<Return>', lambda event: scan_fingerprint())
       


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
