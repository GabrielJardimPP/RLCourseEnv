import gymnasium as gym
from gymnasium import spaces
import numpy as np

class GoiabaEnv(gym.Env):
    metadata = {'render_modes': ['human']}

    def __init__(self, rewards_dict, prob_bus_if_wait = .4, render_mode=None):
        super().__init__()

        self.prob_bus_if_wait = prob_bus_if_wait
        self.rewards = rewards_dict

        # Action - Chooses waiting (0) or goiaba (1)
        self.action_space = spaces.Discrete(2)

        # Observation - Either:
        #   Hungry/Not Home (0)
        #   Not Hungry/ Not Home (1)
        # Other state (Not hungry/ Home) is implicit from the termination

        self.observation_space = spaces.Discrete(2)

        self.state = None
        self.rng = None
        
    def reset(self, seed, options=None):
        self.rng = np.random.default_rng(seed)
        
        self.state = 0
        observation = self.state
        info = {'prob:': 1.0}

        return observation, info

    def step(self, action):
        cur_obs = self.state
        if cur_obs == 1:
            observation = 1
            reward = self.rewards['self_loop_hunger']
            # convention: 
            # terminated = truncated = True
            # means that we have non-zero reward  prob 1 self-loop
            terminated = True
            truncated = True
            info = {'prob': 1.0}

        elif cur_obs == 0:
            if action == 0:
                # waits
                if self.rng.random() <= self.prob_bus_if_wait:
                    # bus arrives
                    observation = 3
                    reward = self.rewards['start_to_home']
                    terminated = True
                    truncated = False
                    info = {'prob': self.prob_bus_if_wait}
                else: 
                    # bus doesn't arrive
                    observation = 0
                    reward = self.rewards['start_to_start']
                    terminated = False
                    truncated = False
                    info = {'prob': 1-self.prob_bus_if_wait}
            elif action == 1:
                # eats goiaba
                observation = 3
                reward = self.rewards['start_and_goiaba']
                terminated = False
                truncated = False
                info = {'prob': 1.0}

        return observation, reward, terminated, truncated, info

    def render(self):
        out = [0,0]
        out[self.state] = 1
        print(out)
            

    
if __name__ == '__main__':
    rewards_dict = {
        'start_to_home': 100.0,
        'start_to_start': -1.0,
        'start_and_goiaba': 10.0,
        'self_loop_hunger': -1.0
    }

    prob_bus = 0.1

    goiaba = GoiabaEnv(rewards_dict, prob_bus_if_wait=prob_bus)

    seed = 1

    obs, _ = goiaba.reset(seed)

    print('-------------\n')
    print('initial state:')
    goiaba.render()


    # policy is wait:
    wait = 0
    eat = 1


    terminated = False
    step = 1
    while not terminated:
        print('\n=====================')
        print(f'Current step is {step}')
        observation, reward, terminated, truncated, info = goiaba.step(wait)
        goiaba.render()
        print(f'Reward: {reward}')
        print(f'Terminated {terminated}')
        print(f'Truncated {truncated}')
        print(f'info = {info}')
        step += 1

    print('R E S E T \n')



    print('-------------\n')
    print('initial state:')
    goiaba.render()
    

    # policy is eat
    terminated = False
    step = 1
    max_step = 100
    while not terminated:
        print('\n=====================')
        print(f'Current step is {step}')
        observation, reward, terminated, truncated, info = goiaba.step(eat)
        goiaba.render()
        print(f'Reward: {reward}')
        print(f'Terminated {terminated}')
        print(f'Truncated {truncated}')
        print(f'info = {info}')
        step += 1
        if step == max_step:
            break