import pygame
import numpy as np
import cv2
import sys
from simulation.spawner import Spawner
from decision_system.system import DecisionSystem


class GridSimulation:
    def __init__(self, background_path, mask_path, cell_size=20, fps=10,
                 car_spawn_probability=0.9, max_new_cars=10, min_parking_time=200):
        """
        Initializes the simulation with a configurable cell size.
        """
        pygame.init()

        # **Set up screen size FIRST**
        self.width, self.height = pygame.image.load(background_path).get_size()
        self.screen_height = self.height + 100  # Add extra space for the UI
        self.screen = pygame.display.set_mode((self.width, self.screen_height))
        pygame.display.set_caption("Pygame Car Simulation")

        # **Now load images AFTER setting the display**
        self.background = pygame.image.load(background_path).convert()

        # **Resize mask to match cell grid size**
        self.cell_size = cell_size  # Defines the size of a single grid cell
        self.grid_width = self.width // self.cell_size  # How many cells fit in width
        self.grid_height = self.height // self.cell_size  # How many cells fit in height
        full_mask = np.load(mask_path, allow_pickle=False)
        self.mask = cv2.resize(full_mask, (self.grid_width, self.grid_height), interpolation=cv2.INTER_NEAREST)

        # **Car Images for Destinations**
        self.car_images = {
            "TOP": self.load_and_scale_image("./fotos/car_red.png"),
            "LEFT": self.load_and_scale_image("./fotos/car_green.png"),
            "BOTTOM": self.load_and_scale_image("./fotos/car_blue.png"),
            "RIGHT": self.load_and_scale_image("./fotos/car_yellow.png")
        }

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
        self.decision_system = DecisionSystem(weight_destination=0.5, weight_spacing=0.5)
        self.spawner = Spawner(self.mask, self.destinations, self.decision_system, car_spawn_probability, max_new_cars, min_parking_time)

        # Slider Configuration
        self.slider = self.create_slider(self.width // 2 - 150, self.height + 40)

        print(f"[DEBUG] Grid Size: {self.grid_width}x{self.grid_height} | Cell Size: {self.cell_size}")
        print(f"[DEBUG] Resized Mask Shape: {self.mask.shape}")

    def load_and_scale_image(self, image_path):
        """
        Loads and scales an image to the cell size.

        :param image_path: Path to the image file.
        :return: Scaled pygame.Surface.
        """
        image = pygame.image.load(image_path).convert_alpha()
        return pygame.transform.smoothscale(image, (self.cell_size, self.cell_size))

    def create_slider(self, x, y):
        """Creates a slider for adjusting weights."""
        return {
            "rect": pygame.Rect(x, y, 300, 10),  # Slider bar
            "knob_rect": pygame.Rect(x + 150 - 5, y - 5, 10, 20),  # Knob position
            "value": 0.5  # Initial slider value
        }

    def draw_slider(self):
        """Draws the slider on the screen."""
        pygame.draw.rect(self.screen, (255, 255, 255), (0, self.height, self.width, 100))  # White background
        pygame.draw.rect(self.screen, (200, 200, 200), self.slider["rect"])  # Slider bar
        pygame.draw.rect(self.screen, (0, 0, 0), self.slider["knob_rect"])  # Knob

        font = pygame.font.SysFont(None, 24)
        spacing_weight = f"Spacing: {self.slider['value']:.2f}"
        destination_weight = f"Destination: {1 - self.slider['value']:.2f}"
        label_spacing = font.render(spacing_weight, True, (0, 0, 0))
        label_destination = font.render(destination_weight, True, (0, 0, 0))
        self.screen.blit(label_spacing, (self.slider["rect"].x, self.slider["rect"].y - 30))
        self.screen.blit(label_destination, (self.slider["rect"].x + 150, self.slider["rect"].y - 30))

    def handle_slider(self, mouse_pos, mouse_pressed):
        """Handles interaction with the slider."""
        if mouse_pressed[0] and self.slider["rect"].collidepoint(mouse_pos):
            self.slider["knob_rect"].x = min(max(mouse_pos[0], self.slider["rect"].x),
                                             self.slider["rect"].x + self.slider["rect"].width - self.slider["knob_rect"].width)
            self.slider["value"] = (self.slider["knob_rect"].x - self.slider["rect"].x) / self.slider["rect"].width

    def draw_cars(self):
        """Draws all cars on the parking lot."""
        self.screen.blit(self.background, (0, 0))

        for car in self.spawner.cars:
            if car.position:
                car_x = car.position[0] * self.cell_size  # Scale position correctly
                car_y = car.position[1] * self.cell_size

                # Select the correct car image based on the destination
                car_image = self.car_images.get(car.destination, None)
                if car_image:
                    self.screen.blit(car_image, (car_x, car_y))
                    print(f"[DEBUG] Drawing {car.destination} car at ({car_x}, {car_y})")

        self.draw_slider()  # Draw the slider
        pygame.display.flip()

    def run(self):
        """Runs the simulation loop."""
        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()  # Properly exit the program

            self.handle_slider(mouse_pos, mouse_pressed)

            # Update decision system weights based on slider
            self.decision_system.weight_spacing = self.slider["value"]
            self.decision_system.weight_destination = 1 - self.slider["value"]

            self.ticks += 1
            print(f"[DEBUG] Tick: {self.ticks}")

            self.spawner.spawn_new_cars()
            self.spawner.update_cars()
            self.draw_cars()
            self.clock.tick(self.fps)

