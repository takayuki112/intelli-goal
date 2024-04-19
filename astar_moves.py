import pygame
import numpy as np
import math
import random

class IntelliGoal:
    def _init_(s):
        s.screen_width = 1240
        s.screen_height = 800
        s.border_width = 10
        s.screen = None
        
        s.goal_radius = 20
        s.player_radius = 10
        
        s.player_speed = 1
        
        # State information
        s.player_x = 0.0
        s.player_y = 0.0
        s.goal_x = 0.0
        s.goal_y = 0.0
        s.state = np.array([s.player_x, s.player_y, s.goal_x, s.goal_y])
        s.prev_distance = math.sqrt((s.player_x - s.goal_x) * 2 + (s.player_y - s.goal_y) * 2)
        s.reward = 0
        
        s.done = False
        s.goal_spawn_range = 300
        
        s.obstacles = []
        s.obst_ids = set()
        s.n_obstacles = 20
        s.scale_factor = 20
        s.path = None
        s.initialize_obstacles()

    def calculate_direction(s, next_pos):
        # Calculate the direction to move based on the next position in the path
        x_diff = next_pos[0] - s.player_x
        y_diff = next_pos[1] - s.player_y

        if x_diff > 0:
            return 4  # Right
        elif x_diff < 0:
            return 3  # Left
        elif y_diff > 0:
            return 2  # Down
        elif y_diff < 0:
            return 1  # Up
        return 0


    def initialize_obstacles(s):
        s.obstacles = []
        s.obst_ids = set()
        for i in range(s.n_obstacles):
            x = random.randint(0, s.screen_width // s.scale_factor) * s.scale_factor
            y = random.randint(0, s.screen_height // s.scale_factor) * s.scale_factor
            
            while (x, y) in s.obst_ids:
                x = random.randint(0, s.screen_width // s.scale_factor) * s.scale_factor
                y = random.randint(0, s.screen_height // s.scale_factor) * s.scale_factor
            s.obstacles.append((x, y))
            s.obst_ids.add((x // s.scale_factor, y // s.scale_factor))

    def reset(s):
        s.player_x = s.screen_width // 2
        s.player_y = s.screen_height // 2
        s.goal_x, s.goal_y = s.respawn_goal()
        s.reward = 0
        s.state = np.array([s.player_x, s.player_y, s.goal_x, s.goal_y])
        s.done = False
        s.initialize_obstacles()
        return s.state

    def respawn_goal(s):
        offset = s.border_width + s.goal_radius
        s.goal_x = s.player_x + random.randint(-s.goal_spawn_range, s.goal_spawn_range)
        s.goal_y = s.player_y + random.randint(-s.goal_spawn_range, s.goal_spawn_range)
        s.goal_x = min(max(s.goal_x, offset), s.screen_width - offset)
        s.goal_y = min(max(s.goal_y, offset), s.screen_height - offset)
        s.prev_distance = math.sqrt((s.player_x - s.goal_x) * 2 + (s.player_y - s.goal_y) * 2)
        return s.goal_x, s.goal_y

    def step(s, action):
        
        if action == 0 and s.path:
            action = s.follow_path()
        
        s.do_action(action)
        return s.state, s.reward, s.done

    def do_action(s, action):
        dx = (action == 4) * s.player_speed - (action == 3) * s.player_speed
        dy = (action == 2) * s.player_speed - (action == 1) * s.player_speed
        new_x = s.player_x + dx
        new_y = s.player_y + dy

        # Check collision with obstacles
        obstacle_collision = False
        for x, y in s.obstacles:
            if new_x in range(x - s.player_radius, x + 20 + s.player_radius) and new_y in range(y - s.player_radius, y + 20 + s.player_radius):
                obstacle_collision = True
                break

        if not obstacle_collision:
            s.player_x = new_x
            s.player_y = new_y

        s.state = np.array([s.player_x, s.player_y, s.goal_x, s.goal_y])

        # Distance to goal
        distance = math.sqrt((s.player_x - s.goal_x) * 2 + (s.player_y - s.goal_y) * 2)
        if s.player_x not in range(s.border_width, s.screen_width - s.border_width) or s.player_y not in range(s.border_width, s.screen_height - s.border_width):
            s.player_x, s.player_y = s.screen_width // 2, s.screen_height // 2
            s.done = True

        if distance < s.goal_radius + s.player_radius:
            s.goal_x, s.goal_y = s.respawn_goal()
            s.done = True
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

    def render(s, mode='human'):
        if s.screen is None:
            pygame.init()
            s.screen = pygame.display.set_mode((s.screen_width, s.screen_height))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        s.screen.fill((0, 0, 0))
        RED = (255, 0, 0)
        BLUE = (0, 0, 255)
        GREEN = (0, 255, 0)
        BORDER_COLOR = (255, 255, 0)

        # Draw border
        pygame.draw.rect(s.screen, BORDER_COLOR, (0, 0, s.screen_width, s.border_width))
        pygame.draw.rect(s.screen, BORDER_COLOR, (0, 0, s.border_width, s.screen_height))
        pygame.draw.rect(s.screen, BORDER_COLOR, (0, s.screen_height - s.border_width, s.screen_width, s.border_width))
        pygame.draw.rect(s.screen, BORDER_COLOR, (s.screen_width - s.border_width, 0, s.border_width, s.screen_height))

        # Draw player and goal
        pygame.draw.circle(s.screen, RED, (s.player_x, s.player_y), 10)
        pygame.draw.circle(s.screen, BLUE, (s.goal_x, s.goal_y), s.goal_radius)

        # Draw obstacles
        for x, y in s.obstacles:
            pygame.draw.rect(s.screen, (255, 255, 255), (x, y, 20, 20))

        # Draw path
        path = s.find_a_star_path()
        if path is not None:
            for pos in path:
                pos = (pos[0] + s.scale_factor // 2, pos[1] + s.scale_factor // 2)
                pygame.draw.circle(s.screen, GREEN, pos, 1)

        # Display reward
        font = pygame.font.Font(None, 36)
        text = font.render("Reward: " + str(round(s.reward, 5)), True, (255, 255, 255))
        s.screen.blit(text, (10, 10))

        pygame.display.update()

    def close(s):
        pygame.quit()

    def find_a_star_path(s):
        grid = Grid(s.screen_width // s.scale_factor, s.screen_height // s.scale_factor, s.obst_ids)
        start = (s.player_x // s.scale_factor, s.player_y // s.scale_factor)
        goal = (s.goal_x // s.scale_factor, s.goal_y // s.scale_factor)
        s.path = reconstruct_path(a_star_search(grid, start, goal), start, goal)
        # Scale path back to screen coordinates
        s.path = [(x * s.scale_factor, y * s.scale_factor) for x, y in s.path]
        return s.path
    
    def find_closest_path_index(s):
        # This function will find the closest path node to the current player position
        min_distance = float('inf')
        closest_index = None
        for index, (px, py) in enumerate(s.path):
            distance = math.sqrt((s.player_x - px) * 2 + (s.player_y - py) * 2)
            if distance < min_distance:
                min_distance = distance
                closest_index = index
        return closest_index
    
    def follow_path(s):
        if not s.path:
            return 0  # No path to follow

        current_index = s.find_closest_path_index()
        if current_index is None:
            return 0  # Path is empty or no close index found

        # Check if we are at the last node
        if current_index == len(s.path) - 1:
            s.path = None  # Clear the path if at the goal
            return 0  # No further action required
        
        # Get the next position in the path
        next_pos = s.path[current_index + 1]

        # Check if the next position leads to a collision with an obstacle
        if s.will_collide_with_obstacle(next_pos):
            # Generate a new path that avoids the obstacle
            s.generate_new_path()
            return 0  # No further action required
    
        return s.calculate_direction(next_pos)

    def will_collide_with_obstacle(s, next_pos):
        # Check if moving to next_pos will lead to a collision with an obstacle
        for x, y in s.obstacles:
            if next_pos[0] in range(x - s.player_radius, x + 20 + s.player_radius) and next_pos[1] in range(y - s.player_radius, y + 20 + s.player_radius):
                return True
        return False

    def generate_new_path(s):
        # Generate a new path that avoids the obstacle
        # You can use any pathfinding algorithm here to generate the new path
        # For simplicity, let's just generate a random path here
        new_goal_x = random.randint(s.border_width, s.screen_width - s.border_width)
        new_goal_y = random.randint(s.border_width, s.screen_height - s.border_width)
        s.goal_x, s.goal_y = new_goal_x, new_goal_y
        s.path = [(s.player_x, s.player_y), (new_goal_x, new_goal_y)]


class Grid:
    def _init_(s, width, height, obstacles):
        s.width = width
        s.height = height
        s.obstacles = obstacles

    def in_bounds(s, id):
        (x, y) = id
        return 0 <= x < s.width and 0 <= y < s.height

    def passable(s, id):
        (x, y) = id
        # Check the current cell and its immediate neighbors
        neighbors_to_check = [(x, y), (x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        for nx, ny in neighbors_to_check:
            if (nx, ny) in s.obstacles:
                return False
        return True

    def neighbors(s, id):
        (x, y) = id
        results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
        results = filter(s.in_bounds, results)
        results = filter(s.passable, results)
        return results

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star_search(grid, start, goal):
    from queue import PriorityQueue
    frontier = PriorityQueue()
    frontier.put((0, start))
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()[1]

        if current == goal:
            break

        for next in grid.neighbors(current):
            new_cost = cost_so_far[current] + 1  # Assumes cost between neighboring nodes is 1
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                frontier.put((priority, next))
                came_from[next] = current

    return came_from

def reconstruct_path(came_from, start, goal):
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from.get(current)
    path.append(start)  # optional
    path.reverse()  # optional
    return path

# Test Env with keyboard input actions
test_env = IntelliGoal()
# test_env.reset()
done = False
i = 1

test_env.initialize_obstacles()
while True:
    test_env.render()
    action = test_env.keyboard_input()
    state, reward, done = test_env.step(action)
    if done:
        print("Reward at step - ", i, " : ", round(reward, 5))
        i += 1
        test_env.reset()