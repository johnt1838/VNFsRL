import numpy as np
import random
from utils import _print

DEBUG = True


class EpsilonGreedyAgent:
    def __init__(self, epsilon):
        self.epsilon = epsilon
        self.actions_rewards = {}

    def choose_action(self, available_actions):
        # print('\n Available actions', available_actions)
        if np.random.random() < self.epsilon or not bool(self.actions_rewards):
            # print('IF')
            # Explore: choose a random action
            _choice = random.choice(available_actions)
            action = (_choice['t_id'], _choice['ElapsedTime'])
        else:

            sorted_actionL = sorted(
                self.actions_rewards.items(), key=lambda x: x[1], reverse=True)
            self.actions_rewards = dict(sorted_actionL)
            # print("ELSE")
            # print("\n Sorted ActionL", sorted_actionL)
            # print(self.actions_rewards)

            for index, available_action in enumerate(available_actions):
                if available_action.isin(self.actions_rewards.values()).any():
                    action = (available_action['t_id'],
                              available_action['ElapsedTime'])
                else:
                    sorted_df_list = sorted(
                        available_actions, key=lambda df: df['ElapsedTime'])
                    # print('Sort list', sorted_df_list)
                    action = (sorted_df_list[0]['t_id'],
                              sorted_df_list[0]['ElapsedTime'])
                    break

            # print("ELSE: AVAILABLE ACTIONS", available_actions)
            # print()
        # print("[Agent]: Returning ", action)
        # print(action)
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
