import pygame
import random
import numpy as np
from simulation.car import Car
from decision_system.system import DecisionSystem

class GridSimulation:
    def __init__(self, background_path="./fotos/background.png", car_image_path="./fotos/car.png", 
                 scale_factor=10, fps=10, car_spawn_probability=0.3, max_new_cars=3, min_parking_time=100):
        """
        Initializes the simulation using a Decision System for parking.
        
        :param background_path: Path to the background image.
        :param car_image_path: Path to the car image.
        :param scale_factor: Factor to resize the grid (higher = bigger cars).
        :param fps: Frames per second (controls simulation speed).
        :param car_spawn_probability: Probability of new cars appearing per frame.
        :param max_new_cars: Maximum number of cars that can arrive in a single frame.
        :param min_parking_time: Minimum time a car stays before considering leaving.
        """
        # Initialize pygame
        pygame.init()
        
        pygame.display.set_mode((1, 1))  # Small temporary display mode

        # Load images
        self.background = pygame.image.load(background_path).convert_alpha()
        self.car_image_original = pygame.image.load(car_image_path).convert_alpha()

        # Set up screen size
        self.width, self.height = self.background.get_size()
        self.scale_factor = scale_factor
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Pygame Car Simulation")

        # Resize car image while maintaining aspect ratio
        self.car_image = self.scale_car_image(self.car_image_original, self.scale_factor)

        # Grid size in cells
        self.grid_width = self.width // self.scale_factor
        self.grid_height = self.height // self.scale_factor

        # FPS and simulation parameters
        self.fps = fps
        self.clock = pygame.time.Clock()
        self.car_spawn_probability = car_spawn_probability
        self.max_new_cars = max_new_cars
        self.min_parking_time = min_parking_time

        # Destinations on the grid
        self.destinations = {
            "TOP": (self.grid_width // 2, 0),
            "LEFT": (0, self.grid_height // 2),
            "BOTTOM": (self.grid_width // 2, self.grid_height - 1),
            "RIGHT": (self.grid_width - 1, self.grid_height // 2)
        }

        # Parking area
        self.sim_x1, self.sim_x2 = 90 // self.scale_factor, 418 // self.scale_factor
        self.sim_y1, self.sim_y2 = 332 // self.scale_factor, 587 // self.scale_factor

        # Decision system
        self.decision_system = DecisionSystem(weight_destination=0.7, weight_spacing=0.3)

        # Parking state
        self.cars = []
        self.occupied_spaces = set()

    def scale_car_image(self, image, max_size):
        """Resizes the car image while keeping its original aspect ratio."""
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

    def spawn_new_cars(self):
        """Attempts to spawn multiple new cars based on probability."""
        if random.random() < self.car_spawn_probability:  # Probability check
            num_cars = random.randint(1, self.max_new_cars)  # Random number of cars arriving
            for _ in range(num_cars):
                destination_name, destination_coords = random.choice(list(self.destinations.items()))
                available_spots = self.get_available_spots()
                best_spot = self.decision_system.choose_best_spot(available_spots, destination_coords, self.occupied_spaces)

                if best_spot:
                    new_car = Car(position=best_spot, destination=destination_name)
                    new_car.time_spent = random.randint(self.min_parking_time, self.min_parking_time + 50)  # Extend parking time
                    self.cars.append(new_car)
                    self.occupied_spaces.add(best_spot)

    def update_cars(self):
        """Update cars: increase time spent, remove leaving cars."""
        new_cars = []
        temp_occupied_spaces = set()

        for car in self.cars:
            car.update_time_spent()
            if car.should_leave():
                continue  # Remove car if it should leave

            new_cars.append(car)
            temp_occupied_spaces.add(car.position)

        self.cars = new_cars
        self.occupied_spaces = temp_occupied_spaces

    def draw_cars(self):
        """Draws all cars on the parking grid."""
        self.screen.blit(self.background, (0, 0))  # Draw background

        for car in self.cars:
            car_x = car.position[0] * self.scale_factor
            car_y = car.position[1] * self.scale_factor
            car_rect = self.car_image.get_rect(center=(car_x + self.scale_factor // 2, car_y + self.scale_factor // 2))
            self.screen.blit(self.car_image, car_rect.topleft)

        pygame.display.flip()

    def run(self):
        """Runs the simulation loop."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.spawn_new_cars()
            self.update_cars()
            self.draw_cars()
            self.clock.tick(self.fps)

        pygame.quit()

