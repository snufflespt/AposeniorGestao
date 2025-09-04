import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

def get_worksheet(sheet_name):
    """Liga ao Google Sheets e devolve a worksheet pedida."""
    creds_dict = st.secrets["google_service_account"]
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    client = gspread.authorize(creds)
    sheet = client.open("Base_IPSS").worksheet(sheet_name)
    return sheet

