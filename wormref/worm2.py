import pygame
import math
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width, screen_height = 800, 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Sphere Game with Snake and Pole Death")

# Colors
black = (0, 0, 0)  # Background color
sphere_blue = (0, 0, 128)  # Dark blue for the sphere's base
blue = (0, 0, 255)  # Bright blue for grid lines
green = (0, 255, 0)  # Player worm color
red = (255, 0, 0)  # Apple color
white = (255, 255, 255)  # Text color

# Circle properties
circle_center = (400, 400)  # Center of the circle
circle_radius = 300  # Radius of the circle

# Sphere rotation parameters
phi_0 = -math.pi / 6  # Initial latitude of the view (tilt)
lambda_0 = 0  # Initial longitude of the view (rotation)
view_rotation_speed = 0.05  # Speed of view adjustment in radians per key press

# Worm properties
worm_segments = 20  # Initial number of worm segments
worm_spacing = 0.1  # Spacing between segments (in radians)
worm_body = [[0, i * worm_spacing] for i in range(worm_segments)]  # Start on the equator
worm_speed = -0.02  # Continuous movement speed of the worm (in radians)
current_axis = "longitude"  # The axis along which the worm is currently traveling
constant_value = 0  # The constant value for the non-dynamic axis (phi or lambda)
segment_radius = 5  # Radius of each worm segment

# Apple properties
apple_phi = random.uniform(-math.pi / 2, math.pi / 2)  # Random latitude
apple_lambda = random.uniform(0, 2 * math.pi)  # Random longitude
apple_radius = 8  # Apple size

# Font for game over text
font = pygame.font.SysFont("Arial", 48)


def calculate_shade(z, min_z, max_z):
    """Calculate the shade of a color based on depth."""
    normalized_z = (z - min_z) / (max_z - min_z)  # Normalize z to [0, 1]
    brightness = int(255 - 255 * normalized_z * 0.98)  # Map to [0, 255]
    return (0, 0, brightness)  # Blue gradient


def project_point(phi, lambd, R, phi_0, lambda_0):
    """Project a point (phi, lambda) onto the 2D plane using orthographic projection."""
    x = R * math.cos(phi) * math.sin(lambd - lambda_0)
    y = R * (math.cos(phi_0) * math.sin(phi) - math.sin(phi_0) * math.cos(phi) * math.cos(lambd - lambda_0))
    z = R * math.cos(phi) * math.cos(lambd - lambda_0)  # Depth (z-coordinate)
    return x, y, z


def pre_render_filled_sphere():
    """Pre-render the filled blue sphere with gradient shading."""
    surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    min_z, max_z = -circle_radius, circle_radius  # Range of z-values

    for y in range(-circle_radius, circle_radius):
        for x in range(-circle_radius, circle_radius):
            if x**2 + y**2 <= circle_radius**2:  # Check if point is inside the circle
                z = math.sqrt(max(0, circle_radius**2 - x**2 - y**2))
                shade = calculate_shade(z, min_z, max_z)
                surface.set_at((circle_center[0] + x, circle_center[1] + y), shade)

    return surface


def draw_orthographic_grid(phi_0, lambda_0):
    """Draw grid lines on a sphere using orthographic projection."""
    num_lat_lines = 6  # Number of latitude lines
    num_lon_lines = 12  # Number of longitude lines
    lat_step = math.pi / num_lat_lines  # Latitude step size
    lon_step = 2 * math.pi / num_lon_lines  # Longitude step size

    min_z, max_z = -circle_radius, circle_radius  # Range of z-values

    # Draw latitude lines
    for i in range(-num_lat_lines + 1, num_lat_lines):  # From -90 to +90 degrees
        phi = i * lat_step / 2  # Latitude in radians
        points = []
        shades = []
        for j in range(361):  # Sweep longitude to draw the line
            lambd = math.radians(j)  # Longitude in radians
            x, y, z = project_point(phi, lambd, circle_radius, phi_0, lambda_0)
            points.append((circle_center[0] + x, circle_center[1] - y))
            shades.append(z)  # Store depth
        for k in range(len(points) - 1):
            shade = calculate_shade(shades[k], min_z, max_z)
            pygame.draw.line(screen, shade, points[k], points[k + 1], 1)

    # Draw longitude lines
    for i in range(num_lon_lines):  # From 0 to 360 degrees
        lambd = i * lon_step  # Longitude in radians
        points = []
        shades = []
        for j in range(-180, 181, 2):  # Sweep latitude to draw the line
            phi = math.radians(j)  # Latitude in radians
            x, y, z = project_point(phi, lambd, circle_radius, phi_0, lambda_0)
            points.append((circle_center[0] + x, circle_center[1] - y))
            shades.append(z)
        for k in range(len(points) - 1):
            shade = calculate_shade(shades[k], min_z, max_z)
            pygame.draw.line(screen, shade, points[k], points[k + 1], 1)


