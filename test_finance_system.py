import contextlib
import importlib.util
import io
import json
import math
import tempfile
from pathlib import Path
from unittest.mock import patch

MODULE_PATH = Path(__file__).with_name("finance_system.py")
spec = importlib.util.spec_from_file_location("finance_system", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
FinanceSystem = module.FinanceSystem

def setup_app(tmp):
    data = Path(tmp) / "data"
    data.mkdir()
    module.DATA_DIR = data
    module.USERS_FILE = data / "users.txt"
    module.TRANSACTIONS_FILE = data / "transactions.txt"
    module.BUDGETS_FILE = data / "budgets.txt"
    app = FinanceSystem()
    app.current_user = {
        "user_id": "fictional-user-001", "full_name": "Demo User",
        "username": "demo", "email": "demo@example.com",
        "phone": "9000000000", "password_hash": "a" * 64,
        "created_at": "2026-01-01 10:00:00"
    }
    return app

def run_tests():
    passed = []
    with tempfile.TemporaryDirectory() as tmp:
        app = setup_app(tmp)

        # Valid income and expense; transaction history persistence after restart.
        app._save_transaction("income", 25000.00, "Salary", "Fictional salary")
        app._save_transaction("expense", 1250.50, "Food", "Fictional groceries")
        restarted_app = FinanceSystem()
        saved = restarted_app._read_data(module.TRANSACTIONS_FILE)
        assert len(saved) == 2 and saved[0]["type"] == "income"
        passed.append("normal income/expense transactions + restart persistence")

        # Budget cancellation and approval.
        module.BUDGETS_FILE.write_text(json.dumps([{
            "user_id": app.current_user["user_id"], "month": "2026-11", "amount": 100.00
        }]), encoding="utf-8")
        with patch("builtins.input", side_effect=["150", "Food", "", "n"]):
            app.add_expense()
        assert len(FinanceSystem._read_data(module.TRANSACTIONS_FILE)) == 2
        with patch("builtins.input", side_effect=["150", "Food", "", "y"]):
            app.add_expense()
        assert len(FinanceSystem._read_data(module.TRANSACTIONS_FILE)) == 3
        passed.append("budget approval and cancellation")

        # Invalid monetary values: nan, inf, and values rounded to zero.
        with patch("builtins.input", side_effect=["nan", "inf", "0.001", "0.01"]):
            amount = FinanceSystem._read_amount("amount: ")
        assert amount == 0.01
        passed.append("NaN, infinity, and sub-cent amount rejection")

        # Month must be canonical and padded.
        assert FinanceSystem._normalize_month("2026-01") == "2026-01"
        try:
            FinanceSystem._normalize_month("2026-1")
            raise AssertionError("unpadded month accepted")
        except ValueError:
            pass
        passed.append("strict YYYY-MM month validation")

        # Monthly report works against valid transaction dates and budgets.
        with patch("builtins.input", return_value="2026-11"), contextlib.redirect_stdout(io.StringIO()) as output:
            app.monthly_summary()
        assert "Month: 2026-11" in output.getvalue()
        passed.append("monthly financial report")

        # Invalid application record such as {} blocks use.
        module.USERS_FILE.write_text("[{}]", encoding="utf-8")
        original = module.USERS_FILE.read_bytes()
        try:
            FinanceSystem._read_data(module.USERS_FILE)
            raise AssertionError("invalid user record accepted")
        except module.DataFileError:
            pass
        assert module.USERS_FILE.read_bytes() == original
        passed.append("schema validation and invalid-record preservation")

        module.USERS_FILE.write_text("{broken json", encoding="utf-8")
        malformed_original = module.USERS_FILE.read_bytes()
        try:
            FinanceSystem._read_data(module.USERS_FILE)
            raise AssertionError("malformed JSON accepted")
        except module.DataFileError:
            pass
        assert module.USERS_FILE.read_bytes() == malformed_original
        passed.append("malformed JSON recovery without data overwrite")

        # Simulate atomic replacement failure; original bytes must remain unchanged.
        module.USERS_FILE.write_text("[]", encoding="utf-8")
        original = module.USERS_FILE.read_bytes()
        try:
            with patch.object(module.os, "replace", side_effect=OSError("simulated disk failure")):
                FinanceSystem._write_data(module.USERS_FILE, [{"sample": "new"}])
            raise AssertionError("simulated save failure was ignored")
        except OSError:
            pass
        assert module.USERS_FILE.read_bytes() == original
        passed.append("failed save preserves original file")

    return passed

if __name__ == "__main__":
    for item in run_tests():
        print("PASS:", item)
