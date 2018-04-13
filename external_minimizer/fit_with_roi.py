"""
Prototype of fitting with ROI using external minimizer.
"""
import bornagain as ba
from bornagain import nm, deg, angstrom
import numpy as np
import lmfit


class SimulationBuilder:
    def __init__(self):
        self.radius = 5.0*nm
        self.lattice_length = 10.0*nm

    def build_simulation(self, params=None):
        if params:
            self.radius = params["radius"].value
            self.lattice_length = params["length"].value

        print("radius: {:6.3f} length:{:6.3f}".format(self.radius, self.lattice_length))

        simulation = ba.GISASSimulation()
        simulation.setDetectorParameters(100, -1.0 * deg, 1.0 * deg,
                                         100, 0.0 * deg, 2.0 * deg)
        simulation.setBeamParameters(1.0 * angstrom, 0.2 * deg, 0.0 * deg)
        simulation.setBeamIntensity(1e+08)
        simulation.setSample(self.build_sample())
        return simulation

    def build_sample(self):
        m_air = ba.HomogeneousMaterial("Air", 0.0, 0.0)
        m_substrate = ba.HomogeneousMaterial("Substrate", 6e-6, 2e-8)
        m_particle = ba.HomogeneousMaterial("Particle", 6e-4, 2e-8)

        sphere_ff = ba.FormFactorFullSphere(self.radius)
        sphere = ba.Particle(m_particle, sphere_ff)
        particle_layout = ba.ParticleLayout()
        particle_layout.addParticle(sphere)

        interference = ba.InterferenceFunction2DLattice.createHexagonal(self.lattice_length)
        pdf = ba.FTDecayFunction2DCauchy(10 * nm, 10 * nm)
        interference.setDecayFunction(pdf)

        particle_layout.setInterferenceFunction(interference)

        air_layer = ba.Layer(m_air)
        air_layer.addLayout(particle_layout)
        substrate_layer = ba.Layer(m_substrate, 0)
        multi_layer = ba.MultiLayer()
        multi_layer.addLayer(air_layer)
        multi_layer.addLayer(substrate_layer)
        return multi_layer


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


def create_experimental_data():
    """
    Generating "real" data by adding noise to the simulated data.
    """
    simulation = SimulationBuilder().build_simulation()
    simulation.runSimulation()

    # retrieving simulated data in the form of numpy array
    real_data = simulation.result().array()

    # spoiling simulated data with noise to produce "real" data
    np.random.seed(0)
    noise_factor = 0.1
    noisy = np.random.normal(real_data, noise_factor*np.sqrt(real_data))
    noisy[noisy < 0.1] = 0.1
    return noisy


def run_fitting():
    real_data = create_experimental_data()

    fit_object = FitObject()
    fit_object.set_data(SimulationBuilder(), real_data)

    ba.ploi

    # fit_object = FitObject()
    # fit_object.set_data(SimulationBuilder(), real_data)
    #
    # params = lmfit.Parameters()
    # params.add('radius', value=8*nm)
    # params.add('length', value=8*nm)
    #
    # result = lmfit.minimize(fit_object.evaluate, params)
    #
    # result.params.pretty_print()



if __name__ == '__main__':
    run_fitting()
