import streamlit as st
import pandas as pd
from datetime import date
from core.auth import require_password
from core.storage import load_user, save_user
from core.rules_engine import generate_card

require_password()

st.title("Daily")

user_id = st.text_input("User ID", value="demo_user")
user = load_user(user_id)

if not user.get("profile"):
    st.warning("No profile yet. Go to Onboarding.")
    st.stop()

tax = pd.read_csv("data/taxonomy.csv").fillna("")

def normalize(s: str) -> str:
    return str(s).strip()

tax["category"] = tax["category"].apply(normalize)
tax["subcategory"] = tax["subcategory"].apply(normalize)
tax["subsubcategory"] = tax["subsubcategory"].apply(normalize)

stakes = st.selectbox("Stakes", ["low", "normal", "high"])

def pick_priority(idx: int):
    st.subheader(f"Priority {idx}")

    categories = sorted([c for c in tax["category"].unique().tolist() if c])
    cat = st.selectbox("Category", ["(none)"] + categories, index=0, key=f"cat_{idx}")
    if cat == "(none)":
        return None

    sub_df = tax[tax["category"] == cat]
    subcategories = sorted([s for s in sub_df["subcategory"].unique().tolist() if s])
    sub = st.selectbox("Subcategory", ["(none)"] + subcategories, index=0, key=f"sub_{idx}")
    if sub == "(none)":
        return None

    subsub_df = sub_df[sub_df["subcategory"] == sub]
    subsubs = sorted([s for s in subsub_df["subsubcategory"].unique().tolist() if s])

    if len(subsubs) > 0:
        subsub = st.selectbox("Detail (optional)", ["(none)"] + subsubs, index=0, key=f"subsub_{idx}")
        if subsub != "(none)":
            return f"{cat} > {sub} > {subsub}"
    return f"{cat} > {sub}"

picks = []
for i in [1, 2, 3]:
    choice = pick_priority(i)
    if choice:
        picks.append(choice)

if st.button("Generate Today Cards"):
    if not picks:
        st.warning("Pick at least one priority.")
        st.stop()

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
