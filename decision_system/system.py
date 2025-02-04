import numpy as np

class DecisionSystem:
    def __init__(self, weight_destination=0.01, weight_spacing=0.99):
        """
        Decision system to choose the best parking spot.

        :param weight_destination: Importance of being close to the destination (0-1).
        :param weight_spacing: Importance of being far from other cars (0-1).
        """
        self.weight_destination = weight_destination
        self.weight_spacing = weight_spacing

    def evaluate_spot(self, spot, destination, occupied_spaces):
        """
        Calculate a score for a given parking spot.

        :param spot: (x, y) tuple representing the parking spot.
        :param destination: (x, y) tuple representing the destination.
        :param occupied_spaces: Set of (x, y) tuples with currently occupied spots.

        :return: Score of the spot (higher is better).
        """
        
        distance_to_dest = np.linalg.norm(np.array(spot) - np.array(destination))

        
        if occupied_spaces:
            distances_to_cars = [np.linalg.norm(np.array(spot) - np.array(car)) for car in occupied_spaces]
            min_distance_to_car = min(distances_to_cars) if distances_to_cars else float("inf")
        else:
            min_distance_to_car = float("inf")  

        
        score = (-self.weight_destination * distance_to_dest) + (self.weight_spacing * min_distance_to_car)
        return score

    def choose_best_spot(self, available_spots, destination, occupied_spaces):
        """
        Choose the best parking spot based on decision criteria.

        :param available_spots: List of free (x, y) spots.
        :param destination: (x, y) tuple representing the destination.
        :param occupied_spaces: Set of (x, y) tuples with currently occupied spots.

        :return: The best parking spot (x, y) or None if no spots available.
        """
        if not available_spots:
            return None  

        best_spot = max(available_spots, key=lambda spot: self.evaluate_spot(spot, destination, occupied_spaces))
        return best_spot

