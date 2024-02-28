import sqlite3
import datetime
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Create a SQLite database
conn = sqlite3.connect("expense_tracker.db")
cursor = conn.cursor()

# Create the expenses table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        address TEXT,
        phone TEXT,
        description TEXT,
        amount REAL,
        date DATE
    )
''')
conn.commit()

# Function to record an expense
def record_expense():
    name = name_entry.get()
    address = address_entry.get()
    phone = phone_entry.get()
    description = description_entry.get()
    amount = amount_entry.get()
    if not name or not address or not phone or not description or not amount:
        messagebox.showerror("Error", "All fields are required.")
        return
    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Error", "Amount must be a number.")
        return

    today = datetime.date.today()
    cursor.execute('INSERT INTO expenses (name, address, phone, description, amount, date) VALUES (?, ?, ?, ?, ?, ?)', (name, address, phone, description, amount, today))
    conn.commit()
    name_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    messagebox.showinfo("Success", "Expense recorded successfully!")

# Function to view expenses and display in a table
def view_expenses():
    cursor.execute('SELECT * FROM expenses')
    expenses = cursor.fetchall()

    if not expenses:
        messagebox.showinfo("Expenses", "No expenses recorded yet.")
    else:
        # Create a frame within the main window to display the table
        table_frame = tk.Frame(root)
        table_frame.grid(row=7, column=0, padx=20, pady=20, sticky='nsew')

        # Create a Treeview widget to display the table
        tree = ttk.Treeview(table_frame, columns=("ID", "Name", "Address", "Phone", "Description", "Amount", "Date"))
        tree.heading("#1", text="ID")
        tree.heading("#2", text="Name")
        tree.heading("#3", text="Address")
        tree.heading("#4", text="Phone")
        tree.heading("#5", text="Description")
        tree.heading("#6", text="Amount")
        tree.heading("#7", text="Date")

        # Increase the width of each column (you can adjust the values)
        tree.column("#1", width=50)
        tree.column("#2", width=150)
        tree.column("#3", width=150)
        tree.column("#4", width=100)
        tree.column("#5", width=200)
        tree.column("#6", width=100)
        tree.column("#7", width=100)

        # Add data to the Treeview
        for expense in expenses:
            # Add the Rupee symbol (₹) as a prefix to the amount
            expense_with_rupees = (expense[0], expense[1], expense[2], expense[3], expense[4], "₹" + str(expense[5]), expense[6])
            tree.insert("", "end", values=expense_with_rupees)

        tree.pack(expand=True, fill="both")

# Create the main window
root = tk.Tk()
root.title("Expense Explorer")
root.configure(bg="light blue")

# Create a frame
frame = tk.Frame(root, bg="light blue")
frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

# Labels
name_label = tk.Label(frame, text="Name:", bg="light blue")
address_label = tk.Label(frame, text="Address:", bg="light blue")
phone_label = tk.Label(frame, text="Phone:", bg="light blue")
description_label = tk.Label(frame, text="Description:", bg="light blue")
amount_label = tk.Label(frame, text="Amount (₹):", bg="light blue")  # Updated label to indicate Rupees

# Entry fields
name_entry = tk.Entry(frame)
address_entry = tk.Entry(frame)
phone_entry = tk.Entry(frame)
description_entry = tk.Entry(frame)
amount_entry = tk.Entry(frame)

# Buttons
record_button = tk.Button(frame, text="Record Expense", command=record_expense, bg="light blue")
view_button = tk.Button(frame, text="View Expenses", command=view_expenses, bg="light blue")

# Arrange components using grid
name_label.grid(row=0, column=0, sticky='w')
name_entry.grid(row=0, column=1, padx=10, pady=5, sticky='we')
address_label.grid(row=1, column=0, sticky='w')
address_entry.grid(row=1, column=1, padx=10, pady=5, sticky='we')
phone_label.grid(row=2, column=0, sticky='w')
phone_entry.grid(row=2, column=1, padx=10, pady=5, sticky='we')
description_label.grid(row=3, column=0, sticky='w')
description_entry.grid(row=3, column=1, padx=10, pady=5, sticky='we')
amount_label.grid(row=4, column=0, sticky='w')
amount_entry.grid(row=4, column=1, padx=10, pady=5, sticky='we')

record_button.grid(row=5, column=0, columnspan=2, pady=10)
view_button.grid(row=6, column=0, columnspan=2, pady=10)

# Define grid weights for responsiveness
for i in range(7):
    frame.rowconfigure(i, weight=1)
frame.columnconfigure(1, weight=1)

# Start the GUI event loop
root.mainloop()

# Close the database connection when the application exits
conn.close()