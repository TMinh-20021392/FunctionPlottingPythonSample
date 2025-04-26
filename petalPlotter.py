import numpy as np
import matplotlib.pyplot as plt

# Parameters
n_petals = 1  # Number of petals
theta_zoom = np.linspace(0, 6 * np.pi, 1000)      # small-scale
theta_large = np.linspace(0, 24 * np.pi, 3000)    # large-scale

# Polar functions
r_zoom = theta_zoom * np.sin(n_petals * theta_zoom)
r_large = theta_large * np.sin(n_petals * theta_large)

# Convert to Cartesian coordinates
x_zoom = r_zoom * np.cos(theta_zoom)
y_zoom = r_zoom * np.sin(theta_zoom)

x_large = r_large * np.cos(theta_large)
y_large = r_large * np.sin(theta_large)

# Plotting
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Left: Zoomed-in view (like around unit circle e^(iθ))
ax1.plot(x_zoom, y_zoom, color='teal')
ax1.set_title("Zoomed-In Petal Pattern (Small Scale)")
ax1.set_xlim(-2, 2)
ax1.set_ylim(-2, 2)
ax1.set_aspect('equal')
ax1.grid(True)

# Right: Full expanding petal pattern
ax2.plot(x_large, y_large, color='darkviolet')
ax2.set_title("Expanding Flower Petal Pattern (Large Scale)")
ax2.set_xlim(-80, 80)
ax2.set_ylim(-80, 80)
ax2.set_aspect('equal')
ax2.grid(True)

plt.tight_layout()
plt.show()
