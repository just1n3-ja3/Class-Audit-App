from google.oauth2.service_account import Credentials
from google.auth.exceptions import GoogleAuthError
import gspread
from gspread.exceptions import APIError, SpreadsheetNotFound, WorksheetNotFound
import os
import logging
from dotenv import load_dotenv

from app.models.transaction import Transaction

load_dotenv()
logger = logging.getLogger(__name__)


class SheetsAuthError(Exception):
    """Raised when Google Sheets credentials/auth setup fails."""
    pass


def _build_client():
    creds_path = os.getenv("GOOGLE_CREDS")
    if not creds_path:
        raise SheetsAuthError("GOOGLE_CREDS environment variable is not set")

    if not os.path.isfile(creds_path):
        raise SheetsAuthError(f"Credentials file not found at: {creds_path}")

    try:
        creds = Credentials.from_service_account_file(
            creds_path,
            scopes=[
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive",
            ],
        )
        return gspread.authorize(creds)
    except (ValueError, KeyError) as e:
        raise SheetsAuthError(f"Invalid service account credentials file: {e}") from e
    except GoogleAuthError as e:
        raise SheetsAuthError(f"Google authentication failed: {e}") from e


class SheetsRepository:
    def __init__(self):
        try:
            client = _build_client()
        except SheetsAuthError:
            raise

        sheet_name = os.getenv("SHEET_NAME", "SHEET_NAME2")
        try:
            self.sheet = client.open(sheet_name).sheet1
        except SpreadsheetNotFound as e:
            raise SheetsAuthError(
                f"Spreadsheet '{sheet_name}' not found, or service account "
                "lacks access to it"
            ) from e
        except APIError as e:
            raise SheetsAuthError(f"Google Sheets API error while opening sheet: {e}") from e
            
    

    def add_record(self, transaction: Transaction):
        try:
            self.sheet.append_row([
                transaction.timestamp,
                transaction.name,
                transaction.record_type,
                transaction.amount,
                transaction.remarks,
            ])
            return (True, "Success")
        except APIError as e:
            logger.error("API error adding record: %s", e)
            return (False, f"API error: {e}")
        except (SpreadsheetNotFound, WorksheetNotFound) as e:
            logger.error("Sheet/worksheet missing: %s", e)
            return (False, f"Sheet not found: {e}")
        except Exception as e:
            logger.exception("Unexpected error adding record")
            return (False, f"Unexpected error: {e}")

    def _get_all_records_safe(self):
        try:
            return self.sheet.get_all_records()
        except APIError as e:
            logger.error("API error fetching records: %s", e)
            raise
        except gspread.exceptions.GSpreadException as e:
            logger.error("Failed to parse sheet rows (check header row): %s", e)
            raise

    @staticmethod
    def _row_to_transaction(row: dict) -> Transaction | None:
        try:
            return Transaction(
                timestamp=row["Time Stamp"],
                name=row["Name"],
                record_type=row["Type"],
                amount=float(row["Amount"]),
                remarks=row.get("Remarks", ""),
            )
        except (KeyError, ValueError, TypeError) as e:
            logger.warning("Skipping malformed row %s: %s", row, e)
            return None

    def _filter_rows(self, column, value) -> list[Transaction]:
        try:
            rows = self._get_all_records_safe()
        except (APIError, gspread.exceptions.GSpreadException):
            return []

        results = []
        for row in rows:
            try:
                if row[column] != value:
                    continue
            except KeyError:
                logger.warning("Expected column '%s' missing in row: %s", column, row)
                continue

            transaction = self._row_to_transaction(row)
            if transaction is not None:
                results.append(transaction)
        return results
    def get_all(self) -> list[Transaction]:
        try:
            rows = self._get_all_records_safe()
        except (APIError, gspread.exceptions.GSpreadException):
                return []
                
        results = []
        for row in rows:
            transaction = self._row_to_transaction(row)
            if transaction is not None:
                    results.append(transaction)
        return results

    def filter_by_date(self, date) -> list[Transaction]:
        return self._filter_rows("Time Stamp", date)

    def filter_by_name(self, name) -> list[Transaction]:
        return self._filter_rows("Name", name)

    def filter_by_type(self, record_type) -> list[Transaction]:
        return self._filter_rows("Type", record_type)