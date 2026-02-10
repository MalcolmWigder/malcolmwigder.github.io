import pygame
import sys
import math
import random

# Initialize Pygame
pygame.init()

# Set up the screen dimensions
screen_width, screen_height = 800, 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Worm Movement with Constant Speed")

# Define colors
black = (0, 0, 0)
worm_color = (0, 255, 0)
blue = (0, 0, 255)

# Worm properties
worm_length = random.randint(10, 30)  # Random number of segments
segment_size = 10  # Size of each segment
worm_body = [[400, 300]]  # Initial position of the worm's head
for i in range(1, worm_length):
    worm_body.append([400, 300 + i * segment_size])  # Add initial body segments

# Movement properties
speed = 2  # Speed of the worm (constant arc length)
step = 0  # Parameter along the curve
current_function = 0  # Index of the current function
delta = 0.01  # Small step size for derivative approximation

# Circle boundary properties
circle_center = (400, 400)  # Circle center
circle_radius = 300  # Circle radius

# Movement functions
functions = [
    lambda t: 300 + 50 * math.sin(math.radians(t)),  # Sine wave
    lambda t: 300 + 50 * math.cos(math.radians(t)),  # Cosine wave
    lambda t: 300 + 0.5 * t,                        # Linear function
    lambda t: 300 + 0.01 * t**2,                    # Quadratic function
    lambda t: 300 - 0.0001 * t**3,                  # Cubic function
    lambda t: 300 + 50 * math.tanh(0.01 * t),       # Hyperbolic tangent
    lambda t: 300 + 50 * math.exp(-0.01 * t),       # Exponential decay
    lambda t: 300 + 50 * math.atan(0.1 * t),        # Arctangent
    lambda t: 300 + 50 * math.log(abs(t + 1)),      # Logarithmic function
    lambda t: 300 + 50 * math.sqrt(abs(t + 1))      # Square root
]

# Game loop variables
clock = pygame.time.Clock()
running = True

def move_worm():
    global step, current_function

    # Current function
    func = functions[current_function]

    # Get current position of the head
    head_x, head_y = worm_body[0]

    # Approximate the derivative dynamically
    f_t = func(step)
    f_t_plus_delta = func(step + delta)
    derivative = (f_t_plus_delta - f_t) / delta

    # Compute the movement direction vector (dx, dy)
    dx = 1  # Increment in x is fixed
    dy = derivative

    # Normalize the movement vector to maintain constant speed
    magnitude = math.sqrt(dx**2 + dy**2)
    dx, dy = dx / magnitude, dy / magnitude

    # Move the head by "speed" units along the curve
    head_x += dx * speed
    head_y += dy * speed

    # Increment step
    step += dx * speed

    # Add the new head position
    worm_body.insert(0, [head_x, head_y])

    # Remove the last segment to maintain worm length
    worm_body.pop()

def check_collision():
    # Check if the worm's head is outside the circle
    head_x, head_y = worm_body[0]
    distance_from_center = math.sqrt((head_x - circle_center[0]) ** 2 + (head_y - circle_center[1]) ** 2)
    return distance_from_center > circle_radius
def random_color():
    """Generate a random RGB color."""
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def respawn_worm():
    # Clear the worm body and reset its position
    global worm_body, current_function, step, worm_color

    # Increment to the next function, wrapping around if needed
    current_function = (current_function + 1) % len(functions)
    step = 0  # Reset step for the new function

    worm_color = random_color()
    # Respawn the worm inside the circle at a random position
    angle = random.uniform(0, 2 * math.pi)
    spawn_x = circle_center[0] + (circle_radius - 20) * math.cos(angle)
    spawn_y = circle_center[1] + (circle_radius - 20) * math.sin(angle)

    # Reinitialize the worm's body with the new head position
    worm_body = [[spawn_x, spawn_y]]
    for i in range(1, worm_length):
        worm_body.append([spawn_x, spawn_y + i * segment_size])
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

    # Move the worm
    move_worm()

    # Check for collision with the circle boundary
    if check_collision():
        print(f"The worm died! Switching to function {current_function + 1}.")
        respawn_worm()

    # Clear the screen
    screen.fill(black)

    # Draw the circle boundary
    pygame.draw.circle(screen, blue, circle_center, circle_radius, 2)
    draw_grid()
    # Draw the worm
    for segment in worm_body:
        pygame.draw.circle(screen, worm_color, (int(segment[0]), int(segment[1])), segment_size // 2)

    # Update the display
    pygame.display.flip()

    # Limit frame rate to 60 frames per second
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
