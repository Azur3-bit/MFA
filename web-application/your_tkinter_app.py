# main

import tkinter as tk
from tkinter import simpledialog, messagebox
# from UipaymentGateways import open_payment_gateway_global





# Constants
filename = "F:\\example.txt"  # Path to the text file on removable storage
saved_key = "12345"
CORRECT_UPI_PIN = "741"
correct_unique_key = "WxaWJFJWXf2bZN5l"

# Define payment_window and payment_status_label as global variables
payment_window = None
payment_status_label = None

# import tkinter as tk
# from tkinter import simpledialog, messagebox

#   # Import shatrunjai dependency
# from fingerprint import FingerPrint



import ctypes
from ctypes import wintypes


SECURITY_MAX_SID_SIZE = 68
WINBIO_TYPE_FINGERPRINT = 0x00000008
WINBIO_POOL_SYSTEM = 0x00000001
WINBIO_FLAG_DEFAULT = 0x00000000
WINBIO_ID_TYPE_SID = 3

# Error Info
WINBIO_E_NO_MATCH = 0x80098005

lib = ctypes.WinDLL(r"C:\Windows\System32\winbio.dll")


class GUID(ctypes.Structure):
    _fields_ = [("Data1", wintypes.DWORD),
                ("Data2", wintypes.WORD),
                ("Data3", wintypes.WORD),
                ("Data4", wintypes.BYTE * 8)
                ]


class AccountSid(ctypes.Structure):
    _fields_ = [("Size", wintypes.ULONG),
                ("Data", ctypes.c_ubyte * SECURITY_MAX_SID_SIZE)
                ]


class Value(ctypes.Union):
    _fields_ = [("NULL", wintypes.ULONG),
                ("Wildcard", wintypes.ULONG),
                ("TemplateGuid", GUID),
                ("AccountSid", AccountSid)
                ]


class WINBIO_IDENTITY(ctypes.Structure):
    _fields_ = [("Type", ctypes.c_uint32),
                ("Value", Value)]


class TOKEN_INFORMATION_CLASS:
    TokenUser = 1
    TokenGroups = 2
    TokenPrivileges = 3


class SID_IDENTIFIER_AUTHORITY(ctypes.Structure):
    _fields_ = [("Value", wintypes.BYTE*6)]


# https://www.csie.ntu.edu.tw/~r92094/c++/Win_Header/WINNT.H
class SID(ctypes.Structure):
    _fields_ = [("Revision", wintypes.BYTE),
                ("SubAuthorityCount", wintypes.BYTE),
                ("IdentifierAuthority", SID_IDENTIFIER_AUTHORITY),
                ("SubAuthority", wintypes.DWORD)]


class SID_AND_ATTRIBUTES(ctypes.Structure):
    _fields_ = [("Sid", ctypes.POINTER(SID)),
                ("Attributes", wintypes.DWORD)]


class TOEKN_USER(ctypes.Structure):
    _fields_ = [("User", SID_AND_ATTRIBUTES)]


