# ppo_brain.py
import json, socket
import numpy as np
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from training_gym import FishingEnv
from stable_baselines3.common.monitor import Monitor

# ---- TRAIN (run once) ----
env = DummyVecEnv([lambda: Monitor(FishingEnv())])
model = PPO("MlpPolicy", env, verbose=1, seed=42)
model.learn(total_timesteps=100_000)
model.save("fishing_ppo2")