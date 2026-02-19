import streamlit as st
from core.auth import require_password
from core.nav import set_user_id, init_user_if_missing

require_password()

st.title("Onboarding")
st.write("Enter your User ID")

user_id = st.text_input("User ID", value=st.session_state.get("user_id", "")).strip()

# Place Next button aligned to the right, below the input field
left, right = st.columns([6, 1])
with right:
    next_clicked = st.button("Next", disabled=(user_id == ""), use_container_width=True)

if next_clicked:
    set_user_id(user_id)
    init_user_if_missing(user_id)
    st.switch_page("pages/2_Power.py")