class FingerPrint:
    def __init__(self):
        self.session_handle = ctypes.c_uint32()
        self.unit_id = ctypes.c_uint32()

        # important  represent which finger you are using
        # full definition is in winbio_types.h
        self.subfactor = ctypes.c_ubyte(0xf5)       # WINBIO_FINGER_UNSPECIFIED_POS_01

        # WINBIO_ID_TYPE_SID = 3
        self.identity = WINBIO_IDENTITY()
        self.IsOpen = False

    def open(self):
        if self.IsOpen:
            return
        ret = lib.WinBioOpenSession(WINBIO_TYPE_FINGERPRINT,  # finger print
                                    WINBIO_POOL_SYSTEM,
                                    WINBIO_FLAG_DEFAULT,
                                    None,
                                    0,
                                    None,
                                    ctypes.byref(self.session_handle))  # pool   system
        if ret & 0xffffffff != 0x0:
            print("Open Failed!")
            return False
        self.IsOpen = True
        return True

    def locate_unit(self):
        ret = lib.WinBioLocateSensor(self.session_handle, ctypes.byref(self.unit_id))
        print(self.unit_id)
        if ret & 0xffffffff != 0x0:
            print("Locate Failed!")
            return False
        return True

    def identify(self):
        reject_detail = ctypes.c_uint32()
        ret = lib.WinBioIdentify(self.session_handle, ctypes.byref(self.unit_id), ctypes.byref(self.identity),
                                 ctypes.byref(self.subfactor),
                                 ctypes.byref(reject_detail))
        if ret & 0xffffffff != 0x0:
            print(hex(ret & 0xffffffff))
            raise Exception("Identify Error")
        print(f"Unit ID\t:{hex(self.unit_id.value)}")
        print(f"Sub Factor\t:{hex(self.subfactor.value)}")
        print(f"Identity Type\t: {self.identity.Type}")
        print(f"Identity AccountSid Data\t: {list(self.identity.Value.AccountSid.Data)[0:self.identity.Value.AccountSid.Size]}")
        print(f"Identity AccountSid Size\t: {self.identity.Value.AccountSid.Size}")
        print(f"Rejected Details:\t{hex(reject_detail.value)}")

    def verify(self):
        match = ctypes.c_bool(0)
        reject_detail = ctypes.c_uint32()
        # get identity
        self.get_current_user_identity()
        ret = lib.WinBioVerify(self.session_handle, ctypes.byref(self.identity),
                               self.subfactor, ctypes.byref(self.subfactor),
                               ctypes.byref(match), ctypes.byref(reject_detail))
        if ret & 0xffffffff == WINBIO_E_NO_MATCH or ret & 0xffffffff == 0:
            return match.value
        else:
            print(hex(ret & 0xffffffff))
            raise Exception("Identify Error")

    def close(self):
        if not self.IsOpen:
            return
        lib.WinBioCloseSession(self.session_handle)
        self.session_handle = 0

    def get_current_user_identity(self):
        self.get_token_information()

    @staticmethod
    def get_process_token():
        """
        Get the current process token
        """
        #  Reference
        #  https://gist.github.com/schlamar/7024668
        GetCurrentProcess = ctypes.windll.kernel32.GetCurrentProcess
        GetCurrentProcess.restype = wintypes.HANDLE
        OpenProcessToken = ctypes.windll.advapi32.OpenProcessToken
        OpenProcessToken.argtypes = (wintypes.HANDLE, wintypes.DWORD, ctypes.POINTER(wintypes.HANDLE))
        OpenProcessToken.restype = wintypes.BOOL
        token = wintypes.HANDLE()

        # https://github.com/Alexpux/mingw-w64/blob/master/mingw-w64-tools/widl/include/winnt.h
        # TOKEN_READ = STANDARD_RIGHTS_READ | TOKEN_QUERY = 0x00020000 | 0x0008 = 0x20008
        # TOKEN_ALL_ACCESS = 0xf01ff

        TOKEN_READ = 0x20008
        res = OpenProcessToken(GetCurrentProcess(), TOKEN_READ, token)
        if not res > 0:
            raise RuntimeError("Couldn't get process token")
        return token

    def get_token_information(self):
        """
        Get token info associated with the current process.
        """
        GetTokenInformation = ctypes.windll.advapi32.GetTokenInformation
        GetTokenInformation.argtypes = [
            wintypes.HANDLE,  # TokenHandle
            ctypes.c_uint,  # TOKEN_INFORMATION_CLASS value
            wintypes.LPVOID,  # TokenInformation
            wintypes.DWORD,  # TokenInformationLength
            ctypes.POINTER(wintypes.DWORD),  # ReturnLength
            ]
        GetTokenInformation.restype = wintypes.BOOL

        CopySid = ctypes.windll.advapi32.CopySid
        CopySid.argtypes = [
            wintypes.DWORD,     # nDestinationSidLength
            ctypes.c_void_p,    # pDestinationSid,
            ctypes.c_void_p     # pSourceSid
        ]
        CopySid.restype = wintypes.BOOL

        GetLengthSid = ctypes.windll.advapi32.GetLengthSid
        GetLengthSid.argtypes = [
            ctypes.POINTER(SID)  # PSID
        ]
        GetLengthSid.restype = wintypes.DWORD

        return_length = wintypes.DWORD(0)
        buffer = ctypes.create_string_buffer(SECURITY_MAX_SID_SIZE)

        res = GetTokenInformation(self.get_process_token(),
                                  TOKEN_INFORMATION_CLASS.TokenUser,
                                  buffer,
                                  SECURITY_MAX_SID_SIZE,
                                  ctypes.byref(return_length)
                                  )
        assert res > 0, "Error in second GetTokenInformation (%d)" % res

        token_user = ctypes.cast(buffer, ctypes.POINTER(TOEKN_USER)).contents
        CopySid(SECURITY_MAX_SID_SIZE,
                self.identity.Value.AccountSid.Data,
                token_user.User.Sid
                )
        self.identity.Type = WINBIO_ID_TYPE_SID
        self.identity.Value.AccountSid.Size = GetLengthSid(token_user.User.Sid)


