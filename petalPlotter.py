import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib as mpl

class PetalPlotterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Petal Plotter")
        self.root.state('zoomed')  # Make window full-screen on Windows
        
        # Set default parameters
        self.n_petals = 3
        self.max_theta = 24 * np.pi
        self.n_points = 3000
        
        # Configure the main window layout
        self.root.columnconfigure(0, weight=1)  # Control panel
        self.root.columnconfigure(1, weight=4)  # Plot area
        self.root.rowconfigure(0, weight=1)
        
        # Create the left control panel
        self.create_control_panel()
        
        # Create the right plot panel
        self.create_plot_panel()
        
        # Initialize the plot
        self.update_plot()

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
        
        apply_button = ttk.Button(petals_frame, text="Apply", command=self.on_apply)
        apply_button.grid(row=0, column=2, padx=(10, 0), sticky="e")
        
        # Formula selection
        formula_frame = ttk.LabelFrame(control_frame, text="Formula Type", padding=10)
        formula_frame.grid(row=2, column=0, pady=(20, 0), sticky="ew")
        
        self.formula_type = tk.StringVar(value="spiral")
        ttk.Radiobutton(formula_frame, text="Spiral Petal", 
                         variable=self.formula_type, value="spiral",
                         command=self.update_plot).grid(row=0, column=0, sticky="w")
        ttk.Radiobutton(formula_frame, text="Classic Rose", 
                         variable=self.formula_type, value="rose",
                         command=self.update_plot).grid(row=1, column=0, sticky="w")
        ttk.Radiobutton(formula_frame, text="Rhodonea (Exact Petals)", 
                         variable=self.formula_type, value="rhodonea",
                         command=self.update_plot).grid(row=2, column=0, sticky="w")
        ttk.Radiobutton(formula_frame, text="Spiral Rhodonea", 
                         variable=self.formula_type, value="spiral_rhodonea",
                         command=self.update_plot).grid(row=3, column=0, sticky="w")
        
        # Function description
        function_frame = ttk.LabelFrame(control_frame, text="Function Information", padding=10)
        function_frame.grid(row=3, column=0, pady=(20, 0), sticky="ew")
        
        self.function_var = tk.StringVar(value="")
        function_label = ttk.Label(function_frame, textvariable=self.function_var, justify="left")
        function_label.grid(row=0, column=0, sticky="w")
        
        # Update function text based on initial selection
        self.update_function_text()
        
        # Instructions
        instructions_frame = ttk.LabelFrame(control_frame, text="Instructions", padding=10)
        instructions_frame.grid(row=4, column=0, pady=(20, 0), sticky="ew")
        
        instructions_text = """• Enter a whole number of petals (1-20)
• Hold Ctrl + Mouse Scroll to zoom in/out
• Right-click and drag to pan the view
• Use toolbar buttons for additional controls
• Double-click on the plot to reset the view
• Try different formula types for various patterns"""
        
        instructions_label = ttk.Label(instructions_frame, text=instructions_text, justify="left")
        instructions_label.grid(row=0, column=0, sticky="w")
        
        # Reset Button
        reset_button = ttk.Button(control_frame, text="Reset View", command=self.reset_view)
        reset_button.grid(row=5, column=0, pady=(20, 0), sticky="ew")

    def create_plot_panel(self):
        # Create frame for the plot
        plot_frame = ttk.Frame(self.root)
        plot_frame.grid(row=0, column=1, sticky="nsew")
        plot_frame.columnconfigure(0, weight=1)
        plot_frame.rowconfigure(0, weight=1)
        plot_frame.rowconfigure(1, weight=0)
        
        # Create matplotlib figure and canvas
        self.fig = Figure(figsize=(10, 8), dpi=100)
        self.ax = self.fig.add_subplot(111)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        
        # Add toolbar
        toolbar_frame = ttk.Frame(plot_frame)
        toolbar_frame.grid(row=1, column=0, sticky="ew")
        toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
        toolbar.update()
        
        # Connect scroll event for zooming
        self.canvas.mpl_connect('scroll_event', self.on_scroll)
        
        # Connect double-click event for resetting view
        self.canvas.mpl_connect('button_press_event', self.on_button_press)

    def update_function_text(self):
        if self.formula_type.get() == "spiral":
            self.function_var.set("""Spiral Petal Formula:
r = θ × sin(n × θ)

Where:
• r is the radius
• θ is the angle
• n is the coefficient

Properties:
• Odd n: creates n petals
• Even n: creates 2n petals
• Spirals outward as θ increases""")
            
        elif self.formula_type.get() == "rose":
            self.function_var.set("""Classic Rose Formula:
r = cos(n × θ)

Where:
• r is the radius
• θ is the angle
• n is the coefficient

Properties:
• Odd n: creates n petals
• Even n: creates 2n petals
• Fixed radius (bounded pattern)""")
            
        elif self.formula_type.get() == "rhodonea":
            self.function_var.set("""Rhodonea Formula (Exact Petals):
r = cos(k × θ)

Where:
• r is the radius
• θ is the angle
• k = n/2 for even n, k = n for odd n

Properties:
• Always creates exactly n petals
• Fixed radius (bounded pattern)""")
            
        elif self.formula_type.get() == "spiral_rhodonea":
            self.function_var.set("""Spiral Rhodonea Formula:
r = θ × cos(k × θ)

Where:
• r is the radius
• θ is the angle
• k = n/2 for even n, k = n for odd n

Properties:
• Always creates exactly n petals
• Spirals outward as θ increases""")

    def update_plot(self):
        # Clear the previous plot
        self.ax.clear()
        
        # Update function text
        self.update_function_text()
        
        # Calculate the curve based on formula type
        theta = np.linspace(0, self.max_theta, self.n_points)
        
        formula_type = self.formula_type.get()
        
        if formula_type == "spiral":
            # Original spiral formula (no correction)
            r = theta * np.sin(self.n_petals * theta)
            title = f"Spiral Petal Pattern"
            note = f"{self.n_petals} petals" if self.n_petals % 2 == 1 else f"{2*self.n_petals} petals"
            
        elif formula_type == "rose":
            # Classic rose curve (no correction)
            r = np.cos(self.n_petals * theta)
            title = f"Classic Rose Pattern"
            note = f"{self.n_petals} petals" if self.n_petals % 2 == 1 else f"{2*self.n_petals} petals"
            
        elif formula_type == "rhodonea":
            # Rhodonea curve with exact petal count correction
            k = self.n_petals if self.n_petals % 2 == 1 else self.n_petals / 2
            r = np.cos(k * theta)
            title = f"Rhodonea Pattern"
            note = f"Exactly {self.n_petals} petals"
            
        elif formula_type == "spiral_rhodonea":
            # Spiral rhodonea with exact petal count correction
            k = self.n_petals if self.n_petals % 2 == 1 else self.n_petals / 2
            r = theta * np.cos(k * theta)
            title = f"Spiral Rhodonea Pattern"
            note = f"Exactly {self.n_petals} petals"
        
        # Convert to Cartesian coordinates
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        
        # Plot the curve
        self.ax.plot(x, y, color='darkviolet', linewidth=1.5)
        
        # Set up the axis
        self.ax.set_title(f"{title}\n({note})", fontsize=14)
        self.ax.set_aspect('equal')
        self.ax.grid(True, linestyle='--', alpha=0.7)
        
        # Get good limits based on the data
        if formula_type in ["spiral", "spiral_rhodonea"]:
            # Expanding patterns
            max_range = max(abs(np.max(x)), abs(np.min(x)), abs(np.max(y)), abs(np.min(y)))
            self.ax.set_xlim(-max_range*1.1, max_range*1.1)
            self.ax.set_ylim(-max_range*1.1, max_range*1.1)
        else:
            # Fixed radius patterns
            self.ax.set_xlim(-1.5, 1.5)
            self.ax.set_ylim(-1.5, 1.5)
        
        # Update the figure
        self.fig.tight_layout()
        self.canvas.draw()

    def on_apply(self):
        try:
            # Validate input - must be an integer between 1 and 20
            value = int(self.petals_var.get())
            if value < 1 or value > 20:
                messagebox.showerror("Invalid Input", "Please enter a whole number between 1 and 20.")
                return
                
            self.n_petals = value
            self.update_plot()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid whole number.")

    def on_scroll(self, event):
        # Zoom with Ctrl+Scroll centered on mouse position
        if event.key == 'control':
            # Get the current x and y limits
            cur_xlim = self.ax.get_xlim()
            cur_ylim = self.ax.get_ylim()
            
            # Get event location
            xdata = event.xdata
            ydata = event.ydata
            if xdata is None or ydata is None:
                return
                
            # Get the directions
            if event.button == 'up':
                scale_factor = 0.9  # Zoom in
            else:
                scale_factor = 1.1  # Zoom out
                
            # Calculate new limits
            new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
            new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor
            
            # Set new limits centered on mouse position
            self.ax.set_xlim([xdata - new_width * (xdata - cur_xlim[0]) / (cur_xlim[1] - cur_xlim[0]),
                             xdata + new_width * (cur_xlim[1] - xdata) / (cur_xlim[1] - cur_xlim[0])])
            self.ax.set_ylim([ydata - new_height * (ydata - cur_ylim[0]) / (cur_ylim[1] - cur_ylim[0]),
                             ydata + new_height * (cur_ylim[1] - ydata) / (cur_ylim[1] - cur_ylim[0])])
            
            self.canvas.draw()

    def on_button_press(self, event):
        # Double-click to reset view
        if event.dblclick:
            self.reset_view()

    def reset_view(self):
        self.update_plot()  # This resets the view by recalculating appropriate limits

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