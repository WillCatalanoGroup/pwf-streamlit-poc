import streamlit as st
from core.auth import require_password

st.set_page_config(page_title="PWF PoC", layout="centered")

require_password()

st.title("PWF Daily PoC")
st.write("Use the sidebar to go through Onboarding, Daily, and History.")
