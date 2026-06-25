from app.Services.transac_service import TransactionService

service = TransactionService()

def start():

    while True:

        print("\n1. Add Income")
        print("2. Exit")

        choice = input("> ")

        if choice == "1":

            amount = float(
                input("Amount: ")
            )

            service.add_income(
                amount
            )

        elif choice == "2":
            break