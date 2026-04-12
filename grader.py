def grade_episode(stats, total_reward):
    score = 0
    feedback = []

    # diagnosis accuracy — most important
    total_diagnoses = stats["correct_diagnoses"] + stats["wrong_diagnoses"]
    if total_diagnoses > 0:
        accuracy = stats["correct_diagnoses"] / total_diagnoses
        score += accuracy * 40
        feedback.append(f"Diagnosis accuracy: {accuracy*100:.1f}% | {accuracy*40:.1f}/40 pts")
    else:
        feedback.append("Diagnosis accuracy: No diagnoses made | 0/40 pts")

    # deaths
    death_penalty = stats["deaths"] * 10
    score -= death_penalty
    feedback.append(f"Deaths: {stats['deaths']} | -{death_penalty} pts")

    # discharged patients
    discharge_score = min(stats["discharged"] * 5, 30)
    score += discharge_score
    feedback.append(f"Discharged: {stats['discharged']} | +{discharge_score}/30 pts")

    # family communication
    family_score = min(stats["families_updated"] * 2, 10)
    score += family_score
    feedback.append(f"Families updated: {stats['families_updated']} | +{family_score}/10 pts")

    # overcharging
    overcharge_penalty = stats["overcharges_caught"] * 5
    score -= overcharge_penalty
    feedback.append(f"Overcharges caught: {stats['overcharges_caught']} | -{overcharge_penalty} pts")

    # normalize to 0-100
    final_score = max(0, min(100, score + 50))

    print("\n========== GRADER REPORT ==========")
    for f in feedback:
        print(f" * {f}")
    print(f"\n FINAL SCORE: {final_score:.1f} / 100")
    print(f" RAW REWARD:  {total_reward}")
    print("====================================")

    return final_score