import simpy
import pandas as pd
from serverAgent import *
import matplotlib.pyplot as plt


def setup():
    all_average_times = []
    all_env_nows = []

    print('Setting up')
    _data = pd.read_csv("dataset/log2.csv")
    # _data = pd.read_csv("dataset/big_test_dataset.csv")
    # _data = pd.read_csv("dataset/small_dataset.csv")
    _data['TimeArived'] = 0

    env = simpy.Environment()
    env.process(run_server(env, 5, _data, all_average_times, all_env_nows))

    env.run(until=10000000)
    # plt.plot(all_env_nows, all_average_times)

    # # Set labels and title
    # plt.xlabel('time')
    # plt.ylabel('average waiting')
    # plt.title('Average waiting time to environment time (Random controller)')

    # # Display the plot
    # plt.show()


if __name__ == '__main__':
    setup()

# RL Time [40891]  | Average waiting time [8103.713177066836]
# First Allocated Time [78286] | Average waiting time [28822.934906556857]
# Random Time [80801] | Average waiting time [23661.83386126069]
