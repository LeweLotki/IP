from simulation.simulation import GridSimulation

if __name__ == "__main__":
    sim = GridSimulation(
        grid_size=(50, 50),
        cell_size=10,
        prob_empty_to_taken=0.1,
        prob_taken_to_empty=0.05,
        fps=10,
        background_path="./fotos/background.png"  # Path to the background image
    )
    sim.run()