# if __name__ == '__main__':
#     myFP = FingerPrint()
#     try:
#         myFP.open()
#         # myFP.identify()
#         print("Please touch the fingerprint sensor to authenticate")
#         if myFP.verify():
#             print("Authenticated")
#         else:
#             print("Please Try Again!")
#     finally:
#         myFP.close()


# adding payment info details 


# bank_name = "default"
# ifsc_code = "none"
# amount = -100

def beneficiary_detail_ui(root):
    root.withdraw()
    beneficiary = tk.Toplevel(root)
    beneficiary.title("Bank Details")
    beneficiary.geometry("450x500")
    beneficiary.configure(bg="lightblue")

    # Title
    title_label = tk.Label(
        beneficiary, text="Enter Bank Details", font=("Arial", 16, "bold"), bg="lightblue"
    )
    title_label.pack(pady=20)

    # Frame for input fields
    input_frame = tk.Frame(beneficiary, bg="lightblue")
    input_frame.pack(pady=10)

    # Label and Entry for Bank Name
    bank_name_label = tk.Label(input_frame, text="Account No.:", font=("Arial", 12), bg="lightblue")
    bank_name_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    bank_name_entry = tk.Entry(input_frame, font=("Arial", 12))
    bank_name_entry.grid(row=0, column=1, padx=10, pady=10)

    # Label and Entry for IFSC Code
    ifsc_label = tk.Label(input_frame, text="IFSC Code:", font=("Arial", 12), bg="lightblue")
    ifsc_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    ifsc_entry = tk.Entry(input_frame, font=("Arial", 12))
    ifsc_entry.grid(row=1, column=1, padx=10, pady=10)

    # Label and Entry for Amount
    amount_label = tk.Label(input_frame, text="Amount to Transfer:", font=("Arial", 12), bg="lightblue")
    amount_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
    amount_entry = tk.Entry(input_frame, font=("Arial", 12))
    amount_entry.grid(row=2, column=1, padx=10, pady=10)

    # Function to retrieve input data and proceed
    def process_beneficiary_details():
        global bank_name, ifsc_code, amount
        bank_name = bank_name_entry.get()
        ifsc_code = ifsc_entry.get()
        amount = amount_entry.get()

        # Here you can proceed with the entered details as required
        # Call the open_payment_gateway_global function with provided arguments
        beneficiary.destroy()
        open_payment_gateway_global(root, username_entry.get())

    # Button to submit beneficiary details
    submit_button = tk.Button(
        beneficiary, text="Submit", font=("Arial", 12, "bold"), bg="green", fg="white", command=process_beneficiary_details
    )
    submit_button.pack(pady=20)

    # Function to go back to the main window
    def go_back():
        beneficiary.withdraw()
        root.deiconify()

    # Button to go back to the main window
    go_back_button = tk.Button(
        beneficiary, text="Go Back", font=("Arial", 12, "bold"), bg="red", fg="white", command=go_back
    )
    go_back_button.pack(pady=5)

    # Handle window close event
    beneficiary.protocol("WM_DELETE_WINDOW", root.quit)
#finger print

# Function to create and show the pop-up window
def show_fingerprint_popup(root):
    scan_popup = tk.Toplevel(root)
    scan_popup.title("Fingerprint Scanner")
    scan_popup.geometry("300x150")

    # Add a label to the pop-up window
    label = tk.Label(scan_popup, text="Please place your finger on the scanner.")
    label.pack(pady=20)

    myfingerPrint = FingerPrint()
    
    def check_fingerprint():
        try:
            myfingerPrint.open()
            print("Hey there! Now place your finger on the scanner, please :)\n")
            
            if myfingerPrint.verify():
                print("Authenticated user\n")
                scan_popup.destroy()  # Close the pop-up window
                payment_successful()
            else:
                print("There is always a second chance for everything\n")
                messagebox.showinfo(
                    "Incorrect Fingerprint", "The fingerprint is incorrect."
                )
                scan_popup.destroy()  # Close the pop-up window
        finally:
            print("Closing connection with the fingerprint scanner\n")
            myfingerPrint.close()
    
    # Trigger fingerprint check after the pop-up window is created
    scan_popup.after(100, check_fingerprint)


def fingerPrint_connection(root):
    print("**** Finger print option selected \n")
    show_fingerprint_popup(root)
       
    


