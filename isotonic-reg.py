import numpy as np
import matplotlib.pyplot as plt
from sklearn.isotonic import IsotonicRegression
from sklearn.linear_model import LinearRegression

# Generate sample data
np.random.seed(42)
x = np.arange(100)
y = np.random.randint(0, 50, size=100)

# Create and fit the isotonic regression model
ir = IsotonicRegression()
y_iso = ir.fit_transform(x, y)

# Create and fit the linear regression model
lr = LinearRegression()
y_linear = lr.fit(x.reshape(-1, 1), y).predict(x.reshape(-1, 1))

# Plot the results
plt.figure(figsize=(12, 6))
plt.scatter(x, y, alpha=0.5, label='Original Data')
plt.scatter(x, y_iso, color='r', label='Isotonic Regression')
plt.scatter(x, y_linear, color='g', label='Linear Regression')
plt.title('Isotonic Regression vs Linear Regression')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.grid(True)

# Display the plot
plt.show()

# Print some statistics
print(f"Number of original data points: {len(x)}")
print(f"Number of monotonic intervals after isotonic regression: {len(ir.f_.x)}")

