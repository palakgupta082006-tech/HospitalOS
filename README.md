---
title: HospitalOS RL Environment
emoji: 🏥
colorFrom: blue
colorTo: green
sdk: docker
pinned: true
---

# 🏥 HospitalOS — RL Environment
> Built for Meta PyTorch OpenEnv Hackathon 2026 | Team Velora

---

## 🔥 The Problem

Every day in Indian hospitals:
- Patients wait hours in emergency without anyone attending them
- Wrong diagnoses lead to wrong treatments and preventable deaths
- Families stand outside with zero information about their loved ones
- Hospital bills don't match the actual care delivered
- Doctors, nurses, beds, ICU slots — nobody is coordinating them together

**This is not one problem. This is a coordination collapse.**

No single system sees the full picture. And that silence costs lives.

---

## 💡 The Solution

**HospitalOS** is a reinforcement learning environment where an AI agent 
learns to coordinate an entire hospital in real time.

The agent simultaneously manages:
- 🧑‍⚕️ Patient triage by severity
- 🔬 Correct diagnosis before treatment
- 🛏️ Bed and ICU allocation
- 💊 Medicine dispensing
- 👨‍👩‍👧 Family communication
- 💰 Bill auditing for overcharging

The agent starts knowing nothing. Through thousands of simulated episodes, 
it learns the optimal sequence of actions to save the most lives, 
respond the fastest, and keep bills fair.

---

## 📊 Results

| Agent | Diagnosis Accuracy | Deaths | Discharged | Score |
|-------|-------------------|--------|------------|-------|
| Random Agent | 14.3% | 5 | 0 | 0.0 / 100 |
| Smart Agent | 100.0% | 0 | 13 | 100.0 / 100 |
| **Improvement** | **+85.7%** | **-5** | **+13** | **+100 pts** |

This gap proves the environment has real depth —
random actions fail catastrophically, learned behavior saves everyone.

---

## 🎯 Reward Function

| Event | Reward |
|-------|--------|
| Correct diagnosis | +25 |
| Critical patient treated fast | +20 |
| Moderate patient treated | +12 |
| Patient discharged successfully | +15 to +20 |
| Family updated on time | +5 |
| Bill is fair | +8 |
| Wrong diagnosis | -40 |
| Treating without diagnosis | -20 |
| Patient death due to delay | -50 |
| Critical patient ignored too long | -30 |
| Overcharging detected | -15 |
| Wasting ICU on non-critical patient | -8 |

---

## 🌍 Real World Impact

- 1.4 billion people affected by India's hospital system
- 0 existing RL benchmarks in this exact domain
- 4 broken systems coordinated simultaneously by one agent
- Directly addresses India's most critical healthcare coordination problem

---

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Environment info |
| `/reset` | POST | Reset environment |
| `/state` | GET | Get current state |
| `/step` | POST | Take an action |
| `/grade` | GET | Get final grader score |
### Live API
https://palak-08-gupta-hospitalos.hf.space

### Interactive Docs
https://palak-08-gupta-hospitalos.hf.space/docs
---

## ⚙️ How to Run Locally

```bash
# clone the repo
git clone https://github.com/palakgupta082006-tech/HospitalOS
cd HospitalOS

# install dependencies
pip install -r requirements.txt

# run comparison — random vs smart agent
python run.py

# run the API server
python server.py
```

---

## 🧠 Environment Design

### State Space
Each step the agent observes:
- All current patients with symptoms, severity, waiting time
- Available resources — beds, ICU slots, doctors, medicines
- Stats — correct diagnoses, deaths, discharged patients
- Current step count

### Action Space
The agent can take 7 actions per step:
- `diagnose` — identify the disease from symptoms
- `treat` — administer medicine
- `assign_bed` — give patient a bed and doctor
- `assign_icu` — move critical patient to ICU
- `update_family` — send status update to family
- `audit_bill` — check and correct patient bill
- `discharge` — send recovered patient home

### Diseases Simulated
cardiac arrest, stroke, appendicitis, pneumonia, dengue, fracture, typhoid

### Episode Structure
- 50 steps per episode
- New patient arrives every 3 steps
- Critical patients die if untreated beyond 10 steps
- Grader scores 0-100 based on outcomes

---

## 📦 Tech Stack

- Python 3.10
- FastAPI
- Uvicorn
- Docker
- Hugging Face Spaces

---

## 👥 Team Velora

- **Palak Gupta** — Team Lead
- **Mili Jha** — Developer

---

## 🏆 Built for

**Meta PyTorch OpenEnv Hackathon 2026**
Scaler School of Technology, Bangalore
