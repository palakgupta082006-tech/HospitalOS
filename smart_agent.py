def smart_agent_action(state):
    patients = state["patients"]
    resources = state["resources"]

    if not patients:
        return None

    # priority 1 — diagnose critical undiagnosed patient first
    for p in patients:
        if p["severity"] == "critical" and not p["diagnosed"]:
            return {
                "patient_id": p["id"],
                "action_type": "diagnose",
                "diagnosis": _guess_diagnosis(p["symptoms"])
            }

    # priority 2 — assign ICU to critical diagnosed patient
    for p in patients:
        if (
            p["severity"] == "critical"
            and p["diagnosed"]
            and not p["in_icu"]
            and resources["icu_slots"] > 0
        ):
            return {
                "patient_id": p["id"],
                "action_type": "assign_icu",
                "diagnosis": None
            }

    # priority 3 — treat diagnosed untreated critical patient
    for p in patients:
        if (
            p["severity"] == "critical"
            and p["diagnosed"]
            and not p["treated"]
        ):
            return {
                "patient_id": p["id"],
                "action_type": "treat",
                "diagnosis": None
            }

    # priority 4 — discharge treated diagnosed patients
    for p in patients:
        if p["treated"] and p["diagnosed"]:
            return {
                "patient_id": p["id"],
                "action_type": "discharge",
                "diagnosis": None
            }

    # priority 5 — diagnose moderate/stable undiagnosed
    for p in patients:
        if not p["diagnosed"]:
            return {
                "patient_id": p["id"],
                "action_type": "diagnose",
                "diagnosis": _guess_diagnosis(p["symptoms"])
            }

    # priority 6 — treat diagnosed untreated moderate/stable
    for p in patients:
        if p["diagnosed"] and not p["treated"]:
            return {
                "patient_id": p["id"],
                "action_type": "treat",
                "diagnosis": None
            }

    # priority 7 — assign bed only if not already assigned
    for p in patients:
        if not p["diagnosed"] and resources["beds"] > 0:
            return {
                "patient_id": p["id"],
                "action_type": "assign_bed",
                "diagnosis": None
            }

    # priority 8 — update family
    for p in patients:
        if not p["family_updated"]:
            return {
                "patient_id": p["id"],
                "action_type": "update_family",
                "diagnosis": None
            }

    # priority 9 — audit bill
    for p in patients:
        return {
            "patient_id": p["id"],
            "action_type": "audit_bill",
            "diagnosis": None
        }

    return None


def _guess_diagnosis(symptoms):
    symptom_map = {
        "cardiac_arrest": ["chest pain", "breathlessness", "sweating", "arm pain"],
        "stroke": ["facial drooping", "arm weakness", "speech difficulty", "confusion"],
        "appendicitis": ["stomach pain", "fever", "nausea", "loss of appetite"],
        "pneumonia": ["cough", "fever", "breathing difficulty", "chills"],
        "dengue": ["high fever", "rash", "joint pain", "headache"],
        "fracture": ["limb pain", "swelling", "inability to move", "bruising"],
        "typhoid": ["prolonged fever", "weakness", "abdominal pain", "rose spots"],
    }

    best_match = None
    best_score = -1

    for diagnosis, diag_symptoms in symptom_map.items():
        score = len(set(symptoms) & set(diag_symptoms))
        if score > best_score:
            best_score = score
            best_match = diagnosis

    return best_match