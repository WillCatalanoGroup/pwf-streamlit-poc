import streamlit as st

def require_password() -> None:
    if st.session_state.get("auth_ok"):
        return

    st.title("Password required")

    try:
        app_pw = st.secrets["APP_PASSWORD"]
    except Exception:
        st.error("Missing APP_PASSWORD secret.")
        st.stop()

    entered = st.text_input("Password", type="password")

    if st.button("Enter"):
        if entered == app_pw:
            st.session_state["auth_ok"] = True
            st.rerun()
        else:
            st.error("Incorrect password.")
            st.stop()

    st.stop()
