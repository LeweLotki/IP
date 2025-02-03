from simulation.simulation import GridSimulation

if __name__ == "__main__":
    sim = GridSimulation(
        background_path="./fotos/background2.png",
        car_image_path="./fotos/car2.png",
        scale_factor=35,  # Bigger cars (10 pixels each)
        fps=10
    )
    sim.run()

