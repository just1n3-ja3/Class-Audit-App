from datetime import date
from app.helpers.helper import app_helper
from app.repositories.sheets_repo import SheetsRepository
from app.models.transaction import Transaction

helper = app_helper()
repo = SheetsRepository()

TYPES = ["Money In", "Money Out"]


def _print_header():
    print(
        f"{'Date':<12} {'Name':<20} {'Type':<10} {'Amount':>12}  Remarks"
    )
    print("-" * 70)


def _print_records(records: list[Transaction]):
    _print_header()
    for record in records:
        print(record)


class TransactionService:
    def add_record(self):
        date_now = date.today()

        name = input("Enter Name: ").strip()
        if not name:
            print("Name cannot be empty.")
            return

        ok, type_choice = helper.int_parse(
            input(f"Enter Record Type: \n 1. {TYPES[0]} \n 2. {TYPES[1]} \n")
        )
        if not ok or type_choice not in (1, 2):
            print("Invalid record type selected.")
            return
        record_type = TYPES[type_choice - 1]

        ok, amount = helper.float_parse(input("Enter Amount: "))
        if not ok:
            print("Invalid amount entered.")
            return

        remarks = input("Your Remarks (Optional): ").strip()

        transaction = Transaction(
            timestamp=date_now.isoformat(),
            name=name,
            record_type=record_type,
            amount=amount,
            remarks=remarks,
        )

        try:
            success, message = repo.add_record(transaction)
            print(message)
        except Exception as e:
            print(f"Failed to add record: {e}")

    def filter_date(self):
        print("Filtering By Date")
        ok, parsed_date = helper.try_parse_date(input("Enter Date (yyyy-mm-dd): "))
        if not ok or parsed_date is None:
            print("Invalid date format. Please use yyyy-mm-dd.")
            return

        date_str = parsed_date.date().isoformat()

        try:
            results = repo.filter_by_date(date_str)
        except Exception as e:
            print(f"Failed to filter by date: {e}")
            return

        if not results:
            print("No records found for that date.")
            return
        _print_records(results)

    def filter_name(self):
        print("Filtering By Name")
        name = input("Enter Last Name Only: ").strip()
        if not name:
            print("Name cannot be empty.")
            return

        try:
            results = repo.filter_by_name(name)
        except Exception as e:
            print(f"Failed to filter by name: {e}")
            return

        if not results:
            print("No records found for that name.")
            return
        _print_records(results)

    def filter_type(self):
        while True:
            print("Filtering By Type")
            ok, choice = helper.int_parse(
                input(f"1.{TYPES[0]}\n2.{TYPES[1]}\n ")
            )

            if not ok or choice not in (1, 2):
                print("Invalid Choice!")
                continue

            record_type = TYPES[choice - 1]
            try:
                results = repo.filter_by_type(record_type)
            except Exception as e:
                print(f"Failed to filter by type: {e}")
                return

            if not results:
                print("No records found for that type.")
            else:
                _print_records(results)
            return

    def print_all(self):
        print("All Records")
        try:
            results = repo.get_all()
        except Exception as e:
            print(f"Failed to fetch records: {e}")
            return

        if not results:
            print("No records found.")
            return
        _print_records(results)