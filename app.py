import streamlit as st
from pages.welcome_page import welcome_page
from pages.request_form import request_form_page
from pages.database_page import database_page
from utils.database import initialize_database

def main():
    initialize_database()

    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Welcome", "Request Form", "Database"])

    # Load the selected page
    if page == "Welcome":
        welcome_page()
    elif page == "Request Form":
        request_form_page()
    elif page == "Database":
        database_page()

if __name__ == "__main__":
    main()
