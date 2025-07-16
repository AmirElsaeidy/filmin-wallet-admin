import streamlit as st
import pandas as pd
import json
import gspread
from google.oauth2 import service_account

st.set_page_config(page_title="FILMIN Wallet", layout="centered")

st.title("🎬 FILMIN Wallet - Admin Panel")

st.info("عرض أحدث التحويلات المالية - للاستخدام الإداري فقط.")

# Load service account info
info = json.loads(st.secrets["GOOGLE_SERVICE_ACCOUNT_JSON"])
    credentials = service_account.Credentials.from_service_account_info(info, scopes=["https://www.googleapis.com/auth/spreadsheets"])

# Connect to Google Sheet
gc = gspread.authorize(credentials)
spreadsheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/1o0jvsh426BUqjln1wvEXlwbZVDoRfNWvPIgg8-mEfr0/edit")
worksheet = spreadsheet.sheet1

# Fetch data
data = worksheet.get_all_records()
df = pd.DataFrame(data)

# Show only last 3 transactions for this demo
st.subheader("📄 آخر 3 تحويلات")
st.dataframe(df.tail(3))

# Admin-only section (can be hidden later)
with st.expander("📊 كل المعاملات"):
    st.dataframe(df)
