import streamlit as st
import pandas as pd
from datetime import date
from core.storage import load_user, save_user
from core.rules_engine import generate_card

st.title("Daily")

user_id = st.text_input("User ID", value="demo_user")
user = load_user(user_id)

if not user.get("profile"):
    st.warning("No profile yet. Go to Onboarding.")
    st.stop()

tax = pd.read_csv("data/taxonomy.csv")

def build_path(row) -> str:
    parts = [row["category"], row["subcategory"]]
    subsub = str(row.get("subsubcategory") or "").strip()
    if subsub and subsub.lower() != "nan":
        parts.append(subsub)
    return " > ".join(parts)

tax["priority_path"] = tax.apply(build_path, axis=1)
paths = tax["priority_path"].unique().tolist()

stakes = st.selectbox("Stakes", ["low", "normal", "high"])

st.subheader("Pick up to 3 priorities")
picks = []
for i in range(1, 4):
    pick = st.selectbox(f"Priority {i}", ["(none)"] + paths, index=0, key=f"p{i}")
    if pick != "(none)":
        picks.append(pick)

if st.button("Generate Today Cards"):
    cards = []
    for p in picks:
        cards.append(generate_card(p, stakes, user["profile"]))

    st.divider()
    for c in cards:
        st.markdown(f"### {c['priority_path']}")
        st.write(c["blocks"]["power"])
        st.write(c["blocks"]["watch"])
        st.write(c["blocks"]["fuel"])

    user["history"].append({"date": str(date.today()), "stakes": stakes, "cards": cards})
    save_user(user)
    st.success("Saved to history.")
