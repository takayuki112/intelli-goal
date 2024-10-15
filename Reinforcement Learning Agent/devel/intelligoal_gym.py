import pygame
import gym 
from gym import spaces
import numpy as np
import math
import random

class IntelliGoal(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(s):
        super(IntelliGoal, s).__init__()
        
        s.screen_width = 1240
        s.screen_height = 800
        s.border_width = 10
        s.screen = None
        
        s.goal_radius = 20
        s.player_radius = 10
        
        s.player_speed = 1
        
        # State information
        s.player_x = 0
        s.player_y = 0
        s.goal_x = 0
        s.goal_y = 0
        s.state = np.array([s.player_x, s.player_y, s.goal_x, s.goal_y])
        s.prev_distance = math.sqrt((s.player_x - s.goal_x) ** 2 + (s.player_y - s.goal_y) ** 2)
        s.done = False
        s.reward = 0
        
        
        # State and Action spaces
        s.action_space = spaces.Discrete(5) # 0: No movement, 1: Up, 2: Down, 3: Left, 4: Right
        # observation space = [player_x, player_y, goal_x, goal_y]
        s.observation_space = spaces.Box(
            low=np.array([0, 0, 0, 0]), 
            high=np.array([s.screen_width, s.screen_height, s.screen_width, s.screen_height]), 
            dtype=np.float32
        )
    
    def reset(s):
        s.player_x = s.screen_width // 2
        s.player_y = s.screen_height // 2
        
        s.goal_x, s.goal_y = s.respawn_goal()
        
        s.reward = 0
        s.done = False
        s.state = np.array([s.player_x, s.player_y, s.goal_x, s.goal_y])
        return s.state
    
    def respawn_goal(s):
        s.goal_x = s.player_x + random.randint(-300, 300)
        s.goal_y = s.player_y + random.randint(-300, 300)
        
        # clip the goal to the screen
        offset = s.border_width + s.goal_radius
        s.goal_x = min( max(s.goal_x, offset), s.screen_width - offset)
        s.goal_y = min( max(s.goal_y, offset), s.screen_height - offset)
        
        pygame.time.wait(120)
        
        s.prev_distance = math.sqrt((s.player_x - s.goal_x) ** 2 + (s.player_y - s.goal_y) ** 2)
        
        return s.goal_x, s.goal_y
        
    def step(s, action):
        #################
        #do more here
        #################
        
        s.do_action(action)
        # s.reward -= 0.01
        
        return s.state, s.reward, s.done, {}
        
   
    def do_action(s, action):
        if not s.action_space.contains(action):
            print("Invalid Action")
        
        s.prev_distance = math.sqrt((s.player_x - s.goal_x) ** 2 + (s.player_y - s.goal_y) ** 2)
        
        s.player_x += (action == 4)*s.player_speed - (action == 3)*s.player_speed 
        s.player_y += (action == 2)*s.player_speed - (action == 1)*s.player_speed
        
        # Distance between player and goal
        distance = math.sqrt((s.player_x - s.goal_x) ** 2 + (s.player_y - s.goal_y) ** 2)

        # Check if the red dot touches the border
        if s.player_x not in range(s.border_width, s.screen_width - s.border_width) or s.player_y not in range(s.border_width, s.screen_height - s.border_width):
            s.player_x, s.player_y = s.screen_width // 2, s.screen_height // 2

        # Check if the goal is reached within a certain range
        if distance < s.goal_radius + s.player_radius:
            s.goal_x, s.goal_y = s.respawn_goal()
            s.reward += 100
            print("reward: ", s.reward)
            s.reset()
            s.done = True
            
    
        s.state = np.array([s.player_x, s.player_y, s.goal_x, s.goal_y])
        
        if s.prev_distance > distance:
            s.reward += 10
        if s.prev_distance < distance:
            s.reward -= 15
     
    
    def keyboard_input(s):
        keys = pygame.key.get_pressed()
        # 1: Up, 2: Down, 3: Left, 4: Right
        if keys[pygame.K_UP]:
            return 1
        if keys[pygame.K_DOWN]:
            return 2
        if keys[pygame.K_LEFT]:
            return 3
        if keys[pygame.K_RIGHT]:
            return 4
        return 0
        
    
    def render(s, mode = 'human'):
        if s.screen == None:
            pygame.init()
            s.screen = pygame.display.set_mode((s.screen_width, s.screen_height))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        s.player_x, s.player_y, s.goal_x, s.goal_y = s.state
        
        s.screen.fill((0, 0, 0))
        RED = (255, 0, 0)
        BLUE = (0, 0, 255)
        BORDER_COLOR = (255, 255, 0)
        
        # Draw the border
        pygame.draw.rect(s.screen, BORDER_COLOR, (0, 0, s.screen_width, s.border_width))
        pygame.draw.rect(s.screen, BORDER_COLOR, (0, 0, s.border_width, s.screen_height))
        pygame.draw.rect(s.screen, BORDER_COLOR, (0, s.screen_height - s.border_width, s.screen_width, s.border_width))
        pygame.draw.rect(s.screen, BORDER_COLOR, (s.screen_width - s.border_width, 0, s.border_width, s.screen_height))

        # Draw the red dot
        pygame.draw.circle(s.screen, RED, (s.player_x, s.player_y), 10)

        # Draw the blue dot
        pygame.draw.circle(s.screen, BLUE, (s.goal_x, s.goal_y), s.goal_radius)
        
        #Display Reward on pygame screen
        font = pygame.font.Font(None, 36)
        text = font.render("Reward: " + str(round(s.reward, 2)), True, (255, 255, 255))
        s.screen.blit(text, (10, 10))
        
        pygame.display.update()
    
    def close(s):
        pygame.quit()
        
        
        
if __name__ == "__main__":        
        
    # Test Env with keyboard input actions
    env = IntelliGoal()
    env.reset()
    done = False
    while not done:
        env.render()
        action = env.keyboard_input()
        state, reward, done, _ = env.step(action)        

        
        