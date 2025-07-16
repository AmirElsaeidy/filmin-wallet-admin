import streamlit as st
import pandas as pd
import json
from google.oauth2 import service_account
import gspread

st.set_page_config(page_title="FILMIN Wallet Admin", layout="wide")

st.title("🎬 FILMIN Wallet Admin Panel")
st.markdown("إدارة التحويلات المالية وتأكيد الرصيد للمستخدمين")

# تحميل بيانات الاعتماد من secrets
info = json.loads(st.secrets["GOOGLE_SERVICE_ACCOUNT_JSON"])
credentials = service_account.Credentials.from_service_account_info(
    info,
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)

# الاتصال بـ Google Sheets
gc = gspread.authorize(credentials)
spreadsheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/1o0jvsh426BUqjln1wvEXlwbZVDoRfNWvPIgg8-mEfr0/edit#gid=0")
worksheet = spreadsheet.sheet1

# جلب البيانات
data = worksheet.get_all_records()
df = pd.DataFrame(data)

# عرض آخر 3 تحويلات فقط للمستخدم
st.subheader("🧾 آخر 3 تحويلات ظاهرة للمستخدم")
if len(df) > 0:
    st.dataframe(df.tail(3), use_container_width=True)
else:
    st.info("لا توجد تحويلات بعد.")

# إدخال اسم المستخدم أو رقم العملية لتأكيد التحويل
st.subheader("✅ تأكيد التحويل اليدوي")

with st.form("confirm_form"):
    email = st.text_input("البريد الإلكتروني أو اسم المستخدم:")
    amount = st.number_input("المبلغ المراد إضافته", min_value=1)
    submit = st.form_submit_button("تأكيد الإضافة")

    if submit:
        worksheet.append_row([email, amount, "تمت الإضافة من الأدمن"])
        st.success(f"تمت إضافة {amount} جنيهًا لحساب {email} ✅")

# ملاحظة إدارية
with st.expander("📌 ملاحظة"):
    st.info("سيتم مراجعة جميع التحويلات المرسلة خلال اليوم وإضافتها بعد الساعة 12:00 صباحاً يوميًا.")
