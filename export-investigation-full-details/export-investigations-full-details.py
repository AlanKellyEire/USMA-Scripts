from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import requests
import json
import time
import re

from credentials import username, password, usma_subdomain

# ============================================================
# CONFIGURATION
# ============================================================

LOGIN_URL = f"https://{usma_subdomain}.alienvault.cloud/#/idp/login"
INVESTIGATIONS_UI_URL = f"https://{usma_subdomain}.alienvault.cloud/#/investigations"

OUTPUT_FILE = "investigations_full.json"

# ============================================================
# CHROME SETUP (VISIBLE + NETWORK LOGGING)
# ============================================================

options = Options()
options.binary_location = "/usr/bin/google-chrome"

options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

# Capture XHR/fetch network traffic
options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 30)

# ============================================================
# LOGIN
# ============================================================

print("🔐 Logging into USMA...")
driver.get(LOGIN_URL)

wait.until(EC.presence_of_element_located((By.ID, "username-input")))
driver.find_element(By.ID, "username-input").send_keys(username)
driver.find_element(By.ID, "password-input").send_keys(password)
driver.find_element(By.ID, "idp-btn-login-button").click()

wait.until(EC.presence_of_element_located((By.ID, "menu-btn-overview")))
print("✅ Login successful")

# ============================================================
# NAVIGATE TO INVESTIGATIONS + EXTRACT REGION, TENANT ID & TOKEN
# FROM NETWORK LOGS
# ============================================================

print("🌍 Detecting region, tenant ID and bearer token from network traffic...")
driver.get(INVESTIGATIONS_UI_URL)

# Give the UI time to issue API requests
time.sleep(8)

logs = driver.get_log("performance")

usma_region = None
usma_tenant_id = None
bearer_token = None

for entry in logs:
    try:
        msg = json.loads(entry["message"])["message"]

        if msg.get("method") == "Network.requestWillBeSent":
            req = msg["params"]["request"]
            url = req.get("url", "")
            headers = req.get("headers", {})

            # Extract region from URL
            if not usma_region:
                match = re.search(
                    r"https://investigations\.([a-z0-9-]+)\.prod\.alienvault\.cloud",
                    url
                )
                if match:
                    usma_region = match.group(1)

            # Normalise header keys to lowercase for reliable lookup
            headers_lower = {k.lower(): v for k, v in headers.items()}

            if not usma_tenant_id and "x-usm-tenantid" in headers_lower:
                raw_tenant = headers_lower["x-usm-tenantid"]
                tenant_match = re.search(r"([a-f0-9-]{36})", raw_tenant)
                if tenant_match:
                    usma_tenant_id = tenant_match.group(1)

            if not bearer_token and "authorization" in headers_lower:
                auth = headers_lower["authorization"]
                if auth.lower().startswith("bearer "):
                    bearer_token = auth  # full "Bearer <token>" string

    except Exception:
        pass

    if usma_region and usma_tenant_id and bearer_token:
        break

if not usma_region:
    driver.quit()
    raise RuntimeError("❌ Failed to detect USMA region from network traffic")

if not usma_tenant_id:
    driver.quit()
    raise RuntimeError("❌ Failed to detect USMA tenant ID from network traffic")

if not bearer_token:
    driver.quit()
    raise RuntimeError("❌ Failed to detect bearer token from network traffic")

print(f"✅ Detected region:    {usma_region}")
print(f"✅ Detected tenant ID: {usma_tenant_id}")
print(f"✅ Detected token:     {bearer_token[:30]}...")

driver.quit()

# ============================================================
# SET UP REQUESTS SESSION WITH CORRECT HEADERS
# ============================================================

session = requests.Session()

session.headers.update({
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "authorization": bearer_token,
    "content-type": "application/json",
    "origin": f"https://{usma_subdomain}.alienvault.cloud",
    "referer": f"https://{usma_subdomain}.alienvault.cloud/",
    "x-usm-tenantid": f"/usma:{usma_tenant_id}",
})

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def fetch_json(url):
    """GET a URL and return parsed JSON."""
    r = session.get(url, timeout=30)
    r.raise_for_status()
    return r.json()


def clean_links(obj):
    """
    Recursively remove _links and _embedded keys from an object
    EXCEPT on attachment items where we want to keep the file href.
    """
    if isinstance(obj, dict):
        return {
            k: clean_links(v)
            for k, v in obj.items()
            if k not in ("_links", "_embedded")
        }
    elif isinstance(obj, list):
        return [clean_links(item) for item in obj]
    return obj


