import os
import pandas as pd
from filelock import FileLock

# File paths for the database and lock file
DATABASE_FILE = "database.csv"
LOCK_FILE = DATABASE_FILE + ".lock"

def initialize_database():
    """
    Initialize the database with required columns if it does not exist.
    """
    if not os.path.exists(DATABASE_FILE):
        columns = [
            "Reference ID",
            "Request Submission Date",
            "Requester Name",
            "Request Purpose",
            "Amount Requested",
            "Status",  # Approval status (Pending, Approved, Declined)
            "Finance Status",  # Finance status (Pending, Issued)
            "Issue Date",  # Date when money was issued
            "Liquidated",  # Amount spent (liquidated)
            "Returned",  # Amount returned (remaining)
            "Liquidated Invoices"  # Attached invoices (file paths or links)
        ]
        pd.DataFrame(columns=columns).to_csv(DATABASE_FILE, index=False)

def read_data():
    """
    Read the database as a Pandas DataFrame.
    """
    if os.path.exists(DATABASE_FILE):
        return pd.read_csv(DATABASE_FILE)
    else:
        initialize_database()
        return pd.DataFrame(columns=[
            "Reference ID",
            "Request Submission Date",
            "Requester Name",
            "Request Purpose",
            "Amount Requested",
            "Status",
            "Finance Status",
            "Issue Date",
            "Liquidated",
            "Returned",
            "Liquidated Invoices"
        ])

def write_data(existing_data, new_request=None):
    """
    Save the database. If a new_request is provided, it appends it to the data.
    Otherwise, overwrites the database with the existing_data.
    """
    with FileLock(LOCK_FILE):
        if new_request is not None:
            # Append the new request to the existing data
            new_data = pd.DataFrame([new_request])
            updated_data = pd.concat([existing_data, new_data], ignore_index=True)
            updated_data.to_csv(DATABASE_FILE, index=False)
        else:
            # Overwrite the entire data with existing_data
            existing_data.to_csv(DATABASE_FILE, index=False)

def get_next_reference_id(data):
    """
    Generate the next unique reference ID based on the existing data.
    """
    if data.empty:
        return "REQ-001"
    else:
        max_id = data["Reference ID"].str.split("-").str[1].astype(int).max()
        return f"REQ-{max_id + 1:03}"

def update_request_status(reference_id, status):
    """
    Update the status of a specific request in the database.
    """
    data = read_data()
    if reference_id in data["Reference ID"].values:
        data.loc[data["Reference ID"] == reference_id, "Status"] = status
        write_data(data)
        return True
    return False

def update_finance_status(reference_id, finance_status, issue_date=None):
    """
    Update the finance status and issue date for a specific request.
    """
    data = read_data()
    if reference_id in data["Reference ID"].values:
        data.loc[data["Reference ID"] == reference_id, ["Finance Status", "Issue Date"]] = [finance_status, issue_date]
        write_data(data)
        return True
    return False

def update_liquidation_details(reference_id, liquidated, returned, invoices):
    """
    Update the liquidation details for a specific request.
    """
    data = read_data()
    if reference_id in data["Reference ID"].values:
        data.loc[data["Reference ID"] == reference_id, ["Liquidated", "Returned", "Liquidated Invoices"]] = [
            liquidated, returned, invoices
        ]
        write_data(data)
        return True
    return False

def edit_request(reference_id, updated_request):
    """
    Edit the details of a specific request in the database.
    """
    data = read_data()
    if reference_id in data["Reference ID"].values:
        for key, value in updated_request.items():
            if key in data.columns:
                data.loc[data["Reference ID"] == reference_id, key] = value
        write_data(data)
        return True
    return False
