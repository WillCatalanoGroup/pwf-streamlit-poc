import streamlit as st
from core.auth import require_password
from core.nav import require_user_id_or_redirect

require_password()
require_user_id_or_redirect()

st.title("Power Traits")
st.write("This page will be built next. For now, use Back to return to Onboarding.")

left, right = st.columns([1, 1])
with left:
    back = st.button("Back", use_container_width=True)
with right:
    st.button("Next", disabled=True, use_container_width=True)

if back:
    st.switch_page("pages/1_Onboarding.py")
