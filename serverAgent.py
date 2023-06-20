import simpy
import pandas as pd
from agent import EpsilonGreedyAgent
from agent2 import EpsilonGreedyAgent2

import numpy as np
from utils import _print

DEBUG = False


wait_times = []
waitlist = []


state = 0

agent = EpsilonGreedyAgent2(0.2)


class Server(object):
    def __init__(self, env, numVNFs):
        self.average_wait_time = 0
        self.env = env
        self.VNF = simpy.Resource(env, numVNFs)

    def manage_process(self, _process):
        _print(
            f'[Manage_process]: ID: { _process["t_id"]} | time: {_process["ElapsedTime"]}', DEBUG)
        _print(f'VNF:[{self.VNF.users}]', DEBUG)

        # print(
        #     f'\nProcess: [{_process["t_id"]}-{_process["SourcePort"]}]\nArrivalTime: [{self.env.now}]'
        # )
        yield self.env.timeout(_process['ElapsedTime'])


def run_server(env, numVNFs, data, all_average_times, all_env_now):
    server = Server(env, numVNFs)
    for index, row in data.iterrows():

        _process = row
        _process['TimeArived'] = env.now
        _print('[run_server]: {_process["SourcePort"]}', DEBUG)
        env.process(process_to_waitlist(env, _process,
                    server, all_average_times, all_env_now))
        yield env.timeout(3)


def process_to_waitlist(env, _process, server, all_average_times, all_env_now):
    global waitlist
    arrival_time = env.now
    waitlist.append(_process)

    with server.VNF.request() as request:
        yield request

        available_actions = waitlist
        # print("Available actions", available_actions)
        # print("Waitlist", waitlist)

        action = agent.choose_action(available_actions)
        agent.update(action)
        # print("Action: ", action)
        # print(" Waitlist[actionm]: ",waitlist[action])
        # print(" Waitlist[actionm][EL]: ",waitlist[action]['ElapsedTime'])

        chosen_process = action
        # print("Chosen process [Server]", chosen_process)

        for index, processWL in enumerate(waitlist):
            if processWL['t_id'] == chosen_process[0]:
                cprocessAtime = processWL['TimeArived']
                chosen_process_index = index
                id_to_remove = processWL['t_id']
                # print(
                #     '\n\n !!!! chosen_process_index [Server ]', processWL['t_id'], chosen_process[0])
                break
        _print('[Server]: Sending process to manage', DEBUG)
        yield env.process(server.manage_process(waitlist[chosen_process_index]))

        # print('num_available:', server.VNF.count)
        # print('capacity:', server.VNF.capacity)
        # print(waitlist)
        # print('In use:', len(server.VNF.users))
        waitlist = [df for df in waitlist if df['t_id'] != id_to_remove]

        wait_times.append(env.now - cprocessAtime)

    sum_waiting_time = sum(wait_times)
    env.average_wait_time = sum_waiting_time/len(wait_times)
    all_average_times.append(env.average_wait_time)
    all_env_now.append(env.now)

    # print(
    #     f'Time [{env.now}]  | Average waiting time [{env.average_wait_time}]', DEBUG)
