import sys
# import .base
from base.pygamewrapper import PyGameWrapper

from utils import percent_round_int
from pygame.constants import K_w, K_a, K_s, K_d

import pygame
import math
from utils.vec2d import vec2d
from random import random


class Prey(pygame.sprite.Sprite):
    def __init__(self,
                 color,
                 radius,
                 speed,
                 sreen_width,
                 sreen_height):

        pygame.sprite.Sprite.__init__(self)

        self.SCREEN_WIDTH = sreen_width
        self.SCREEN_HEIGHT = sreen_height

        self.speed = speed
        self.radius = radius

        image = pygame.Surface((radius * 2, radius * 2))
        image.fill((0, 0, 0))
        image.set_colorkey((0, 0, 0))

        pygame.draw.circle(
            image,
            color,
            (radius, radius),
            radius,
            0
        )

        self.image = image.convert()
        self.rect = self.image.get_rect()

    def set_pos(self, pos_init):
        self.pos = vec2d(pos_init)
        self.rect.center = pos_init

    def update(self, dx, dy):

        dx = self.speed * dx
        dy = self.speed * dy

        if self.pos.x + dx > self.SCREEN_WIDTH - self.radius:
            self.pos.x = self.SCREEN_WIDTH - self.radius
        elif self.pos.x + dx <= self.radius:
            self.pos.x = self.radius
        else:
            self.pos.x = self.pos.x + dx

        if self.pos.y + dy > self.SCREEN_HEIGHT - self.radius:
            self.pos.y = self.SCREEN_HEIGHT - self.radius
        elif self.pos.y + dy <= self.radius:
            self.pos.y = self.radius
        else:
            self.pos.y = self.pos.y + dy

        self.rect.center = ((self.pos.x, self.pos.y))


class Hunter(pygame.sprite.Sprite):
    def __init__(self,
                 radius,
                 color,
                 speed,
                 sreen_width,
                 sreen_height):

        pygame.sprite.Sprite.__init__(self)

        self.SCREEN_WIDTH = sreen_width
        self.SCREEN_HEIGHT = sreen_height

        self.speed = speed
        self.radius = radius

        image = pygame.Surface([radius * 2, radius * 2])
        image.set_colorkey((0, 0, 0))

        pygame.draw.circle(
            image,
            color,
            (radius, radius),
            radius,
            0
        )

        self.image = image.convert()
        self.rect = self.image.get_rect()

    def set_pos(self, pos_init):
        self.pos = vec2d(pos_init)
        self.rect.center = pos_init

    def update(self, dx, dy):

        new_x = self.pos.x + dx * self.speed
        new_y = self.pos.y + dy * self.speed

        # if its not against a wall we want a total decay of 50
        if new_x >= self.SCREEN_WIDTH - self.radius * 2:
            self.pos.x = self.SCREEN_WIDTH - self.radius * 2
        elif new_x < 0.0:
            self.pos.x = 0.0
        else:
            self.pos.x = new_x

        if new_y > self.SCREEN_HEIGHT - self.radius * 2:
            self.pos.y = self.SCREEN_HEIGHT - self.radius * 2
        elif new_y < 0.0:
            self.pos.y = 0.0
        else:
            self.pos.y = new_y

        self.rect.center = (self.pos.x, self.pos.y)

    def draw(self, screen):
        screen.blit(self.image, self.rect.center)


