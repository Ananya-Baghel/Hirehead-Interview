import json, uuid
from pathlib import Path
from typing import Dict

BASE = Path(__file__).resolve().parent.parent
DATA = json.loads((BASE/"data"/"negotiation_scenarios.json").read_text())

SESS: Dict[str, dict] = {}

def start(role: str, candidate_anchor: float, batna: str | None):
    scen = next((s for s in DATA["scenarios"] if s["role"].lower()==role.lower()), DATA["scenarios"][0])
    sid = str(uuid.uuid4())
    SESS[sid] = {
        "role": role,
        "budget_min": scen["budget_min"],
        "budget_max": scen["budget_max"],
        "company_anchor": scen["company_anchor"],
        "benefits": scen["benefits_anchor"],
        "candidate_anchor": candidate_anchor,
        "batna": batna or "not specified",
        "round": 0
    }
    msg = f"Our initial offer for {role} is {scen['company_anchor']} LPA with {', '.join(scen['benefits_anchor'])}."
    return sid, msg

def respond(session_id: str, candidate_message: str):
    s = SESS[session_id]
    s["round"] += 1

    # parse simple counters: look for numbers
    import re
    asks = re.findall(r"(\d+(?:\.\d+)?)", candidate_message)
    ask_val = float(asks[-1]) if asks else s["candidate_anchor"]

    # counter strategy: move 30% of distance up to budget_max; stop when near top
    last = s.get("last_offer", s["company_anchor"])
    target = min(s["budget_max"], last + 0.3*(ask_val - last))
    new_offer = round(max(s["budget_min"], target), 2)
    s["last_offer"] = new_offer

    # tweak benefits if salary capped
    add_benefit = None
    if new_offer >= s["budget_max"] - 0.1 and s["round"] >= 2:
        extra = "extra WFH day" if "extra WFH day" not in s["benefits"] else "conference budget 50k"
        s["benefits"].append(extra)
        add_benefit = extra

    reply = f"Thanks for sharing. We can propose {new_offer} LPA"
    if add_benefit:
        reply += f" plus {add_benefit}"
    reply += "."
    return {"offer": new_offer, "benefits": s["benefits"], "message": reply}
