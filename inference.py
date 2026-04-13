import os
import json
import requests

# environment variables with defaults
API_BASE_URL = os.environ.get("API_BASE_URL", "https://palak-08-gupta-hospitalos.hf.space")
MODEL_NAME = os.environ.get("MODEL_NAME", "gpt-4o-mini")
HF_TOKEN = os.environ.get("HF_TOKEN", "")

DIAGNOSES = [
    "cardiac_arrest", "appendicitis", "fracture",
    "pneumonia", "stroke", "dengue", "typhoid"
]

def _guess_diagnosis(symptoms: list) -> str:
    symptom_map = {
        "cardiac_arrest": ["chest pain", "breathlessness", "sweating", "arm pain"],
        "stroke": ["facial drooping", "arm weakness", "speech difficulty", "confusion"],
        "appendicitis": ["stomach pain", "fever", "nausea", "loss of appetite"],
        "pneumonia": ["cough", "fever", "breathing difficulty", "chills"],
        "dengue": ["high fever", "rash", "joint pain", "headache"],
        "fracture": ["limb pain", "swelling", "inability to move", "bruising"],
        "typhoid": ["prolonged fever", "weakness", "abdominal pain", "rose spots"],
    }
    best_match = "pneumonia"
    best_score = -1
    for diagnosis, diag_symptoms in symptom_map.items():
        score = len(set(symptoms) & set(diag_symptoms))
        if score > best_score:
            best_score = score
            best_match = diagnosis
    return best_match

def get_action(state: dict) -> dict:
    patients = state.get("patients", [])

    if not patients:
        return {"patient_id": -1, "action_type": "wait", "diagnosis": None}

    # find critical undiagnosed first
    for p in patients:
        if p["severity"] == "critical" and not p["diagnosed"]:
            return {
                "patient_id": p["id"],
                "action_type": "diagnose",
                "diagnosis": _guess_diagnosis(p["symptoms"])
            }

    # find critical diagnosed not in icu
    for p in patients:
        if p["severity"] == "critical" and p["diagnosed"] and not p["in_icu"]:
            return {
                "patient_id": p["id"],
                "action_type": "assign_icu",
                "diagnosis": None
            }

    # treat diagnosed untreated
    for p in patients:
        if p["diagnosed"] and not p["treated"]:
            return {
                "patient_id": p["id"],
                "action_type": "treat",
                "diagnosis": None
            }

    # discharge treated
    for p in patients:
        if p["treated"] and p["diagnosed"]:
            return {
                "patient_id": p["id"],
                "action_type": "discharge",
                "diagnosis": None
            }

    # diagnose remaining
    for p in patients:
        if not p["diagnosed"]:
            return {
                "patient_id": p["id"],
                "action_type": "diagnose",
                "diagnosis": _guess_diagnosis(p["symptoms"])
            }

    # update family
    for p in patients:
        if not p["family_updated"]:
            return {
                "patient_id": p["id"],
                "action_type": "update_family",
                "diagnosis": None
            }

    # audit bill
    return {
        "patient_id": patients[0]["id"],
        "action_type": "audit_bill",
        "diagnosis": None
    }

def main():
    # START log — required structured format
    print(json.dumps({
        "type": "START",
        "env": "HospitalOS",
        "model": MODEL_NAME,
        "api_base": API_BASE_URL,
    }), flush=True)

    try:
        # reset environment
        reset_response = requests.post(f"{API_BASE_URL}/reset", timeout=30)
        state = reset_response.json().get("observation", {})
    except Exception as e:
        print(json.dumps({"type": "ERROR", "message": str(e)}), flush=True)
        return

    total_reward = 0
    step = 0
    done = False

    while not done:
        step += 1

        # get action
        action = get_action(state)

        try:
            # take step
            step_response = requests.post(
                f"{API_BASE_URL}/step",
                json=action,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            result = step_response.json()
        except Exception as e:
            print(json.dumps({"type": "ERROR", "step": step, "message": str(e)}), flush=True)
            break

        state = result.get("observation", {})
        reward = result.get("reward", 0)
        done = result.get("done", False)
        total_reward = result.get("total_reward", 0)

        # STEP log — required structured format
        print(json.dumps({
            "type": "STEP",
            "step": step,
            "action_type": action["action_type"],
            "patient_id": action["patient_id"],
            "diagnosis": action.get("diagnosis"),
            "reward": reward,
            "total_reward": total_reward,
            "done": done,
        }), flush=True)

        if step >= 50:
            break

    # get final grade
    try:
        grade_response = requests.get(f"{API_BASE_URL}/grade", timeout=30)
        grade = grade_response.json()
        final_score = grade.get("final_score", 0)
        stats = grade.get("stats", {})
    except Exception:
        final_score = 0
        stats = {}

    # END log — required structured format
    print(json.dumps({
        "type": "END",
        "total_steps": step,
        "total_reward": total_reward,
        "final_score": final_score,
        "stats": stats,
    }), flush=True)

if __name__ == "__main__":
    main()
