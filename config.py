# config.py
"""
Configuration file for Device Compliance & SDP Dispatch Tool.
Modify these settings to fit your organization's environment and rules.
"""

# ==========================================
# 1. ADMIN & USER PERMISSIONS
# ==========================================
# Authorised admin usernames/emails who can edit ticket templates on-the-fly
ADMIN_USERS = [
    "admin1@yourdomain.com",
    "admin2@yourdomain.com",
    "itsupport@yourdomain.com",
]

# ==========================================
# 2. REPORT FORMATTING & CSV HEADER OFFSETS
# ==========================================
# Number of metadata rows to skip at the top of raw CSV exports
UPDATES_SKIPROWS = 11
MCM_SKIPROWS = 3

# Column target positions (1-based index mapped to 'H1', 'H2', etc.)
# Windows Updates Report
UPDATES_PC_NAME_COL = "H1"       # Column A: Hostname
UPDATES_COUNT_COL = "H10"        # Column J: Missing Critical Updates

# MCM Last Scan Report
MCM_PC_NAME_COL = "H1"           # Column A: Hostname
MCM_SCAN_DAYS_COL = "H6"         # Column F: Days Since Last Scan

# ==========================================
# 3. COMPLIANCE THRESHOLDS
# ==========================================
MIN_MISSING_UPDATES = 1          # Minimum updates missing to flag a PC
MIN_INACTIVE_DAYS = 14           # Minimum inactive days to flag a PC

# ==========================================
# 4. DISPATCH WORKER CONFIGURATION
# ==========================================
MAX_WORKERS = 5                  # Concurrent API request threads for SDP

# ==========================================
# 5. DOMAIN & ASSET SEARCH
# ==========================================
DEFAULT_DOMAIN_SUFFIX = "yourdomain.com"

def get_search_candidates(base_pc: str) -> list:
    """Generates AD FQDN and hostname search targets for SDP asset lookup."""
    return [
        f"{base_pc.upper()}.{DEFAULT_DOMAIN_SUFFIX}",
        f"{base_pc.lower()}.{DEFAULT_DOMAIN_SUFFIX}",
        base_pc.upper(),
        base_pc.lower(),
    ]

# ==========================================
# 6. SITE MAPPING LOGIC
# ==========================================
def get_site_from_pc(pc_name: str) -> str:
    """Determines SDP Site name based on hostname prefix/naming rules."""
    pc_upper = str(pc_name).strip().upper()

    if pc_upper.startswith("NY"):
        return "New York HQ"
    elif pc_upper.startswith("LON"):
        return "London Office"
    elif pc_upper.startswith("SYD"):
        return "Sydney Office"
    else:
        return "All Sites"

# ==========================================
# 7. SERVICEDESK PLUS (SDP) PAYLOAD DEFAULTS
# ==========================================
SDP_REQUESTER_EMAIL = "itsupport@yourdomain.com"
SDP_CATEGORY = "Compliance Checks"
SDP_REQUEST_TYPE = "Support"
SDP_MODE = "Web form"
SDP_IMPACT = "Affects User"
SDP_URGENCY = "Medium"
SDP_PRIORITY = "Medium"

# ==========================================
# 8. DEFAULT TICKET TEMPLATES
# ==========================================
DEFAULT_TICKET_TEMPLATE = (
    "This is an automated notification regarding {PCName}.\n\n"
    "Compliance Findings:\n"
    "- Missing Critical Updates: {Updates}\n"
    "- Days since last check-in: {MCMScan}\n\n"
    "Please connect to the network as soon as possible to receive outstanding updates.\n\n"
    "SDP Asset Register Info:\n"
    "- Assigned Site: {Site}\n"
    "- Asset State: {AssetState}\n"
    "- Assigned User: {AssignedUser}"
)

def get_note_template(updates, mcm_scan, asset_state, assigned_user) -> str:
    """Generates the HTML-formatted note appended to existing SDP tickets."""
    updates_str = updates if updates != "" else "0"
    mcm_str = mcm_scan if mcm_scan != "" else "0"
    
    return (
        f"<b>Automated Compliance Check Update</b><br><br>"
        f"Compliance Findings:<br>"
        f"- Missing Critical Updates: {updates_str}<br>"
        f"- Days since last check-in: {mcm_str}<br><br>"
        f"SDP Asset Status: <b>{asset_state}</b> | Assigned User: <b>{assigned_user}</b>"
    )