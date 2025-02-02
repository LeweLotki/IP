import pygame
import random
import numpy as np
from simulation.car import Car
from decision_system.system import DecisionSystem

class GridSimulation:
    def __init__(self, background_path="./fotos/background.png", car_image_path="./fotos/car.png", scale_factor=10, fps=10):
        """
        Initializes the simulation using a Decision System for parking.
        
        :param background_path: Path to the background image.
        :param car_image_path: Path to the car image.
        :param scale_factor: Factor to resize the grid (higher = bigger cars).
        :param fps: Frames per second (controls simulation speed).
        """
        # Initialize pygame
        pygame.init()
        
        pygame.display.set_mode((1, 1))  # Small temporary display mode

        # Load background image
        self.background = pygame.image.load(background_path).convert_alpha()
        self.width, self.height = self.background.get_size()

        # Load car image with transparency
        self.car_image_original = pygame.image.load(car_image_path).convert_alpha()
        self.scale_factor = scale_factor  # Defines grid cell size

        # Compute scaled size while maintaining aspect ratio
        self.car_image = self.scale_car_image(self.car_image_original, self.scale_factor)

        # **Set the actual window size**
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Pygame Car Simulation")

        # **Grid size in cells, not pixels**
        self.grid_width = self.width // self.scale_factor
        self.grid_height = self.height // self.scale_factor

        self.fps = fps
        self.clock = pygame.time.Clock()

        # **Define fixed destinations on the grid borders**
        self.destinations = {
            "TOP": (self.grid_width // 2, 0),  # Instytut Telekomunikacji
            "LEFT": (0, self.grid_height // 2),  # Instytut Fizyki
            "BOTTOM": (self.grid_width // 2, self.grid_height - 1),  # DS AGH
            "RIGHT": (self.grid_width - 1, self.grid_height // 2)  # Others
        }

        # **Correct the parking area coordinates (convert pixels to grid)**
        self.sim_x1, self.sim_x2 = 90 // self.scale_factor, 418 // self.scale_factor
        self.sim_y1, self.sim_y2 = 332 // self.scale_factor, 587 // self.scale_factor

        # **Decision system for choosing the best spot**
        self.decision_system = DecisionSystem(weight_destination=0.7, weight_spacing=0.3)

        # **List of parked cars**
        self.cars = []
        self.occupied_spaces = set()  # Track occupied spaces
        self.spawn_initial_cars()

    def scale_car_image(self, image, max_size):
        """Scales the car image while keeping its original aspect ratio."""
        original_width, original_height = image.get_size()
        aspect_ratio = original_width / original_height

        if original_width > original_height:
            new_width = max_size
            new_height = int(max_size / aspect_ratio)
        else:
            new_height = max_size
            new_width = int(max_size * aspect_ratio)

        return pygame.transform.smoothscale(image, (new_width, new_height))

    def get_available_spots(self):
        """Returns a list of all free parking spots."""
        return [(x, y) for x in range(self.sim_x1, self.sim_x2)
                        for y in range(self.sim_y1, self.sim_y2)
                        if (x, y) not in self.occupied_spaces]

    def spawn_initial_cars(self):
        """Spawn initial set of cars in the parking lot area using the Decision System."""
        for _ in range(10):  # Generate 10 cars initially
            destination_name, destination_coords = random.choice(list(self.destinations.items()))
            available_spots = self.get_available_spots()
            best_spot = self.decision_system.choose_best_spot(available_spots, destination_coords, self.occupied_spaces)

            if best_spot:
                self.cars.append(Car(position=best_spot, destination=destination_name))
                self.occupied_spaces.add(best_spot)  # Mark spot as taken

    def draw_cars(self):
        """Draw cars as images on the parking lot with the background image."""
        self.screen.blit(self.background, (0, 0))  # **Draw background**

        # **Draw each car**
        for car in self.cars:
            car_x = car.position[0] * self.scale_factor
            car_y = car.position[1] * self.scale_factor

            car_rect = self.car_image.get_rect(center=(car_x + self.scale_factor // 2, car_y + self.scale_factor // 2))
            self.screen.blit(self.car_image, car_rect.topleft)

        pygame.display.flip()

    def run(self):
        """Run the simulation (only spawns cars, no movement)."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.draw_cars()
            self.clock.tick(self.fps)  # **Control FPS**

        pygame.quit()

