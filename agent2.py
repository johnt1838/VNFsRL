import numpy as np
import random
from utils import _print

DEBUG = True


class EpsilonGreedyAgent2:
    def __init__(self, epsilon):
        self.epsilon = epsilon
        self.actions_rewards = {(0, 1): 0}

    def choose_action(self, available_actions):

        # print(available_actions)

        # print('\n Available actions', available_actions)
        if np.random.random() < self.epsilon or not bool(self.actions_rewards):
            # print('IF')
            # Explore: choose a random action
            _choice = random.choice(available_actions)
            action = (_choice['t_id'], _choice['ElapsedTime'])
        else:
            best_new_interval = available_actions[0]
            for index, available_action in enumerate(available_actions):
                for key in self.actions_rewards.keys():
                    if self.actions_rewards[key] >

        return action

    def update(self, action):

        # action = (id, time)
        # if len(self.actions_rewards) == 0:
        #     print("time", action[1])
        #     self.actions_rewards[0] = 0
        if action[1] in self.actions_rewards:
            self.actions_rewards[action[1]] += 1
        else:
            self.actions_rewards[action[1]] = 0
