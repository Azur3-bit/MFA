import tkinter as tk
from tkinter import simpledialog, messagebox

  # Import shatrunjai dependency





# Constants
filename = "F:\\example.txt"  # Path to the text file on removable storage
saved_key = "12345"
CORRECT_UPI_PIN = "741"
correct_unique_key = "WxaWJFJWXf2bZN5l"

# Define payment_window and payment_status_label as global variables
payment_window = None
payment_status_label = None

#finger print

def fingerPrint_connection():
    # Create the main window
    from fingerprint import FingerPrint
    
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Create the pop-up window for fingerprint scanning
    scan_popup = tk.Toplevel()
    scan_popup.title("Fingerprint Scanner")
    scan_popup.geometry("300x150")

    # Add a label to the pop-up window
    label = tk.Label(scan_popup, text="Please place your finger on the scanner.")
    label.pack(pady=20)

    # Function to close the pop-up window
    def close_popup():
        scan_popup.destroy()

    print("**** Finger print option selected \n")
    
    myfingerPrint = FingerPrint()
    
    try:
        myfingerPrint.open()
        print("Hey there! Now place your finger on the scanner, please :)\n")
        
        if myfingerPrint.verify():
            print("Authenticated user\n")
            close_popup()  # Close the pop-up window
            payment_successful()
        else:
            print("There is always a second chance for everything\n")
            messagebox.showinfo(
                "Incorrect Fingerprint", "The fingerprint is incorrect."
            )
            close_popup()  # Close the pop-up window
    finally:
        print("Closing connection with the fingerprint scanner\n")
        myfingerPrint.close()
    
    root.mainloop()

def payment_successful():
    # Destroy all widgets in the payment window except the payment status label
    for widget in payment_window.winfo_children():
        if widget != payment_status_label:
            widget.destroy()
    payment_status_label.config(text="Payment Successful", fg="green")


def upi_pin(root, username):
    print(" **** upi_pin selected \n")
    password = simpledialog.askstring("Password Authentication", "Enter your password:")
    if password == CORRECT_UPI_PIN:
        print("Username:", username)
        print("UPI pin entered:", password)
        payment_successful()  # Call payment_successful function
    else:
        messagebox.showinfo(
            "Incorrect Password", "The password you entered is incorrect."
        )


def qr_code_helper(root, username):
    from decode_qrcode import decode_qr_code

    print(" **** QR Code selected")
    curr_QrCodeString = decode_qr_code()
    if curr_QrCodeString == correct_unique_key:
        print("QR code matched")
        payment_successful()
    else:
        print("QR code not matched")
        messagebox.showinfo(
            "Incorrect QR Code", "The QR code you entered is incorrect."
        )


def open_payment_gateway_global(root, username):
    global payment_window, payment_status_label  # Declare payment_window and payment_status_label as global
    root.withdraw()
    payment_window = tk.Toplevel(root)
    payment_window.title("Payment Gateway")
    payment_window.geometry("400x300")

    # Transaction Processing heading
    heading_label = tk.Label(
        payment_window,
        text="Transaction Processing ...",
        font=("Arial", 16, "bold"),
        fg="orange",
    )
    heading_label.pack(pady=(20, 10))

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

    def physicalKey_helper():
        from findKey import compare_file_with_key
        print(" **** Physical key selected")
        result = compare_file_with_key(filename, saved_key)
        print("physical key matched ? : " + str(result))
        if result:
            payment_successful()
        else:
            print("Physical key not matched")
            messagebox.showinfo(
                "Incorrect Physical Key", "The physical key you entered is incorrect."
            )

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
        command=lambda: qr_code_helper(root, username),  # Call qr_code_helper function
    )
    qr_code_button.pack(pady=5)

    physical_key_button = tk.Button(
        payment_window,
        text="Physical Key",
        font=("Arial", 12),
        command=lambda: physicalKey_helper(),
    )
    physical_key_button.pack(pady=5)

    biometric_button = tk.Button(
        payment_window,
        text="Biometric",
        font=("Arial", 12),
        command=lambda: fingerPrint_connection(),
    )
    biometric_button.pack(pady=5)

    # Payment status label
    payment_status_label = tk.Label(payment_window, text="", font=("Arial", 14))
    payment_status_label.pack(pady=10)

    # Handle window close event
    payment_window.protocol("WM_DELETE_WINDOW", root.quit)
