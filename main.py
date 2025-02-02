from simulation.simulation import GridSimulation

if __name__ == "__main__":
    sim = GridSimulation(
        background_path="./fotos/background.png",
        scale_factor=35,  # Bigger cars (10 pixels each)
        fps=10
    )
    sim.run()

