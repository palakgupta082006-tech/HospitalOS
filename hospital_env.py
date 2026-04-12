from patient import generate_patient
import random

class HospitalEnv:
    def __init__(self):
        self.max_steps = 50
        self.reset()

    def reset(self):
        self.patients = []
        self.patient_counter = 0
        self.resources = {
            "beds": 10,
            "icu_slots": 3,
            "doctors": 4,
            "medicines": 30,
        }
        self.total_reward = 0
        self.step_count = 0
        self.stats = {
            "correct_diagnoses": 0,
            "wrong_diagnoses": 0,
            "deaths": 0,
            "discharged": 0,
            "overcharges_caught": 0,
            "families_updated": 0,
        }
        self._spawn_patients(5)
        return self._get_state()

    def _spawn_patients(self, count):
        for _ in range(count):
            self.patient_counter += 1
            self.patients.append(generate_patient(self.patient_counter))

    def _get_state(self):
        return {
            "patients": [
                {
                    "id": p["id"],
                    "symptoms": p["symptoms"],
                    "severity": p["severity"],
                    "waiting_time": p["waiting_time"],
                    "diagnosed": p["diagnosed"],
                    "treated": p["treated"],
                    "in_icu": p["in_icu"],
                    "family_updated": p["family_updated"],
                }
                for p in self.patients
            ],
            "resources": self.resources.copy(),
            "stats": self.stats.copy(),
            "step": self.step_count,
        }

    def _check_critical_deaths(self):
        reward = 0
        dead = []
        for p in self.patients:
            if (
                p["severity"] == "critical"
                and p["waiting_time"] > 10
                and not p["treated"]
            ):
                reward -= 50
                self.stats["deaths"] += 1
                dead.append(p)
        for p in dead:
            self.patients.remove(p)
        return reward

    def step(self, action):
        reward = 0
        self.step_count += 1

        # spawn new patient every 3 steps
        if self.step_count % 3 == 0:
            self.patient_counter += 1
            self.patients.append(generate_patient(self.patient_counter))

        # increment waiting time for all untreated patients
        for p in self.patients:
            if not p["treated"]:
                p["waiting_time"] += 1

        # check if any critical patient has waited too long
        reward += self._check_critical_deaths()

        # get target patient and action
        patient_id = action.get("patient_id")
        action_type = action.get("action_type")

        # handle wait action or invalid patient
        if patient_id == -1 or action_type == "wait":
            return self._get_state(), reward, self.step_count >= self.max_steps

        patient = next(
            (p for p in self.patients if p["id"] == patient_id), None
        )

        # patient not found
        if not patient:
            return self._get_state(), reward, self.step_count >= self.max_steps

        # === ACTION HANDLING ===

        if action_type == "diagnose":
            agent_diagnosis = action.get("diagnosis")
            if agent_diagnosis == patient["correct_diagnosis"]:
                reward += 25
                patient["diagnosed"] = True
                patient["diagnosis_given"] = agent_diagnosis
                self.stats["correct_diagnoses"] += 1
            else:
                reward -= 40
                patient["diagnosed"] = False
                patient["diagnosis_given"] = agent_diagnosis
                self.stats["wrong_diagnoses"] += 1

        elif action_type == "treat":
            if not patient["diagnosed"]:
                reward -= 20
            elif self.resources["medicines"] > 0:
                patient["treated"] = True
                self.resources["medicines"] -= 1
                if patient["severity"] == "critical":
                    reward += 20
                elif patient["severity"] == "moderate":
                    reward += 12
                else:
                    reward += 8
            else:
                reward -= 10

        elif action_type == "assign_bed":
            if self.resources["beds"] > 0 and not patient["assigned_doctor"]:
                self.resources["beds"] -= 1
                if self.resources["doctors"] > 0:
                    self.resources["doctors"] -= 1
                patient["assigned_doctor"] = f"Dr_{random.randint(1, 4)}"
                reward += 5
            else:
                reward -= 3

        elif action_type == "assign_icu":
            if (
                self.resources["icu_slots"] > 0
                and patient["severity"] == "critical"
                and not patient["in_icu"]
            ):
                self.resources["icu_slots"] -= 1
                patient["in_icu"] = True
                reward += 15
            elif patient["severity"] != "critical":
                reward -= 8
            else:
                reward -= 5

        elif action_type == "update_family":
            if not patient["family_updated"]:
                patient["family_updated"] = True
                self.stats["families_updated"] += 1
                reward += 5

        elif action_type == "audit_bill":
            overcharge = patient["bill"] - patient["actual_care_cost"]
            if overcharge > 500:
                reward -= 15
                self.stats["overcharges_caught"] += 1
            else:
                reward += 8

        elif action_type == "discharge":
            if patient["treated"] and patient["diagnosed"]:
                patient["discharged"] = True
                self.patients.remove(patient)
                self.resources["beds"] += 1
                self.stats["discharged"] += 1
                if patient["waiting_time"] < 10:
                    reward += 20
                else:
                    reward += 15
            else:
                reward -= 10

        self.total_reward += reward
        done = self.step_count >= self.max_steps

        return self._get_state(), reward, done

    def render(self):
        print(f"\n{'='*50}")
        print(f"Step     : {self.step_count}")
        print(f"Reward   : {self.total_reward}")
        print(f"Resources: {self.resources}")
        print(f"Patients : {len(self.patients)}")
        print(f"Stats    : {self.stats}")
        print(f"{'='*50}")