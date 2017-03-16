import numpy as np
import math


# from ..agent import Agent, Hunter, Prey

def percent_round_int(percent, x):
    return np.round(percent * x).astype(int)


def count_distant(agent1, agent2):
    try:
        dis = math.sqrt((agent1.pos.x - agent2.pos.x) ** 2 + (agent1.pos.y - agent2.pos.y) ** 2)
    except (AttributeError, TypeError):
        raise AssertionError('Object should extend from Agent Class')
    return dis
