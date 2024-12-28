import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# Constants for Google Sheets connection
SHEET_URL = 'https://docs.google.com/spreadsheets/d/1PJ0F1NP9RVR3a3nB6O1sZO_4WlBrexRPRw33C7AjW8E/edit?gid=0#gid=0'
TAB_NAME = 'Database'
JSON_FILE_PATH = 'clever-bee-442514-j7-23cb031a9b05.json'  # Update to your new JSON file path

# Create a connection to Google Sheets
def create_gsheets_connection():
    try:
        credentials = Credentials.from_service_account_file(JSON_FILE_PATH)
        client = gspread.authorize(credentials)
        return client.open_by_url(SHEET_URL).worksheet(TAB_NAME)
    except Exception as e:
        st.error(f"Error connecting to Google Sheets: {e}")
        return None

# Insert data into Google Sheets
def insert_data(requester_name, purpose, amount_requested):
    sheet = create_gsheets_connection()
    if sheet:
        try:
            # Get the current number of entries in the sheet to calculate Reference ID
            current_rows = len(sheet.get_all_values())
            reference_id = current_rows  # or however you want to generate the Reference ID
            # Insert data into the next row
            sheet.append_row([reference_id, "", requester_name, purpose, amount_requested])  # Update as needed for submission date
            st.success("Request submitted successfully!")
        except Exception as e:
            st.error(f"Error inserting data: {e}")

# Streamlit app layout
def main():
    st.title("E-Operation Request System")

    menu = ["Submit Request", "View Requests"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Submit Request":
        st.subheader("Submit a New Request")
        requester_name = st.text_input("Requester Name")
        purpose = st.text_area("Purpose of Request")
        amount_requested = st.number_input("Amount Requested", min_value=0.0, step=0.01)

        if st.button("Submit"):
            if requester_name and purpose and amount_requested > 0:
                insert_data(requester_name, purpose, amount_requested)
            else:
                st.warning("Please fill out all fields correctly.")

    elif choice == "View Requests":
        st.subheader("All Submitted Requests")
        # To implement: code to retrieve and display requests from Google Sheets
        st.info("Viewing requests feature is not yet implemented.")

if __name__ == "__main__":
    main()
