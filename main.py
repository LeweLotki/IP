import pygame
import numpy as np

# Grid size
GRID_SIZE = (50, 50)  # (rows, cols)
CELL_SIZE = 10  # Pixel size of each cell

# Probability values
PROB_EMPTY_TO_TAKEN = 0.1  # 10% chance to switch from 0 -> 1
PROB_TAKEN_TO_EMPTY = 0.05  # 5% chance to switch from 1 -> 0

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize pygame
pygame.init()
WIDTH, HEIGHT = GRID_SIZE[1] * CELL_SIZE, GRID_SIZE[0] * CELL_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Cell Simulation")

# Initialize random state grid (0 = empty, 1 = taken)
grid = np.random.choice([0, 1], size=GRID_SIZE)

def update_grid(grid):
    """Update grid based on probabilities."""
    new_grid = grid.copy()
    
    # Generate random probabilities for each cell
    rand_vals = np.random.rand(*grid.shape)

    # Apply probability rules
    new_grid[(grid == 0) & (rand_vals < PROB_EMPTY_TO_TAKEN)] = 1
    new_grid[(grid == 1) & (rand_vals < PROB_TAKEN_TO_EMPTY)] = 0

    return new_grid

def draw_grid(grid):
    """Draw the grid on the screen."""
    screen.fill(WHITE)  # Clear screen
    for row in range(GRID_SIZE[0]):
        for col in range(GRID_SIZE[1]):
            color = BLACK if grid[row, col] == 1 else WHITE
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

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

