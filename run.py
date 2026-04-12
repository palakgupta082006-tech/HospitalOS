from hospital_env import HospitalEnv
from grader import grade_episode
from smart_agent import smart_agent_action
import random

DIAGNOSES = [
    "cardiac_arrest", "appendicitis", "fracture",
    "pneumonia", "stroke", "dengue", "typhoid"
]
ACTIONS = [
    "diagnose", "treat", "assign_bed",
    "assign_icu", "update_family", "audit_bill", "discharge"
]

def run_random_agent():
    print("\n" + "="*60)
    print("RANDOM AGENT")
    print("="*60)
    env = HospitalEnv()
    state = env.reset()
    done = False

    while not done:
        if not state["patients"]:
            # no patients right now, take empty step
            action = {
                "patient_id": -1,
                "action_type": "wait",
                "diagnosis": None,
            }
        else:
            patient = random.choice(state["patients"])
            action = {
                "patient_id": patient["id"],
                "action_type": random.choice(ACTIONS),
                "diagnosis": random.choice(DIAGNOSES),
            }

        result = env.step(action)

        # safety check
        if result is None:
            break

        state, reward, done = result
        print(
            f"Step {env.step_count:02d} | "
            f"Action: {action['action_type']:15s} | "
            f"Reward: {reward:+d} | "
            f"Total: {env.total_reward}"
        )

    return grade_episode(env.stats, env.total_reward)


def run_smart_agent():
    print("\n" + "="*60)
    print("SMART AGENT")
    print("="*60)
    env = HospitalEnv()
    state = env.reset()
    done = False

    while not done:
        if not state["patients"]:
            action = {
                "patient_id": -1,
                "action_type": "wait",
                "diagnosis": None,
            }
        else:
            action = smart_agent_action(state)
            if not action:
                action = {
                    "patient_id": -1,
                    "action_type": "wait",
                    "diagnosis": None,
                }

        result = env.step(action)

        # safety check
        if result is None:
            break

        state, reward, done = result
        print(
            f"Step {env.step_count:02d} | "
            f"Action: {action['action_type']:15s} | "
            f"Reward: {reward:+d} | "
            f"Total: {env.total_reward}"
        )

    return grade_episode(env.stats, env.total_reward)


# run both and compare
random_score = run_random_agent()
smart_score = run_smart_agent()

print("\n" + "="*60)
print("FINAL COMPARISON")
print("="*60)
print(f"Random Agent Score : {random_score:.1f} / 100")
print(f"Smart Agent Score  : {smart_score:.1f} / 100")
print(f"Improvement        : +{smart_score - random_score:.1f} points")
print("="*60)