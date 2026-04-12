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

def call_llm(prompt: str) -> str:
    """Call LLM using OpenAI-compatible API to decide action."""
    try:
        import openai
        client = openai.OpenAI(
            base_url=os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"),
            api_key=os.environ.get("OPENAI_API_KEY", "sk-placeholder"),
        )
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
        )
        return response.choices[0].message.content.strip()
    except Exception:
        # fallback to rule-based if LLM unavailable
        return "diagnose"

def get_action_from_llm(state: dict) -> dict:
    """Use LLM to decide best action given current hospital state."""
    patients = state.get("patients", [])
    resources = state.get("resources", {})

    if not patients:
        return {"patient_id": -1, "action_type": "wait", "diagnosis": None}

    # build prompt for LLM
    patient = patients[0]
    symptoms = patient.get("symptoms", [])
    severity = patient.get("severity", "stable")
    diagnosed = patient.get("diagnosed", False)
    treated = patient.get("treated", False)

    prompt = f"""You are a hospital coordinator AI.
Patient severity: {severity}
Symptoms: {symptoms}
Diagnosed: {diagnosed}
Treated: {treated}
Resources: beds={resources.get('beds')}, icu={resources.get('icu_slots')}, medicines={resources.get('medicines')}

Choose ONE action from: diagnose, treat, assign_bed, assign_icu, update_family, audit_bill, discharge
If action is diagnose, also choose diagnosis from: {DIAGNOSES}

Reply in JSON format only:
{{"action_type": "diagnose", "diagnosis": "cardiac_arrest"}}
"""

    llm_response = call_llm(prompt)

    try:
        parsed = json.loads(llm_response)
        action_type = parsed.get("action_type", "diagnose")
        diagnosis = parsed.get("diagnosis", None)
    except Exception:
        # fallback
        if not diagnosed:
            action_type = "diagnose"
            diagnosis = _guess_diagnosis(symptoms)
        elif not treated:
            action_type = "treat"
            diagnosis = None
        else:
            action_type = "discharge"
            diagnosis = None

    return {
        "patient_id": patient["id"],
        "action_type": action_type,
        "diagnosis": diagnosis,
    }

def _guess_diagnosis(symptoms: list) -> str:
    """Rule-based fallback diagnosis."""
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

def run_inference():
    """Run full episode with LLM agent and structured logging."""

    # START log
    print(json.dumps({
        "type": "START",
        "env": "HospitalOS",
        "model": MODEL_NAME,
        "api_base": API_BASE_URL,
    }))

    # reset environment
    reset_response = requests.post(f"{API_BASE_URL}/reset")
    state = reset_response.json().get("observation", {})
    total_reward = 0
    step = 0

    done = False
    while not done:
        step += 1

        # get action from LLM
        action = get_action_from_llm(state)

        # take step in environment
        step_response = requests.post(
            f"{API_BASE_URL}/step",
            json=action,
            headers={"Content-Type": "application/json"}
        )
        result = step_response.json()

        state = result.get("observation", {})
        reward = result.get("reward", 0)
        done = result.get("done", False)
        total_reward = result.get("total_reward", 0)

        # STEP log — structured format
        print(json.dumps({
            "type": "STEP",
            "step": step,
            "action": action,
            "reward": reward,
            "total_reward": total_reward,
            "done": done,
        }))

        if step >= 50:
            break

    # get final grade
    grade_response = requests.get(f"{API_BASE_URL}/grade")
    grade = grade_response.json()

    # END log
    print(json.dumps({
        "type": "END",
        "total_steps": step,
        "total_reward": total_reward,
        "final_score": grade.get("final_score", 0),
        "stats": grade.get("stats", {}),
    }))

if __name__ == "__main__":
    run_inference()
