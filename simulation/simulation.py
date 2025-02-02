import pygame
import numpy as np

class GridSimulation:
    def __init__(self, background_path="./fotos/background.png", scale_factor=15, prob_empty_to_taken=0.1, prob_taken_to_empty=0.05, fps=10):
        """
        Initializes the simulation with resizable grid cells.
        
        :param background_path: Path to the background image.
        :param scale_factor: Factor to resize the grid (higher = bigger cells, fewer grid points).
        :param prob_empty_to_taken: Probability of an empty cell (0) turning into a taken cell (1).
        :param prob_taken_to_empty: Probability of a taken cell (1) turning into an empty cell (0).
        :param fps: Frames per second (controls simulation speed).
        """
        # Initialize pygame
        pygame.init()
        
        # Load background image
        self.background = pygame.image.load(background_path)
        self.width, self.height = self.background.get_size()
        
        # Scale factor for larger cells
        self.scale_factor = scale_factor
        self.grid_width = self.width // self.scale_factor
        self.grid_height = self.height // self.scale_factor

        # Create window matching image size
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Pygame Cell Simulation")

        # Set probabilities
        self.prob_empty_to_taken = prob_empty_to_taken
        self.prob_taken_to_empty = prob_taken_to_empty
        self.fps = fps

        # Colors
        self.BLACK = (0, 0, 0)

        # Grid size is smaller, based on scale factor
        self.grid_size = (self.grid_height, self.grid_width)
        self.grid = np.zeros(self.grid_size, dtype=int)  # Initially all empty

        # Select a predefined region for simulation (scaled to match new grid)
        self.select_simulation_area()

        self.clock = pygame.time.Clock()

    def select_simulation_area(self):
        """Selects two fixed points to define a simulation square region in the scaled grid."""
        x1, y1 = 90 // self.scale_factor, 332 // self.scale_factor
        x2, y2 = 418 // self.scale_factor, 587 // self.scale_factor

        # Ensure x1, y1 is the top-left and x2, y2 is the bottom-right
        self.sim_x1, self.sim_x2 = min(x1, x2), max(x1, x2)
        self.sim_y1, self.sim_y2 = min(y1, y2), max(y1, y2)

    def update_grid(self):
        """Update grid only inside the selected square region."""
        new_grid = self.grid.copy()

        # Generate random probabilities for each cell inside the selected area
        rand_vals = np.random.rand(self.sim_y2 - self.sim_y1, self.sim_x2 - self.sim_x1)

        # Apply probability rules only inside the square
        sub_grid = new_grid[self.sim_y1:self.sim_y2, self.sim_x1:self.sim_x2]
        sub_grid[(sub_grid == 0) & (rand_vals < self.prob_empty_to_taken)] = 1
        sub_grid[(sub_grid == 1) & (rand_vals < self.prob_taken_to_empty)] = 0
        new_grid[self.sim_y1:self.sim_y2, self.sim_x1:self.sim_x2] = sub_grid

        self.grid = new_grid

    def draw_grid(self):
        """Draw the grid on the screen with the background image."""
        # Draw background
        self.screen.blit(self.background, (0, 0))

        # Draw black squares only for taken cells (1) inside the simulation region
        for row in range(self.sim_y1, self.sim_y2):
            for col in range(self.sim_x1, self.sim_x2):
                if self.grid[row, col] == 1:
                    pygame.draw.rect(self.screen, self.BLACK, 
                                     (col * self.scale_factor, row * self.scale_factor, 
                                      self.scale_factor, self.scale_factor))  # Larger cell

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

