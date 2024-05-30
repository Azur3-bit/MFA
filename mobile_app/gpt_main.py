import tkinter as tk
from tkinter import simpledialog, messagebox
import ctypes
from ctypes import wintypes

# Constants
filename = "F:\\example.txt"  # Path to the text file on removable storage
saved_key = "12345"
CORRECT_UPI_PIN = "741"
correct_unique_key = "WxaWJFJWXf2bZN5l"

# Define payment_window and payment_status_label as global variables
payment_window = None
payment_status_label = None

# Fingerprint constants
SECURITY_MAX_SID_SIZE = 68
WINBIO_TYPE_FINGERPRINT = 0x00000008
WINBIO_POOL_SYSTEM = 0x00000001
WINBIO_FLAG_DEFAULT = 0x00000000
WINBIO_ID_TYPE_SID = 3
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


class SID_IDENTIFIER_AUTHORITY(ctypes.Structure):
    _fields_ = [("Value", wintypes.BYTE*6)]


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
        self.subfactor = ctypes.c_ubyte(0xf5)  # WINBIO_FINGER_UNSPECIFIED_POS_01
        self.identity = WINBIO_IDENTITY()
        self.IsOpen = False

    def open(self):
        if self.IsOpen:
            return
        ret = lib.WinBioOpenSession(WINBIO_TYPE_FINGERPRINT, WINBIO_POOL_SYSTEM,
                                    WINBIO_FLAG_DEFAULT, None, 0, None,
                                    ctypes.byref(self.session_handle))
        if ret & 0xffffffff != 0x0:
            print("Open Failed!")
            return False
        self.IsOpen = True
        return True

    def locate_unit(self):
        ret = lib.WinBioLocateSensor(self.session_handle, ctypes.byref(self.unit_id))
        if ret & 0xffffffff != 0x0:
            print("Locate Failed!")
            return False
        return True

    def verify(self):
        match = ctypes.c_bool(0)
        reject_detail = ctypes.c_uint32()
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
        GetCurrentProcess = ctypes.windll.kernel32.GetCurrentProcess
        GetCurrentProcess.restype = wintypes.HANDLE
        OpenProcessToken = ctypes.windll.advapi32.OpenProcessToken
        OpenProcessToken.argtypes = (wintypes.HANDLE, wintypes.DWORD, ctypes.POINTER(wintypes.HANDLE))
        OpenProcessToken.restype = wintypes.BOOL
        token = wintypes.HANDLE()
        TOKEN_READ = 0x20008
        res = OpenProcessToken(GetCurrentProcess(), TOKEN_READ, token)
        if not res > 0:
            raise RuntimeError("Couldn't get process token")
        return token

    def get_token_information(self):
        GetTokenInformation = ctypes.windll.advapi32.GetTokenInformation
        GetTokenInformation.argtypes = [
            wintypes.HANDLE,
            ctypes.c_uint,
            wintypes.LPVOID,
            wintypes.DWORD,
            ctypes.POINTER(wintypes.DWORD),
        ]
        GetTokenInformation.restype = wintypes.BOOL

        CopySid = ctypes.windll.advapi32.CopySid
        CopySid.argtypes = [
            wintypes.DWORD,
            ctypes.c_void_p,
            ctypes.c_void_p
        ]
        CopySid.restype = wintypes.BOOL

        GetLengthSid = ctypes.windll.advapi32.GetLengthSid
        GetLengthSid.argtypes = [ctypes.POINTER(SID)]
        GetLengthSid.restype = wintypes.DWORD

        return_length = wintypes.DWORD(0)
        buffer = ctypes.create_string_buffer(SECURITY_MAX_SID_SIZE)

        res = GetTokenInformation(self.get_process_token(),
                                  TOKEN_INFORMATION_CLASS.TokenUser,
                                  buffer,
                                  SECURITY_MAX_SID_SIZE,
                                  ctypes.byref(return_length))
        assert res > 0, "Error in GetTokenInformation"

        token_user = ctypes.cast(buffer, ctypes.POINTER(TOEKN_USER)).contents
        CopySid(SECURITY_MAX_SID_SIZE,
                self.identity.Value.AccountSid.Data,
                token_user.User.Sid)
        self.identity.Type = WINBIO_ID_TYPE_SID
        self.identity.Value.AccountSid.Size = GetLengthSid(token_user.User.Sid)


