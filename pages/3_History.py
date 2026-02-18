import streamlit as st
from core.auth import require_password
from core.storage import load_user

require_password()

st.title("History")

user_id = st.text_input("User ID", value="demo_user")
user = load_user(user_id)

hist = list(reversed(user.get("history", [])))
if not hist:
    st.info("No history yet.")
    st.stop()

for day in hist:
    day_date = day.get("date", "")
    stress = day.get("stress_now", "—")
    energy = day.get("energy_now", "—")

    # Backward compatibility:
    # - Older entries: may have day["stakes"] (single global), and no selections
    # - New entries: have selections with per-priority stakes
    old_stakes = day.get("stakes")  # may be missing
    selections = day.get("selections", [])

    if old_stakes:
        header = f"{day_date} (stakes: {old_stakes}, stress: {stress}, energy: {energy})"
    else:
        header = f"{day_date} (stress: {stress}, energy: {energy})"

    with st.expander(header):
        if selections:
            st.markdown("**Selections**")
            for s in selections:
                p = s.get("priority_path", "")
                stks = s.get("stakes", "—")
                st.write(f"- {p} (stakes: {stks})")
            st.divider()

        cards = day.get("cards", [])
        if not cards:
            st.info("No cards saved for this day.")
            continue

        for c in cards:
            st.markdown(f"**{c.get('priority_path','')}**")
            blocks = c.get("blocks", {})
            st.write(blocks.get("power", ""))
            st.write(blocks.get("watch", ""))
            st.write(blocks.get("fuel", ""))
            st.divider()
