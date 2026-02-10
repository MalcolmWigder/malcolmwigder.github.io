import pygame
import sys
import math
import random

# Initialize Pygame
pygame.init()

# Set up the screen dimensions
screen_width, screen_height = 800, 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Fluid Worm Game with Circle Boundary")

# Define colors
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

# Worm properties
segment_size = 10  # Size of each worm segment
worm_body = [[400, 400]]  # Initial position of the worm's head
worm_color = green  # Worm color
direction = (1, 0)  # Initial direction (x, y)

# Food properties
food_color = red
food_radius = 8

# Circle boundary properties
circle_center = (400, 400)  # Center of the circle
circle_radius = 300  # Radius of the circle

# Movement properties
speed = 2  # Movement speed of the worm
clock = pygame.time.Clock()
running = True

def spawn_food():
    """Generate a new random food position strictly within the circle."""
    while True:
        # Generate a random angle and radius within the circle
        angle = random.uniform(0, 2 * math.pi)
        radius = random.uniform(0, circle_radius - food_radius)
        # Convert polar coordinates to Cartesian coordinates
        x = circle_center[0] + int(radius * math.cos(angle))
        y = circle_center[1] + int(radius * math.sin(angle))
        return [x, y]

# Initial food position
food_position = spawn_food()

def check_collision_with_self():
    """Check if the worm's head collides with its body."""
    return worm_body[0] in worm_body[1:]

def check_collision_with_food():
    """Check if the worm's head collides with the food."""
    head_x, head_y = worm_body[0]
    return math.sqrt((head_x - food_position[0]) ** 2 + (head_y - food_position[1]) ** 2) < food_radius

def check_collision_with_boundary():
    """Check if the worm's head is outside the circle boundary."""
    head_x, head_y = worm_body[0]
    distance_from_center = math.sqrt((head_x - circle_center[0]) ** 2 + (head_y - circle_center[1]) ** 2)
    return distance_from_center > circle_radius

def move_worm():
    """Move the worm in the current direction."""
    global food_position

    head_x, head_y = worm_body[0]
    new_head = [head_x + direction[0] * speed, head_y + direction[1] * speed]

    # Insert the new head position
    worm_body.insert(0, new_head)

    # Check for collision with food
    if check_collision_with_food():
        food_position = spawn_food()  # Generate new food
    else:
        worm_body.pop()  # Remove the last segment to maintain worm length
def draw_grid():
    """Draw soft Euclidean gridlines on the canvas."""
    grid_color = (50, 50, 50)  # Light gray color for the grid
    spacing = 50  # Distance between gridlines

    # Draw vertical lines
    for x in range(0, screen_width, spacing):
        pygame.draw.line(screen, grid_color, (x, 0), (x, screen_height))

    # Draw horizontal lines
    for y in range(0, screen_height, spacing):
        pygame.draw.line(screen, grid_color, (0, y), (screen_width, y))
       
# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Capture user input for direction change
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and direction != (0, 1):
        direction = (0, -1)
    if keys[pygame.K_DOWN] and direction != (0, -1):
        direction = (0, 1)
    if keys[pygame.K_LEFT] and direction != (1, 0):
        direction = (-1, 0)
    if keys[pygame.K_RIGHT] and direction != (-1, 0):
        direction = (1, 0)

    # Move the worm
    move_worm()

    # Check for collisions
    if check_collision_with_self():
        print("Game Over! You crashed into yourself.")
        running = False
    if check_collision_with_boundary():
        print("Game Over! You went outside the circle.")
        running = False

    # Clear the screen
    screen.fill(black)

    # Draw the circle boundary
    pygame.draw.circle(screen, blue, circle_center, circle_radius, 2)
    draw_grid()
    # Draw the worm
    for segment in worm_body:
        pygame.draw.circle(screen, worm_color, (int(segment[0]), int(segment[1])), segment_size // 2)

    # Draw the food
    pygame.draw.circle(screen, food_color, (food_position[0], food_position[1]), food_radius)

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
