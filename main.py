from simulation.simulation import GridSimulation

if __name__ == "__main__":
    sim = GridSimulation(
        background_path="./fotos/background2.png",
        # car_image_path="./fotos/car2.png",
        mask_path="./fotos/mask_corrected.npy",
        cell_size=30,  # Control the size of the car/grid cells
        fps=10,
        car_spawn_probability=0.5,  # Adjust probability of cars appearing
        max_new_cars=5,  # Allow multiple cars per frame
        min_parking_time=200  # Longer parking time
    )
    sim.run()

