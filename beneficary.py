def beneficiary_detail_ui(root):
    root.withdraw()
    beneficiary = tk.Toplevel(root)
    beneficiary.title("Add beneficiary")
    beneficiary.geometry("450x500")

    # Label and Entry for Bank Name
    bank_name_label = tk.Label(beneficiary, text="Bank Name:", font=("Arial", 12))
    bank_name_label.pack(pady=5)
    bank_name_entry = tk.Entry(beneficiary, font=("Arial", 12))
    bank_name_entry.pack(pady=5)

    # Label and Entry for IFSC Code
    ifsc_label = tk.Label(beneficiary, text="IFSC Code:", font=("Arial", 12))
    ifsc_label.pack(pady=5)
    ifsc_entry = tk.Entry(beneficiary, font=("Arial", 12))
    ifsc_entry.pack(pady=5)

    # Label and Entry for Amount
    amount_label = tk.Label(beneficiary, text="Amount to Transfer:", font=("Arial", 12))
    amount_label.pack(pady=5)
    amount_entry = tk.Entry(beneficiary, font=("Arial", 12))
    amount_entry.pack(pady=5)

    # Function to retrieve input data and proceed
    def process_beneficiary_details():
        bank_name = bank_name_entry.get()
        ifsc_code = ifsc_entry.get()
        amount = amount_entry.get()

        # Here you can proceed with the entered details as required

    # Button to submit beneficiary details
    submit_button = tk.Button(beneficiary, text="Submit", font=("Arial", 12), command=process_beneficiary_details)
    submit_button.pack(pady=10)

    # Function to go back to the main window
    def go_back():
        beneficiary.withdraw()
        root.deiconify()

    # Button to go back to the main window
    go_back_button = tk.Button(beneficiary, text="Go Back", font=("Arial", 12), command=go_back)
    go_back_button.pack(pady=1)

    # Handle window close event
    beneficiary.protocol("WM_DELETE_WINDOW", root.quit)

beneficiary_detail_ui(root)