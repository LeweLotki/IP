# AGH Parking Simulation

## Overview

This project simulates car parking at the AGH University campus. It models the dynamic process of cars arriving at a parking lot and uses a decision-making system to determine the most optimal parking spot for each car. The simulation incorporates randomness in car spawning and leverages two configurable parameters to influence the decision-making process:

1. **Proximity to Destination**: The desire for cars to park close to their assigned destination.
2. **Spacing**: The desire for cars to park as far away from other cars as possible.

## Features

- **Simulation Environment**: A visual representation of the AGH campus parking lot, displaying parked cars in real-time.
- **Dynamic Decision System**: A customizable system that determines the parking spot based on proximity to the destination and spacing preferences.
- **Randomized Car Spawning**: Cars are spawned at random intervals and assigned to random destinations.
- **User-Interactive UI**: A slider allows users to adjust the weights of the decision-making parameters (proximity vs. spacing) in real time.
- **Colored Cars**: Cars are visually differentiated by destination using different colors.

## Project Structure

The project is divided into the following modules:

### 1. **Simulation**
- Handles the visual representation and logic of the parking lot.
- Spawns cars with random attributes and assigns destinations.
- Includes a user interface (UI) with a slider to adjust decision system parameters dynamically.

### 2. **Decision System**
- Implements the logic to evaluate parking spots.
- Considers two parameters:
  - **Weight for Proximity to Destination**: A higher value prioritizes parking spots closer to the car's destination.
  - **Weight for Spacing**: A higher value prioritizes parking spots farther away from other parked cars.
- Dynamically updates weights based on user interaction with the slider.

### 3. **Spawner**
- Manages the spawning of new cars.
- Ensures cars are assigned to destinations and that parking spots are updated based on occupancy.

## Installation

### Prerequisites
- Python 3.10 or higher
- `pygame` library
- `numpy` library
- `opencv-python` library
- `poetry` (for dependency management)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/agh-parking-simulation.git
   cd agh-parking-simulation
   ```

2. Install dependencies using `poetry`:
   ```bash
   poetry install
   ```

3. Run the simulation:
   ```bash
   poetry run python main.py
   ```

## How It Works

1. **Initialization**:
   - The simulation loads a background map of the AGH parking lot.
   - Parking spots are defined using a preloaded parking mask (`.npy` file).
   - Cars are represented as colored rectangles, with each color corresponding to a specific destination.

2. **Dynamic Decision System**:
   - Cars evaluate parking spots based on proximity to their destination and spacing from other cars.
   - Users can adjust the weights of these parameters in real time using the slider in the UI.

3. **Car Spawning**:
   - Cars are spawned at random intervals with randomized destinations.
   - Each car parks based on the decision system's logic.

4. **UI Interaction**:
   - A slider in the UI allows users to adjust the decision system's behavior:
     - Move the slider to the left to prioritize **proximity to destination**.
     - Move the slider to the right to prioritize **spacing**.

## Usage

- Launch the simulation using `poetry run python main.py`.
- Observe the cars parking in real-time.
- Use the slider to experiment with different parking behaviors:
  - **Proximity to Destination**: Cars park as close to their destination as possible.
  - **Spacing**: Cars park as far from other cars as possible.
  - **Mixed Behavior**: Adjust the slider to find a balance between the two.

## Example Output

- **Proximity to Destination**:
  Cars cluster near their destinations.
- **Spacing**:
  Cars spread out across the parking lot, maximizing the distance between them.
- **Interactive Slider**:
  Dynamically changes the behavior of the decision system in real-time.

## Contributions

Contributions to this project are welcome! Feel free to fork the repository and submit pull requests with improvements, bug fixes, or new features.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
