import streamlit as st
from core.storage import load_user

st.title("History")

user_id = st.text_input("User ID", value="demo_user")
user = load_user(user_id)

hist = list(reversed(user.get("history", [])))
if not hist:
    st.info("No history yet.")
    st.stop()

for day in hist:
    with st.expander(f"{day['date']} (stakes: {day['stakes']})"):
        for c in day["cards"]:
            st.markdown(f"**{c['priority_path']}**")
            st.write(c["blocks"]["power"])
            st.write(c["blocks"]["watch"])
            st.write(c["blocks"]["fuel"])
            st.divider()
