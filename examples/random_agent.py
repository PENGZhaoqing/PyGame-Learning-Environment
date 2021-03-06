import numpy as np
from ple import PLE
from ple.games.pong import Pong


class NaiveAgent():
    """
            This is our naive agent. It picks actions at random!
    """

    def __init__(self, actions):
        self.actions = actions

    def pickAction(self, reward, obs):
        return self.actions[np.random.randint(0, len(self.actions))]


fps = 30  # fps we want to run at
frame_skip = 2
num_steps = 1
force_fps = False  # slower speed
display_screen = True

reward = 0.0
max_noops = 20
nb_frames = 15000

# make a PLE instance.
env = PLE(Pong(), fps=fps, frame_skip=frame_skip, num_steps=num_steps,
        force_fps=force_fps, display_screen=display_screen)

# our Naive agent!
agent = NaiveAgent(env.getActionSet())

# init agent and game.
env.init()

# lets do a random number of NOOP's
for i in range(np.random.randint(0, max_noops)):
    reward = env.act(env.NOOP)

# start our training loop
for f in range(nb_frames):
    # if the game is over
    if env.game_over():
        env.reset_game()

    obs = env.getScreenRGB()
    action = agent.pickAction(reward, obs)
    reward = env.act(action)

    # if f % 50 == 0:
    #     p.saveScreen("tmp/screen_capture.png")

    print f

    if f > 50:
        env.display_screen = True
        env.force_fps = True
