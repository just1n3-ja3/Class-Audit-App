# Auditors Ground

A simple command-line app for tracking **Money In** / **Money Out** transactions, backed by a Google Sheet as the data store.

Any record you add, filter, or list is read from and written to a Google Sheet of your choice — so anyone can reuse this app for their own bookkeeping just by connecting their own Google API credentials. No database setup required.

---

## Features

- Add transaction records (name, type, amount, remarks)
- Filter records by date
- Filter records by name
- Filter records by type (Money In / Money Out)
- View all records
- Clean, aligned CLI output with a title banner

---

## Requirements

- Python 3.10+
- A Google account
- A Google Cloud project with the **Google Sheets API** and **Google Drive API** enabled

---

## Setup

### 1. Clone and install dependencies

```bash
git clone <your-repo-url>
cd Audit-Class-Funds
python3 -m venv .venv
source .venv/bin/activate    # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Create a Google Cloud project and service account

This app authenticates using a **service account** — a non-human Google account your app uses to access Sheets/Drive on your behalf.

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project (or select an existing one).
3. In the search bar, enable these two APIs:
   - **Google Sheets API**
   - **Google Drive API**
4. Go to **APIs & Services → Credentials**.
5. Click **Create Credentials → Service account**.
6. Give it any name (e.g. `auditors-ground-bot`) and click **Done**.
7. Click into the new service account → **Keys** tab → **Add Key → Create new key → JSON**.
8. A `.json` file will download — this is your credentials file. **Keep it private; never commit it to git.**

### 3. Create your Google Sheet

1. Create a new Google Sheet.
2. Add a header row with these exact column names (the app reads these as keys):

   | Time Stamp | Name | Type | Amount | Remarks |
   |---|---|---|---|---|

3. Share the sheet with your service account's email address (found inside the JSON file as `client_email`), giving it **Editor** access — otherwise the app can't read or write to it.

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GOOGLE_CREDS=/absolute/path/to/your-credentials-file.json
SHEET_NAME=Your Google Sheet Name
```

- `GOOGLE_CREDS` — absolute path to the JSON key file from step 2.
- `SHEET_NAME` — the exact name of the Google Sheet you created in step 3 (not the URL, the sheet's title).

### 5. Run the app

```bash
python3 run.py
```

You should see the title screen, followed by a menu to add or filter records.

---

## Project Structure

```
Audit-Class-Funds/
├── app/
│   ├── CLI/
│   │   └── menu.py            # Menu loop and title screen
│   ├── helpers/
│   │   └── helper.py          # Input parsing helpers (int/float/date)
│   ├── models/
│   │   └── transaction.py     # Transaction dataclass
│   ├── repositories/
│   │   └── sheets_repo.py     # Google Sheets read/write logic
│   └── services/
│       └── transac_service.py # Business logic / CLI prompts
├── run.py                     # Entry point
├── requirements.txt
└── .env                       # Your local config (not committed)
```

> Adjust this tree if your actual folder names differ — this reflects the structure used throughout development.

---

## Troubleshooting

**`Startup failed: GOOGLE_CREDS environment variable is not set`**
Your `.env` file is missing, misnamed, or not in the project root the app is run from.

**`Spreadsheet '...' not found, or service account lacks access to it`**
Either `SHEET_NAME` doesn't exactly match your sheet's title, or you forgot to share the sheet with the service account's `client_email`.

**`Invalid service account credentials file`**
The JSON key file is corrupted, edited, or `GOOGLE_CREDS` points to the wrong file.

**Import errors for `pyfiglet` or other packages**
Make sure your virtual environment is activated (`source .venv/bin/activate`) before running `pip install -r requirements.txt` or `python3 run.py`.

---

## Notes

- This app stores transaction timestamps as plain date strings (`YYYY-MM-DD`), not full datetimes.
- Remarks are optional when adding a record.
- All sheet reads/writes go through `gspread`, so normal Google Sheets quotas and rate limits apply.
