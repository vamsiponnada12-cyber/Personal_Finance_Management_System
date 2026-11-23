# Personal Finance Management System

## 1. Project Overview

The **Personal Finance Management System** is a Python console application for managing personal income, expenses, monthly budgets, and savings summaries. Users can register, log in, record transactions, and view financial reports.

The application stores records locally as JSON-formatted text files in the `data` folder. The Python standard library is used; no third-party packages are required.

## 2. Objectives

- Provide user registration, login, and password reset.
- Validate email format, mobile numbers, passwords, and financial amounts.
- Record income and expenses by category.
- Set and monitor monthly budgets.
- Ask permission before saving an expense that exceeds the monthly budget.
- Calculate savings and generate monthly financial summaries.
- Demonstrate Python functions, classes, validation, exception handling, and file handling.

## 3. Implemented Features

1. **User Registration** — Create an account with name, username, Gmail address, mobile number, and password.
2. **User Login** — Sign in using the registered username or Gmail address.
3. **Forgot Password** — Reset the password after matching the registered Gmail address and phone number. This is not an OTP-based verification.
4. **Input Validation** — Validate Gmail format, Indian mobile number, password rules, and positive finite financial amounts.
5. **Add Income** — Save income with a source/category and description.
6. **Add Expense** — Save expenses under supported categories.
7. **Monthly Budget** — Create or update a budget using the `YYYY-MM` format.
8. **Budget Approval** — If an expense exceeds the remaining budget, the user can approve or cancel saving it.
9. **Transaction History** — View saved income and expense records.
10. **Category-wise Expense Summary** — View expense totals by category.
11. **Savings Summary** — Calculate total income, expenses, savings, and savings rate.
12. **Highest Expense** — Identify the largest expense.
13. **Monthly Financial Summary** — View income, expenses, savings, and budget status for a selected month.
14. **Profile** — View registered account details.
15. **Safe File Handling** — Validate stored records and use temporary-file replacement when saving to reduce the risk of data loss.

## 4. Technologies Used

- Python 3
- JSON, `datetime`, `hashlib`, `re`, `uuid`, `math`, `os`, and `tempfile` (standard-library modules)
- Lists and dictionaries
- Functions and classes
- Exception handling
- Text-file storage
- Command-line interface (CLI)

No external Python packages are required.

## 5. Project Structure

```text
Personal_Finance_Management_System/
│
├── main.py
├── finance_system.py
├── README.md
├── .gitignore
│
└── data/
    ├── users.txt
    ├── transactions.txt
    └── budgets.txt
```

### File Description

- `main.py` — Application entry point. It creates the `FinanceSystem` object and launches the application.
- `finance_system.py` — Contains the application logic, menus, validation, transaction processing, reports, and file operations.
- `README.md` — Project documentation.
- `.gitignore` — Lists files and folders that should not be committed.
- `data/users.txt` — Stores registered user records.
- `data/transactions.txt` — Stores income and expense records.
- `data/budgets.txt` — Stores monthly budget records.

## 6. How to Run

1. Install Python 3.
2. Open the project folder in VS Code.
3. Open **Terminal → New Terminal**.
4. Run:

```bash
py main.py
```

5. Register an account, then log in.
6. Use the menu to add income, record expenses, set budgets, and view reports.

The application creates the `data` folder and its empty data files when they do not already exist.

## 7. Budget Management

- Create or update a monthly budget using the exact `YYYY-MM` format, for example `2026-01`.
- When a new expense would exceed the budget, the application displays the budget and projected spending.
- Enter `y` to approve and save the expense.
- Enter any other response to cancel it.
- The monthly report displays income, expenses, savings, budget, and remaining budget.

## 8. Data Storage and Recovery

The application uses JSON-formatted records inside `.txt` files.

- `users.txt` stores account details and password hashes.
- `transactions.txt` stores transaction details.
- `budgets.txt` stores monthly budget details.

Loaded JSON records are checked for required fields, data types, valid dates, transaction types, and valid financial amounts. If a file is unreadable or contains invalid records, the application stops that operation and displays a recovery message instead of treating the file as empty.

When saving, the application writes to a temporary file first and replaces the original only after the write completes successfully. If a save fails, the existing file is preserved and no success message is displayed.

**Important:** Keep backup copies of the `data` folder. Do not edit data files while the application is running. Sample records, if added for demonstration, must use clearly fictional details.

## 9. Python Concepts Demonstrated

- Lists and dictionaries
- Functions and methods
- Classes and objects
- Conditional statements and loops
- Input validation
- Exception handling
- JSON serialization
- Text-file handling
- Standard-library modules

## 10. Current Limitations

- The application is a local console-based system.
- It does not provide a web interface or mobile application.
- Gmail format is checked, but actual Gmail OTP verification is not implemented.
- Forgot Password matches the registered Gmail and phone number; it does not send an OTP.
- Financial data is stored locally in text files.
- The project is intended for learning and demonstration purposes.

## 11. Possible Future Improvements

- Add verified email OTP authentication.
- Add savings goals and goal-progress tracking.
- Add spending suggestions and previous-month comparisons.
- Add budget-usage alerts at configurable thresholds.
- Develop a graphical user interface or web application.
- Integrate a database such as MySQL.
- Generate PDF and Excel reports.
- Add charts for expense analysis.
- Add transaction editing and deletion.

## 12. GitHub Upload

1. Create a repository on GitHub.
2. Open the project folder in VS Code.
3. Open the terminal and run:

```bash
git init
git add .
git commit -m "Update Personal Finance Management System"
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your repository URL. If the repository already has a remote configured, do not add it again; use `git push`.

## 13. Conclusion

The Personal Finance Management System helps users record income and expenses, manage monthly budgets, and review savings. It demonstrates Python programming fundamentals, input validation, safe file handling, and basic financial reporting.

**Developed by: Ponnada Sri Vamsi**
