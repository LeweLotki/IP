import random
import numpy as np
from simulation.car import Car
from decision_system.system import DecisionSystem

class Spawner:
    def __init__(self, mask, destinations, decision_system, car_spawn_probability=0.9, max_new_cars=10, min_parking_time=200):
        """
        Handles car spawning logic.
        """
        self.mask = mask
        self.destinations = destinations
        self.decision_system = decision_system
        self.car_spawn_probability = car_spawn_probability
        self.max_new_cars = max_new_cars
        self.min_parking_time = min_parking_time

        self.cars = []
        self.occupied_spaces = set()

        
        self.valid_parking_spots = np.count_nonzero(self.mask == 1)
        print(f"[DEBUG] Resized Mask Loaded: Size {self.mask.shape}, Valid Parking Spots: {self.valid_parking_spots}")

    def get_available_spots(self):
        """Returns a list of free parking spots based on the mask."""
        spots = [(x, y) for x in range(self.mask.shape[1])  
                        for y in range(self.mask.shape[0])  
                        if (x, y) not in self.occupied_spaces and self.mask[y, x] == 1]
        
        print(f"[DEBUG] Available spots: {len(spots)} (should match valid parking spots)")
        return spots

    def spawn_new_cars(self):
        """Spawns new cars with random attributes and assigns them using the Decision System."""
        if random.random() < self.car_spawn_probability:
            num_cars = random.randint(1, self.max_new_cars)
            print(f"[DEBUG] Spawning {num_cars} new cars")

            for _ in range(num_cars):
                destination_name, destination_coords = random.choice(list(self.destinations.items()))
                available_spots = self.get_available_spots()

                if available_spots:  
                    best_spot = self.decision_system.choose_best_spot(available_spots, destination_coords, self.occupied_spaces)

                    if best_spot:
                        print(f"[DEBUG] Placing car at {best_spot} with destination {destination_name}")
                        new_car = Car(position=best_spot, destination=destination_name)
                        new_car.time_spent = random.randint(self.min_parking_time, self.min_parking_time + 50)  
                        self.cars.append(new_car)
                        self.occupied_spaces.add(best_spot)
                    else:
                        print(f"[DEBUG] No suitable spot found for car with destination {destination_name}")
    def update_cars(self):
        """Updates car positions and removes those that should leave."""
        new_cars = []
        temp_occupied_spaces = set()

        for car in self.cars:
            car.update_time_spent()
            if car.should_leave():
                print(f"[DEBUG] Car at {car.position} left the parking lot")
                continue  

            new_cars.append(car)
            temp_occupied_spaces.add(car.position)

        self.cars = new_cars
        self.occupied_spaces = temp_occupied_spaces
        print(f"[DEBUG] Cars currently parked: {len(self.cars)}")
