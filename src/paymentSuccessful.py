import tkinter as tk
from tkinter import simpledialog, messagebox


from UipaymentGateways import payment_window


def payment_successful():
    # Destroy all widgets in the payment window except the payment status label
    for widget in payment_window.winfo_children():
        if widget != payment_status_label:
            widget.destroy()
    payment_status_label.config(text="Payment Successful", fg="green")
