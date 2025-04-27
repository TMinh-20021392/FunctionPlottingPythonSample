import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
import matplotlib as mpl

from PlotApp import PlotApp

class ButterflyPlotterApp(PlotApp):
    def __init__(self, root):
        # Initialize parameters
        self.max_theta = 24 * np.pi
        self.n_points = 5000
        
        # Initialize the base class
        super().__init__(root, "Butterfly Curve Plotter")

    def create_control_panel(self):
        # Create frame for controls
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.grid(row=0, column=0, sticky="nsew")
        control_frame.columnconfigure(0, weight=1)
        
        # Title
        title_label = ttk.Label(control_frame, text="Butterfly Curve Plotter", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, pady=(0, 20), sticky="w")
        
        # Equation information
        equation_frame = ttk.LabelFrame(control_frame, text="Equation Information", padding=10)
        equation_frame.grid(row=1, column=0, pady=(0, 20), sticky="ew")
        
        equation_text = """Butterfly Curve Equation:

r = eᶿˢⁱⁿ⁽ᶿ⁾ - 2cos(4θ) + sin⁵((2θ - π)/24)

Where:
• r is the radius
• θ is the angle
• e is the mathematical constant (≈2.71828)
• π is the mathematical constant pi (≈3.14159)

This equation generates a butterfly-shaped curve
in polar coordinates."""
        
        equation_label = ttk.Label(equation_frame, text=equation_text, justify="left")
        equation_label.grid(row=0, column=0, sticky="w")
        
        # Instructions
        instructions_frame = ttk.LabelFrame(control_frame, text="Instructions", padding=10)
        instructions_frame.grid(row=2, column=0, pady=(0, 20), sticky="ew")
        
        instructions_text = """• Hold Ctrl + Mouse Scroll to zoom in/out
• Right-click and drag to pan the view
• Use toolbar buttons for additional controls
• Double-click on the plot to reset the view"""
        
        instructions_label = ttk.Label(instructions_frame, text=instructions_text, justify="left")
        instructions_label.grid(row=0, column=0, sticky="w")
        
        # Reset Button
        reset_button = ttk.Button(control_frame, text="Reset View", command=self.reset_view)
        reset_button.grid(row=3, column=0, pady=(0, 20), sticky="ew")
        
        # Add some spacing at the bottom
        spacer = ttk.Label(control_frame, text="")
        spacer.grid(row=4, column=0, sticky="ew")

    def update_plot(self):
        # Clear the previous plot
        self.ax.clear()
        
        # Calculate theta values
        theta = np.linspace(0, self.max_theta, self.n_points)
        
        # Calculate r using the butterfly curve equation
        wing_frequency = 4 # Number of wings
        wing_amplitude = 2 # Size of the wings
        sine_stretch = 24 # Stretching factor

        r = np.exp(np.sin(theta)) - wing_amplitude * np.cos(wing_frequency * theta) + np.power(np.sin((2 * theta - np.pi) / sine_stretch), 5)
        
        # Convert to Cartesian coordinates
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        
        # Plot the curve
        self.ax.plot(x, y, color='purple', linewidth=1.5)
        
        # Set up the axis
        self.ax.set_title("Butterfly Curve", fontsize=14)
        self.ax.set_aspect('equal')
        self.ax.grid(True, linestyle='--', alpha=0.7)
        
        # Get good limits based on the data
        max_range = max(abs(np.max(x)), abs(np.min(x)), abs(np.max(y)), abs(np.min(y)))
        self.ax.set_xlim(-max_range*1.1, max_range*1.1)
        self.ax.set_ylim(-max_range*1.1, max_range*1.1)
        
        # Update the figure
        self.fig.tight_layout()
        self.canvas.draw()


def main():
    # Configure matplotlib to use a more modern style
    plt.style.use('ggplot')
    
    # Create the tkinter root window
    root = tk.Tk()
    
    # Create and run the app
    app = ButterflyPlotterApp(root)
    
    # Start the main loop
    root.mainloop()

if __name__ == "__main__":
    main()