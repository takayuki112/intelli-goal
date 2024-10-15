import gym
import numpy as np
import pygame
from gym import spaces
import random
import math

class CustomEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super(CustomEnv, self).__init__()
        self.screen_width = 1240
        self.screen_height = 800
        self.player_speed = 5
        self.goal_speed = 0
        self.action_space = spaces.Discrete(5)  # Define action space (0: Noop, 1: Up, 2: Down, 3: Left, 4: Right)
        self.observation_space = spaces.Box(low=np.array([0, 0]), high=np.array([self.screen_width, self.screen_height]), dtype=np.float32)  # Define observation space
        self.goal_radius = 20
        self.border_width = 10
        self.state = None
        self.steps_beyond_done = None
        self.screen = None
        self.clock = pygame.time.Clock()

    def step(self, action):
        assert self.action_space.contains(action), "%r (%s) invalid" % (action, type(action))
        player_x, player_y, goal_x, goal_y = self.state
        player_x += (action == 3) * -self.player_speed + (action == 4) * self.player_speed
        player_y += (action == 1) * -self.player_speed + (action == 2) * self.player_speed

        # Ensure the player stays within the screen bounds
        player_x = np.clip(player_x, self.border_width, self.screen_width - self.border_width)
        player_y = np.clip(player_y, self.border_width, self.screen_height - self.border_width)

        self.state = (player_x, player_y, goal_x, goal_y)
        
        # Calculate reward, done, and info
        done = math.sqrt((player_x - goal_x) ** 2 + (player_y - goal_y) ** 2) < self.goal_radius
        reward = 1 if done else 0
        info = {}

        return np.array(self.state), reward, done, info

    def reset(self):
        self.state = (self.screen_width // 2, self.screen_height // 2, random.randint(self.border_width, self.screen_width - self.border_width), random.randint(self.border_width, self.screen_height - self.border_width))
        self.steps_beyond_done = None
        return np.array(self.state)

    def render(self, mode='human'):
        if self.screen is None:
            pygame.init()
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.screen.fill((0, 0, 0))
        player_x, player_y, goal_x, goal_y = self.state
        pygame.draw.circle(self.screen, (255, 0, 0), (int(player_x), int(player_y)), 10)
        pygame.draw.circle(self.screen, (0, 0, 255), (int(goal_x), int(goal_y)), self.goal_radius)
        pygame.display.flip()
        self.clock.tick(60)

    def close(self):
        if self.screen is not None:
            pygame.quit()
            self.screen = None

# Test the environment
if __name__ == "__main__":
    env = CustomEnv()
    observation = env.reset()
    for _ in range(1000):
        action = env.action_space.sample()  # Take a random action
        observation, reward, done, info = env.step(action)
        env.render()
        if done:
            observation = env.reset()
    env.close()
