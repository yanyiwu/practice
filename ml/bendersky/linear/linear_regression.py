import numpy as np
import time

def generate_data(n, m=2.25, b=6.0, stddev=1.5):
    """Generate n data points approximating given line.
    m, b: line slope and intercept.
    stddev: standard deviation of added error.
    Returns pair x, y: arrays of length n.
    """
    x = np.linspace(-2.0, 2.0, n)
    y = x * m + b + np.random.normal(loc=0, scale=stddev, size=n)
    return x, y

def compute_cost(x, y, m, b):
    """Compute the MSE cost of a prediction based on m, b.

    x: inputs vector
    y: observed outputs vector
    m, b: regression parameters

    Returns: a scalar cost.
    """
    yhat = m * x + b
    diff = yhat - y
    # Vectorized computation using a dot product to compute sum of squares.
    cost = np.dot(diff.T, diff) / float(x.shape[0])
    # Cost is a 1x1 matrix, we need a scalar.
    return cost.flat[0]

def gradient_descent(x, y, nsteps, learning_rate = 0.1):
    m = 0.0
    b = 0.0
    n = x.shape[0]
    yield m, b, compute_cost(x, y, m, b)
    for step in range(nsteps):
        dm = learning_rate * 2 * ((m * x + b - y) * x).sum() / float(n)
        db = learning_rate * 2 * (m * x + b - y).sum() / float(n)
        m = m - dm
        b = b -db
        yield m, b, compute_cost(x, y, m, b)
    pass

if __name__ == '__main__':
    np.random.seed(int(time.time()))
    x,y = generate_data(500)
    import matplotlib.pyplot as plt
    #plt.plot(x, y)
    #plt.show()
    for m, b, c in gradient_descent(x, y, 300):
        print m,b,c
