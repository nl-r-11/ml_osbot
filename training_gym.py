import gymnasium as gym
from gymnasium import spaces # we need to define the space of values
import random

# state: inventory spaces(0-28), fishing status(0-1), at fishing spot(0-1), at bank (0-1)
# actions: fish, bank, walk to fishing spot, walk to bank, just turned on get inventory and get to fishing area

class FishingEnv(gym.Env):
    def __init__(self):
        self.action_Space = spaces.Discrete(5)
        self.observation_space = spaces.Box(low=0,high=1.0,shape=(4,),dtype=float)
        self.reset()


    def reset(self):
        # here we can set the instance variables of the observation values
        # such as # invent slots etc, it should be random
        self.inventory = random.randint(0,28)
        
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
        pass
        # here we reward the ppo based off the current state and if it made a good choice based off it
        reward = 0




 