from simulation.simulation import GridSimulation

if __name__ == "__main__":
    sim = GridSimulation(
        background_path="./fotos/background2.png",
        mask_path="./fotos/mask_corrected.npy",
        cell_size=30,
        fps=10,
        car_spawn_probability=0.5,
        max_new_cars=5,  
        min_parking_time=200
    )
    sim.run()

