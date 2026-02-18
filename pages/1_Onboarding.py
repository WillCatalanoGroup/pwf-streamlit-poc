import streamlit as st
import yaml
from core.storage import load_user, save_user

st.title("Onboarding")

user_id = st.text_input("User ID", value="demo_user")
user = load_user(user_id)

traits = yaml.safe_load(open("data/pwf_traits.yml", "r", encoding="utf-8"))

power_labels = {t["label"]: t["id"] for t in traits["powers"]}
watch_labels = {t["label"]: t["id"] for t in traits["watches"]}
fuel_labels  = {t["label"]: t["id"] for t in traits["fuels"]}

st.subheader("Pick your top 1 in each (PoC)")
power = st.selectbox("Power 💪", list(power_labels.keys()))
watch = st.selectbox("Watch 👀", list(watch_labels.keys()))
fuel  = st.selectbox("Fuel 🔥", list(fuel_labels.keys()))

if st.button("Save profile"):
    user["profile"] = {
        "power_id": power_labels[power],
        "watch_id": watch_labels[watch],
        "fuel_id": fuel_labels[fuel],
    }
    save_user(user)
    st.success("Saved. Go to Daily.")
