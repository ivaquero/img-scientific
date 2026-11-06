"""
Original Author: Xavier Yang
Link: https://github.com/ivaquero
"""

import numpy as np


def multi_gaussian_product(mean1, cov1, mean2, cov2):
    cov1 = np.asarray(cov1)
    cov2 = np.asarray(cov2)
    mean1 = np.asarray(mean1)
    mean2 = np.asarray(mean2)

    sum_inv = np.linalg.inv(cov1 + cov2)
    mean = cov2 @ sum_inv @ mean1 + cov1 @ sum_inv @ mean2
    cov = cov1 @ sum_inv @ cov2

    return mean, cov
