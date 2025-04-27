import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib as mpl

from PlotApp import PlotApp

class PetalPlotterApp(PlotApp):
    def __init__(self, root):
        # Set default parameters
        self.n_petals = 3
        self.max_theta = 24 * np.pi
        self.n_points = 3000
        self.face_radius = 1
        
        # Initialize the base class
        super().__init__(root, "Interactive Petal Plotter")

    def create_control_panel(self):
        # Create frame for controls
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.grid(row=0, column=0, sticky="nsew")
        control_frame.columnconfigure(0, weight=1)
        
        # Title
        title_label = ttk.Label(control_frame, text="Petal Plotter Controls", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, pady=(0, 20), sticky="w")
        
        # Input for number of petals
        petals_frame = ttk.Frame(control_frame)
        petals_frame.grid(row=1, column=0, pady=(0, 10), sticky="ew")
        
        petals_label = ttk.Label(petals_frame, text="Number of Petals:")
        petals_label.grid(row=0, column=0, sticky="w")
        
        self.petals_var = tk.StringVar(value=str(self.n_petals))
        self.petals_entry = ttk.Entry(petals_frame, textvariable=self.petals_var, width=10)
        self.petals_entry.grid(row=0, column=1, padx=(10, 0), sticky="e")
        
        # Input for face radius
        face_frame = ttk.Frame(control_frame)
        face_frame.grid(row=2, column=0, pady=(0, 10), sticky="ew")
        
        face_label = ttk.Label(face_frame, text="Face Radius:")
        face_label.grid(row=0, column=0, sticky="w")
        
        self.face_var = tk.StringVar(value=str(self.face_radius))
        self.face_entry = ttk.Entry(face_frame, textvariable=self.face_var, width=10)
        self.face_entry.grid(row=0, column=1, padx=(10, 0), sticky="e")
        
        apply_button = ttk.Button(control_frame, text="Apply", command=self.on_apply)
        apply_button.grid(row=3, column=0, padx=(10, 0), pady=(0, 10), sticky="e")
        
        # Formula selection
        formula_frame = ttk.LabelFrame(control_frame, text="Formula Type", padding=10)
        formula_frame.grid(row=4, column=0, pady=(20, 0), sticky="ew")
        
        self.formula_type = tk.StringVar(value="spiral_sin")
        ttk.Radiobutton(formula_frame, text="Spiral Petal (Sin)", 
                         variable=self.formula_type, value="spiral_sin",
                         command=self.update_plot).grid(row=0, column=0, sticky="w")
        ttk.Radiobutton(formula_frame, text="Spiral Petal (Cos)", 
                         variable=self.formula_type, value="spiral_cos",
                         command=self.update_plot).grid(row=1, column=0, sticky="w")
        ttk.Radiobutton(formula_frame, text="Rhodonea (Sin)", 
                         variable=self.formula_type, value="rhodonea_sin",
                         command=self.update_plot).grid(row=2, column=0, sticky="w")
        ttk.Radiobutton(formula_frame, text="Rhodonea (Cos)", 
                         variable=self.formula_type, value="rhodonea_cos",
                         command=self.update_plot).grid(row=3, column=0, sticky="w")
        
        # Function description
        function_frame = ttk.LabelFrame(control_frame, text="Function Information", padding=10)
        function_frame.grid(row=5, column=0, pady=(20, 0), sticky="ew")
        
        self.function_var = tk.StringVar(value="")
        function_label = ttk.Label(function_frame, textvariable=self.function_var, justify="left")
        function_label.grid(row=0, column=0, sticky="w")
        
        # Update function text based on initial selection
        self.update_function_text()
        
        # Instructions
        instructions_frame = ttk.LabelFrame(control_frame, text="Instructions", padding=10)
        instructions_frame.grid(row=6, column=0, pady=(20, 0), sticky="ew")
        
        instructions_text = """• Enter a whole number of petals (1-20)
• Enter face radius (0-1, affects rhodonea plots)
• Hold Ctrl + Mouse Scroll to zoom in/out
• Right-click and drag to pan the view
• Use toolbar buttons for additional controls
• Double-click on the plot to reset the view
• Try different formula types for various patterns"""
        
        instructions_label = ttk.Label(instructions_frame, text=instructions_text, justify="left")
        instructions_label.grid(row=0, column=0, sticky="w")
        
        # Reset Button
        reset_button = ttk.Button(control_frame, text="Reset View", command=self.reset_view)
        reset_button.grid(row=7, column=0, pady=(20, 0), sticky="ew")

    def update_function_text(self):
        formula_type = self.formula_type.get()
        
        if formula_type == "spiral_sin":
            self.function_var.set("""Spiral Petal (Sin) Formula:
r = θ × sin((n × θ) / 2)²

Where:
• r is the radius
• θ is the angle
• n is the number of petals

Properties:
• Always creates exactly n petals
• Spirals outward as θ increases
• Uses sine function for calculation""")
            
        elif formula_type == "spiral_cos":
            self.function_var.set("""Spiral Petal (Cos) Formula:
r = θ × cos((n × θ) / 2)²

Where:
• r is the radius
• θ is the angle
• n is the number of petals

Properties:
• Always creates exactly n petals
• Spirals outward as θ increases
• Uses cosine function for calculation""")
            
        elif formula_type == "rhodonea_sin":
            self.function_var.set("""Rhodonea (Sin) Formula:
r = sin(k × θ) + face_radius

Where:
• r is the radius
• θ is the angle
• k is adjusted to ensure n petals:
  - For even n: k = n/2 (with absolute value)
  - For odd n: k = n
• face_radius is the central area size

Properties:
• Always creates exactly n petals
• Fixed radius (bounded pattern)
• Uses sine function for calculation
• Face radius adds a central area""")
            
        elif formula_type == "rhodonea_cos":
            self.function_var.set("""Rhodonea (Cos) Formula:
r = cos(k × θ) + face_radius

Where:
• r is the radius
• θ is the angle
• k is adjusted to ensure n petals:
  - For even n: k = n/2 (with absolute value)
  - For odd n: k = n
• face_radius is the central area size

Properties:
• Always creates exactly n petals
• Fixed radius (bounded pattern)
• Uses cosine function for calculation
• Face radius adds a central area""")

    def update_plot(self):
        # Clear the previous plot
        self.ax.clear()
        
        # Update function text
        self.update_function_text()
        
        # Calculate the curve based on formula type
        theta = np.linspace(0, self.max_theta, self.n_points)
        
        formula_type = self.formula_type.get()
        
        if formula_type == "spiral_sin":
            # Spiral formula with sin function - exact petal count
            r = theta * np.sin((self.n_petals * theta) / 2) ** 2
            title = "Spiral Petal Pattern (Sin)"
            color = 'darkviolet'
            
        elif formula_type == "spiral_cos":
            # Spiral formula with cos function - exact petal count
            r = theta * np.cos((self.n_petals * theta) / 2) ** 2
            title = "Spiral Petal Pattern (Cos)"
            color = 'crimson'
            
        elif formula_type == "rhodonea_sin":
            # Rhodonea curve with sin function - exact petal count
            k = self.n_petals if self.n_petals % 2 == 1 else self.n_petals / 2
            if self.n_petals % 2 == 1:
                # odd: sin(kθ) gives k petals
                r = np.sin(k * theta) + self.face_radius
            else:
                # even: use abs to fold negative radii back, giving k*2 = n petals
                r = np.abs(np.sin(k * theta)) + self.face_radius
            title = "Rhodonea Pattern (Sin)"
            color = 'darkblue'

        elif formula_type == "rhodonea_cos":
            # Rhodonea curve with cos function - exact petal count
            k = self.n_petals if self.n_petals % 2 == 1 else self.n_petals / 2
            if self.n_petals % 2 == 1:
                r = np.cos(k * theta) + self.face_radius
            else:
                r = np.abs(np.cos(k * theta)) + self.face_radius
            title = "Rhodonea Pattern (Cos)"
            color = 'darkgreen'
        
        # Convert to Cartesian coordinates
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        
        # Plot the curve
        self.ax.plot(x, y, color=color, linewidth=1.5)
        
        # Set up the axis
        face_info = ""
        if formula_type.startswith("rhodonea"):
            face_info = f", Face Radius: {self.face_radius}"
        
        self.ax.set_title(f"{title}\n(Exactly {self.n_petals} petals{face_info})", fontsize=14)
        self.ax.set_aspect('equal')
        self.ax.grid(True, linestyle='--', alpha=0.7)
        
        # Get good limits based on the data
        max_range = max(abs(np.max(x)), abs(np.min(x)), abs(np.max(y)), abs(np.min(y)))
        self.ax.set_xlim(-max_range*1.1, max_range*1.1)
        self.ax.set_ylim(-max_range*1.1, max_range*1.1)
        
        # Update the figure
        self.fig.tight_layout()
        self.canvas.draw()

    def on_apply(self):
        # Initialize variables to track if we need to update the plot
        update_needed = False
        
        # Validate petal input - must be an integer between 1 and 20
        try:
            petal_value = int(self.petals_var.get())
            if petal_value < 1:
                petal_value = 1
                self.petals_var.set(1)
            elif petal_value > 20:
                petal_value = 20
                self.petals_var.set(20)
            self.n_petals = petal_value
            update_needed = True
        except ValueError:
            # Handle case where petal input isn't a valid integer
            petal_value = 1
            self.petals_var.set(1)
            self.n_petals = petal_value
            update_needed = True
        
        # Validate face radius input
        try:
            face_value = float(self.face_var.get())
            self.face_radius = face_value
            update_needed = True
        except ValueError:
            # Handle case where face input isn't a valid float
            face_value = 1.5
            self.face_var.set(1.5)
            self.face_radius = face_value
            update_needed = True
        
        # Only update the plot if at least one input was valid or corrected
        if update_needed:
            self.update_plot()

def main():
    # Configure matplotlib to use a more modern style
    plt.style.use('ggplot')
    
    # Create the tkinter root window
    root = tk.Tk()
    
    # Create and run the app
    app = PetalPlotterApp(root)
    
    # Start the main loop
    root.mainloop()

if __name__ == "__main__":
    main()