import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("AI Mini-Project")

# Define colors
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Define ball properties
BALL_RADIUS = 20

# Define initial positions
red_ball_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
blue_ball_pos = [random.randint(BALL_RADIUS, SCREEN_WIDTH - BALL_RADIUS), random.randint(BALL_RADIUS, SCREEN_HEIGHT - BALL_RADIUS)]

# Define initial speeds for blue ball
blue_ball_speed_x = random.randint(-3, 3)
blue_ball_speed_y = random.randint(-3, 3)

# Define initial speed for red ball
red_ball_speed = 2

clock = pygame.time.Clock()

# Define a function to calculate the heuristic (Manhattan distance)
def heuristic(node, goal):
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

# Define the A* algorithm
def astar(start, goal, grid):
    open_set = [start]
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        current = min(open_set, key=lambda x: f_score.get(x, float('inf')))
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        open_set.remove(current)
        for neighbor in get_neighbors(current, grid):
            tentative_g_score = g_score[current] + 1  # Assuming each move has a cost of 1
            if tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                if neighbor not in open_set:
                    open_set.append(neighbor)

    return None  # No path found

# Define a function to get valid neighbors of a cell
def get_neighbors(cell, grid):
    neighbors = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            neighbor = (cell[0] + dx, cell[1] + dy)
            if 0 <= neighbor[0] < len(grid) and 0 <= neighbor[1] < len(grid[0]) and grid[neighbor[0]][neighbor[1]] == 0:
                neighbors.append(neighbor)
    return neighbors

iteration = 0

# Main loop
running = True
while running and iteration < 6:

    iteration += 1

    # Reset positions
    red_ball_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
    blue_ball_pos = [random.randint(BALL_RADIUS, SCREEN_WIDTH - BALL_RADIUS), random.randint(BALL_RADIUS, SCREEN_HEIGHT - BALL_RADIUS)]

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    blue_ball_speed_x *= 1.5
    blue_ball_speed_y *= 1.5

    while True:  # Inner loop for a single chase session
        screen.fill((0, 0, 0))

        # Update blue ball position based on velocity
        blue_ball_pos[0] += blue_ball_speed_x
        blue_ball_pos[1] += blue_ball_speed_y

        # Ensure blue ball stays within the frame
        if blue_ball_pos[0] < BALL_RADIUS or blue_ball_pos[0] > SCREEN_WIDTH - BALL_RADIUS:
            blue_ball_speed_x *= -1
        if blue_ball_pos[1] < BALL_RADIUS or blue_ball_pos[1] > SCREEN_HEIGHT - BALL_RADIUS:
            blue_ball_speed_y *= -1

        # Calculate path using A*
        start = (int(red_ball_pos[0]) // BALL_RADIUS, int(red_ball_pos[1]) // BALL_RADIUS)
        goal = (int(blue_ball_pos[0]) // BALL_RADIUS, int(blue_ball_pos[1]) // BALL_RADIUS)
        grid = [[0] * (SCREEN_WIDTH // BALL_RADIUS) for _ in range(SCREEN_HEIGHT // BALL_RADIUS)]
        path = astar(start, goal, grid)

        # Move red ball towards the blue ball's direction
        if path:
            next_cell = path[1] if len(path) > 1 else path[0]
            next_pos = (next_cell[0] * BALL_RADIUS + BALL_RADIUS // 2, next_cell[1] * BALL_RADIUS + BALL_RADIUS // 2)
            dx = next_pos[0] - red_ball_pos[0]
            dy = next_pos[1] - red_ball_pos[1]
        else:
            dx = blue_ball_pos[0] - red_ball_pos[0]
            dy = blue_ball_pos[1] - red_ball_pos[1]

        # Move the red ball towards the blue ball's direction
        distance = ((dx) * 2 + (dy) * 2) ** 0.5
        if distance > 0:
            move_x = min(red_ball_speed, distance) * dx / distance
            move_y = min(red_ball_speed, distance) * dy / distance
            red_ball_pos[0] += move_x
            red_ball_pos[1] += move_y

        # Draw balls
        pygame.draw.circle(screen, RED, (int(red_ball_pos[0]), int(red_ball_pos[1])), BALL_RADIUS)
        pygame.draw.circle(screen, BLUE, (int(blue_ball_pos[0]), int(blue_ball_pos[1])), BALL_RADIUS)

        # Update the display
        pygame.display.flip()

        # Check for collision
        distance = ((red_ball_pos[0] - blue_ball_pos[0]) * 2 + (red_ball_pos[1] - blue_ball_pos[1]) * 2) ** 0.5
        if distance < BALL_RADIUS * 2:
            break  # Break inner loop if collision occurs

        # Cap the frame rate
        clock.tick(60)

pygame.quit()