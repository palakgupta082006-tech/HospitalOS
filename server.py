from fastapi import FastAPI
from pydantic import BaseModel
from hospital_env import HospitalEnv
from grader import grade_episode
from typing import Optional
import uvicorn

app = FastAPI(title="HospitalOS RL Environment")

env = HospitalEnv()
state = env.reset()

class Action(BaseModel):
    patient_id: int
    action_type: str
    diagnosis: Optional[str] = None

@app.get("/")
def root():
    return {
        "name": "HospitalOS",
        "description": "RL Environment for Indian Hospital Coordination",
        "version": "1.0",
        "endpoints": ["/reset", "/state", "/step", "/grade"]
    }

@app.post("/reset")
def reset():
    global env, state
    env = HospitalEnv()
    state = env.reset()
    return {
        "observation": state,
        "message": "Environment reset successfully"
    }

@app.get("/state")
def get_state():
    return {
        "observation": state,
        "step": env.step_count,
        "total_reward": env.total_reward,
        "done": env.step_count >= env.max_steps
    }

@app.post("/step")
def step(action: Action):
    global state
    action_dict = {
        "patient_id": action.patient_id,
        "action_type": action.action_type,
        "diagnosis": action.diagnosis,
    }
    new_state, reward, done = env.step(action_dict)
    state = new_state
    return {
        "observation": new_state,
        "reward": reward,
        "done": done,
        "total_reward": env.total_reward,
        "info": env.stats
    }

@app.get("/grade")
def grade():
    score = grade_episode(env.stats, env.total_reward)
    return {
        "final_score": score,
        "stats": env.stats,
        "total_reward": env.total_reward
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)