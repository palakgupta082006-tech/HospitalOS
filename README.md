---
title: HospitalOS RL Environment
emoji: 🏥
colorFrom: blue
colorTo: green
sdk: docker
pinned: true
---

# 🏥 HospitalOS — RL Environment

AI-powered RL environment for hospital management.

Built for Meta PyTorch OpenEnv Hackathon.

## 🚀 Overview
An intelligent agent simulates real-time hospital operations — managing patients, doctors, ICU resources, billing, and family communication simultaneously.

## 📊 Results
| Agent | Score |
|-------|-------|
| Random | 0.0 / 100 |
| Smart | 100.0 / 100 |

## 🔌 API Endpoints
| Endpoint | Method |
|----------|--------|
| /reset | POST |
| /state | GET |
| /step | POST |
| /grade | GET |

## ⚙️ Run Locally
```bash
python run.py
```

## 🌐 Usage
Once deployed, access the API at:

- `/docs` → Interactive Swagger UI  
- `/reset` → Reset environment  
- `/state` → Get current state  
- `/step` → Take an action  
- `/grade` → Get final score  

## 📦 Tech Stack
- Python
- FastAPI
- Reinforcement Learning Environment

## ✨ Features
- Real-time patient management simulation  
- Resource allocation (beds, ICU, doctors)  
- Billing validation and auditing  
- Family communication tracking  
- Smart agent vs random agent comparison  

## 👥 Team
Velora  
- Palak Gupta (Team Lead)  
- Mili Jha