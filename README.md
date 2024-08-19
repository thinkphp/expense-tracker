# expense-tracker
An expense tracker where users can log their expenses, categorize them, and view reports. Concepts: Data storage (using files or SQLite), filtering, summarizing data, date handling.


#### Database Setup:
setup_database(): Initializes an SQLite database with a table for storing expenses.
add_expense(): Adds a new expense record to the database.
fetch_expenses(): Retrieves all expense records.
fetch_expenses_by_category(): Retrieves the sum of expenses grouped by category.

#### GUI Components:
Input Frame: Contains fields for entering the amount, category, and date of the expense.
Report Frame: Contains buttons to show all expenses or a summary by category.
Text Area: Displays the results of the reports.

#### Expense Tracking Logic:
add_expense(): Validates and adds expenses to the database.
show_expenses(): Displays all recorded expenses.
show_category_summary(): Displays a summary of expenses grouped by category.
