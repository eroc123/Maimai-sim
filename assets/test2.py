import pygame
import sys
import math

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
SEGMENT_SIZE = 20
SEGMENT_SPEED = 2
ANGLE = 30  # Moving at a 30 degree angle

# Convert angle to radians for trigonometric functions
angle_rad = math.radians(ANGLE)

# Calculate x and y speed components
x_speed = SEGMENT_SPEED * math.cos(angle_rad)
y_speed = SEGMENT_SPEED * math.sin(angle_rad)

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Expanding Segment at 30 Degrees")

# Clock to control the frame rate
clock = pygame.time.Clock()

# List to store segment positions
segments = []

# Initial position of the first segment
start_x = SCREEN_WIDTH // 2
start_y = SCREEN_HEIGHT // 2

# Add the first segment
segments.append(pygame.Rect(start_x, start_y, SEGMENT_SIZE, SEGMENT_SIZE))

# Main game loop
running = True
while running:
    screen.fill(WHITE)  # Clear the screen with a white background
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update segment positions and add a new segment
    if len(segments) > 0:
        # Get the position of the last segment
        last_segment = segments[-1]
        
        # Determine the new position for the next segment
        new_segment = last_segment.copy()
        new_segment.x += x_speed
        new_segment.y -= y_speed  # Moving up since Pygame's origin is at the top-left

        # Add the new segment to the list
        segments.append(new_segment)

    # Draw all the segments
    for segment in segments:
        pygame.draw.rect(screen, RED, segment)

    # Limit the frame rate
    clock.tick(FPS)

    # Update the display
    pygame.display.flip()

# Quit pygame
pygame.quit()
sys.exit()