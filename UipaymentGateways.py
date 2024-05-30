import tkinter as tk
from tkinter import simpledialog, messagebox

  # Import shatrunjai dependency
from fingerprint import FingerPrint





# Constants
filename = "F:\\example.txt"  # Path to the text file on removable storage
saved_key = "12345"
CORRECT_UPI_PIN = "741"
correct_unique_key = "WxaWJFJWXf2bZN5l"

# Define payment_window and payment_status_label as global variables
payment_window = None
payment_status_label = None

#finger print

# Function to create and show the pop-up window


def fingerPrint_connection():
    print("**** [option selected] Finger print option selected \n")
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Create the pop-up window for fingerprint scanning
    scan_popup = tk.Toplevel()
    scan_popup.title("Fingerprint Scanner")
    scan_popup.geometry("300x150")

    # Add a label to the pop-up window
    label = tk.Label(scan_popup, text="Please place your finger on the scanner.")
    label.pack(pady=20)

    myfingerPrint = FingerPrint()
    
    try:
        print(" [Block notification] Entered try block\n")
        # root.mainloop()
        print("[Finger print device] Finger print device connected \n")
        myfingerPrint.open()
        print("[User-Notice] Now place your finger on the scanner, please :)\n")
        
        if myfingerPrint.verify():
            print("[User-Notice] Authenticated user\n")
            scan_popup.destroy()  # Close the pop-up window
            messagebox.showinfo(
                "Fingerprint Matched", "FingerPrint matched, User Authenticated."
            )
            payment_successful(root)
        else:
            print("[User-Notice] Incorrect Fingerprint", "The fingerprint is incorrect.\n")
            messagebox.showinfo(
                "Incorrect Fingerprint", "The fingerprint is incorrect."
            )
            scan_popup.destroy()  # Close the pop-up window
    finally:
        print("[User-Notice] Closing connection with the fingerprint scanner\n")
        myfingerPrint.close()
       
    

def payment_successful_done():
    # Destroy all widgets in the payment window except the payment status label
    for widget in payment_window.winfo_children():
        if widget != payment_status_label:
            widget.destroy()
    payment_status_label.config(text="Payment Successful", fg="green")


# Define the frames for the loading animation
loading_frames = ["Loading.", "Loading..", "Loading..."]

def payment_successful(root):

    payment_window = tk.Toplevel(root)
    payment_window.geometry("400x200")

    payment_status_label = tk.Label(payment_window, text="Processing Payment...", font=("Arial", 14))
    payment_status_label.pack(pady=20)

    frame_index = 0

    def update_loading_animation():
        nonlocal frame_index
        frame_index = (frame_index + 1) % len(loading_frames)
        payment_status_label.config(text=loading_frames[frame_index])
        payment_window.after(300, update_loading_animation)  # Update every 500 ms

    def payment_successful_main():
        # Stop the loading animation by stopping the after loop
        payment_window.after_cancel(update_loading_animation)

        # Destroy all widgets in the payment window except the payment status label
        for widget in payment_window.winfo_children():
            if widget != payment_status_label:
                widget.destroy()

        # Update the payment status label
        payment_status_label.config(text="Payment Successful", fg="green")
        payment_status_label.destroy()
        payment_window.destroy()
        return payment_successful_done()


    update_loading_animation()
    payment_window.after(900, payment_successful_main)  # Simulate payment process

    # root.mainloop()

# Call the function to create and display the payment window



def upi_pin(root, username):
    print("[Dev-signal]**** upi_pin selected \n")
    password = simpledialog.askstring("Password Authentication", "Enter your password:")
    if password == CORRECT_UPI_PIN:
        print("[User-Notice] Username:", username)
        print("[User-Notice] UPI pin entered:", password)
        payment_successful(root)  # Call payment_successful rootfunction
    else:
        messagebox.showinfo(
            "Incorrect Password", "The password you entered is incorrect."
        )


def qr_code_helper(root, username):
    from decode_qrcode import decode_qr_code

    print("[Dev-signal] **** QR Code selected")
    curr_QrCodeString = decode_qr_code()
    if curr_QrCodeString == correct_unique_key:
        print("[Dev-signal] QR code matched")
        payment_successful(root)
    else:
        print("[User-Notice] QR code not matched")
        messagebox.showinfo(
            "Incorrect QR Code", "The QR code you entered is incorrect."
        )

const_physical_key_PIN = CORRECT_UPI_PIN

def physicalKey_helper():
    from findKey import compare_file_with_key
    print("[Dev-signal] **** Physical key selected")

    password = simpledialog.askstring("Password Authentication", "Enter your password:")
    if password == CORRECT_UPI_PIN:
        print("[User-Notice] Physical pin entered:", password)
        result = compare_file_with_key(filename, saved_key)
        print("[Dev-signal] physical key matched ? : " + str(result))
        if result:
            print("[Dev-signal] payment Successful called\n")
            payment_successful(root)
        else:
            print("[Dev-signal] Physical key not matched")
            messagebox.showinfo(
                "Incorrect Physical Key", "The physical key you entered is incorrect."
            )

    else:
        messagebox.showinfo(
            "Incorrect Password", "The password you entered is incorrect."
        )

    
    

def open_payment_gateway_global(root):
    global payment_window, payment_status_label  # Declare payment_window and payment_status_label as global
    root.withdraw()
    payment_window = tk.Toplevel(root)
    payment_window.title("Payment Gateway")
    payment_window.geometry("450x500")

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

    # Go Back button
    def go_back():
        payment_window.withdraw()
        root.deiconify()

    go_back_button = tk.Button(
        payment_window,
        text="Go Back",
        font=("Arial", 12),
        command=go_back
    )
    go_back_button.pack(pady=1)

    # Handle window close event
    payment_window.protocol("WM_DELETE_WINDOW", root.quit)

    # Payment status label
    payment_status_label = tk.Label(payment_window, text="", font=("Arial", 14))
    payment_status_label.pack(pady=10)

    # Handle window close event
    payment_window.protocol("WM_DELETE_WINDOW", root.quit)
