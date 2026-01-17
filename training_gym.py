import gymnasium as gym
from gymnasium import spaces # we need to define the space of values
import random
import numpy as np

# state: inventory spaces(0-28), fishing status(0-1), at fishing spot(0-1), at bank (0-1)
# actions: fish, bank, walk to fishing spot, walk to bank, just turned on get inventory and get to fishing area

class FishingEnv(gym.Env):
    def __init__(self):
        self.action_space = spaces.Discrete(5)
        self.observation_space = spaces.Box(low=0,high=1.0,shape=(4,),dtype=float)
        self.reset()

    def _obs(self):
        # return current environment state
        return np.array([self.inventory / 28.0, float(self.fishing), float(self.at_bank), float(self.at_fishing)],dtype=np.float32)


    def reset(self, seed=None, options=None):
        # here we can set the instance variables of the observation values
        # such as # invent slots etc, it should be random
        #self.inventory = random.randint(0,28)
        self.inventory = 2
        
        if(self.inventory == 28):
            # full invent, cant fish
            self.fishing = 0
        else:   
            self.fishing = random.randint(0,1)

        if(self.fishing == 1):
            self.at_fishing = 1
            self.at_bank = 0
        else:
            # not fishing, choose exactly one location
            self.at_fishing = random.randint(0,1)
            self.at_bank = 1-self.at_fishing
 
        return self._obs(), {}

    def step(self,action):
        # here we reward the ppo based off the current state and if it made a good choice based off it
        reward = 0
        terminated = False 

        if action == 0:
            # fish action
            # good: we are at fishing, bad: anything else
            if self.inventory < 28 and self.at_fishing:
                self.inventory += 1
                reward += 1
            else:
                reward -=1 

        elif action == 1:
            # bank action
            if self.inventory == 28 and self.at_bank == 1:
                reward += 1 + (self.inventory - 2) * 0.1 # penalize early banking
                self.inventory = 2
                terminated = True
            else:
                reward -= 1
            
        elif action == 2:
            # walk to fishing spot
            if self.inventory < 28 and self.inventory > 0 and self.at_fishing == 0:
                reward += 0.2
                self.at_fishing = 1
                self.at_bank = 0
            else: 
                reward -= 0.5

        elif action == 3:
            # walk to bank
            if self.inventory == 28 and self.at_bank == 0:
                reward += 0.2
                self.at_bank = 1
                self.at_fishing = 0
            else: 
                reward -= 0.5

        elif action == 4:
            # get supplies
            if self.inventory == 0:
                self.inventory = 2
                reward += 2
            else:
                reward -= 1

        return self._obs(), reward, terminated, False, {}




 