import tkinter as tk               # Import Tkinter library for GUI (windows, buttons, forms)
from tkinter import ttk,messagebox # ttk: styled widgets, messagebox: popup messages
import pandas as pd                # Pandas for data storage and calculations
import matplotlib.pyplot as pie    # Matplotlib for charts (pie chart visualization)
from datetime import datetime      # For working with dates (today’s date)
import os                          # For file operations (check if file exists)

FILE_NAME="transactions.csv"       # Name of the CSV file to store transactions

# If the file does not exist, create an empty CSV with required columns
if not os.path.exists(FILE_NAME):
    df=pd.DataFrame(columns=["Type","Amount","Category","Date"]) # Create empty DataFrame
    df.to_csv(FILE_NAME,index=False)  # Save DataFrame to CSV file

# Function to add transactions (Income or Expense)
def add_transactions(t_type,amount,category,date):  
    try:
        amount=float(amount)                        # Convert amount to float, error if invalid
        df=pd.read_csv(FILE_NAME)                   # Load existing data from CSV
        # Create a new row with transaction details
        new_row = pd.DataFrame([{"Type": t_type, "Amount": amount, "Category": category, "Date": date}]) 
        # Append new row to DataFrame
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(FILE_NAME,index=False)            # Save updated DataFrame back to CSV
        messagebox.showinfo("Success",f"{t_type} add successfully!") # Show success popup
    except ValueError:
        messagebox.showerror("Error","Please enter a valid amount.") # Show error popup if amount invalid

# Function to open a form window for adding Income/Expense
def open_form(t_type):                                                
    form=tk.Toplevel(root)                             # Create new popup window
    form.title(f"Add {t_type}")                        # Set window title

    tk.Label(form,text="Amount:").pack()               # Label for amount
    amount_entry=tk.Entry(form)                        # Input box for amount
    amount_entry.pack()

    tk.Label(form,text="Category:").pack()             # Label for category
    category_entry=tk.Entry(form)                      # Input box for category
    category_entry.pack()

    tk.Label(form,text="Date (YYYY-MM-DD):").pack()    # Label for date
    date_entry=tk.Entry(form)                          # Input box for date
    date_entry.insert(0,datetime.today().strftime("%Y-%m-%d")) # Pre-fill with today’s date
    date_entry.pack()

    # Function to submit form data
    def submit():
        add_transactions(t_type, amount_entry.get(),category_entry.get(),date_entry.get()) # Add transaction
        form.destroy()                                # Close form window after submission

    tk.Button(form,text="Submit",command=submit).pack() # Submit button

# Function to view summary of income, expenses, and balance
def view_summary():
    df=pd.read_csv(FILE_NAME)                         # Load data from CSV
    income=df[df["Type"]=="Income"]["Amount"].sum()   # Sum of all Income
    expense=df[df["Type"]=="Expense"]["Amount"].sum() # Sum of all Expense
    balance=income-expense                            # Balance = Income - Expense

    # Format summary message
    summary=f"Total Income: ₹{income:.2f}\nTotal Expense: ₹{expense:.2f}\nBalance: ₹{balance:.2f}"
    messagebox.showinfo("Summary",summary)            # Show summary popup

# Function to reset all data (clear CSV file)
def reset_data():
    df = pd.DataFrame(columns=["Type","Amount","Category","Date"]) # Empty DataFrame
    df.to_csv(FILE_NAME, index=False)                 # Save empty DataFrame to CSV
    messagebox.showinfo("Reset", "All transactions cleared!") # Show reset confirmation

# Function to show expense chart (pie chart)
def show_chat():
    df=pd.read_csv(FILE_NAME)                         # Load data from CSV
    expense_df=df[df["Type"]=="Expense"]              # Filter only Expense rows
    if expense_df.empty:                              # If no expenses exist
        messagebox.showinfo("No Data","No expenses to show.") # Show message
        return
    category_sum=expense_df.groupby("Category")["Amount"].sum() # Group expenses by category
    category_sum.plot.pie(autopct='%1.1f%%',startangle=90)      # Plot pie chart
    pie.title("Expenses by Category")                 # Set chart title
    pie.ylabel("")                                    # Remove y-axis label
    pie.show()                                        # Display chart

# Create main application window
root=tk.Tk()
root.title("Personal Finance Tracker")                # Set window title
root.geometry("300x300")                              # Set window size

# Add GUI elements (labels and buttons)
tk.Label(root, text="Finance Tracker", font=("Arial", 16)).pack(pady=10) # Title label
tk.Button(root, text="Add Income", width=20, command=lambda: open_form("Income")).pack(pady=5) # Add Income button
tk.Button(root, text="Add Expense", width=20, command=lambda: open_form("Expense")).pack(pady=5) # Add Expense button
tk.Button(root, text="View Summary", width=20, command=view_summary).pack(pady=5) # View Summary button
tk.Button(root, text="Show Expense Chart", width=20, command=show_chat).pack(pady=5) # Show Chart button
tk.Button(root, text="Exit", width=20, command=root.quit).pack(pady=20) # Exit button
tk.Button(root, text="Reset Data", width=20, command=reset_data).pack(pady=5) # Reset Data button

# Run the Tkinter event loop (keeps window open)
root.mainloop()
