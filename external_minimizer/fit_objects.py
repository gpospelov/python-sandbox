"""
Prototype of new FitObject
"""


class FitObject:
    def __init__(self):
        self.m_simulation_builder = None
        self.m_experimental_data = None
        pass

    def set_data(self, simulation_builder, real_data):
        self.m_simulation_builder = simulation_builder
        self.m_experimental_data = real_data

    def evaluate(self, params):
        simulation = self.m_simulation_builder.build_simulation(params)
        simulation.runSimulation()
        result = simulation.result().array().flatten()
        exp = self.m_experimental_data.flatten()
        res = result-exp
        return res

