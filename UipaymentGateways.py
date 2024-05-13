import tkinter as tk

from findKey import is_removable_disk
from findKey import compare_file_with_key


from tkinter import simpledialog, messagebox

# changes
filename = "G:\\example.txt"  # Path to the text file on removable storage
saved_key = "12345"
CORRECT_UPI_PIN = "741"


def upi_pin(root, username):  # Add username as an argument
    print("UPI Pin selected")
    password = simpledialog.askstring("Password Authentication", "Enter your password:")
    if password == CORRECT_UPI_PIN:
        print("Username:", username)  # Log the username
        # print("Password entered:", password)
        print("upi pin entered : ", password)
        # Open payment gateway layout
        open_payment_gateway_global(root, username)  # Pass root as an argument
    else:
        messagebox.showinfo(
            "Incorrect Password", "The password you entered is incorrect."
        )


def open_payment_gateway_global(root, username):  # Add root as an argument
    root.withdraw()  # Hide the main window
    payment_window = tk.Toplevel(root)
    payment_window.title("Payment Gateway")
    payment_window.geometry(
        "400x300"
    )  # Adjusted height to accommodate additional buttons

    # Transaction Processing heading
    heading_label = tk.Label(
        payment_window,
        text="Transaction Processing ...",
        font=("Arial", 16, "bold"),
        fg="orange",
    )
    heading_label.pack(pady=(20, 10))  # Adjusted padding for top and bottom

    # Payment gateway layout
    amount_label = tk.Label(
        payment_window, text="Rs. 500", font=("Arial", 14, "bold"), fg="green"
    )
    amount_label.pack()

    bank_info_label = tk.Label(
        payment_window,
        text="Bank Name: ICICI Bank\nIFSC Code: ICICII89520",
        font=("Arial", 10),
    )
    bank_info_label.pack()

    # # Add payment options/buttons
    # payment_button1 = tk.Button(payment_window, text="Option 1", font=("Arial", 12), command=lambda: print("Payment option 1 selected"))
    # payment_button1.pack(pady=5)

    # payment_button2 = tk.Button(payment_window, text="Option 2", font=("Arial", 12), command=lambda: print("Payment option 2 selected"))
    # payment_button2.pack(pady=5)

    def aux_physicalKey():
        print(" +++ Physical key selected")
        result = compare_file_with_key(filename, saved_key)
        print("physical key matched ? : " + str(result))

    # Additional buttons
    upi_pin_button = tk.Button(
        payment_window,
        text="UPI Pin",
        font=("Arial", 12),
        command=lambda: upi_pin(root, username),
    )
    upi_pin_button.pack(pady=5)

    qr_code_button = tk.Button(
        payment_window,
        text="QR Code",
        font=("Arial", 12),
        command=lambda: print("QR Code selected"),
    )
    qr_code_button.pack(pady=5)

    physical_key_button = tk.Button(
        payment_window,
        text="Physical Key",
        font=("Arial", 12),
        command=lambda: aux_physicalKey(),
    )
    physical_key_button.pack(pady=5)

    biometric_button = tk.Button(
        payment_window,
        text="Biometric",
        font=("Arial", 12),
        command=lambda: print("Biometric - fingerprint selected"),
    )
    biometric_button.pack(pady=5)

    # Handle window close event
    payment_window.protocol("WM_DELETE_WINDOW", root.quit)
