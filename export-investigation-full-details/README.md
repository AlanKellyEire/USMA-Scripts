# USM Anywhere Investigation Exporter

A Python script that logs into a USM Anywhere (USMA) instance using Selenium,
automatically detects the investigations API region and authentication tokens
from browser network traffic, and exports all investigations — including their
full notes, evidence, attachments, and history — as a single JSON file.

---

## How It Works

1. Launches Chrome via Selenium and logs into your USMA instance.
2. Navigates to the Investigations UI and captures Chrome network logs to
   automatically detect:
   - The API region (e.g. eu-west-1)
   - The tenant ID required by the x-usm-tenantid header
   - The Bearer token used for API authentication
3. Transfers these credentials into a requests session and closes the browser.
4. Paginates through all investigations via the Investigations v3 API.
5. For each investigation, fetches and inlines the full content of:
   - notes       - inline array of note objects
   - evidence    - inline array of evidence objects
   - attachments - inline array, each item includes a downloadHref for the file
   - history     - inline array of audit/history events
6. Writes one JSON object per investigation to investigations_full.json.

---

## Project Structure

    usma-exporter/
    ├── usma-login-selenium3.py   # Main script
    ├── credentials.py            # Your USMA credentials (never commit this)
    ├── requirements.txt          # Python dependencies
    ├── .gitignore                # Prevents credentials/output leaking to git
    └── README.md                 # This file

---

## Requirements

### System

- Python 3.8+
- Google Chrome installed on your system
  - Linux default: /usr/bin/google-chrome
  - macOS default: /Applications/Google Chrome.app/Contents/MacOS/Google Chrome
  - Update options.binary_location in the script if your path differs
- ChromeDriver installed and on your PATH
  - Must match your installed Chrome version
  - Or use chromedriver-autoinstaller (included in requirements.txt) to handle
    this automatically

### Python Packages

    pip install -r requirements.txt

---

## Setup

### 1. Clone or copy the project files into a directory of your choice

    git clone <repo-url> usma-exporter
    cd usma-exporter

### 2. Create and activate a Python virtual environment

    python3 -m venv venv
    source venv/bin/activate          # Linux / macOS
    venv\Scripts\activate           # Windows

### 3. Install dependencies

    pip install -r requirements.txt

### 4. Fill in your credentials

Edit credentials.py with your USMA login details:

    username       = "your.email@example.com"
    password       = "yourpassword"
    usma_subdomain = "your-instance-name"   # e.g. my-company (without .alienvault.cloud)

Never commit credentials.py to version control. It is already excluded in .gitignore.

### 5. Verify ChromeDriver matches your Chrome version

    google-chrome --version    # Linux
    chromedriver --version

Both major version numbers must match. If they do not, chromedriver-autoinstaller
will handle this automatically at runtime when installed via requirements.txt.

### 6. Update the Chrome binary path if needed

Open usma-login-selenium3.py and find this line near the top:

    options.binary_location = "/usr/bin/google-chrome"

Update it to match your system if Chrome is installed elsewhere.

---

## Usage

    source venv/bin/activate
    python3 usma-login-selenium3.py

### Example Output

    Logging into USMA...
    Login successful
    Detecting region, tenant ID and bearer token from network traffic...
    Detected region:    eu-west-1
    Detected tenant ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    Detected token:     Bearer xxxxxxxxxxxxxx...
    Fetching all investigations (paginated)...
      HTTP status: 200 (page=1)
      Fetched 20 investigations, total so far: 20
    Found 20 investigations total
    Expanding investigation xxxxxxxx-... - My Investigation
    ...
    Saved 20 investigations to investigations_full.json
    Complete

---

## Output Format

investigations_full.json contains a JSON array. Each element is one investigation
with all sub-resources fully inlined. _links and _embedded are stripped from all
objects. Attachment items retain a downloadHref field pointing to the actual file.

Example structure:

    [
      {
        "title": "My Investigation",
        "description": "...",
        "deployment": "my-instance.alienvault.cloud",
        "status": "Open",
        "severity": "Critical",
        "intent": "Reconnaissance and Probing",
        "assignedTo": "user@example.com",
        "threatIndicator": "Undetermined",
        "sequenceId": 1,
        "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
        "tenant": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
        "lastModified": { "by": "...", "on": "2026-01-27T08:52:18Z" },
        "created":      { "by": "...", "on": "2026-01-27T08:52:18Z" },
        "notes": [],
        "evidence": [],
        "attachments": [
          {
            "id": "...",
            "filename": "screenshot.png",
            "downloadHref": "https://investigations.<region>.prod.alienvault.cloud/..."
          }
        ],
        "history": [
          {
            "id": "...",
            "modified": { "by": "...", "on": "..." },
            "target": { "type": "investigation", "id": "..." },
            "action": "Created"
          }
        ]
      }
    ]

---

## Optional: Filter by Status

By default the script exports all investigations for the deployment regardless
of status. To restrict to only Open and In Review (matching the UI default),
update the q value in the search payload section of the script:

    "q": f"deployment=='{usma_subdomain}';(status=='Open',status=='In Review')"

---

## Optional: Timestamped Output Files

To keep a snapshot per run rather than overwriting the output file each time,
change the OUTPUT_FILE line near the top of the script:

    from datetime import datetime
    OUTPUT_FILE = f"investigations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

---

## Scheduling

### Linux / macOS (cron)

To run the export daily at 06:00, open your crontab:

    crontab -e

Add the following line, updating the paths to match your installation:

    0 6 * * * /path/to/venv/bin/python3 /path/to/usma-exporter/usma-login-selenium3.py >> /path/to/usma-export.log 2>&1

The script logs in fresh on every run so the bearer token is always current.

### Windows (Task Scheduler)

1. Open Task Scheduler and create a new Basic Task.
2. Set the trigger to Daily at your preferred time.
3. Set the action to:
   - Program: C:\path\to\venv\Scripts\python.exe
   - Arguments: C:\path\to\usma-exporter\usma-login-selenium3.py

---

## Troubleshooting

| Error                           | Likely cause                            | Fix                                                    |
|---------------------------------|-----------------------------------------|--------------------------------------------------------|
| Failed to detect USMA region    | Page did not load in time               | Increase time.sleep(8) to 12 or higher                 |
| Failed to detect bearer token   | Chrome logging not capturing API calls  | Ensure goog:loggingPrefs capability is set             |
| 400 Bad Request                 | Wrong payload or FIQL syntax error      | Check the q string in the search payload               |
| 401 Unauthorized                | Bearer token expired mid-run            | Re-run the script to get a fresh token                 |
| ChromeDriver version mismatch   | Chrome updated but ChromeDriver did not | Run: pip install --upgrade chromedriver-autoinstaller  |
| Login fails / element not found | USMA UI changed element IDs             | Inspect login page and update By.ID selectors          |
| Chrome binary not found         | Wrong path in options.binary_location   | Update the path in the script to match your system     |

---

## Security Notes

- credentials.py contains plaintext credentials. Restrict file permissions:

    chmod 600 credentials.py        # Linux / macOS

- investigations_full.json may contain sensitive security incident data.
  Do not store in public, shared, or unencrypted locations.
- The Bearer token is held in memory only during the session and is never
  written to disk by the script.
- If storing this project in a Git repository, ensure it is private and
  confirm that credentials.py and investigations_full.json are listed in
  .gitignore before your first commit.