def payment_successful():
    global payment_status_label, payment_window
    for widget in payment_window.winfo_children():
        if widget != payment_status_label:
            widget.destroy()
    payment_status_label.config(text="Payment Successful", fg="green")


def upi_pin(root, username):
    password = simpledialog.askstring("Password Authentication", "Enter your password:")
    if password == CORRECT_UPI_PIN:
        payment_successful()
    else:
        messagebox.showinfo("Incorrect Password", "The password you entered is incorrect.")


def qr_code_helper(root, username):
    from decode_qrcode import decode_qr_code

    curr_QrCodeString = decode_qr_code()
    if curr_QrCodeString == correct_unique_key:
        payment_successful()
    else:
        messagebox.showinfo("Incorrect QR Code", "The QR code you entered is incorrect.")


def open_payment_gateway_global(root, username):
    global payment_window, payment_status_label
    root.withdraw()
    payment_window = tk.Toplevel(root)
    payment_window.title("Payment Gateway")
    payment_window.geometry("400x300")

    heading_label = tk.Label(payment_window, text="Transaction Processing ...", font=("Arial", 16, "bold"), fg="orange")
    heading_label.pack(pady=(20, 10))

    amount_label = tk.Label(payment_window, text="Rs. 500", font=("Arial", 14, "bold"), fg="green")
    amount_label.pack()

    bank_info_label = tk.Label(payment_window, text="Bank Name: ICICI Bank\nIFSC Code: ICICII89520", font=("Arial", 10))
    bank_info_label.pack()

    def physicalKey_helper():
        from findKey import compare_file_with_key
        result = compare_file_with_key(filename, saved_key)
        if result:
            payment_successful()
        else:
            messagebox.showinfo("Incorrect Physical Key", "The physical key you entered is incorrect.")

    upi_pin_button = tk.Button(payment_window, text="UPI Pin", font=("Arial", 12), command=lambda: upi_pin(root, username))
    upi_pin_button.pack(pady=5)

    qr_code_button = tk.Button(payment_window, text="QR Code", font=("Arial", 12), command=lambda: qr_code_helper(root, username))
    qr_code_button.pack(pady=5)

    physical_key_button = tk.Button(payment_window, text="Physical Key", font=("Arial", 12), command=physicalKey_helper)
    physical_key_button.pack(pady=5)

    biometric_button = tk.Button(payment_window, text="Biometric", font=("Arial", 12), command=lambda: fingerPrint_connection(root))
    biometric_button.pack(pady=5)

    payment_status_label = tk.Label(payment_window, text="", font=("Arial", 12))
    payment_status_label.pack(pady=(20, 10))

    payment_window.protocol("WM_DELETE_WINDOW", lambda: on_closing(payment_window, root))


def on_closing(top_window, root):
    top_window.destroy()
    root.deiconify()


def fingerPrint_connection(root):
    finger_print = FingerPrint()
    if not finger_print.open():
        print("Error opening fingerprint sensor.")
        return
    if not finger_print.locate_unit():
        print("Error locating fingerprint sensor.")
        return
    result = finger_print.verify()
    if result:
        payment_successful()
    else:
        messagebox.showinfo("Fingerprint Error", "Fingerprint verification failed.")
    finger_print.close()


def main_window():
    root = tk.Tk()
    root.title("Secure Payment")
    root.geometry("300x200")

    label = tk.Label(root, text="Welcome to Secure Payment", font=("Arial", 16))
    label.pack(pady=(30, 20))

    username = "User"  # Replace with actual username if needed

    def on_proceed():
        open_payment_gateway_global(root, username)

    proceed_button = tk.Button(root, text="Proceed to Payment", font=("Arial", 14), command=on_proceed)
    proceed_button.pack(pady=20)

    root.mainloop()


if __name__ == "__main__":
    main_window()
