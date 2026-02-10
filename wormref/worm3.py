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
pygame.display.set_caption("Hyperbolic Snake Game with Grid")

# Colors
black = (0, 0, 0)  # Background color
white = (255, 255, 255)  # Boundary color
green = (0, 255, 0)  # Snake color
red = (255, 0, 0)  # Food color
gray = (200, 200, 200)  # Grid line color

# Disk properties (Poincaré Disk)
disk_center = (400, 400)
disk_radius = 300

# Hyperbolic Snake properties
snake_segments = 10  # Initial number of snake segments
segment_radius = 5  # Radius of each snake segment
snake_body = [[0, 0.1 * i] for i in range(snake_segments)]  # Start near the center
snake_speed = 0.02  # Speed in hyperbolic space
snake_direction = math.pi / 2  # Start moving upward

# Food properties
food_position = [random.uniform(-1, 1), random.uniform(-1, 1)]  # Random hyperbolic coordinates
while math.sqrt(food_position[0]**2 + food_position[1]**2) >= 1:
    food_position = [random.uniform(-1, 1), random.uniform(-1, 1)]  # Ensure food is inside the disk

def poincare_to_screen(x, y):
    """Convert Poincaré disk coordinates to screen coordinates."""
    screen_x = disk_center[0] + x * disk_radius
    screen_y = disk_center[1] - y * disk_radius
    return int(screen_x), int(screen_y)


def draw_poincare_disk():
    """Draw the Poincaré disk."""
    pygame.draw.circle(screen, white, disk_center, disk_radius, 2)  # Draw boundary
    
def draw_ortho(theta1, theta2):
    """
    Compute the center and radius of a circle orthogonal to the unit circle
    and passing through two points specified by angles theta1 and theta2.
    Draw only the parts of the circle inside the Poincaré disk, with dimming.
    """
    # Convert angles to points on the unit circle
    P1 = np.array([np.cos(theta1), np.sin(theta1)])
    P2 = np.array([np.cos(theta2), np.sin(theta2)])

    # Midpoint of P1 and P2
    midpoint = (P1 + P2) / 2

    # Perpendicular bisector direction (rotated 90 degrees)
    perp_direction = np.array([-(P2[1] - P1[1]), P2[0] - P1[0]])
    perp_direction = perp_direction / np.linalg.norm(perp_direction)  # Normalize

    # Solve for the circle center along the perpendicular bisector
    t = np.sqrt(1 - np.linalg.norm(midpoint)**2)  # Distance to center
    center1 = midpoint + t * perp_direction
    center2 = midpoint - t * perp_direction

    # Choose the center that satisfies the orthogonality condition
    if np.linalg.norm(center1)**2 - 1 > 0:
        center = center1
    else:
        center = center2

    # Compute the radius
    radius = np.sqrt(center[0]**2 + center[1]**2 - 1)

    # Convert center and radius to screen coordinates
    screen_center = poincare_to_screen(center[0], center[1])

    # Generate points on the circle and draw only inside the disk
    theta = np.linspace(0, 2 * np.pi, 500)
    for i in range(len(theta) - 1):
        # Calculate two consecutive points on the circle
        x1 = center[0] + radius * np.cos(theta[i])
        y1 = center[1] + radius * np.sin(theta[i])
        x2 = center[0] + radius * np.cos(theta[i + 1])
        y2 = center[1] + radius * np.sin(theta[i + 1])

        # Skip points outside the disk
        if x1**2 + y1**2 > 1 or x2**2 + y2**2 > 1:
            continue

        # Dim brightness based on distance from the center
        brightness = int(255 * (1 - np.sqrt(x1**2 + y1**2)))
        dim_color = (brightness, brightness, brightness)

        # Draw the line segment
        pygame.draw.line(screen, dim_color, poincare_to_screen(x1, y1), poincare_to_screen(x2, y2), 1)

