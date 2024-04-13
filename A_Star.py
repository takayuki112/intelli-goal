import pygame
import random
import math
import time
import queue

class NavEnv:

    def __init__(self):
        self.player_x = 0
        self.player_y = 0
        self.goal_x = 0
        self.goal_y = 0
        self.player_speed = 0
        self.goal_speed = 1
        self.goal_direction = (0, 0)
        self.constant_goal_speed_increment = 0.002
        self.level_up_goal_speed_increment = 0.2
        self.base_player_speed = 8
        self.player_acceleration = 0.6
        self.max_speed = 75

    def run_game(self):
        pygame.init()
        screen_width, screen_height = 1240, 800
        screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Pakadam Pakadai")
        RED = (255, 0, 0)
        BLUE = (0, 0, 255)
        BORDER_COLOR = (255, 255, 255)
        border_width = 10
        self.player_x, self.player_y = screen_width // 2, screen_height // 2
        self.goal_x, self.goal_y = random.randint(border_width, screen_width - border_width), random.randint(border_width, screen_height - border_width)
        self.goal_radius = 20
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            screen.fill((0, 0, 0))
            pygame.draw.rect(screen, BORDER_COLOR, (0, 0, screen_width, border_width))
            pygame.draw.rect(screen, BORDER_COLOR, (0, 0, border_width, screen_height))
            pygame.draw.rect(screen, BORDER_COLOR, (0, screen_height - border_width, screen_width, border_width))
            pygame.draw.rect(screen, BORDER_COLOR, (screen_width - border_width, 0, border_width, screen_height))
            pygame.draw.circle(screen, RED, (self.player_x, self.player_y), 10)
            pygame.draw.circle(screen, BLUE, (self.goal_x, self.goal_y), self.goal_radius)
            pygame.display.update()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and self.player_x > border_width:
                self.player_x -= self.player_speed
            if keys[pygame.K_RIGHT] and self.player_x < screen_width - border_width:
                self.player_x += self.player_speed
            if keys[pygame.K_UP] and self.player_y > border_width:
                self.player_y -= self.player_speed
            if keys[pygame.K_DOWN] and self.player_y < screen_height - border_width:
                self.player_y += self.player_speed
            if keys[pygame.K_SPACE]:
                self.player_speed = min(self.player_speed+2, self.max_speed)
            else:
                self.player_speed = self.base_player_speed

            self.update_goal_position(screen_width, screen_height, border_width)

            distance = math.sqrt((self.player_x - self.goal_x) ** 2 + (self.player_y - self.goal_y) ** 2)
            if self.player_x <= border_width or self.player_x >= screen_width - border_width or self.player_y <= border_width or self.player_y >= screen_height - border_width:
                self.player_x, self.player_y = screen_width // 2, screen_height // 2

            if distance < self.goal_radius:
                self.goal_x = random.randint(border_width - 15, screen_width - border_width - 15)
                self.goal_y = random.randint(border_width - 15, screen_height - border_width - 15)
                self.goal_speed += self.level_up_goal_speed_increment
            pygame.time.delay(30)

        pygame.quit()

    def get_state(self):
        return (self.player_x, self.player_y, self.goal_x, self.goal_y)

    def update_goal_position(self, screen_width, screen_height, border_width):
        # Update goal position and direction
        goal_margin = 25
        if self.direction_change_timer <= 0:
            self.goal_direction = (random.randint(-2, 2), random.randint(-2, 2))
            self.direction_change_timer = self.direction_change_interval
        else:
            self.goal_x += self.goal_direction[0] * self.goal_speed
            self.goal_y += self.goal_direction[1] * self.goal_speed
            self.direction_change_timer -= 1
        self.goal_x = max(border_width + goal_margin, min(self.goal_x, screen_width - border_width - goal_margin))
        self.goal_y = max(border_width + goal_margin, min(self.goal_y, screen_height - border_width - goal_margin))
        self.goal_speed += self.constant_goal_speed_increment

    def do_actions(self, actions):
        if actions[0] == 1:  # up
            self.player_y -= self.player_speed
        if actions[1] == 1:  # down
            self.player_y += self.player_speed
        if actions[2] == 1:  # left
            self.player_x -= self.player_speed
        if actions[3] == 1:  # right
            self.player_x += self.player_speed
        if actions[4] == 1:  # space
            self.player_speed += self.player_acceleration
        time.sleep(0.1)

    def heuristic(self, state, goal):
        # A simple heuristic: Manhattan distance between player and goal
        return abs(state[0] - goal[0]) + abs(state[1] - goal[1])

    def astar_search(self, start_state, goal_state):
        frontier = queue.PriorityQueue()
        frontier.put(start_state, 0)
        came_from = {}
        cost_so_far = {}
        came_from[start_state] = None
        cost_so_far[start_state] = 0

        while not frontier.empty():
            current_state = frontier.get()

            if current_state == goal_state:
                break

            for action in self.get_possible_actions():
                next_state = self.apply_action(current_state, action)
                new_cost = cost_so_far[current_state] + 1  # Assuming each step costs 1

                if next_state not in cost_so_far or new_cost < cost_so_far[next_state]:
                    cost_so_far[next_state] = new_cost
                    priority = new_cost + self.heuristic(goal_state, next_state)
                    frontier.put(next_state, priority)
                    came_from[next_state] = current_state

        path = self.reconstruct_path(came_from, start_state, goal_state)
        return path

    def get_possible_actions(self):
        # Define possible actions here
        return [(0, -1), (0, 1), (-1, 0), (1, 0)]

    def apply_action(self, state, action):
        # Apply the action to the state and return the new state
        return (state[0] + action[0], state[1] + action[1], state[2], state[3])

    def reconstruct_path(self, came_from, start_state, goal_state):
        current_state = goal_state
        path = []
        while current_state != start_state:
            path.append(current_state)
            current_state = came_from[current_state]
        path.append(start_state)
        path.reverse()
        return path

if __name__ == "__main__":
    navEnv = NavEnv()
    start_state = navEnv.get_state()
    goal_state = (navEnv.goal_x, navEnv.goal_y)
    path = navEnv.astar_search(start_state, goal_state)
    for state in path:
        actions = navEnv.get_actions_for_state(start_state, state)
        navEnv.do_actions(actions)