def fingerPrint_connection_userLogin(root):
    print("**** Finger print option selected \n")
    show_fingerprint_popup_userLogin(root)
       
def show_fingerprint_popup_userLogin(root):
    scan_popup = tk.Toplevel(root)
    scan_popup.title("Fingerprint Scanner")
    scan_popup.geometry("300x150")
    username = username_entry.get()
    
    # Add a label to the pop-up window
    label = tk.Label(scan_popup, text="Please place your finger on the scanner.")
    label.pack(pady=20)

    myfingerPrint = FingerPrint()
    
    def check_fingerprint():
        try:
            myfingerPrint.open()
            print("Hey there! Now place your finger on the scanner, please :)\n")
            
            if myfingerPrint.verify():
                print("Authenticated user\n")
                scan_popup.destroy()  # Close the pop-up window
                beneficiary_detail_ui(root)
            else:
                print("There is always a second chance for everything\n")
                messagebox.showinfo(
                    "Incorrect Fingerprint", "The fingerprint is incorrect."
                )
                scan_popup.destroy()  # Close the pop-up window
        finally:
            print("Closing connection with the fingerprint scanner\n")
            myfingerPrint.close()
    
    # Trigger fingerprint check after the pop-up window is created
    scan_popup.after(100, check_fingerprint)






# def payment_successful():
#     # Destroy all widgets in the payment window except the payment status label
#     for widget in payment_window.winfo_children():
#         if widget != payment_status_label:
#             widget.destroy()
#     payment_status_label.config(text="Payment Successful", fg="green")

def payment_successful_done():
    # Destroy all widgets in the payment window except the payment status label
    for widget in payment_window.winfo_children():
        if widget != payment_status_label:
            widget.destroy()
    payment_status_label.config(text="Payment Successful", fg="green")

    
loading_frames = ["Loading.", "Loading..", "Loading..."]

def payment_successful(root):
    print("[payment_successful] control reached function call\n")
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
    payment_window.after(1000, payment_successful_main)  # Simulate payment process



def upi_pin(root, username):
    print(" **** upi_pin selected \n")
    password = simpledialog.askstring("Password Authentication", "Enter your password:", show='*')
    if password == CORRECT_UPI_PIN:
        print("Username:", username)
        print("Transaction pin entered:", password)
        payment_successful(root)  # Call payment_successful function
    else:
        messagebox.showinfo(
            "Incorrect Password", "The password you entered is incorrect."
        )


# def qr_code_helper(root, username):
#     from decode_qrcode import decode_qr_code

#     print(" **** QR Code selected")
#     curr_QrCodeString = decode_qr_code()
#     if curr_QrCodeString == correct_unique_key:
#         print("QR code matched")
#         payment_successful()
#     else:
#         print("QR code not matched")
#         messagebox.showinfo(
#             "Incorrect QR Code", "The QR code you entered is incorrect."
#         )
def open_payment_gateway_global(root, username):
    global payment_window, payment_status_label  # Declare payment_window and payment_status_label as global
    root.withdraw()
    payment_window = tk.Toplevel(root)
    payment_window.title("Payment Gateway")
    payment_window.geometry("450x500")
    payment_window.configure(bg="lightblue")

    # Transaction Processing heading
    heading_label = tk.Label(
        payment_window,
        text="Transaction Processing ...",
        font=("Arial", 16, "bold"),
        fg="black",
        bg="lightblue"
    )
    heading_label.pack(pady=(20, 10))

    # Payment gateway layout
    amount_label = tk.Label(
        payment_window, text=f"Rs. {amount}", font=("Arial", 14, "bold"), fg="green", bg="lightblue"
    )
    amount_label.pack()

    bank_info_label = tk.Label(
        payment_window,
        text=f"Bank Name: {bank_name}\nIFSC Code: {ifsc_code}",
        font=("Arial", 10),
        bg="lightblue"
    )
    bank_info_label.pack()

    const_physical_key_PIN = CORRECT_UPI_PIN

    def physicalKey_helper():
        import psutil

        def is_removable_disk(path):
            """Check if the path is on a removable disk."""
            partitions = psutil.disk_partitions()
            for partition in partitions:
                if path.startswith(partition.mountpoint):
                    if 'removable' in partition.opts or 'cdrom' in partition.opts:
                        return True
            return False

        def compare_file_with_key(filename, saved_key):
            try:
                if not is_removable_disk(filename):
                    print("File is not on a removable storage device.")
                    return False
                
                # Open the file and read its content
                with open(filename, 'r') as file:
                    file_content = file.read()
                
                # Compare the file content with the saved key
                if file_content.strip() == saved_key.strip():
                    print("[compare_file_with_key] file contents : ", file_content)
                    return True
                else:
                    return False
            except FileNotFoundError:
                print("File not found!")
                return False
            except Exception as e:
                print("An error occurred:", e)
                return False

        print("[Dev-signal] **** Physical key selected")

        password = simpledialog.askstring("Password Authentication", "Enter your password:", show='*')
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

    # Additional buttons
    upi_pin_button = tk.Button(
        payment_window,
        text="Transaction Pin",
        font=("Arial", 12, "bold"),
        bg="#007bff",
        fg="white",
        command=lambda: upi_pin(root, username),
    )
    upi_pin_button.pack(pady=5)

    physical_key_button = tk.Button(
        payment_window,
        text="Physical Key",
        font=("Arial", 12, "bold"),
        bg="#007bff",
        fg="white",
        command=lambda: physicalKey_helper(),
    )
    physical_key_button.pack(pady=5)

    biometric_button = tk.Button(
        payment_window,
        text="Biometric",
        font=("Arial", 12, "bold"),
        bg="#007bff",
        fg="white",
        command=lambda: fingerPrint_connection(root),
    )
    biometric_button.pack(pady=5)

    # Payment status label
    payment_status_label = tk.Label(payment_window, text="", font=("Arial", 14), bg="lightblue")
    payment_status_label.pack(pady=10)

    # Go Back button
    def go_back():
        payment_window.withdraw()
        root.deiconify()

    go_back_button = tk.Button(
        payment_window,
        text="Go Back",
        font=("Arial", 12, "bold"),
        bg="#dc3545",
        fg="white",
        command=go_back
    )
    go_back_button.pack(pady=5)

    # Handle window close event
    payment_window.protocol("WM_DELETE_WINDOW", root.quit)