def draw_worm():
    """Draw the worm as a series of segments on the sphere."""
    min_z, max_z = -circle_radius, circle_radius
    for phi, lambd in worm_body:
        x, y, z = project_point(phi, lambd, circle_radius, phi_0, lambda_0)
        pygame.draw.circle(screen, green, (circle_center[0] + int(x), circle_center[1] - int(y)), segment_radius)


def draw_apple():
    """Draw the apple on the sphere."""
    x, y, z = project_point(apple_phi, apple_lambda, circle_radius, phi_0, lambda_0)
    pygame.draw.circle(screen, red, (circle_center[0] + int(x), circle_center[1] - int(y)), apple_radius)


def update_worm():
    """Update the worm's position based on continuous movement."""
    global worm_body, constant_value, current_axis

    # Get the current head position
    head_phi, head_lambda = worm_body[0]

    # Update based on the current axis of travel
    if current_axis == "longitude":
        # Move along longitude lines
        new_phi = constant_value
        new_lambda = (head_lambda + worm_speed) % (2 * math.pi)
    elif current_axis == "latitude":
        # Move along latitude lines
        new_phi = max(-math.pi / 2, min(math.pi / 2, head_phi + worm_speed))
        new_lambda = constant_value

    # Update the worm's body
    worm_body = [[new_phi, new_lambda]] + worm_body[:-1]


def check_collision():
    """Check if the worm's head collides with the apple."""
    global apple_phi, apple_lambda, worm_body

    head_phi, head_lambda = worm_body[0]
    dist = math.sqrt((head_phi - apple_phi)**2 + (head_lambda - apple_lambda)**2)
    if dist < 0.1:  # Adjust threshold as needed
        # Respawn apple
        apple_phi = random.uniform(-math.pi / 2, math.pi / 2)
        apple_lambda = random.uniform(0, 2 * math.pi)
        # Grow worm
        worm_body.append(worm_body[-1])


def check_pole_collision():
    """Check if the worm's head collides with a pole."""
    global running

    head_phi, _ = worm_body[0]
    if abs(head_phi) >= math.pi / 2 - 0.05:  # Near the poles
        # Game over
        game_over_text = font.render("Game Over!", True)
        # Game over
        game_over_text = font.render("Game Over!", True, white)
        screen.blit(game_over_text, (screen_width // 2 - 150, screen_height // 2 - 50))
        pygame.display.flip()
        pygame.time.wait(2000)  # Pause for 2 seconds
        running = False


def change_axis(axis):
    """Change the axis of travel for the worm."""
    global current_axis, constant_value

    if axis == "longitude":
        current_axis = "longitude"
        constant_value = worm_body[0][0]  # Lock latitude
    elif axis == "latitude":
        current_axis = "latitude"
        constant_value = worm_body[0][1]  # Lock longitude


# Pre-render the filled sphere
sphere_surface = pre_render_filled_sphere()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get key states for view adjustment and worm movement
    keys = pygame.key.get_pressed()

    # Adjust camera with WASD keys
    if keys[pygame.K_w]:  # Tilt upward
        phi_0 = max(-math.pi / 2, phi_0 - view_rotation_speed)
    if keys[pygame.K_s]:  # Tilt downward
        phi_0 = min(math.pi / 2, phi_0 + view_rotation_speed)
    if keys[pygame.K_a]:  # Rotate view left
        lambda_0 -= view_rotation_speed
    if keys[pygame.K_d]:  # Rotate view right
        lambda_0 += view_rotation_speed

    # Control worm with arrow keys
    if keys[pygame.K_UP]:
        change_axis("latitude")  # Travel along latitude lines
        worm_speed = abs(worm_speed)
    if keys[pygame.K_DOWN]:
        change_axis("latitude")  # Travel along latitude lines
        worm_speed = -abs(worm_speed)
    if keys[pygame.K_LEFT]:
        change_axis("longitude")  # Travel along longitude lines
        worm_speed = abs(worm_speed)
    if keys[pygame.K_RIGHT]:
        change_axis("longitude")  # Travel along longitude lines
        worm_speed = -abs(worm_speed)

    # Update worm's position
    update_worm()

    # Check for collision with apple
    check_collision()

    # Check for collision with poles
    check_pole_collision()

    # Clear the screen
    screen.fill(black)

    # Render the pre-rendered filled sphere
    screen.blit(sphere_surface, (0, 0))

    # Draw the orthographic grid
    draw_orthographic_grid(phi_0, lambda_0)

    # Draw the worm
    draw_worm()

    # Draw the apple
    draw_apple()

    # Update the display
    pygame.display.flip()

    # Control frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
