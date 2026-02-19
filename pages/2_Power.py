import json
from pathlib import Path
import streamlit as st

from core.auth import require_password
from core.nav import get_user_id, require_user_id_or_redirect, user_path

require_password()
require_user_id_or_redirect()

st.title("Power Traits")
st.write(
    "Select your top Power traits from the lists below. "
    "We recommend choosing the ones with asterisks, but you can choose whichever you like."
)

# Placeholder options (temporary labels)
POWER_OPTIONS = [
    "*Trait 1.01",
    "*Trait 1.02",
    "Trait 1.03",
    "Trait 1.04",
    "Trait 1.05",
    "Trait 1.06",
    "Trait 1.07",
]

uid = get_user_id()
p = user_path(uid)

doc = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {"user_id": uid, "profile": {}, "history": []}
profile = doc.get("profile", {})

# Store placeholder selections under new keys; keep legacy key for compatibility
current_1 = profile.get("power_trait_1", POWER_OPTIONS[0])
current_2 = profile.get("power_trait_2", POWER_OPTIONS[1])

power_1 = st.selectbox("Power Trait 1", POWER_OPTIONS, index=POWER_OPTIONS.index(current_1) if current_1 in POWER_OPTIONS else 0)
power_2 = st.selectbox("Power Trait 2", POWER_OPTIONS, index=POWER_OPTIONS.index(current_2) if current_2 in POWER_OPTIONS else 1)

valid = (power_1 != power_2)

# Buttons: Back (left), Next (right)
left, right = st.columns([1, 1])

with left:
    back_clicked = st.button("Back", use_container_width=True)

with right:
    next_clicked = st.button("Next", disabled=not valid, use_container_width=True)

if back_clicked:
    st.switch_page("pages/1_Onboarding.py")

# Persist selections on Next
if next_clicked:
    profile["power_trait_1"] = power_1
    profile["power_trait_2"] = power_2

    # Backward-compatible: set a legacy single value used by current rules engine
    profile["power_id"] = power_1

    doc["profile"] = profile
    p.write_text(json.dumps(doc, indent=2), encoding="utf-8")

    st.switch_page("pages/3_Watch.py")
