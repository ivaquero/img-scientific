import matplotlib.pyplot as plt
import numpy as np


def transformation_1(point):
    x, y = point
    x_new = 0.85 * x + 0.04 * y
    y_new = -0.04 * x + 0.85 * y + 1.6
    return x_new, y_new


def transformation_2(point):
    x, y = point
    x_new = 0.20 * x - 0.26 * y
    y_new = 0.23 * x + 0.22 * y + 1.6
    return x_new, y_new


def transformation_3(point):
    x, y = point
    x_new = -0.15 * x + 0.28 * y
    y_new = 0.26 * x + 0.24 * y + 0.44
    return x_new, y_new


def transformation_4(point):
    _, y = point
    x_new = 0.0
    y_new = 0.16 * y
    return x_new, y_new


transformations = [
    transformation_1,
    transformation_2,
    transformation_3,
    transformation_4,
]
probabilities = [0.85, 0.07, 0.07, 0.01]


def generate_fern(num_points):
    points = [(0, 0)]
    current_point = np.array([0, 0])
    rng = np.random.default_rng()
    for _ in range(num_points):
        random_transformation = rng.choice(transformations, p=probabilities)
        current_point = random_transformation(current_point)
        points.append(tuple(current_point))

    return points


num_points = 50000
fern_points = generate_fern(num_points)

x_vals, y_vals = zip(*fern_points, strict=True)

plt.figure(figsize=(6, 9))
plt.scatter(x_vals, y_vals, s=0.2, c="green")
plt.title("Barnsley Fern")
plt.axis("off")
plt.show()
