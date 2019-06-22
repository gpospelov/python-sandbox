"""
Plots mandelbrot set.
"""
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors
from tqdm import tqdm


MAX_ITER = 1000
RE_MIN, RE_MAX, N_RE = -2.0, 1.0, 1000
IM_MIN, IM_MAX, N_IM = -1.0, 1.0, 1000


def generate_c():
    """
    Generates sequence of complex constants for mandelbrot set.
    """
    re_points = np.linspace(RE_MIN, RE_MAX, N_RE)
    im_points = np.linspace(IM_MIN, IM_MAX, N_IM)
    for nx, re_value in np.ndenumerate(re_points):
        for ny, im_value in np.ndenumerate(im_points):
            yield nx, ny, complex(re_value, im_value)


def get_bounded_niter(c):
    """
    Returns number of iterations where z-sequence is bounded.
    """
    z = complex(0, 0)
    n_iter = 0
    while abs(z) <= 2.0 and n_iter<MAX_ITER:
        z = z*z + c
        n_iter += 1
    return n_iter


def plot_mandelbrot():
    """
    Plots mandelbrot set.
    """
    array = np.zeros((N_RE, N_IM))
    for nx, ny, c in tqdm(generate_c(), total=N_RE*N_IM):
        # color = 255 - int(get_bounded_niter(c) * 255 / MAX_ITER)
        # array[nx][ny] = color
        array[nx][ny] = get_bounded_niter(c)

    fig = plt.figure(figsize=(15, 15))
    # norm = colors.Normalize(0, 255*1.2)  # for better gradient appearance
    norm = colors.LogNorm(1.0, MAX_ITER)
    im = plt.imshow(array, norm=norm, extent = [RE_MIN, RE_MAX, IM_MIN, IM_MAX], aspect="auto", cmap="afmhot")
    fig.savefig("mandelbrot.png")
    plt.colorbar(im)


if __name__ == '__main__':
    plot_mandelbrot()
    plt.show()



