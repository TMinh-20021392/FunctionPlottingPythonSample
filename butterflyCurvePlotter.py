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
        
        # Initialize butterfly curve parameters with defaults
        self.wing_frequency = 4  # Number of wings
        self.wing_amplitude = 2  # Size of the wings
        self.sine_stretch = 24   # Stretching factor
        
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
        
        # Parameters frame
        params_frame = ttk.LabelFrame(control_frame, text="Curve Parameters", padding=10)
        params_frame.grid(row=1, column=0, pady=(0, 20), sticky="ew")
        params_frame.columnconfigure(0, weight=1)
        params_frame.columnconfigure(1, weight=1)
        
        # Wing Frequency
        freq_label = ttk.Label(params_frame, text="Wing Frequency:")
        freq_label.grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        self.freq_var = tk.StringVar(value=str(self.wing_frequency))
        self.freq_entry = ttk.Entry(params_frame, textvariable=self.freq_var, width=10)
        self.freq_entry.grid(row=0, column=1, padx=(10, 0), sticky="e", pady=(0, 5))
        
        freq_info = ttk.Label(params_frame, text="(Number of wings)")
        freq_info.grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 10))
        
        # Wing Amplitude
        amp_label = ttk.Label(params_frame, text="Wing Amplitude:")
        amp_label.grid(row=2, column=0, sticky="w", pady=(0, 5))
        
        self.amp_var = tk.StringVar(value=str(self.wing_amplitude))
        self.amp_entry = ttk.Entry(params_frame, textvariable=self.amp_var, width=10)
        self.amp_entry.grid(row=2, column=1, padx=(10, 0), sticky="e", pady=(0, 5))
        
        amp_info = ttk.Label(params_frame, text="(Size of wings)")
        amp_info.grid(row=3, column=0, columnspan=2, sticky="w", pady=(0, 10))
        
        # Sine Stretch
        stretch_label = ttk.Label(params_frame, text="Sine Stretch:")
        stretch_label.grid(row=4, column=0, sticky="w", pady=(0, 5))
        
        self.stretch_var = tk.StringVar(value=str(self.sine_stretch))
        self.stretch_entry = ttk.Entry(params_frame, textvariable=self.stretch_var, width=10)
        self.stretch_entry.grid(row=4, column=1, padx=(10, 0), sticky="e", pady=(0, 5))
        
        stretch_info = ttk.Label(params_frame, text="(Stretching factor)")
        stretch_info.grid(row=5, column=0, columnspan=2, sticky="w", pady=(0, 10))
        
        # Apply button
        apply_button = ttk.Button(params_frame, text="Apply Changes", command=self.on_apply)
        apply_button.grid(row=6, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        
        # Equation information
        equation_frame = ttk.LabelFrame(control_frame, text="Equation Information", padding=10)
        equation_frame.grid(row=2, column=0, pady=(0, 20), sticky="ew")
        
        equation_text = """Butterfly Curve Equation:

r = eᶿˢⁱⁿ⁽ᶿ⁾ - A×cos(F×θ) + sin⁵((2θ - π)/S)

Where:
• r is the radius
• θ is the angle
• e is the mathematical constant (≈2.71828)
• π is the mathematical constant pi (≈3.14159)
• F is the wing frequency
• A is the wing amplitude
• S is the sine stretch factor

This equation generates a butterfly-shaped curve
in polar coordinates."""
        
        equation_label = ttk.Label(equation_frame, text=equation_text, justify="left")
        equation_label.grid(row=0, column=0, sticky="w")
        
        # Instructions
        instructions_frame = ttk.LabelFrame(control_frame, text="Instructions", padding=10)
        instructions_frame.grid(row=3, column=0, pady=(0, 20), sticky="ew")
        
        instructions_text = """• Adjust parameters to customize the butterfly shape
• Hold Ctrl + Mouse Scroll to zoom in/out
• Right-click and drag to pan the view
• Use toolbar buttons for additional controls
• Double-click on the plot to reset the view"""
        
        instructions_label = ttk.Label(instructions_frame, text=instructions_text, justify="left")
        instructions_label.grid(row=0, column=0, sticky="w")
        
        # Reset Button
        reset_button = ttk.Button(control_frame, text="Reset View", command=self.reset_view)
        reset_button.grid(row=4, column=0, pady=(0, 20), sticky="ew")
        
        # Add some spacing at the bottom
        spacer = ttk.Label(control_frame, text="")
        spacer.grid(row=5, column=0, sticky="ew")

    def on_apply(self):
        # Initialize variable to track if we need to update the plot
        update_needed = False
        
        # Validate wing frequency
        try:
            freq_value = int(self.freq_var.get())
            if freq_value < 0:
                freq_value = 4
                self.freq_var.set("4")
            self.wing_frequency = freq_value
            update_needed = True
        except ValueError:
            # Handle invalid input
            self.wing_frequency = 4
            self.freq_var.set("4")
            update_needed = True
        
        # Validate wing amplitude
        try:
            amp_value = float(self.amp_var.get())
            if amp_value < 0:
                amp_value = 2
                self.amp_var.set("2")
            self.wing_amplitude = amp_value
            update_needed = True
        except ValueError:
            # Handle invalid input
            self.wing_amplitude = 2
            self.amp_var.set("2")
            update_needed = True
        
        # Validate sine stretch
        try:
            stretch_value = int(self.stretch_var.get())
            if stretch_value < 0:
                stretch_value = 24
                self.stretch_var.set("24")
            self.sine_stretch = stretch_value
            update_needed = True
        except ValueError:
            # Handle invalid input
            self.sine_stretch = 24
            self.stretch_var.set("24")
            update_needed = True
        
        # Only update the plot if at least one input was valid or corrected
        if update_needed:
            self.update_plot()

    def update_plot(self):
        # Clear the previous plot
        self.ax.clear()
        
        # Calculate theta values
        theta = np.linspace(0, self.max_theta, self.n_points)
        
        # Calculate r using the butterfly curve equation with the current parameters
        r = np.exp(np.sin(theta)) - self.wing_amplitude * np.cos(self.wing_frequency * theta) + np.power(np.sin((2 * theta - np.pi) / self.sine_stretch), 5)
        
        # Convert to Cartesian coordinates
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        
        # Plot the curve
        self.ax.plot(x, y, color='purple', linewidth=1.5)
        
        # Set up the axis
        self.ax.set_title(f"Butterfly Curve\nFrequency: {self.wing_frequency}, Amplitude: {self.wing_amplitude}, Stretch: {self.sine_stretch}", fontsize=14)
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