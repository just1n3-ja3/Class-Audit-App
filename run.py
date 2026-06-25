from google.oauth2.service_account import Credentials
import gspread
import os
from dotenv import load_dotenv

load_dotenv()

creds = Credentials.from_service_account_file(
    os.getenv("GOOGLE_CREDS"),
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
)


client = gspread.authorize(creds)

sheet = client.open(os.getenv("SHEET_NAME","Class Funds 26-27")).sheet1

sheet.append_row([
    "2026-06-25",
    "Collection",
    500
])

print("Success")