# Constant password
CORRECT_PASSWORD = "123"


def authenticate_with_password(root):  # Add root as an argument
    username = username_entry.get()  # Retrieve username from the entry widget
    password = simpledialog.askstring("Password Authentication", "Enter your password:", show='*')
    if password == CORRECT_PASSWORD:
        print("Username:", username)  # Log the username
        print("Password entered:", password)
        # Open payment gateway layout


        # ---- changed for beneficiary 
        # open_payment_gateway_global(root, username)  # Pass root as an argument
        beneficiary_detail_ui(root)
    else:
        messagebox.showinfo(
            "Incorrect Password", "The password you entered is incorrect."
        )


# def fingerPrint_connection_mainScreen(root):
#     print(" **** finger print option selected \n")

#     # from fingerprint import FingerPrint 
#     username = username_entry.get()
#     myfingerPrint = FingerPrint()
    
#     try:
#         myfingerPrint.open()
#         print("hey there ! now place your finger on scanner please :)\n")
#         if myfingerPrint.verify():
#             print("hey authenicated user \n")
#             open_payment_gateway_global(root,username)
#         else:
#             print("there always a second chance for everything \n")
#             messagebox.showinfo(
#                 "Incorrect FingerPrint", "The FingerPrint is incorrect."
#             )
#     finally:
#         print("closing connectin with FingerPrint scanner\n")
#         myfingerPrint.close() 




if __name__ == "__main__":
    root = tk.Tk()  # Define root here
    root.title("User Authentication")
    root.configure(bg="lightblue")

    # Set the window size to a constant value
    window_width = 400
    window_height = 250
    window_position_x = (root.winfo_screenwidth() - window_width) // 2
    window_position_y = (root.winfo_screenheight() - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{window_position_x}+{window_position_y}")

    # Large heading
    heading_label = tk.Label(root, text="SRM HACKATHON", font=("Arial", 24, "bold"), bg="lightblue")
    heading_label.pack(pady=10)

    # Input username text box
    username_frame = tk.Frame(root, bg="lightblue")
    username_frame.pack(pady=10)

    username_label = tk.Label(username_frame, text="Enter your username:", font=("Arial", 12), bg="lightblue")
    username_label.pack(side=tk.LEFT)

    username_entry = tk.Entry(username_frame, font=("Arial", 12))
    username_entry.pack(side=tk.LEFT, padx=5)

    # Frame to hold authentication buttons
    auth_frame = tk.Frame(root, bg="lightblue")
    auth_frame.pack(pady=10)

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
        command=lambda: fingerPrint_connection_userLogin(root),
    )
    biometric_button.grid(row=0, column=1, padx=5, pady=5)

    root.mainloop()