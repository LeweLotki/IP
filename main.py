import pygame
import numpy as np
import cv2

# Grid size
GRID_SIZE = (50, 50)  # (rows, cols)
CELL_SIZE = 10  # Pixel size of each cell

# Probability values
PROB_EMPTY_TO_TAKEN = 0.1  # 10% chance to switch from 0 -> 1
PROB_TAKEN_TO_EMPTY = 0.05  # 5% chance to switch from 1 -> 0

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)

# Initialize pygame
pygame.init()
WIDTH, HEIGHT = GRID_SIZE[1] * CELL_SIZE, GRID_SIZE[0] * CELL_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Parking Simulation")

# Load background image
background = pygame.image.load("./fotos/backgorund.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Load the mask
mask = np.load("./fotos/mask_corrected.npy", allow_pickle=False)
mask = cv2.resize(mask, (GRID_SIZE[1], GRID_SIZE[0]), interpolation=cv2.INTER_NEAREST)

# Initialize random state grid (0 = empty, 1 = taken, only on parking areas)
grid = (np.random.choice([0, 1], size=GRID_SIZE) * (mask == 1)).astype(int)  # Only allow on parking areas

def update_grid(grid):
    """Update grid based on probabilities, considering mask."""
    new_grid = grid.copy()
    
    # Generate random probabilities for each cell
    rand_vals = np.random.rand(*grid.shape)

    # Apply probability rules, respecting the mask
    new_grid[(grid == 0) & (rand_vals < PROB_EMPTY_TO_TAKEN) & (mask == 1)] = 1
    new_grid[(grid == 1) & (rand_vals < PROB_TAKEN_TO_EMPTY)] = 0

    return new_grid

def draw_grid(grid):
    """Draw the grid on the screen."""
    screen.blit(background, (0, 0))  # Draw background
    for row in range(GRID_SIZE[0]):
        for col in range(GRID_SIZE[1]):
            if mask[row, col] == 2:
                pygame.draw.rect(screen, GRAY, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))  # Roads
            if grid[row, col] == 1:
                pygame.draw.rect(screen, BLACK, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))  # Parked Cars
    
    pygame.display.flip()

# Main loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    grid = update_grid(grid)
    draw_grid(grid)

    clock.tick(10)  # Control speed (10 FPS)

pygame.quit()
