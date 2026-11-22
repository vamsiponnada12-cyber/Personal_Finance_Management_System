import json
import hashlib
import re
import uuid
from datetime import datetime
from pathlib import Path


DATA_DIR = Path(__file__).parent / "data"
USERS_FILE = DATA_DIR / "users.txt"
TRANSACTIONS_FILE = DATA_DIR / "transactions.txt"
BUDGETS_FILE = DATA_DIR / "budgets.txt"


class FinanceSystem:
    """Menu-driven personal finance application with TXT-based storage."""

    def __init__(self):
        DATA_DIR.mkdir(exist_ok=True)
        self.current_user = None
        self._ensure_file(USERS_FILE, [])
        self._ensure_file(TRANSACTIONS_FILE, [])
        self._ensure_file(BUDGETS_FILE, [])

    @staticmethod
    def _ensure_file(path, default):
        if not path.exists():
            path.write_text(json.dumps(default, indent=4), encoding="utf-8")

    @staticmethod
    def _read_data(path):
        try:
            with path.open("r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            print(f"Warning: Could not read {path.name}. Starting with empty data.")
            return []

    @staticmethod
    def _write_data(path, data):
        with path.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def _hash_password(password):
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    @staticmethod
    def _valid_email(email):
        # This checks Gmail address format; it does not send an OTP or verify inbox ownership.
        pattern = r"^[a-zA-Z0-9][a-zA-Z0-9._+-]*@gmail\.com$"
        return bool(re.fullmatch(pattern, email.strip()))

    @staticmethod
    def _valid_phone(phone):
        return bool(re.fullmatch(r"[6-9][0-9]{9}", phone.strip()))

    @staticmethod
    def _valid_password(password):
        # Minimum 8 characters, with uppercase, lowercase, digit and special character.
        return (
            len(password) >= 8
            and re.search(r"[A-Z]", password)
            and re.search(r"[a-z]", password)
            and re.search(r"[0-9]", password)
            and re.search(r"[^A-Za-z0-9]", password)
        )

    @staticmethod
    def _read_amount(prompt):
        while True:
            try:
                amount = float(input(prompt).strip())
                if amount <= 0:
                    print("Amount must be greater than zero.")
                    continue
                return round(amount, 2)
            except ValueError:
                print("Please enter a valid number.")

    @staticmethod
    def _read_nonempty(prompt):
        while True:
            value = input(prompt).strip()
            if value:
                return value
            print("This field cannot be empty.")

    def register(self):
        print("\n========== USER REGISTRATION ==========")
        users = self._read_data(USERS_FILE)

        full_name = self._read_nonempty("Full name: ")
        while True:
            username = self._read_nonempty("Create username: ").lower()
            if any(u["username"] == username for u in users):
                print("Username already exists. Choose another username.")
            else:
                break

        while True:
            email = self._read_nonempty("Gmail address: ").lower()
            if not self._valid_email(email):
                print("Enter a valid Gmail address (example: name@gmail.com).")
            elif any(u["email"] == email for u in users):
                print("This Gmail address is already registered.")
            else:
                break

        while True:
            phone = self._read_nonempty("10-digit mobile number: ")
            if not self._valid_phone(phone):
                print("Enter a valid 10-digit Indian mobile number starting with 6, 7, 8 or 9.")
            else:
                break

        while True:
            password = self._read_nonempty(
                "Create password (8+ chars, upper/lowercase, number, special char): "
            )
            if not self._valid_password(password):
                print("Password does not meet the required conditions.")
                continue
            confirm = self._read_nonempty("Confirm password: ")
            if password != confirm:
                print("Passwords do not match. Try again.")
            else:
                break

        user = {
            "user_id": str(uuid.uuid4()),
            "full_name": full_name,
            "username": username,
            "email": email,
            "phone": phone,
            "password_hash": self._hash_password(password),
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        users.append(user)
        self._write_data(USERS_FILE, users)
        print("\nRegistration successful. You can now log in.")
        print("Note: Gmail format is checked, but inbox ownership is not OTP-verified.")

    def forgot_password(self):
        """Reset a password after matching the registered Gmail and phone number."""
        print("\n=========== FORGOT PASSWORD ===========")
        users = self._read_data(USERS_FILE)

        email = self._read_nonempty("Enter registered Gmail: ").lower()
        phone = self._read_nonempty("Enter registered 10-digit mobile number: ")

        user_found = None
        for user in users:
            if user.get("email", "").lower() == email and user.get("phone", "") == phone:
                user_found = user
                break

        if user_found is None:
            print("Gmail or mobile number does not match our records.")
            return

        print("Account details matched. You can create a new password.")
        while True:
            new_password = self._read_nonempty(
                "Enter new password (8+ chars, upper/lowercase, number, special char): "
            )
            if not self._valid_password(new_password):
                print("Password must contain at least 8 characters, uppercase, lowercase, a number and a special character.")
                continue

            confirm_password = self._read_nonempty("Confirm new password: ")
            if new_password != confirm_password:
                print("Passwords do not match. Please try again.")
                continue
            break

        user_found["password_hash"] = self._hash_password(new_password)
        self._write_data(USERS_FILE, users)
        print("\nPassword reset successfully! Please login using your new password.")

    def login(self):
        print("\n=============== USER LOGIN ===============")
        users = self._read_data(USERS_FILE)
        login_id = self._read_nonempty("Username or Gmail: ").lower()
        password = self._read_nonempty("Password: ")
        password_hash = self._hash_password(password)

        for user in users:
            if (user["username"] == login_id or user["email"] == login_id) and \
                    user["password_hash"] == password_hash:
                self.current_user = user
                print(f"\nWelcome, {user['full_name']}!")
                return True

        print("Invalid username/email or password.")
        return False

    def _user_transactions(self):
        transactions = self._read_data(TRANSACTIONS_FILE)
        return [t for t in transactions if t["user_id"] == self.current_user["user_id"]]

    def _save_transaction(self, transaction_type, amount, category, description):
        all_transactions = self._read_data(TRANSACTIONS_FILE)
        transaction = {
            "transaction_id": "TXN-" + uuid.uuid4().hex[:10].upper(),
            "user_id": self.current_user["user_id"],
            "type": transaction_type,
            "amount": amount,
            "category": category,
            "description": description,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.now().strftime("%H:%M:%S")
        }
        all_transactions.append(transaction)
        self._write_data(TRANSACTIONS_FILE, all_transactions)
        print(f"Transaction saved successfully. ID: {transaction['transaction_id']}")

    def add_income(self):
        print("\n----------- ADD INCOME -----------")
        amount = self._read_amount("Income amount (Rs.): ")
        source = self._read_nonempty("Income source (Salary, Freelance, etc.): ")
        description = input("Description (optional): ").strip() or source
        self._save_transaction("income", amount, source, description)

    def add_expense(self):
        print("\n----------- RECORD EXPENSE -----------")
        amount = self._read_amount("Expense amount (Rs.): ")
        categories = [
            "Food", "Transport", "Shopping", "Bills", "Education",
            "Health", "Entertainment", "Rent", "Travel", "Other"
        ]
        print("Categories:", ", ".join(categories))
        category = self._read_nonempty("Enter category: ").title()
        if category not in categories:
            print("Unknown category. It will be saved under 'Other'.")
            category = "Other"
        description = input("Description (optional): ").strip() or category

        month = datetime.now().strftime("%Y-%m")
        budget = self._get_budget(month)
        spent = sum(
            t["amount"] for t in self._user_transactions()
            if t["type"] == "expense" and t["date"].startswith(month)
        )
        if budget is not None and spent + amount > budget:
            print(f"Budget warning: this expense exceeds your monthly budget.")
            print(f"Budget: Rs. {budget:.2f} | Already spent: Rs. {spent:.2f}")
            print(f"After this expense: Rs. {spent + amount:.2f}")
            choice = input("Save this expense anyway? (y/n): ").strip().lower()
            if choice != "y":
                print("Expense cancelled.")
                return
        self._save_transaction("expense", amount, category, description)

    def set_monthly_budget(self):
        print("\n----------- SET MONTHLY BUDGET -----------")
        month = input("Month (YYYY-MM), press Enter for current month: ").strip()
        if not month:
            month = datetime.now().strftime("%Y-%m")
        try:
            datetime.strptime(month, "%Y-%m")
        except ValueError:
            print("Invalid month format. Use YYYY-MM.")
            return

        amount = self._read_amount("Monthly budget (Rs.): ")
        budgets = self._read_data(BUDGETS_FILE)
        found = False
        for budget in budgets:
            if budget["user_id"] == self.current_user["user_id"] and budget["month"] == month:
                budget["amount"] = amount
                found = True
                break
        if not found:
            budgets.append({
                "user_id": self.current_user["user_id"],
                "month": month,
                "amount": amount
            })
        self._write_data(BUDGETS_FILE, budgets)
        print(f"Budget for {month} saved: Rs. {amount:.2f}")

    def _get_budget(self, month):
        budgets = self._read_data(BUDGETS_FILE)
        for budget in budgets:
            if budget["user_id"] == self.current_user["user_id"] and budget["month"] == month:
                return budget["amount"]
        return None

    def transaction_history(self):
        print("\n----------- TRANSACTION HISTORY -----------")
        transactions = sorted(self._user_transactions(), key=lambda t: (t["date"], t["time"]))
        if not transactions:
            print("No transactions found.")
            return
        print(f"{'ID':<16} {'DATE':<12} {'TYPE':<9} {'CATEGORY':<16} {'AMOUNT':>12}")
        print("-" * 70)
        for t in transactions:
            print(f"{t['transaction_id']:<16} {t['date']:<12} {t['type']:<9} "
                  f"{t['category']:<16} Rs.{t['amount']:>9.2f}")
            print(f"  Description: {t['description']}")
        total_income = sum(t["amount"] for t in transactions if t["type"] == "income")
        total_expense = sum(t["amount"] for t in transactions if t["type"] == "expense")
        print("-" * 70)
        print(f"Total income:   Rs. {total_income:.2f}")
        print(f"Total expenses: Rs. {total_expense:.2f}")
        print(f"Net savings:    Rs. {total_income - total_expense:.2f}")

    def category_summary(self):
        print("\n----------- CATEGORY-WISE EXPENSE SUMMARY -----------")
        totals = {}
        for t in self._user_transactions():
            if t["type"] == "expense":
                totals[t["category"]] = totals.get(t["category"], 0) + t["amount"]
        if not totals:
            print("No expenses recorded.")
            return
        for category, amount in sorted(totals.items(), key=lambda item: item[1], reverse=True):
            print(f"{category:<18} Rs. {amount:.2f}")
        print(f"\nTotal expenses: Rs. {sum(totals.values()):.2f}")

    def savings_summary(self):
        transactions = self._user_transactions()
        income = sum(t["amount"] for t in transactions if t["type"] == "income")
        expenses = sum(t["amount"] for t in transactions if t["type"] == "expense")
        print("\n----------- SAVINGS SUMMARY -----------")
        print(f"Total income:   Rs. {income:.2f}")
        print(f"Total expenses: Rs. {expenses:.2f}")
        print(f"Total savings:  Rs. {income - expenses:.2f}")
        if income > 0:
            print(f"Savings rate:   {(income - expenses) / income * 100:.2f}%")

    def highest_expense(self):
        expenses = [t for t in self._user_transactions() if t["type"] == "expense"]
        print("\n----------- HIGHEST EXPENSE -----------")
        if not expenses:
            print("No expenses recorded.")
            return
        highest = max(expenses, key=lambda t: t["amount"])
        print(f"Amount:      Rs. {highest['amount']:.2f}")
        print(f"Category:    {highest['category']}")
        print(f"Date:        {highest['date']}")
        print(f"Description: {highest['description']}")

    def monthly_summary(self):
        print("\n----------- MONTHLY FINANCIAL SUMMARY -----------")
        month = input("Enter month (YYYY-MM), press Enter for current month: ").strip()
        if not month:
            month = datetime.now().strftime("%Y-%m")
        try:
            datetime.strptime(month, "%Y-%m")
        except ValueError:
            print("Invalid month format. Use YYYY-MM.")
            return

        transactions = [
            t for t in self._user_transactions() if t["date"].startswith(month)
        ]
        income = sum(t["amount"] for t in transactions if t["type"] == "income")
        expenses = sum(t["amount"] for t in transactions if t["type"] == "expense")
        budget = self._get_budget(month)
        print(f"\nMonth: {month}")
        print(f"Income:   Rs. {income:.2f}")
        print(f"Expenses: Rs. {expenses:.2f}")
        print(f"Savings:  Rs. {income - expenses:.2f}")
        if budget is not None:
            print(f"Budget:   Rs. {budget:.2f}")
            print(f"Remaining budget: Rs. {budget - expenses:.2f}")
            if expenses > budget:
                print("Status: Budget exceeded.")
            else:
                print("Status: Within budget.")
        else:
            print("No budget has been set for this month.")

    def profile(self):
        print("\n----------- MY PROFILE -----------")
        for field in ("full_name", "username", "email", "phone", "created_at"):
            print(f"{field.replace('_', ' ').title()}: {self.current_user[field]}")

    def user_menu(self):
        while self.current_user:
            print("\n========== PERSONAL FINANCE MENU ==========")
            print("1. Add Income")
            print("2. Record Expense")
            print("3. Set Monthly Budget")
            print("4. View Transaction History")
            print("5. Category-Wise Expense Summary")
            print("6. Savings Calculation")
            print("7. Identify Highest Expense")
            print("8. Monthly Financial Summary")
            print("9. View My Profile")
            print("10. Logout")
            choice = input("Enter your choice (1-10): ").strip()

            actions = {
                "1": self.add_income,
                "2": self.add_expense,
                "3": self.set_monthly_budget,
                "4": self.transaction_history,
                "5": self.category_summary,
                "6": self.savings_summary,
                "7": self.highest_expense,
                "8": self.monthly_summary,
                "9": self.profile
            }
            if choice in actions:
                try:
                    actions[choice]()
                except (OSError, KeyError, TypeError) as error:
                    print(f"Could not complete this action: {error}")
            elif choice == "10":
                print(f"Logged out. Goodbye, {self.current_user['full_name']}!")
                self.current_user = None
            else:
                print("Invalid choice. Select a number from 1 to 10.")

    def run(self):
        while True:
            print("\n==========================================")
            print("       PERSONAL FINANCE MANAGEMENT")
            print("==========================================")
            print("1. Register")
            print("2. Login")
            print("3. Forgot Password")
            print("4. Exit")
            choice = input("Enter your choice (1-4): ").strip()

            if choice == "1":
                try:
                    self.register()
                except OSError as error:
                    print(f"Registration could not be saved: {error}")
            elif choice == "2":
                if self.login():
                    self.user_menu()
            elif choice == "3":
                try:
                    self.forgot_password()
                except OSError as error:
                    print(f"Password reset could not be saved: {error}")
            elif choice == "4":
                print("Thank you for using Personal Finance Management System.")
                break
            else:
                print("Invalid choice. Select 1, 2, 3 or 4.")


if __name__ == "__main__":
    FinanceSystem().run()
