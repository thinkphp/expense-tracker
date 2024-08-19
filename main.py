import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from datetime import datetime

def setup_database():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_expense(amount, category, date):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO expenses (amount, category, date)
        VALUES (?, ?, ?)
    ''', (amount, category, date))
    conn.commit()
    conn.close()

def fetch_expenses():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('SELECT * FROM expenses')
    records = c.fetchall()
    conn.close()
    return records

def fetch_expenses_by_category():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('SELECT category, SUM(amount) FROM expenses GROUP BY category')
    records = c.fetchall()
    conn.close()
    return records

def plot_expenses_by_category(plot_frame):
    records = fetch_expenses_by_category()
    categories = [record[0] for record in records]
    amounts = [record[1] for record in records]

    fig, ax = plt.subplots(figsize=(5, 4))
    ax.bar(categories, amounts, color='skyblue')
    ax.set_xlabel('Category')
    ax.set_ylabel('Total Amount')
    ax.set_title('Expenses by Category')
    plt.xticks(rotation=45, ha='right')

    for widget in plot_frame.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")

        setup_database()

        self.input_frame = tk.Frame(root)
        self.input_frame.pack(pady=20)

        self.label_amount = tk.Label(self.input_frame, text="Amount:")
        self.label_amount.pack(side=tk.LEFT, padx=10)
        self.entry_amount = tk.Entry(self.input_frame)
        self.entry_amount.pack(side=tk.LEFT)

        self.label_category = tk.Label(self.input_frame, text="Category:")
        self.label_category.pack(side=tk.LEFT, padx=10)
        self.entry_category = tk.Entry(self.input_frame)
        self.entry_category.pack(side=tk.LEFT)

        self.label_date = tk.Label(self.input_frame, text="Date (YYYY-MM-DD):")
        self.label_date.pack(side=tk.LEFT, padx=10)
        self.entry_date = tk.Entry(self.input_frame)
        self.entry_date.pack(side=tk.LEFT)

        self.button_add = tk.Button(self.input_frame, text="Add Expense", command=self.add_expense)
        self.button_add.pack(side=tk.LEFT, padx=10)

        self.report_frame = tk.Frame(root)
        self.report_frame.pack(pady=20)

        self.button_show = tk.Button(self.report_frame, text="Show Expenses", command=self.show_expenses)
        self.button_show.pack(side=tk.LEFT, padx=10)

        self.button_category_summary = tk.Button(self.report_frame, text="Show Category Summary", command=self.show_category_summary)
        self.button_category_summary.pack(side=tk.LEFT, padx=10)

        self.button_plot = tk.Button(self.report_frame, text="Plot Category Expenses", command=self.plot_expenses)
        self.button_plot.pack(side=tk.LEFT, padx=10)

        self.text_report = tk.Text(root, height=10, width=50)
        self.text_report.pack(pady=20)

        self.plot_frame = tk.Frame(root)
        self.plot_frame.pack(pady=20)

    def add_expense(self):
        amount = self.entry_amount.get()
        category = self.entry_category.get()
        date = self.entry_date.get()

        if not amount or not category or not date:
            messagebox.showerror("Input Error", "Please fill all fields")
            return

        try:
            amount = float(amount)
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Input Error", "Invalid amount or date format")
            return

        add_expense(amount, category, date)
        messagebox.showinfo("Success", "Expense added successfully")

    def show_expenses(self):
        records = fetch_expenses()
        self.text_report.delete(1.0, tk.END)
        for record in records:
            self.text_report.insert(tk.END, f"ID: {record[0]}, Amount: {record[1]}, Category: {record[2]}, Date: {record[3]}\n")

    def show_category_summary(self):
        records = fetch_expenses_by_category()
        self.text_report.delete(1.0, tk.END)
        for record in records:
            self.text_report.insert(tk.END, f"Category: {record[0]}, Total Amount: {record[1]}\n")

    def plot_expenses(self):
        plot_expenses_by_category(self.plot_frame)

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()
    