class HunterWorld(PyGameWrapper):
    """
    Based Karpthy's WaterWorld in `REINFORCEjs`_.

    .. _REINFORCEjs: https://github.com/karpathy/reinforcejs

    Parameters
    ----------
    width : int
        Screen width.

    height : int
        Screen height, recommended to be same dimension as width.

    num_creeps : int (default: 3)
        The number of creeps on the screen at once.
    """

    def __init__(self,
                 width=48,
                 height=48,
                 num_preys=1,
                 num_hunters=1):

        actions = {
            "up": K_w,
            "left": K_a,
            "right": K_d,
            "down": K_s
        }

        PyGameWrapper.__init__(self, width, height, actions=actions)
        self.BG_COLOR = (255, 255, 255)
        self.PREY_NUM = num_preys
        self.HUNTER_NUM = num_hunters

        radius = percent_round_int(width, 0.047)


        self.HUNTER_COLOR = (60, 60, 140)
        self.HUNTER_SPEED = 0.25 * width
        self.HUNTER_RADIUS = radius

        self.PREY_COLORS = (40, 140, 40)
        self.PREY_SPEED = 0.25 * width
        self.PREY_RADIUS = radius


        self.hunters = []
        self.preys = []

    def _handle_player_events(self):
        self.dx = 0
        self.dy = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                key = event.key

                if key == self.actions["left"]:
                    self.dx -= self.AGENT_SPEED

                if key == self.actions["right"]:
                    self.dx += self.AGENT_SPEED

                if key == self.actions["up"]:
                    self.dy -= self.AGENT_SPEED

                if key == self.actions["down"]:
                    self.dy += self.AGENT_SPEED

    def getGameState(self):
        """

        Returns
        -------

        dict
            * player x position.
            * player y position.
            * player x velocity.
            * player y velocity.
            * player distance to each creep

        """

        state = {
            "player_x": self.player.pos.x,
            "player_y": self.player.pos.y,
            "player_velocity_x": self.player.vel.x,
            "player_velocity_y": self.player.vel.y,
            "creep_dist": {
                "GOOD": [],
                "BAD": []
            }
        }

        for c in self.creeps:
            dist = math.sqrt((self.player.pos.x - c.pos.x) **
                             2 + (self.player.pos.y - c.pos.y) ** 2)
            state["creep_dist"][c.TYPE].append(dist)

        return state

    def _rand_start(self, agents):
        pos = []
        for agent in agents:
            pos_x = random.uniform(agent.radius, self.width - agent.radius)
            pos_y = random.uniform(agent.radius, self.height - agent.radius)
            pos.append(vec2d(pos_x, pos_y))

        for i in range(len(agents)):
            for j in range(i + 1, len(agents)):
                dist = math.sqrt((pos[i].x - pos[j].x) ** 2 + (pos[i].y - pos[j].y) ** 2)
                while dist <= (agent[i].radius + agent[j].radius):
                    pos[i].x = random.uniform(agent[i].radius, self.width - agent[i].radius)
                    pos[i].y = random.uniform(agent[i].radius, self.height - agent[i].radius)
                    dist = math.sqrt((pos[i].x - pos[j].x) ** 2 + (pos[i].y - pos[j].y) ** 2)
        return pos

    def getScore(self):
        return self.score

    def game_over(self):
        """
            Return bool if the game has 'finished'
        """
        return (self.creep_counts['GOOD'] == 0)

    def init(self):

        """
            Starts/Resets the game to its inital state
        """

        for i in range(self.HUNTER_NUM):
            hunter = Hunter(
                self.HUNTER_RADIUS,
                self.HUNTER_COLOR,
                self.HUNTER_SPEED,
                self.width,
                self.height
            )
            self.hunters.append(hunter)

        for i in range(self.PREY_NUM):
            prey = Prey(
                self.PREY_RADIUS,
                self.PREY_COLOR,
                self.PREY_SPEED,
                self.width,
                self.height
            )
            self.hunters.append(hunter)


        if len(self.hunters) == 0:

        else:
            self.player.pos = vec2d(self.HUNTER_INIT_POS)

        if self.creeps is None:
            self.creeps = pygame.sprite.Group()
        else:
            self.creeps.empty()

        for i in range(self.N_CREEPS):
            self._add_creep()

        creep = Creep(
            self.CREEP_COLORS[creep_type],
            self.CREEP_RADII[creep_type],
            pos,
            self.rng.choice([-1, 1], 2),
            self.rng.rand() * self.CREEP_SPEED,
            self.CREEP_REWARD[creep_type],
            self.CREEP_TYPES[creep_type],
            self.width,
            self.height,
            self.rng.rand()
        )

        self.creeps.add(creep)

        self.score = 0
        self.ticks = 0
        self.lives = -1

    def step(self, dt):
        """
            Perform one step of game emulation.
        """
        dt /= 1000.0
        self.screen.fill(self.BG_COLOR)

        self.score += self.rewards["tick"]

        self._handle_player_events()
        self.player.update(self.dx, self.dy, dt)

        hits = pygame.sprite.spritecollide(self.player, self.creeps, True, pygame.sprite.collide_circle)
        for creep in hits:
            self.creep_counts[creep.TYPE] -= 1
            self.score += creep.reward
            self._add_creep()

        if self.creep_counts["GOOD"] == 0:
            self.score += self.rewards["win"]

        self.creeps.update(dt)

        self.player.draw(self.screen)
        self.creeps.draw(self.screen)


if __name__ == "__main__":
    import numpy as np

    pygame.init()
    game = HunterWorld(width=256, height=256, num_creeps=10)
    game.screen = pygame.display.set_mode(game.getScreenDims(), 0, 32)
    game.clock = pygame.time.Clock()
    game.rng = np.random.RandomState(24)
    game.init()

    while True:
        dt = game.clock.tick_busy_loop(30)
        game.step(dt)
        pygame.display.update()
