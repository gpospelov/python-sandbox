"""
Checking access GISASSimulation::result()
-checks empty simulation
-test various plotting utils
"""
import bornagain as ba
from simulation_builder import SimulationBuilder
from matplotlib import pyplot as plt
import numpy as np


def test_plot_utils():
    simulation = SimulationBuilder().build_simulation()
    # simulation.runSimulation()
    result = simulation.result()

    fig = plt.figure(figsize=(12.80, 10.24))
    plt.subplot(2, 2, 1)

    arr = np.zeros((5, 3))
    ba.plot_array(arr)

    plt.subplot(2, 2, 2)
    arr = np.array([[ 1,  2,  3,  4,  5],
                    [ 6,  7,  8,  9, 10],
                    [11, 12, 13, 14, 15]])
    ba.plot_array(arr)


    plt.subplot(2, 2, 3)
    ba.plot_colormap(result)

    plt.subplot(2, 2, 4)
    ba.plot_histogram(result.histogram2d())

    fig.tight_layout()


def test_roi():
    simulation = SimulationBuilder().build_simulation()
    result = simulation.result()

    fig = plt.figure(figsize=(12.80, 10.24))
    plt.subplot(2, 2, 1)


if __name__ == '__main__':
    # test_plot_utils()
    test_roi()
    plt.show()
