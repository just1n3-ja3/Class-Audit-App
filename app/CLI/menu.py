from app.services.transac_service import TransactionService
from app.helpers.helper import app_helper

try:
    import pyfiglet
    _HAS_PYFIGLET = True
except ImportError:
    _HAS_PYFIGLET = False

service = TransactionService()
helper = app_helper()

MENU_OPTIONS = [
    "Add Record",
    "Filter Records by Date",
    "Filter Records by Name",
    "Filter Records by Type",
    "See the whole Records",
]


def _print_title():
    if _HAS_PYFIGLET:
        print(pyfiglet.figlet_format("Auditors Ground", font="slant"))
    else:
        print("=" * 60)
        print("                   AUDITORS GROUND")
        print("=" * 60)
    print("           Track your Money In / Money Out")
    print("=" * 60)
    print()


def _print_menu():
    for index, item in enumerate(MENU_OPTIONS, start=1):
        print(f"{index}. {item}")
    print("Type 'exit' to quit.")


def start():
    _print_title()

    while True:
        _print_menu()
        raw_choice = input("\nEnter your choice: ").strip()

        if raw_choice.upper() == "EXIT":
            print("Goodbye!")
            return

        ok, choice = helper.int_parse(raw_choice)
        if not ok:
            print("Invalid Choice!\n")
            continue

        if choice == 1:
            service.add_record()
        elif choice == 2:
            service.filter_date()
        elif choice == 3:
            service.filter_name()
        elif choice == 4:
            service.filter_type()
        elif choice == 5:
            service.print_all()
        else:
            print("Invalid Choice!")

        print()  