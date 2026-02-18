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

def pick_priority(idx: int):
    st.subheader(f"Priority {idx}")

    cats = (
        tax[["category_id", "category_label"]]
        .drop_duplicates()
        .sort_values("category_label")
        .to_dict(orient="records")
    )
    cat_label_list = [c["category_label"] for c in cats]
    cat_label = st.selectbox("Category", ["(none)"] + cat_label_list, index=0, key=f"cat_{idx}")
    if cat_label == "(none)":
        return None

    cat_id = next(c["category_id"] for c in cats if c["category_label"] == cat_label)

    sub_df = tax[tax["category_id"] == cat_id][["subcategory_id", "subcategory_label"]].drop_duplicates()
    subs = sub_df.sort_values("subcategory_label").to_dict(orient="records")
    sub_label_list = [s["subcategory_label"] for s in subs]
    sub_label = st.selectbox("Subcategory", ["(none)"] + sub_label_list, index=0, key=f"sub_{idx}")
    if sub_label == "(none)":
        return None

    sub_id = next(s["subcategory_id"] for s in subs if s["subcategory_label"] == sub_label)

    subsub_df = tax[(tax["category_id"] == cat_id) & (tax["subcategory_id"] == sub_id)]
    subsubs = subsub_df[["subsubcategory_id", "subsubcategory_label"]].drop_duplicates()
    subsubs = subsubs[subsubs["subsubcategory_id"].astype(str).str.strip() != ""]

    subsub_id = ""
    subsub_label = ""
    if len(subsubs) > 0:
        subsubs = subsubs.sort_values("subsubcategory_label").to_dict(orient="records")
        subsub_label_list = [s["subsubcategory_label"] for s in subsubs]
        chosen = st.selectbox("Detail (optional)", ["(none)"] + subsub_label_list, index=0, key=f"subsub_{idx}")
        if chosen != "(none)":
            subsub_label = chosen
            subsub_id = next(s["subsubcategory_id"] for s in subsubs if s["subsubcategory_label"] == chosen)

    stakes = st.selectbox("Stakes for this priority", ["low", "medium", "high"], index=1, key=f"stakes_{idx}")

    if subsub_id:
        priority_key = f"{cat_id} > {sub_id} > {subsub_id}"
        priority_display = f"{cat_label} > {sub_label} > {subsub_label}"
    else:
        priority_key = f"{cat_id} > {sub_id}"
        priority_display = f"{cat_label} > {sub_label}"

    return {"priority_key": priority_key, "priority_display": priority_display, "stakes": stakes}

st.subheader("Right now")
stress = st.selectbox("Stress level right now", ["low", "medium", "high"], index=1, key="stress_now")
energy = st.selectbox("Energy level right now", ["low", "medium", "high"], index=1, key="energy_now")

selections = []
for i in [1, 2, 3]:
    sel = pick_priority(i)
    if sel:
        selections.append(sel)

if st.button("Generate Today Cards"):
    if not selections:
        st.warning("Pick at least one priority.")
        st.stop()

    cards = []
    for sel in selections:
        card = generate_card(sel["priority_key"], sel["stakes"], user["profile"])
        card["priority_display"] = sel["priority_display"]
        cards.append(card)

    st.divider()
    for c in cards:
        shown = c.get("priority_display") or c.get("priority_path")
        st.markdown(f"### {shown} (stakes: {c['stakes']})")
        st.write(c["blocks"]["power"])
        st.write(c["blocks"]["watch"])
        st.write(c["blocks"]["fuel"])

    user["history"].append({
        "date": str(date.today()),
        "stress_now": stress,
        "energy_now": energy,
        "selections": selections,
        "cards": cards,
    })
    save_user(user)
    st.success("Saved to history.")