def extract_attachments(attachment_response):
    """
    For attachments we keep the file download href on each item
    but strip all other _links/_embedded noise.
    Returns a list of attachment objects, each with a 'downloadHref' field.
    """
    items = attachment_response.get("attachments", [])
    result = []
    for item in items:
        cleaned = {k: v for k, v in item.items() if k not in ("_links", "_embedded")}
        # Preserve the file download link as a plain field
        href = item.get("_links", {}).get("self", {}).get("href")
        if href:
            cleaned["downloadHref"] = href
        result.append(cleaned)
    return result

# ============================================================
# INVESTIGATIONS SEARCH (PAGINATED POST)
# ============================================================

INVESTIGATIONS_SEARCH_URL = (
    f"https://investigations.{usma_region}.prod.alienvault.cloud/"
    f"investigations/v3/investigations/search"
)

print("🔍 Fetching all investigations (paginated)...")

all_investigations = []
per_page = 100
page = 1  # 1-indexed

while True:
    payload = {
        "perPage": per_page,
        "page": page,
        "sort": "created.on,desc",
        "q": f"deployment=='{usma_subdomain}'"
    }

    resp = session.post(
        INVESTIGATIONS_SEARCH_URL,
        json=payload,
        timeout=30
    )

    print(f"  HTTP status: {resp.status_code} (page={page})")

    if not resp.ok:
        print(f"  ❌ Error body: {resp.text}")
        resp.raise_for_status()

    data = resp.json()
    batch = data.get("investigations", [])

    if not batch:
        break

    all_investigations.extend(batch)
    print(f"  Fetched {len(batch)} investigations, total so far: {len(all_investigations)}")

    if len(batch) < per_page:
        break

    page += 1
    time.sleep(0.2)

print(f"📄 Found {len(all_investigations)} investigations total")

# ============================================================
# EXPAND EACH INVESTIGATION (FOLLOW ALL LINKS, INLINE OBJECTS)
# ============================================================

expanded_investigations = []

for inv in all_investigations:
    inv_id = inv.get("id")
    print(f"📌 Expanding investigation {inv_id} — {inv.get('title', 'Untitled')}")

    # Start with base fields only — strip _links and _embedded from root
    expanded = {
        k: v for k, v in inv.items()
        if k not in ("_links", "_embedded")
    }

    # ── notes ──────────────────────────────────────────────
    notes_href = inv.get("_links", {}).get("notes", {}).get("href")
    if notes_href:
        try:
            raw = fetch_json(notes_href)
            # Inline the notes array directly, strip internal _links
            expanded["notes"] = clean_links(raw.get("notes", []))
        except Exception as e:
            expanded["notes"] = {"error": str(e)}
        time.sleep(0.1)

    # ── evidence ───────────────────────────────────────────
    evidence_href = inv.get("_links", {}).get("evidence", {}).get("href")
    if evidence_href:
        try:
            raw = fetch_json(evidence_href)
            expanded["evidence"] = clean_links(raw.get("evidence", []))
        except Exception as e:
            expanded["evidence"] = {"error": str(e)}
        time.sleep(0.1)

    # ── attachments ────────────────────────────────────────
    # Special case: keep the file download href on each attachment item
    attachments_href = inv.get("_links", {}).get("attachments", {}).get("href")
    if attachments_href:
        try:
            raw = fetch_json(attachments_href)
            expanded["attachments"] = extract_attachments(raw)
        except Exception as e:
            expanded["attachments"] = {"error": str(e)}
        time.sleep(0.1)

    # ── history ────────────────────────────────────────────
    history_href = inv.get("_links", {}).get("history", {}).get("href")
    if history_href:
        try:
            raw = fetch_json(history_href)
            expanded["history"] = clean_links(raw.get("history", []))
        except Exception as e:
            expanded["history"] = {"error": str(e)}
        time.sleep(0.1)

    expanded_investigations.append(expanded)

# ============================================================
# OUTPUT
# ============================================================

with open(OUTPUT_FILE, "w") as f:
    json.dump(expanded_investigations, f, indent=2)

print(f"💾 Saved {len(expanded_investigations)} investigations to {OUTPUT_FILE}")
print("✅ Complete")
