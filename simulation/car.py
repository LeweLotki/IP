import random
import numpy as np

class Car:
    DESTINATIONS = {
        "TOP": "Instytut Telekomunikacji",
        "LEFT": "Instytut Fizyki",
        "BOTTOM": "DS AGH",
        "RIGHT": "Others"
    }

    def __init__(self, position, destination):
        """
        Represents a car parked in the grid.
        
        :param position: (x, y) tuple indicating the car's position on the grid.
        :param destination: One of the predefined destinations.
        """
        self.position = position
        self.destination = destination
        self.time_spent = 0

    def update_time_spent(self):
        """Increase the time spent in the parking lot."""
        self.time_spent += 1

    def should_leave(self):
        """
        Determines if the car should leave the parking.
        The longer the car is parked, the lower the chance it will leave.
        
        :return: True if the car should leave, otherwise False.
        """
        base_probability = 0.3  # Initial probability of leaving
        decay_factor = 0.01  # The longer it stays, the lower the chance
        probability_to_leave = max(0.05, base_probability - (self.time_spent * decay_factor))
        
        return random.random() < probability_to_leave

    def __repr__(self):
        return f"Car(pos={self.position}, dest={self.destination}, time_spent={self.time_spent})"

