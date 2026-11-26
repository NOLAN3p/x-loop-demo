from dataclasses import dataclass, asdict
import json

FIELDS = ("objective", "acceptance", "owner")

def critique(brief):
    return [key for key in FIELDS if not isinstance(brief.get(key), str) or not brief[key].strip()]

def run(brief):
    if not isinstance(brief, dict):
        raise TypeError("brief must be a dictionary")
    draft = {key: brief.get(key) for key in FIELDS}
    issues = critique(draft)
    trace = [{"stage": "plan", "fields": list(FIELDS)}, {"stage": "critic", "missing": issues}]
    for key in issues:
        draft[key] = "DRAFT: confirm " + key
    trace.append({"stage": "repair", "changed": issues})
    remaining = critique(draft)
    review = bool(remaining or any(v.startswith("DRAFT:") for v in draft.values() if isinstance(v,str)))
    trace.append({"stage": "validate", "requires_review": review})
    return {"brief": draft, "status": "review_required" if review else "structurally_valid", "trace": trace}

if __name__ == "__main__":
    print(json.dumps(run({"objective": "Prepare a sample project"}), indent=2))
