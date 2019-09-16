from lmfit import minimize, Parameters
from matplotlib import pyplot as plt
import numpy as np


def func(params, x):
    amp = params['amp']
    phaseshift = params['phase']
    freq = params['frequency']
    decay = params['decay']
    print(amp.value, phaseshift.value, freq.value, decay.value)

    model = amp * np.sin(x*freq + phaseshift) * np.exp(-x*x*decay)
    return model


class Model:
    def __init__(self):
        self._fig = plt.figure(figsize=(10.25, 7.69))
        self._fig.canvas.draw()
        self.m_x = np.linspace(0.0, 10.0, 100)
        self.m_params = Parameters()
        self.m_params.add('amp', value=10)
        self.m_params.add('decay', value=0.05)
        self.m_params.add('phase', value=1.0)
        self.m_params.add('frequency', value=4.0)
        self.m_eps_data = np.full_like(self.m_x, 0.01)
        self.m_data = func(self.m_params, self.m_x)

    def residual(self, params):
        model = func(params, self.m_x)
        return (self.m_data - model) / self.m_eps_data

    def reset(self):
        self._fig.clf()

    def plot(self, params, iter, resid):
        self.reset()
        plt.subplot(2, 1, 1)
        plt.plot(self.m_x, resid, 'r-')
        plt.subplot(2, 1, 2)
        plt.plot(self.m_x, self.m_data, 'b-')
        plt.plot(self.m_x, func(params, self.m_x), 'k-')
        plt.pause(0.01)


def run_minimization():
    x, data, eps_data = get_data()

    params = Parameters()
    params.add('amp', value=1, min=0.0)
    params.add('decay', value=0.1, min=0.0)
    params.add('phase', value=0.1, min=0.0, max=3.1)
    params.add('frequency', value=1.0, min=0.0)

    model = Model()

    out = minimize(model.residual, params, iter_cb=model.plot)
    out.params.pretty_print()


def get_data():
    params = Parameters()
    params.add('amp', value=10)
    params.add('decay', value=0.05)
    params.add('phase', value=0.0)
    params.add('frequency', value=4.0)
    x = np.linspace(1.0, 10.0, 100)
    eps_data = np.full_like(x, 0.01)
    return x, func(params, x), eps_data


def plot_func():
    x, data, eps_data = get_data()
    plt.plot(x, data)
    plt.show()


if __name__ == '__main__':
    # plot_func()
    run_minimization()
    plt.show()
