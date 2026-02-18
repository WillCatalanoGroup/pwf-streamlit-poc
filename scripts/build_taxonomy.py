import csv
import pandas as pd

spec = [
    ("meetings", "Meetings & Calls", [
        ("lead", "Lead (you own the agenda and outcomes)", "you own the agenda and outcomes"),
        ("contribute", "Contribute (you need to influence or add signal)", "you need to influence or add signal"),
        ("align", "Align (resolve confusion, get everyone on the same page)", "resolve confusion, get everyone on the same page"),
        ("decide", "Decide (turn options into a commitment)", "turn options into a commitment"),
        ("repair", "Repair (tension, conflict, or trust needs attention)", "tension, conflict, or trust needs attention"),
    ]),
    ("messages", "Messages (Email/Slack/Text)", [
        ("clear_inbox", "Clear the inbox (triage and respond fast)", "triage and respond fast"),
        ("crisp_update", "Write a crisp update (status, decision, next steps)", "status, decision, next steps"),
        ("ask_need", "Ask for what you need (request, unblock, confirm)", "request, unblock, confirm"),
        ("misunderstanding", "Resolve a misunderstanding (tone, intent, confusion)", "tone, intent, confusion"),
        ("logistics", "Coordinate logistics (times, handoffs, who owns what)", "times, handoffs, who owns what"),
    ]),
    ("focus", "Focus Work", [
        ("think", "Think it through (sense-making, strategy, problem framing)", "sense-making, strategy, problem framing"),
        ("build", "Build/create (make the thing: analysis, design, draft, model)", "make the thing: analysis, design, draft, model"),
        ("fix", "Fix/clean up (refactor, simplify, reduce mess)", "refactor, simplify, reduce mess"),
        ("learn", "Learn/research (read, synthesize, form a view)", "read, synthesize, form a view"),
        ("finish", "Finish (close loops, package, ship)", "close loops, package, ship"),
    ]),
    ("writing", "Writing & Docs", [
        ("draft", "Draft (first version, get it out)", "first version, get it out"),
        ("edit", "Edit (tighten, simplify, improve flow)", "tighten, simplify, improve flow"),
        ("clarify", "Clarify (turn fuzzy into clear: purpose, plan, instructions)", "turn fuzzy into clear: purpose, plan, instructions"),
        ("document", "Document (create a reference others can use)", "create a reference others can use"),
        ("send", "Send (publish/share with the right framing)", "publish/share with the right framing"),
    ]),
    ("decisions", "Decisions & Tradeoffs", [
        ("choose_dir", "Choose a direction (pick A vs B)", "pick A vs B"),
        ("prioritize", "Prioritize (what matters today, what waits)", "what matters today, what waits"),
        ("decision_rule", "Define the decision rule (what good means, how we'll decide)", "what good means, how we'll decide"),
        ("buy_in", "Get buy-in (alignment and commitment)", "alignment and commitment"),
        ("commit", "Commit and communicate (announce, assign, move)", "announce, assign, move"),
    ]),
    ("planning", "Planning & Priorities", [
        ("scope", "Scope the work (what is in/out)", "what is in/out"),
        ("sequence", "Sequence (what happens first/next/later)", "what happens first/next/later"),
        ("resource", "Resource (time, people, budget, tools)", "time, people, budget, tools"),
        ("milestones", "Set milestones (checkpoints and owners)", "checkpoints and owners"),
        ("risk", "Risk plan (what could go wrong and how we'll handle it)", "what could go wrong and how we'll handle it"),
    ]),
    ("quality", "Review & Quality", [
        ("review", "Review work (give feedback, approve or redirect)", "give feedback, approve or redirect"),
        ("qa", "QA/check details (accuracy, completeness, edge cases)", "accuracy, completeness, edge cases"),
        ("sanity", "Sanity check (does this make sense overall)", "does this make sense overall"),
        ("standard", "Protect the standard (quality bar, brand, compliance)", "quality bar, brand, compliance"),
        ("learn_results", "Learn from results (what worked, what didn't, adjust)", "what worked, what didn't, adjust"),
    ]),
    ("people", "People (Leading or Managing Others)", [
        ("checkin", "1:1 / check-in (support, clarity, alignment)", "support, clarity, alignment"),
        ("feedback", "Feedback (give, receive, or reset expectations)", "give, receive, or reset expectations"),
        ("delegate", "Delegate (hand off ownership clearly)", "hand off ownership clearly"),
        ("coach", "Coach (develop capability, unblock growth)", "develop capability, unblock growth"),
        ("hard_moment", "Handle a hard moment (conflict, performance, boundaries)", "conflict, performance, boundaries"),
    ]),
    ("client", "Customer/Client", [
        ("deliver", "Deliver value (do the work, move it forward)", "do the work, move it forward"),
        ("expectations", "Set expectations (scope, timeline, success criteria)", "scope, timeline, success criteria"),
        ("trust", "Build trust (credibility, responsiveness, clarity)", "credibility, responsiveness, clarity"),
        ("friction", "Handle friction (pushback, disappointment, change request)", "pushback, disappointment, change request"),
        ("expand", "Expand (identify next value, renew, upsell without being salesy)", "identify next value, renew, upsell without being salesy"),
    ]),
    ("admin", "Admin & Coordination", [
        ("schedule", "Schedule (meetings, travel, calendars)", "meetings, travel, calendars"),
        ("process", "Process tasks (expenses, forms, approvals)", "expenses, forms, approvals"),
        ("followup", "Track and follow up (waiting on, reminders, nudges)", "waiting on, reminders, nudges"),
        ("handoff", "Handoff (transfer work cleanly to someone else)", "transfer work cleanly to someone else"),
        ("reset", "Reset the system (clean up lists, files, workspace)", "clean up lists, files, workspace"),
    ]),
]

rows = []
for cat_id, cat_label, subs in spec:
    for sub_id, sub_label, desc in subs:
        rows.append({
            "category_id": cat_id,
            "category_label": cat_label,
            "subcategory_id": sub_id,
            "subcategory_label": sub_label,
            "subsubcategory_id": "",
            "subsubcategory_label": "",
            "description": desc,
        })

df = pd.DataFrame(rows, columns=[
    "category_id","category_label","subcategory_id","subcategory_label",
    "subsubcategory_id","subsubcategory_label","description"
])

# Quote all fields to avoid comma parsing issues forever
df.to_csv("data/taxonomy.csv", index=False, quoting=csv.QUOTE_ALL)
print("Wrote data/taxonomy.csv with", df.shape[0], "rows and", df.shape[1], "columns")
