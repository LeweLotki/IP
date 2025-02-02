from simulation.simulation import GridSimulation

if __name__ == "__main__":
    sim = GridSimulation(
        background_path="./fotos/background.png",
        prob_empty_to_taken=0.1,
        prob_taken_to_empty=0.05,
        fps=10
    )
    sim.run()

