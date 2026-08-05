# 💻 MCM & ServiceDesk Plus Compliance Automation Tool

A secure, high-performance Streamlit web application designed to merge, clean, and process device compliance reports, enabling IT Support teams to automatically log or update tickets in **ServiceDesk Plus (SDP)**. 

Built with **Python**, **Streamlit**, and concurrent batch processing (`ThreadPoolExecutor`), this tool speeds up ticket generation while maintaining real-time audit control and emergency stop capabilities.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.25%2B-red.svg)](https://streamlit.io/)

---

## ⚡ Key Features

* **Parallel Processing Engine:** Dispatches requests concurrently in batches of 5 (5x speedup compared to sequential API calls).
* **Automated Data Sanitisation:** Strips metadata header noise, normalises hostnames and matches records across report types.
* **Smart Ticket Handling:** Identifies existing open tickets to append notes rather than creating duplicate tickets.
* **Emergency Stop & Audit:** Instantly stops outgoing API requests and outputs an audit log of all actions taken prior to cancellation.
* **Stateless & Private:** Session data runs in memory and clears automatically when the tab is closed.

---

## 🖼️ Interface Preview

### 1. Upload & Merged Review
Upload raw CSV exports to correlate missing updates and MCM scan activity into a unified review table.

![Merged Results Table](images/mcm-automation_merged.png)

### 2. Concurrent Dispatch & Audit
Monitor real-time ticket creation with progress indicators and emergency stop protection.

![Dispatch System](images/mcm-automation_dispatch.png)

---

## 🚀 Quick Start & Local Setup

### Prerequisites
* **Python 3.9+** installed on your environment.
* Access to a **ServiceDesk Plus (SDP)** instance with API access enabled.
* An **Azure AD / SSO App Registration** (if enforcing organisational SSO).

### 1. Clone Repository
git clone https://github.com/your-org/mcm-sdp-compliance-tool.git
cd mcm-sdp-compliance-tool

### 2. Create Virtual Environment & Install Dependencies
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt

### 3. Configure Secrets
Modify your secrets manager in your Streamlit app settings:

# ServiceDesk Plus API Settings
SDP_BASE_URL = "https://your-sdp-instance.com/api/v3"
SDP_TECHNICIAN_KEY = "your-sdp-api-key-here"

# OAuth / Azure SSO Configuration (Optional)
CLIENT_ID = "your-azure-client-id"
CLIENT_SECRET = "your-azure-client-secret"
TENANT_ID = "your-azure-tenant-id"

![Secrets Manager Example](images/streamlit-secrets.png)

### 4. Run the Streamlit App
streamlit run app.py

---

## 🛠️ Personalising for Your Organisation

To adapt this tool for your organisation's specific environment, review and modify the following key areas in the code:

### 1. Adjusting Compliance Thresholds (`app.py`)
Update the default filtering logic to match your IT security policies:
MIN_MISSING_UPDATES = 1     # Minimum required missing critical updates to flag
MAX_MCM_INACTIVE_DAYS = 14  # Max allowed days since last check-in

### 2. CSV Header Skip Logic (`app.py`)
Depending on how your MCM / WSUS reporting tools export reports, adjust the header row offset:
WINDOWS_UPDATE_HEADER_OFFSET = 11  # Rows skipped for Slot 1
MCM_SCAN_HEADER_OFFSET = 3         # Rows skipped for Slot 2

### 3. SDP Ticket Template & Site Mapping (`app.py`)
Customise the JSON payload sent to ServiceDesk Plus to match your custom fields, ticket templates, or site categorisation:
payload = {
    "request": {
        "subject": f"Compliance Action Required: {hostname}",
        "description": f"Machine {hostname} is non-compliant...",
        "template": {"name": "Your Custom SDP Template"},
        "category": {"name": "IT Infrastructure"},
        # Add custom fields specific to your SDP setup here
    }
}

### 4. Parallel Worker Limits (`app.py`)
The application defaults to 5 concurrent threads to balance speed with SDP rate limits. You can adjust this based on your API server capacity:
MAX_WORKERS = 5

### 5. Computer Naming Conventions (`app.py`)
The tool relies on exact hostname matching across both CSV reports and your ServiceDesk Plus Asset Register. 
* By default, the parser cleans hostnames by converting them to **UPPERCASE** and stripping domain suffixes (e.g., `LAPTOP-01.domain.com` becomes `LAPTOP-01`).
* If your organization uses a specific naming prefix, suffix, or custom asset tagging scheme, update the regex/string sanitization functions in `app.py` to match how devices are identified in your SDP environment. 

---

## ⚙️ Logic Flow

[ Raw CSV 1: Windows Updates ] ──┐
                                 ├──> [ Normalise Hostnames & Filter ] ──> [ Parallel Dispatch (5 Workers) ] ──> [ ServiceDesk Plus API ]
[ Raw CSV 2: MCM Last Scan ] ───┘

1. **Upload & Parsing:** Raw CSVs drop into designated slots, automatically stripping metadata headers.
2. **Key Matching:** Normalises hostnames (uppercase, strips domain suffixes) to cross-reference data.
3. **Threshold Check:** Flags devices with 1 or more missing updates OR 14 or more days inactive.
4. **Execution:** Submits concurrent API payload requests to SDP to fetch open tickets or create new ones.

---

## 💬 Issues & Support

If you encounter a bug, have a feature request, or run into issues with report formatting:

1. **Check existing issues:** Search the [GitHub Issues](../../issues) tab to see if it has already been reported.
2. **Open a new issue:** Provide details about the expected vs. actual behavior, along with any relevant error logs (ensuring no sensitive data or credentials are included).
3. **Pull Requests:** Contributions are welcome! If you'd like to fix a bug or add a feature, feel free to fork the repo and submit a PR.

*Note: This is an open-source project maintained in my spare time, so responses may vary based on availability.*

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
