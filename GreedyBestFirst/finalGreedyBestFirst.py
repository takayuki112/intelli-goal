# Import necessary libraries
import pygame
import gymnasium as gym
from gymnasium import spaces
import numpy as np
import math
import random

# Define the IntelliGoal class
class IntelliGoal(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super(IntelliGoal, self).__init__()
        
        # Initialize screen parameters
        self.screen_width = 1240
        self.screen_height = 800
        self.border_width = 10
        self.screen = None
        
        # Initialize goal and player parameters
        self.goal_radius = 20
        self.player_radius = 10
        self.player_speed = 2
        self.goal_speed_limit= 100

        # Initialize state information
        self.player_x = 0
        self.player_y = 0
        self.goal_x = 0.0
        self.goal_y = 0.0
        self.state = np.array([self.player_x, self.player_y, self.goal_x, self.goal_y])
        self.reward = 0
        self.score = 0
        self.done = False
        self.truncated = False
        self.truncation_step_limit = 1000
        self.truncation_step_counter = 0
        self.goal_spawn_range = 300
        self.prev_goal_position = (0, 0)
        self.position_change_timer = 0

        # Initialize goal movement parameters
        self.goal_speed = 0.1
        self.goal_direction = (0, 0)
        self.direction_change_timer = 50000
        self.direction_change_interval = 200
        self.constant_goal_speed_increment = 0.002
        self.level_up_goal_speed_increment = 0.01

        # Define action and observation spaces
        self.action_space = spaces.Discrete(5)
        self.observation_space = spaces.Box(
            low=np.array([0, 0, 0, 0]), 
            high=np.array([self.screen_width, self.screen_height, self.screen_width, self.screen_height]), 
            dtype=np.int32
        )

    # Define seed method
    def seed(self, seed=None):
        if seed is not None and (seed < 0 or seed >= 2**32):
            raise ValueError("Seed must be between 0 and 2**32 - 1")
        self.np_random, seed = gym.utils.seeding.np_random(seed)
        return [seed]

    # Define reset method
    def reset(self, seed=0):
        self.seed(seed)
        self.player_x = self.screen_width // 2
        self.player_y = self.screen_height // 2
        self.goal_x, self.goal_y = self.respawn_goal()
        self.reward = 0
        self.state = np.array([self.player_x, self.player_y, self.goal_x, self.goal_y])
        self.done = False
        self.truncated = False
        self.truncation_step_counter = 0
        return self.state, {}

    # Define respawn_goal method
    def respawn_goal(self):
        self.goal_x = self.player_x + random.randint(-self.goal_spawn_range, self.goal_spawn_range)
        self.goal_y = self.player_y + random.randint(-self.goal_spawn_range, self.goal_spawn_range)
        offset = self.border_width + self.goal_radius
        self.goal_x = min(max(self.goal_x, offset), self.screen_width - offset)
        self.goal_y = min(max(self.goal_y, offset), self.screen_height - offset)
        self.prev_distance = math.sqrt((self.player_x - self.goal_x) ** 2 + (self.player_y - self.goal_y) ** 2)
        return self.goal_x, self.goal_y

    # Define step method
    def step(self, action):
        self.reward = 0
        if self.goal_speed<self.goal_speed_limit:
            self.goal_speed+=self.constant_goal_speed_increment
        self.do_action(action)
        self.dynamic_goal()
        return self.state, self.reward, self.done, self.truncated, {}

    # Define do_action method
    def do_action(s, action):
        if not s.action_space.contains(action):
            print("Greedy Action")
        
        s.prev_distance = math.sqrt((s.player_x - s.goal_x) ** 2 + (s.player_y - s.goal_y) ** 2)
        
        # consider origin on top left of screen (x++ means move right, y++ means move down)
        def do_action(s, action):
            if not s.action_space.contains(action):
                print("Greedy Action")
        
        s.prev_distance = math.sqrt((s.player_x - s.goal_x) ** 2 + (s.player_y - s.goal_y) ** 2)
        
        # consider origin on top left of screen (x++ means move right, y++ means move down)
        if action == 1:
            s.player_y -= s.player_speed
        elif action == 2:
            s.player_y += s.player_speed
        elif action == 3:
            s.player_x -= s.player_speed
        elif action == 4:
            s.player_x += s.player_speed
        elif action == 5:  # Diagonal up-left
            s.player_x -= s.player_speed
            s.player_y -= s.player_speed
        elif action == 6:  # Diagonal up-right
            s.player_x += s.player_speed
            s.player_y -= s.player_speed
        elif action == 7:  # Diagonal down-left
            s.player_x -= s.player_speed
            s.player_y += s.player_speed
        elif action == 8:  # Diagonal down-right
            s.player_x += s.player_speed
            s.player_y += s.player_speed

        # Clip player position to stay within screen bounds
        s.player_x = max(s.border_width, min(s.player_x, s.screen_width - s.border_width))
        s.player_y = max(s.border_width, min(s.player_y, s.screen_height - s.border_width))

        s.state = np.array([s.player_x, s.player_y, s.goal_x, s.goal_y])

        #need to add diagonal movement options


        s.state = np.array([s.player_x, s.player_y, s.goal_x, s.goal_y])

        if s.player_x not in range(s.border_width, s.screen_width - s.border_width) or s.player_y not in range(s.border_width, s.screen_height - s.border_width):
            s.player_x, s.player_y = s.screen_width // 2, s.screen_height // 2
        distance = math.sqrt((s.player_x - s.goal_x) ** 2 + (s.player_y - s.goal_y) ** 2)
        if distance < s.goal_radius + s.player_radius:
            s.goal_x, s.goal_y = s.respawn_goal()
            if s.goal_speed<s.goal_speed_limit:
                s.goal_speed += s.level_up_goal_speed_increment
            s.score += 1
            s.done = True 
            s.state = np.array([s.player_x, s.player_y, s.goal_x, s.goal_y])

    # Define dynamic_goal method
    def dynamic_goal(self): 
        if self.direction_change_timer <= 0:
            self.goal_direction = (random.randint(-2, 2), random.randint(-2, 2))
            self.direction_change_timer = self.direction_change_interval
        else:
            self.goal_x += self.goal_direction[0] * self.goal_speed
            self.goal_y += self.goal_direction[1] * self.goal_speed
            self.direction_change_timer -= 1
        goal_margin = 25
        self.goal_x = max(self.border_width + goal_margin, min(self.goal_x, self.screen_width - self.border_width - goal_margin))
        self.goal_y = max(self.border_width + goal_margin, min(self.goal_y, self.screen_height - self.border_width - goal_margin))
        current_goal_position = (self.goal_x, self.goal_y)
        if current_goal_position == self.prev_goal_position:
            self.position_change_timer += 1
        else:
            self.position_change_timer = 0
            self.prev_goal_position = current_goal_position
        if self.position_change_timer >= 3:
            self.goal_direction = (random.randint(-2, 2), random.randint(-2, 2))
            self.position_change_timer = 0
        self.state = np.array([self.player_x, self.player_y, self.goal_x, self.goal_y])

    # Define bestFirst method
    def bestFirst(s):
    # Calculate the horizontal and vertical distances between player and goal
        delta_x = s.goal_x - s.player_x
        delta_y = s.goal_y - s.player_y

        # Determine the direction for each axis
        if delta_y < 0:  # Player is above the goal
            if delta_x < 0:  # Player is also left of the goal
                return 5  # Diagonal up-left
            elif delta_x > 0:  # Player is right of the goal
                return 6  # Diagonal up-right
            else:  # Player is directly above the goal
                return 1  # Up
        elif delta_y > 0:  # Player is below the goal
            if delta_x < 0:  # Player is left of the goal
                return 7  # Diagonal down-left
            elif delta_x > 0:  # Player is also right of the goal
                return 8  # Diagonal down-right
            else:  # Player is directly below the goal
                return 2  # Down
        else:  # Player is on the same vertical line as the goal
            if delta_x < 0:  # Player is left of the goal
                return 3  # Left
            elif delta_x > 0:  # Player is right of the goal
                return 4  # Right
            else:  # Player is at the goal position
                return 0  # No movement


    # Define render method
    def render(self, mode='human'):
        if self.screen is None:
            pygame.init()
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        self.player_x, self.player_y, self.goal_x, self.goal_y = self.state
        self.screen.fill((0, 0, 0))
        RED = (255, 0, 0)
        BLUE = (0, 0, 255)
        BORDER_COLOR = (255, 255, 0)
        pygame.draw.rect(self.screen, BORDER_COLOR, (0, 0, self.screen_width, self.border_width))
        pygame.draw.rect(self.screen, BORDER_COLOR, (0, 0, self.border_width, self.screen_height))
        pygame.draw.rect(self.screen, BORDER_COLOR, (0, self.screen_height - self.border_width, self.screen_width, self.border_width))
        pygame.draw.rect(self.screen, BORDER_COLOR, (self.screen_width - self.border_width, 0, self.border_width, self.screen_height))
        pygame.draw.circle(self.screen, RED, (self.player_x, self.player_y), 10)
        pygame.draw.circle(self.screen, BLUE, (self.goal_x, self.goal_y), self.goal_radius)
        font = pygame.font.Font(None, 36)
        text = font.render("Current Score: " + str(self.score), True, (255, 255, 255))
        self.screen.blit(text, (10, 10))
        pygame.display.update()

    # Define close method
    def close(self):
        pygame.quit()

# Test the environment
test_env = IntelliGoal()
test_env.reset(0)
done = False
i = 1

while True:
    try:
        test_env.render()
        action = test_env.bestFirst()
        state, reward, done, truncated, _ = test_env.step(action)
        if done or truncated:
            print("current streak: "+str(i))
            print("current score: "+str(test_env.score))
            i += 1
            test_env.reset(0)
    except:
        print("Environment Closed")
        break

# Close the Pygame window
test_env.close()
