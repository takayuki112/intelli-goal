import pygame
import random
import math
import random
import time

class SimEnv:

    def __init__(s):
        s.player_x = 0
        s.player_y = 0
        s.goal_x = 0
        s.goal_y = 0
        s.prev_goal_position = (0, 0)  # Previous position of the goal
        s.position_change_timer = 0  # Timer to track position changes
        s.player_speed = 0
        s.goal_speed = 1  # Initial speed of the goal
        
        s.goal_direction = (0, 0)  # Initial direction of the goal
        s.direction_change_timer = 0
        s.direction_change_interval = 60  # Interval for changing direction (in frames)
        s.constant_goal_speed_increment = 0.000
        s.level_up_goal_speed_increment = 0.0
        
        s.base_player_speed = 8
        s.player_acceleration = 0.6
        s.max_speed = 75

    def run_game(s):
        pygame.init()
        # Set up the screen
        screen_width, screen_height = 1240, 800
        screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Pakadam Pakadai")

        #------------TO USE EXTERNAL ASSET IMAGES-----------------------------------------------------
        # Load images
        # bg_image = pygame.image.load("./assets/bg.jpg").convert_alpha()
        # ufo_image = pygame.image.load("./goal.png").convert_alpha()
        # player_image = pygame.image.load("./agent.png").convert_alpha()
        
        # # # Scale images 
        # bg_image = pygame.transform.scale(bg_image, (screen_width, screen_height))  # Scale to screen size
        # player_image = pygame.transform.scale(player_image, (30, 35))  # Scale to 20x20 pixels
        # ufo_image = pygame.transform.scale(ufo_image, (65, 40))  # Scale to 40x40 pixels
        
        # Define colors
        RED = (255, 0, 0)
        BLUE = (0, 0, 255)
        BORDER_COLOR = (255, 255, 255)

        # Border dimensions
        border_width = 10

        # Initialize player position
        s.player_x, s.player_y = screen_width // 2, screen_height // 2

        # Initialize goal position
        s.goal_x, s.goal_y = random.randint(border_width, screen_width - border_width), random.randint(border_width, screen_height - border_width)
        s.goal_radius = 20

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Clear the screen
            screen.fill((0, 0, 0))
            # screen.blit(bg_image, (0, 0))

            # Draw the border
            pygame.draw.rect(screen, BORDER_COLOR, (0, 0, screen_width, border_width))
            pygame.draw.rect(screen, BORDER_COLOR, (0, 0, border_width, screen_height))
            pygame.draw.rect(screen, BORDER_COLOR, (0, screen_height - border_width, screen_width, border_width))
            pygame.draw.rect(screen, BORDER_COLOR, (screen_width - border_width, 0, border_width, screen_height))

            # Draw the red dot
            pygame.draw.circle(screen, RED, (s.player_x, s.player_y), 10)

            # Draw the blue dot
            pygame.draw.circle(screen, BLUE, (s.goal_x, s.goal_y), s.goal_radius)
            
            # Use assets
            # screen.blit(player_image, (s.player_x - player_image.get_width() // 2, s.player_y - player_image.get_height() // 2))
            # screen.blit(ufo_image, (s.goal_x - ufo_image.get_width() // 2, s.goal_y - ufo_image.get_height() // 2))
            
            pygame.display.update()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and s.player_x > border_width:
                s.player_x -= s.player_speed
            if keys[pygame.K_RIGHT] and s.player_x < screen_width - border_width:
                s.player_x += s.player_speed
            if keys[pygame.K_UP] and s.player_y > border_width:
                s.player_y -= s.player_speed
            if keys[pygame.K_DOWN] and s.player_y < screen_height - border_width:
                s.player_y += s.player_speed
            # Accelerate the player
            if keys[pygame.K_SPACE]:
                # s.player_speed += 2
                s.player_speed = min(s.player_speed+2, s.max_speed)
            else:
                s.player_speed = s.base_player_speed

#####################################################################################################
#----------UNCOMMENT FOR DYANMIC GOAL MOVEMENT -----------------------------------------------------
#####################################################################################################

            # # Update goal position and direction
            # if s.direction_change_timer <= 0:
            #     # Change direction
            #     s.goal_direction = (random.randint(-2, 2), random.randint(-2, 2))
            #     # Reset direction change timer
            #     s.direction_change_timer = s.direction_change_interval
            # else:
            #     # Continue in the current direction
            #     s.goal_x += s.goal_direction[0] * s.goal_speed
            #     s.goal_y += s.goal_direction[1] * s.goal_speed
            #     s.direction_change_timer -= 1

            # # Ensure the goal stays within the screen bounds with a margin inside the borders
            # goal_margin = 25  # Adjust this value as needed
            # s.goal_x = max(border_width + goal_margin, min(s.goal_x, screen_width - border_width - goal_margin))
            # s.goal_y = max(border_width + goal_margin, min(s.goal_y, screen_height - border_width - goal_margin))

            # # Increase goal speed gradually
            # s.goal_speed += s.constant_goal_speed_increment

            # # Check if the goal position is changing
            # current_goal_position = (s.goal_x, s.goal_y)
            # if current_goal_position == s.prev_goal_position:
            #     # Increment the timer if the position remains the same
            #     s.position_change_timer += 1
            # else:
            #     # Reset the timer if the position changes
            #     s.position_change_timer = 0
            #     # Update the previous position
            #     s.prev_goal_position = current_goal_position

            # # Check if the goal is stuck and change direction if necessary
            # if s.position_change_timer >= 3:  #threshold as needed
            #     s.goal_direction = (random.randint(-2, 2), random.randint(-2, 2))
            #     s.position_change_timer = 0
            
#####################################################################################################            
#----------DYANMIC GOAL MOVEMENT SECTION ENDS-----------------------------------------------------            
#####################################################################################################
            
            # Calculate the distance between player and goal
            distance = math.sqrt((s.player_x - s.goal_x) ** 2 + (s.player_y - s.goal_y) ** 2)

            # Check if the red dot touches the border
            if s.player_x <= border_width or s.player_x >= screen_width - border_width or s.player_y <= border_width or s.player_y >= screen_height - border_width:
                s.player_x, s.player_y = screen_width // 2, screen_height // 2

            # Check if the goal is reached within a certain range
            if distance < s.goal_radius:
                s.goal_x = random.randint(border_width - 15, screen_width - border_width - 15)
                s.goal_y = random.randint(border_width - 15, screen_height - border_width - 15)
                # Level Up
                s.goal_speed += s.level_up_goal_speed_increment

                

            pygame.time.delay(30)

        pygame.quit()

    def get_state(s):
        return s.state

    def do_actions(s, actions):
        print(actions)
        if actions[0] == 1:  # up
            s.player_y -= s.player_speed
        if actions[1] == 1:  # down
            s.player_y += s.player_speed
        if actions[2] == 1:  # left
            s.player_x -= s.player_speed
        if actions[3] == 1:  # right
            s.player_x += s.player_speed
        if actions[4] == 1:  # space
            s.player_speed += s.player_acceleration

        time.sleep(0.1)


if __name__ == "__main__":
    navEnv = SimEnv()
    navEnv.run_game()