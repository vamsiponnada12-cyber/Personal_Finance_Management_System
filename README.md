
# Personal Finance Management System

## 1. Project Overview

The **Personal Finance Management System** is a Python-based console application designed to help users manage their personal financial activities. Users can register, log in, record income and expenses, set monthly budgets, track savings, and view financial reports.

The application stores user details, transactions, and budget information in text files so that the data can be accessed again when the program runs.

## 2. Objectives

- Create a user registration and login system.
- Validate email addresses and mobile numbers.
- Record income and expenses.
- Organize expenses into different categories.
- Set and monitor monthly budgets.
- Ask user permission before saving an expense that exceeds the monthly budget.
- Track savings and financial goals.
- Generate monthly financial reports.
- Store user information and transaction records using TXT files.
- Practice Python programming concepts.

## 3. Features

1. **User Registration** — Create a new account with personal details.
2. **User Login** — Access the application using registered credentials.
3. **Email Validation** — Check whether the entered email address follows the required format.
4. **Mobile Number Validation** — Accept only valid 10-digit Indian mobile numbers.
5. **Add Income** — Record income details with category and amount.
6. **Add Expense** — Record expenses under different categories.
7. **Set Monthly Budget** — Create a monthly spending limit.
8. **Budget Warning** — Display a warning when expenses reach 80% of the monthly budget.
9. **Budget Permission** — When an expense exceeds the budget, ask the user for permission before saving the transaction. If the user selects No, the expense is not saved.
10. **Budget Analysis** — Compare the monthly budget with actual expenses.
11. **Savings Suggestions** — Provide suggestions based on spending patterns.
12. **Previous Month Comparison** — Compare the current month's financial activity with the previous month.
13. **Savings Goal** — Set and track a personal savings target.
14. **Transaction History** — Display the user's saved income and expense records.
15. **Category-wise Expense Summary** — Calculate total spending for each expense category.
16. **Highest Expense Identification** — Identify the highest recorded expense.
17. **Monthly Financial Summary** — Calculate total income, expenses, and savings.
18. **User-wise Data Storage** — Maintain separate financial records for each registered user.

## 4. Technologies Used

- Python 3
- JSON module
- datetime module
- hashlib module
- re module
- Lists and Dictionaries
- Functions and Classes
- Exception Handling
- TXT File Handling
- Command-Line Interface (CLI)

No external Python packages are required.

## 5. Project Structure

```text
Personal_Finance_Management_System/
│
├── main.py
├── README.md
├── requirements.txt
├── .gitignore
│
└── data/
    ├── users.txt
    ├── transactions.txt
    └── budgets.txt
```

**File Description:**

- `main.py` — Contains the complete Python application.
- `README.md` — Contains project documentation.
- `requirements.txt` — Contains project dependency information.
- `.gitignore` — Specifies files that should not be uploaded to GitHub.
- `users.txt` — Stores registered user information.
- `transactions.txt` — Stores income and expense transactions.
- `budgets.txt` — Stores monthly budget and savings goal information.

## 6. How to Run

### Step 1: Install Python

Install Python 3 if it is not already installed.

### Step 2: Open the Project Folder

Open the project folder in VS Code.

### Step 3: Open Terminal

Choose **Terminal → New Terminal** in VS Code.

### Step 4: Run the Program

Execute the following command:

```bash
py main.py
```

### Step 5: Register an Account

- Enter your name.
- Enter a valid email address.
- Enter a valid 10-digit mobile number.
- Create a password according to the password requirements.

### Step 6: Login

Enter your registered email and password to access the application.

### Step 7: Use the Application

After successful login, use the available menu options to manage your financial activities.

## 7. Budget Management

The application provides monthly budget monitoring.

- **100% Budget Usage:** Displays a warning when spending reaches 100% of the budget.
- **Budget Exceeded:** Asks the user for permission before saving an expense that exceeds the available budget.
- **Permission Granted:** The expense is saved.
- **Permission Denied:** The expense is not saved.
- **Budget Analysis:** Displays the budget amount, actual expenses, and remaining balance.
- **Savings Suggestions:** Provides suggestions based on spending categories.
- **Previous Month Comparison:** Helps compare financial activity between two months.
- **Savings Goal:** Tracks progress towards the user's savings target.

## 8. Data Storage

The application uses TXT files with JSON-formatted records to store information.

### users.txt

Stores registered user details.

### transactions.txt

Stores income and expense transaction records.

### budgets.txt

Stores monthly budget and savings goal details.

Each user's financial records are associated with their user account.

**Note:** Keep the data files in the `data` folder. Do not manually change their contents while the application is running.

## 9. Python Concepts Demonstrated

- **Lists:** Store multiple transaction records.
- **Dictionaries:** Organize user, transaction, and budget information.
- **Functions:** Perform separate operations for different features.
- **Classes and Objects:** Organize the application using object-oriented programming.
- **Conditional Statements:** Implement login checks and budget validation.
- **Loops:** Display menus and repeat operations.
- **Exception Handling:** Handle invalid inputs and file-related errors.
- **Basic Modules:** Use built-in Python modules.
- **TXT File Handling:** Store and retrieve application data.
- **JSON:** Convert structured data into a format suitable for text-file storage.

## 10. Current Limitations

- The application is a local console-based system.
- It does not provide a web interface or mobile application.
- Email format validation does not perform actual Gmail OTP verification.
- Financial records are stored locally in text files.
- The application is intended for learning and demonstration purposes.

## 11. Possible Future Improvements

- Add Gmail OTP verification.
- Develop a graphical user interface (GUI).
- Integrate a database such as MySQL.
- Generate PDF and Excel financial reports.
- Add graphical charts for expense analysis.
- Add transaction editing and deletion.
- Develop a web-based version of the application.

## 12. GitHub Upload

1. Create a new repository on GitHub, for example `personal-finance-management-system`.
2. Open the project folder in VS Code.
3. Initialize Git using the terminal.
4. Add the project files.
5. Commit and push the project to GitHub.

Example commands:

```bash
git init
git add .
git commit -m "Add Personal Finance Management System"
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your GitHub repository URL.

**Developed by: Ponnada Sri Vamsi**

## 13. Conclusion

The Personal Finance Management System is a Python-based application that helps users manage income, expenses, monthly budgets, and savings. It includes user registration, login, input validation, budget permission handling, financial analysis, and text-file storage.

This project demonstrates important Python concepts such as functions, lists, dictionaries, classes, objects, conditional statements, exception handling, and file handling.
