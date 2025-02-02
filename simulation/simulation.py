import pygame
import numpy as np

class GridSimulation:
    def __init__(self, grid_size=(50, 50), cell_size=10, prob_empty_to_taken=0.1, prob_taken_to_empty=0.05, fps=10, background_path="./fotos/background.png"):
        """
        Initializes the simulation.
        
        :param grid_size: Tuple (rows, cols) defining the grid size.
        :param cell_size: Size of each cell in pixels.
        :param prob_empty_to_taken: Probability of an empty cell (0) turning into a taken cell (1).
        :param prob_taken_to_empty: Probability of a taken cell (1) turning into an empty cell (0).
        :param fps: Frames per second (controls simulation speed).
        :param background_path: Path to the background image.
        """
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.prob_empty_to_taken = prob_empty_to_taken
        self.prob_taken_to_empty = prob_taken_to_empty
        self.fps = fps
        
        # Colors
        self.BLACK = (0, 0, 0)

        # Initialize pygame
        pygame.init()
        self.width = self.grid_size[1] * self.cell_size
        self.height = self.grid_size[0] * self.cell_size
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Pygame Cell Simulation")

        # Load background image
        self.background = pygame.image.load(background_path)
        self.background = pygame.transform.scale(self.background, (self.width, self.height))

        # Initialize random state grid
        self.grid = np.random.choice([0, 1], size=self.grid_size)
        self.clock = pygame.time.Clock()

    def update_grid(self):
        """Update grid based on probabilities."""
        new_grid = self.grid.copy()
        
        # Generate random probabilities for each cell
        rand_vals = np.random.rand(*self.grid.shape)

        # Apply probability rules
        new_grid[(self.grid == 0) & (rand_vals < self.prob_empty_to_taken)] = 1
        new_grid[(self.grid == 1) & (rand_vals < self.prob_taken_to_empty)] = 0

        self.grid = new_grid

    def draw_grid(self):
        """Draw the grid on the screen with the background image."""
        # Draw background
        self.screen.blit(self.background, (0, 0))
        
        # Draw black squares only for taken cells (1)
        for row in range(self.grid_size[0]):
            for col in range(self.grid_size[1]):
                if self.grid[row, col] == 1:  # Only draw black squares for taken cells
                    pygame.draw.rect(self.screen, self.BLACK, 
                                     (col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size))

        pygame.display.flip()

    def run(self):
        """Run the simulation."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.update_grid()
            self.draw_grid()
            self.clock.tick(self.fps)  # Control FPS

        pygame.quit()

