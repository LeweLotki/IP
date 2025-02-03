import pygame
import numpy as np
import cv2
import sys  
from simulation.spawner import Spawner
from decision_system.system import DecisionSystem

class GridSimulation:
    def __init__(self, background_path, car_image_path, mask_path, cell_size=20, fps=10, 
                 car_spawn_probability=0.9, max_new_cars=10, min_parking_time=200):
        """
        Initializes the simulation with a configurable cell size.
        """
        pygame.init()

        # **Set up screen size FIRST**
        self.width, self.height = pygame.image.load(background_path).get_size()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Pygame Car Simulation")

        # **Now load images AFTER setting the display**
        self.background = pygame.image.load(background_path).convert()
        self.car_image_original = pygame.image.load(car_image_path).convert_alpha()

        # **Resize mask to match cell grid size**
        self.cell_size = cell_size  # Defines the size of a single grid cell
        self.grid_width = self.width // self.cell_size  # How many cells fit in width
        self.grid_height = self.height // self.cell_size  # How many cells fit in height
        full_mask = np.load(mask_path, allow_pickle=False)
        self.mask = cv2.resize(full_mask, (self.grid_width, self.grid_height), interpolation=cv2.INTER_NEAREST)

        # **Scale car image to exactly match cell size**
        self.car_image = pygame.transform.smoothscale(self.car_image_original, (self.cell_size, self.cell_size))

        # FPS settings
        self.fps = fps
        self.clock = pygame.time.Clock()
        self.ticks = 0  # Track simulation ticks

        # Define fixed destinations
        self.destinations = {
            "TOP": (self.grid_width // 2, 0),
            "LEFT": (0, self.grid_height // 2),
            "BOTTOM": (self.grid_width // 2, self.grid_height - 1),
            "RIGHT": (self.grid_width - 1, self.grid_height // 2)
        }

        # Initialize Decision System and Spawner
        self.decision_system = DecisionSystem(weight_destination=0.7, weight_spacing=0.3)
        self.spawner = Spawner(self.mask, self.destinations, self.decision_system, car_spawn_probability, max_new_cars, min_parking_time)

        print(f"[DEBUG] Grid Size: {self.grid_width}x{self.grid_height} | Cell Size: {self.cell_size}")
        print(f"[DEBUG] Resized Mask Shape: {self.mask.shape}")

    def draw_cars(self):
        """Draws all cars on the parking lot."""
        self.screen.blit(self.background, (0, 0))

        for car in self.spawner.cars:
            if car.position:
                car_x = car.position[0] * self.cell_size  # Scale position correctly
                car_y = car.position[1] * self.cell_size
                self.screen.blit(self.car_image, (car_x, car_y))  # Draw at exact grid position
                print(f"[DEBUG] Drawing car at screen pos: ({car_x}, {car_y})")  # Debug drawing

        pygame.display.flip()

    def run(self):
        """Runs the simulation loop."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()  # Properly exit the program

            self.ticks += 1
            print(f"[DEBUG] Tick: {self.ticks}")

            self.spawner.spawn_new_cars()
            self.spawner.update_cars()
            self.draw_cars()
            self.clock.tick(self.fps)

