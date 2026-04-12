import random

SYMPTOMS_MAP = {
    "cardiac_arrest": ["chest pain", "breathlessness", "sweating", "arm pain"],
    "appendicitis": ["stomach pain", "fever", "nausea", "loss of appetite"],
    "fracture": ["limb pain", "swelling", "inability to move", "bruising"],
    "pneumonia": ["cough", "fever", "breathing difficulty", "chills"],
    "stroke": ["facial drooping", "arm weakness", "speech difficulty", "confusion"],
    "dengue": ["high fever", "rash", "joint pain", "headache"],
    "typhoid": ["prolonged fever", "weakness", "abdominal pain", "rose spots"],
}

SEVERITY_MAP = {
    "cardiac_arrest": "critical",
    "stroke": "critical",
    "appendicitis": "moderate",
    "pneumonia": "moderate",
    "dengue": "moderate",
    "fracture": "stable",
    "typhoid": "stable",
}

TREATMENT_COST = {
    "cardiac_arrest": 5000,
    "stroke": 4500,
    "appendicitis": 3000,
    "pneumonia": 2000,
    "dengue": 1500,
    "fracture": 1800,
    "typhoid": 1200,
}

def generate_patient(patient_id):
    diagnosis = random.choice(list(SYMPTOMS_MAP.keys()))
    return {
        "id": patient_id,
        "symptoms": SYMPTOMS_MAP[diagnosis],
        "correct_diagnosis": diagnosis,
        "severity": SEVERITY_MAP[diagnosis],
        "waiting_time": 0,
        "assigned_doctor": None,
        "diagnosed": False,
        "diagnosis_given": None,
        "treated": False,
        "discharged": False,
        "in_icu": False,
        "bill": random.randint(
            TREATMENT_COST[diagnosis],
            TREATMENT_COST[diagnosis] + 2000
        ),
        "actual_care_cost": TREATMENT_COST[diagnosis],
        "family_updated": False,
    }