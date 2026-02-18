import csv
import pandas as pd

tax = pd.read_csv("data/taxonomy.csv").fillna("")

required_cols = ["category_id", "subcategory_id", "subsubcategory_id"]
for c in required_cols:
    if c not in tax.columns:
        raise SystemExit(f"Missing column in taxonomy.csv: {c}")

def make_key(row) -> str:
    cat = str(row["category_id"]).strip()
    sub = str(row["subcategory_id"]).strip()
    subsub = str(row.get("subsubcategory_id", "")).strip()
    return f"{cat} > {sub} > {subsub}" if subsub else f"{cat} > {sub}"

keys = sorted({
    make_key(r)
    for _, r in tax[required_cols].drop_duplicates().iterrows()
})

rows = []
for k in keys:
    rows.append({"priority_path": k, "stakes": "low", "template_id": "stakes_low", "weight": 10})
    rows.append({"priority_path": k, "stakes": "medium", "template_id": "stakes_medium", "weight": 10})
    rows.append({"priority_path": k, "stakes": "high", "template_id": "stakes_high", "weight": 10})

# Always keep a generic fallback row
rows.append({"priority_path": "any", "stakes": "any", "template_id": "generic_any_priority", "weight": 1})

df = pd.DataFrame(rows, columns=["priority_path", "stakes", "template_id", "weight"])
df.to_csv("data/rules.csv", index=False, quoting=csv.QUOTE_ALL)

print("taxonomy keys:", len(keys))
print("rules rows:", len(df))
print("expected rows:", len(keys) * 3 + 1)
