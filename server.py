import simpy
import pandas as pd
import random
from utils import _print

DEBUG = True

wait_times = []
waitlist = []


class Server(object):
    def __init__(self, env, numVNFs):
        self.env = env
        self.VNF = simpy.Resource(env, numVNFs)

    def manage_process(self, _process):
        # print('[Manage_process]: ID:', _process['t_id'],
        #       ' time:', _process['ElapsedTime'])
        # print('env.now=', self.env.now
        #       )
        # print(f'VNF:[{self.VNF.users}]')

        # print(
        #     f'\nProcess: [{_process["t_id"]}-{_process["SourcePort"]}]\nArrivalTime: [{self.env.now}]'
        # )
        yield self.env.timeout(_process['ElapsedTime'])


def run_server(env, numVNFs, data, all_average_times, all_env_now):
    server = Server(env, numVNFs)
    for index, row in data.iterrows():
        # _print(f'[Environment time]: {env.now}', True)
        _process = row
        _process['TimeArived'] = env.now
        # _print(f'[run_server]: {_process["SourcePort"]}', True)
        env.process(process_to_waitlist(env, _process,
                    server, all_average_times, all_env_now))
        yield env.timeout(3)


def process_to_waitlist(env, _process, server, all_average_times, all_env_now):

    waitlist.append(_process)

    with server.VNF.request() as request:
        yield request

        # Choose the first process in the waitlist
        # random_index = random.randint(0, len(waitlist) - 1)
        # chosen_process = waitlist[random_index]
        # cprocessAtime = waitlist[random_index]['TimeArived']

        chosen_process = waitlist[0]
        cprocessAtime = waitlist[0]['TimeArived']
        waitlist.pop(0)
        wait_times.append(env.now - cprocessAtime)
        yield env.process(server.manage_process(chosen_process))

    sum_waiting_time = sum(wait_times)
    average_waiting_time = sum_waiting_time/len(wait_times)
    all_average_times.append(average_waiting_time)
    all_env_now.append(env.now)
    # _print(f'Waiting Per Process {wait_times}', True)
    # print(f'Time [{env.now}] | Average waiting time [{average_waiting_time}]')
