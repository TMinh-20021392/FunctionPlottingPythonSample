import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
from tkinter import ttk, messagebox
import math
import matplotlib as mpl

from PlotApp import PlotApp

class StarPolygonPlotterApp(PlotApp):
    def __init__(self, root):
        # Initialize parameters
        self.p = 5  # Number of points (default to a regular pentagon)
        self.q = 2  # Connection step (default to connect every 2nd point)
        self.n_points = 1000  # Resolution for plotting
        
        # Initialize the base class
        super().__init__(root, "Star Polygon Plotter")

    def create_control_panel(self):
        """Create the content for the scrollable control panel"""
        # Title
        title_label = ttk.Label(self.control_frame, text="Star Polygon Plotter", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, pady=(0, 20), sticky="w")
        
        # Parameters frame
        params_frame = ttk.LabelFrame(self.control_frame, text="Polygon Parameters", padding=10)
        params_frame.grid(row=1, column=0, pady=(0, 20), sticky="ew")
        params_frame.columnconfigure(0, weight=1)
        params_frame.columnconfigure(1, weight=1)
        
        # P parameter
        p_label = ttk.Label(params_frame, text="P Value:")
        p_label.grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        self.p_var = tk.StringVar(value=str(self.p))
        self.p_entry = ttk.Entry(params_frame, textvariable=self.p_var, width=10)
        self.p_entry.grid(row=0, column=1, padx=(10, 0), sticky="e", pady=(0, 5))
        
        p_info = ttk.Label(params_frame, text="(Number of points, must be ≥ 3)")
        p_info.grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 10))
        
        # Q parameter
        q_label = ttk.Label(params_frame, text="Q Value:")
        q_label.grid(row=2, column=0, sticky="w", pady=(0, 5))
        
        self.q_var = tk.StringVar(value=str(self.q))
        self.q_entry = ttk.Entry(params_frame, textvariable=self.q_var, width=10)
        self.q_entry.grid(row=2, column=1, padx=(10, 0), sticky="e", pady=(0, 5))
        
        q_info = ttk.Label(params_frame, text="(Connection step, 1 ≤ q < p/2)")
        q_info.grid(row=3, column=0, columnspan=2, sticky="w", pady=(0, 10))
        
        # Apply button
        apply_button = ttk.Button(params_frame, text="Apply Changes", command=self.on_apply)
        apply_button.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        
        # Explanation
        explanation_frame = ttk.LabelFrame(self.control_frame, text="Star Polygon Information", padding=10)
        explanation_frame.grid(row=2, column=0, pady=(0, 20), sticky="ew")
        
        explanation_text = """A star polygon {p/q} is formed by:

• Placing p points equally around a circle
• Connecting each point to the point q steps away
• Continuing until all points are connected

Requirements:
• p and q must be positive integers
• p and q must be relatively prime (no common factors)
• To create a proper star: 1 ≤ q < p/2

Examples:
• {5/2}: Regular pentagram (5-pointed star)
• {7/3}: 7-pointed star
• {8/3}: 8-pointed star"""
        
        explanation_label = ttk.Label(explanation_frame, text=explanation_text, justify="left")
        explanation_label.grid(row=0, column=0, sticky="w")
        
        # Instructions
        instructions_frame = ttk.LabelFrame(self.control_frame, text="Instructions", padding=10)
        instructions_frame.grid(row=3, column=0, pady=(0, 20), sticky="ew")
        
        instructions_text = """• Enter values for p and q
• p and q must be relatively prime integers
• Hold Ctrl + Mouse Scroll to zoom in/out
• Right-click and drag to pan the view
• Use toolbar buttons for additional controls
• Double-click on the plot to reset the view"""
        
        instructions_label = ttk.Label(instructions_frame, text=instructions_text, justify="left")
        instructions_label.grid(row=0, column=0, sticky="w")
        
        # Reset Button
        reset_button = ttk.Button(self.control_frame, text="Reset View", command=self.reset_view)
        reset_button.grid(row=4, column=0, pady=(0, 20), sticky="ew")
        
        # Add some spacing at the bottom
        spacer = ttk.Label(self.control_frame, text="")
        spacer.grid(row=5, column=0, sticky="ew")

    def gcd(self, a, b):
        """Calculate the greatest common divisor of a and b"""
        while b:
            a, b = b, a % b
        return a

    def are_relatively_prime(self, a, b):
        """Check if a and b are relatively prime (gcd = 1)"""
        return self.gcd(a, b) == 1

    def on_apply(self):
        """Handle apply button click - validate inputs and update plot"""
        # Validate p (number of points)
        try:
            p_value = int(self.p_var.get())
            if p_value < 3:
                messagebox.showerror("Invalid Input", "P must be at least 3")
                return
        except ValueError:
            messagebox.showerror("Invalid Input", "P must be a positive integer")
            return
        
        # Validate q (connection step)
        try:
            q_value = int(self.q_var.get())
            if q_value < 1:
                messagebox.showerror("Invalid Input", "Q must be at least 1")
                return
            if q_value >= p_value/2:
                messagebox.showerror("Invalid Input", f"Q must be less than P/2 ({p_value/2})")
                return
        except ValueError:
            messagebox.showerror("Invalid Input", "Q must be a positive integer")
            return
        
        # Check if p and q are relatively prime
        if not self.are_relatively_prime(p_value, q_value):
            messagebox.showerror("Invalid Input", f"P and Q must be relatively prime\nGCD({p_value}, {q_value}) = {self.gcd(p_value, q_value)}")
            return
        
        # Update parameters and plot
        self.p = p_value
        self.q = q_value
        self.update_plot()

    def update_plot(self):
        """Update the star polygon plot with current parameters"""
        # Clear the previous plot
        self.ax.clear()
        
        # Calculate the points on the circle
        theta = 2 * np.pi * np.arange(self.p) / self.p
        x = np.cos(theta)
        y = np.sin(theta)
        
        # Create a list of points for the star polygon
        points_x = []
        points_y = []
        
        # For drawing the star polygon with lines
        for i in range(self.p):
            # Start point
            points_x.append(x[i])
            points_y.append(y[i])
            
            # Connect to the point q steps away (wrapping around if needed)
            target_idx = (i + self.q) % self.p
            points_x.append(x[target_idx])
            points_y.append(y[target_idx])
            
            # Add None to break the line for the next segment
            points_x.append(None)
            points_y.append(None)
        
        # Plot the regular polygon outline (dashed)
        polygon_x = np.append(x, x[0])
        polygon_y = np.append(y, y[0])
        self.ax.plot(polygon_x, polygon_y, 'b--', alpha=0.5, label="Regular Polygon")
        
        # Plot the star polygon (solid)
        self.ax.plot(points_x, points_y, 'r-', linewidth=1.5, label="Star Polygon")
        
        # Plot the points
        self.ax.plot(x, y, 'ko', markersize=6)
        
        # Set up the axis
        title = f"Star Polygon {{p/q}} = {{{self.p}/{self.q}}}"
        self.ax.set_title(title, fontsize=14)
        self.ax.set_aspect('equal')
        self.ax.grid(True, linestyle='--', alpha=0.7)
        
        # Add legend
        self.ax.legend(loc='upper right')
        
        # Set limits with a bit of padding
        padding = 0.2
        self.ax.set_xlim(-1-padding, 1+padding)
        self.ax.set_ylim(-1-padding, 1+padding)
        
        # Remove axis labels
        self.ax.set_xticklabels([])
        self.ax.set_yticklabels([])
        
        # Number the points (optional)
        for i in range(self.p):
            self.ax.annotate(str(i), (x[i]*1.1, y[i]*1.1), fontsize=10)
        
        # Update the figure
        self.fig.tight_layout()
        self.canvas.draw()


def main():
    # Configure matplotlib to use a more modern style
    plt.style.use('ggplot')
    
    # Create the tkinter root window
    root = tk.Tk()
    
    # Create and run the app
    app = StarPolygonPlotterApp(root)
    
    # Start the main loop
    root.mainloop()

if __name__ == "__main__":
    main()