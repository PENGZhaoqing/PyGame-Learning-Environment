import random
from ple import PLE
from ple.games.hunterworld import HunterWorld
import random

rewards = {
    "positive": 1.0,
    "negative": -1.0,
    "tick": 0.0,
    "loss": -5.0,
    "win": 5.0
}

game = HunterWorld(width=256, height=256,
                   num_preys=5,
                   num_hunters=2)
env = PLE(game, fps=30, force_fps=False, display_screen=True,
          reward_values=rewards)

env.init()
multi_actions = env.getMultiActionSet()
for i in range(1000):
    if env.game_over():
        env.reset_game()

    action_list = []
    for action in multi_actions:
        action = action.values()
        action_list.append(random.choice(action))

    reward = env.multi_act(action_list)

    print "Score: {:0.3f} | Reward: {:0.3f} ".format(env.score(), reward)
