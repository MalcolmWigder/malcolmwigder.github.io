import pygame
import math
import numpy as np
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width, screen_height = 800, 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Dynamic Curvature Snake Game")

# Colors
black = (0, 0, 0)  # Background color
white = (255, 255, 255)  # Boundary color
green = (0, 255, 0)  # Snake color
red = (255, 0, 0)  # Normal food color
blue = (0, 0, 255)  # Blue apple (hyperbolicity)
yellow = (255, 255, 0)  # Yellow apple (sphericity)
gray = (200, 200, 200)  # Grid line color

# Disk properties (Poincaré Disk)
disk_center = (400, 400)
disk_radius = 300

apple_types = {
    "normal": (red, "normal"),     # Red apple (normal effect)
    "blue": (blue, "hyperbolic"),  # Blue apple (increase hyperbolicity)
    "yellow": (yellow, "spherical")  # Yellow apple (increase sphericity)
}
current_apple_type = "normal"

K = 0  # Start with hyperbolic space (negative curvature)

# Snake properties
snake_segments = 10  # Initial number of snake segments
segment_radius = 5  # Radius of each snake segment
snake_body = [[0, 0.1 * i] for i in range(snake_segments)]  # Start near the center
snake_speed = 0.01  # Speed in hyperbolic space
snake_direction = math.pi / 2  # Start moving upward
def draw_poincare_disk():
    """Draw the Poincaré disk."""
    pygame.draw.circle(screen, white, disk_center, disk_radius, 2)  # Draw boundary
 
# Food properties
food_position = [random.uniform(-1, 1), random.uniform(-1, 1)]  # Random initial food position
while math.sqrt(food_position[0]**2 + food_position[1]**2) >= 1:
    food_position = [random.uniform(-1, 1), random.uniform(-1, 1)]  # Ensure food is inside the disk
def poincare_to_screen(x, y):
    """Convert Poincaré disk coordinates to screen coordinates."""
    screen_x = disk_center[0] + x * disk_radius
    screen_y = disk_center[1] - y * disk_radius
    return int(screen_x), int(screen_y)

def generate_apple_position(k=2):
    """
    Generate a random apple position in the Poincaré disk with radial probability.
    :param k: Steepness of the probability density function (higher makes edge apples rarer).
    :return: (x, y) position in hyperbolic coordinates.
    """
    u = random.uniform(0, 1)
    r = (1 - u**(1 / (k + 1)))**0.1  # Inverse transform sampling for radial distribution
    theta = random.uniform(0, 2 * math.pi)
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    return x, y

def geodesic_radius(r, K):
    """
    Compute the Euclidean radius of a geodesic circle for given distance and curvature.
    
    :param r: Geodesic distance.
    :param K: Curvature factor.
    :return: Euclidean radius of the circle.
    """
    if K < 0:  # Hyperbolic space
        return math.tanh(r / 2) / math.sqrt(abs(K))
    elif K > 0:  # Spherical space
        return math.tan(r / 2) / math.sqrt(K)
    else:  # Flat space (Euclidean)
        return r
    
def draw_concentric_circles(num_circles=5, max_distance=2):
    """
    Draw concentric circles representing equal distances in the curved space.
    
    :param num_circles: Number of circles to draw.
    :param max_distance: Maximum geodesic distance for the outermost circle.
    """
    for i in range(1, num_circles + 1):
        # Compute the geodesic distance for this circle
        r_h = i * (max_distance / num_circles)  # Divide the maximum distance
        r_e = geodesic_radius(r_h, K)  # Compute Euclidean radius

        # Convert to screen space
        euclidean_radius = int(r_e * disk_radius)
        
        # Skip circles that exceed the Poincaré disk boundary
        if euclidean_radius >= disk_radius:
            break

        # Draw the circle
        pygame.draw.circle(screen, gray, disk_center, euclidean_radius, 1)


def move_snake():
    """Move the snake's head in hyperbolic or spherical space and update its body."""
    global snake_body
    head_x, head_y = snake_body[0]
    dx = snake_speed * math.cos(snake_direction)
    dy = snake_speed * math.sin(snake_direction)
    r_squared = head_x**2 + head_y**2
    if K < 0:  # Hyperbolic space
        norm = (1 - r_squared) / abs(K)
    elif K > 0:  # Spherical space
        norm = (1 + r_squared) / K
    else:  # Flat space
        norm = 1

    dx *= norm
    dy *= norm
    new_head_x = head_x + dx
    new_head_y = head_y + dy
    if new_head_x**2 + new_head_y**2 >= 1 and K <= 0:
        return False
    snake_body = [[new_head_x, new_head_y]] + snake_body[:-1]
    return True

def transition_curvature(target_K, step=0.1):
    """Gradually transition the curvature factor K toward target_K."""
    global K
    if K < target_K:
        K = min(K + step, target_K)
    elif K > target_K:
        K = max(K - step, target_K)

def check_collision():
    """Check if the snake eats the food and apply the apple's effect."""
    global food_position, K, snake_body

    head_x, head_y = snake_body[0]
    food_x, food_y = food_position
    distance = math.sqrt((head_x - food_x)**2 + (head_y - food_y)**2)

    if distance < 0.05:  # Collision threshold
        apple_effect = apple_types[current_apple_type][1]  # Get the effect

        if apple_effect == "normal":
            # Normal apple: Grow the snake
            snake_body.append(snake_body[-1])
        elif apple_effect == "hyperbolic":
            # Blue apple: Increase hyperbolicity
            transition_curvature(K - 0.5)
            print("Space is now more hyperbolic: K =", K)
        elif apple_effect == "spherical":
            # Yellow apple: Increase sphericity
            transition_curvature(K + 0.5)
            print("Space is now more spherical: K =", K)

        # Respawn food
        respawn_food()

def draw_snake():
    """Draw the snake."""
    for segment in snake_body:
        x, y = poincare_to_screen(segment[0], segment[1])
        pygame.draw.circle(screen, green, (x, y), segment_radius)

def draw_food():
    """Draw the food (apple) with the color corresponding to its type."""
    global food_position, current_apple_type
    x, y = poincare_to_screen(food_position[0], food_position[1])
    color = apple_types[current_apple_type][0]  # Get the color for the current apple type
    pygame.draw.circle(screen, color, (x, y), segment_radius)
def respawn_food():
    """Generate a new food position and assign a random type."""
    global food_position, current_apple_type
    food_position = generate_apple_position(k=4)  # Place the apple
    current_apple_type = random.choice(list(apple_types.keys()))  # Randomly choose apple type

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        snake_direction += 0.1
    if keys[pygame.K_RIGHT]:
        snake_direction -= 0.1
    if not move_snake():
        print("Game Over!")
        running = False
    check_collision()
    screen.fill(black)
    draw_poincare_disk()
    draw_concentric_circles(num_circles=15, max_distance=3)
    draw_snake()
    draw_food()
    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
