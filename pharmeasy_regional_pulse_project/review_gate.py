"""Human approval gate with append-only JSONL audit trail."""
from datetime import datetime, timezone
import json
import uuid

ALLOWED = {"approve","edit","reject"}

def review_gate_v1(report, decision, reviewer_note=""):
    if decision not in ALLOWED:
        raise ValueError(f"decision must be one of {sorted(ALLOWED)}")
    updated = dict(report)
    updated["review_decision"] = decision
    updated["reviewer_note"] = reviewer_note
    updated["external_use_allowed"] = decision == "approve"
    updated["reviewed_at"] = datetime.now(timezone.utc).isoformat()
    event = {"timestamp":updated["reviewed_at"],"run_id":str(uuid.uuid4()),"region":report.get("region","ALL"),"decision":decision,"reviewer_note":reviewer_note}
    with open("audit_log.jsonl","a",encoding="utf-8") as f:
        f.write(json.dumps(event,ensure_ascii=False)+"\n")
    return updated

def test_harness():
    try:
        open("audit_log.jsonl","w",encoding="utf-8").close()
    except OSError:
        pass
    report={"region":"Guntur","insight":"Example draft for review"}
    for decision, note in [("approve","Numbers checked against SQL output."),("edit","Clarify that cause is not verified."),("reject","Evidence needs re-check.")]:
        print("BEFORE:",report)
        after=review_gate_v1(report,decision,note)
        print("AFTER:",after)
    try:
        review_gate_v1(report,"publish","Invalid decision should fail")
    except ValueError as exc:
        print("Invalid decision correctly blocked:",exc)

if __name__ == "__main__": test_harness()
