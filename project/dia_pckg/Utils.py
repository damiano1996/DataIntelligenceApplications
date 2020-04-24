import numpy as np


def polynomial(y, rank):
    """
        Polynomial approximation
    :param y: vector to smooth
    :param rank: rank of the poly
    :return:
    """
    x = range(len(y))
    coeffs = np.polyfit(x, y, rank)
    new_y = []
    for xi in x:
        new_xi = 0

        for i in range(rank + 1):
            coef = coeffs[len(coeffs) - 1 - i]
            new_xi += coef * xi ** i
        new_y.append(new_xi)

    return np.asarray(new_y)