def fractal(iterations, base_angles=None):
    """
    Generate and draw a fractal pattern of orthogonal circles.

    :param iterations: Number of fractal iterations.
    :param base_angles: Starting angles for the circles.
    """
    if base_angles is None:
        base_angles = [(0, 2 * np.pi)]  # Initial angles

    for _ in range(iterations):
        new_angles = []
        for theta1, theta2 in base_angles:
            # Draw the orthogonal circle for the current angles
            draw_ortho(theta1, theta2)

            # Create 90-degree intervals between theta1 and theta2
            angle_step = (theta2 - theta1) / 4  # Divide into 4 parts (90 degrees each)
            for i in range(4):
                sub_theta1 = theta1 + i * angle_step
                sub_theta2 = theta1 + (i + 1) * angle_step
                new_angles.append((sub_theta1, sub_theta2))

        # Update base_angles for the next iteration
        base_angles = new_angles



def draw_hyperbolic_grid():
    """Draw grid lines for the Poincaré disk."""
    # Radial geodesics (lines emanating from the center)
    for theta in range(0, 360, 90):  # Every 30 degrees
        angle = math.radians(theta)
        end_x = math.cos(angle)
        end_y = math.sin(angle)
        pygame.draw.line(screen, gray, poincare_to_screen(0, 0), poincare_to_screen(end_x, end_y), 1)

    
    iterations = 3
    fractal(iterations)

def move_snake():
    """Move the snake's head in hyperbolic space and update its body."""
    global snake_body

    # Get current head position
    head_x, head_y = snake_body[0]

    # Move head along the current direction
    dx = snake_speed * math.cos(snake_direction)
    dy = snake_speed * math.sin(snake_direction)

    # Apply hyperbolic metric to ensure movement respects the Poincaré disk
    norm = 1 - (head_x**2 + head_y**2)
    dx *= norm**2
    dy *= norm**2

    # New head position
    new_head_x = head_x + dx
    new_head_y = head_y + dy

    # Check if the new head position is still inside the disk
    if new_head_x**2 + new_head_y**2 >= 1:
        return False  # Snake dies if it exits the disk

    # Update snake body
    snake_body = [[new_head_x, new_head_y]] + snake_body[:-1]
    return True


def check_collision():
    """Check if the snake eats the food."""
    global food_position, snake_body

    head_x, head_y = snake_body[0]
    food_x, food_y = food_position
    distance = math.sqrt((head_x - food_x)**2 + (head_y - food_y)**2)

    if distance < 0.05:  # Collision threshold in hyperbolic coordinates
        # Grow snake
        snake_body.append(snake_body[-1])
        # Respawn food
        respawn_food()


def draw_snake():
    """Draw the snake."""
    for segment in snake_body:
        x, y = poincare_to_screen(segment[0], segment[1])
        pygame.draw.circle(screen, green, (x, y), segment_radius)

def draw_food():
    """Draw the food on the screen."""
    x, y = poincare_to_screen(food_position[0], food_position[1])
    pygame.draw.circle(screen, red, (x, y), segment_radius)
def generate_apple_position(k=2):
    """
    Generate a random apple position in the Poincaré disk with radial probability.
    
    :param k: Steepness of the probability density function (higher makes edge apples rarer).
    :return: (x, y) position in hyperbolic coordinates.
    """
    # Generate a random radius using inverse transform sampling
    u = random.uniform(0, 1)
    r = (1 - u**(1 / (k + 1)))**0.1

    # Generate a random angle
    theta = random.uniform(0, 2 * math.pi)

    # Convert to Cartesian coordinates
    x = r * math.cos(theta)
    y = r * math.sin(theta)

    return x, y

def respawn_food():
    """Generate a new food position based on radial probability."""
    global food_position
    food_position = generate_apple_position(k=4)  # Adjust k as needed


# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get key states for snake direction
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        snake_direction += 0.1  # Rotate left
    if keys[pygame.K_RIGHT]:
        snake_direction -= 0.1  # Rotate right

    # Move the snake
    if not move_snake():
        print("Game Over!")
        running = False

    # Check for collisions
    check_collision()

    # Clear the screen
    screen.fill(black)

    # Draw the game elements
    draw_poincare_disk()
    draw_hyperbolic_grid()
    draw_snake()
    draw_food()

    # Update the display
    pygame.display.flip()

    # Control frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
