from app.Repositories.sheets_repo import SheetsRepository

repo = SheetsRepository()

class TransactionService:

    def add_income(
        self,
        amount
    ):

        repo.save([
            "Income",
            amount
        ])