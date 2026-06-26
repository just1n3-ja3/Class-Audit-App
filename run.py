import sys
from app.repositories.sheets_repo import SheetsAuthError

try:
    from app.CLI.menu import start
except SheetsAuthError as e:
    print(f"Startup failed: {e}")
    print("Check your .env file (GOOGLE_CREDS, SHEET_NAME) and credentials file.")
    sys.exit(1)


if __name__ == "__main__":
    try:
        start()
    except KeyboardInterrupt:
        print("\nInterrupted. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)