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
        
        # Function description
        function_frame = ttk.LabelFrame(control_frame, text="Function Information", padding=10)
        function_frame.grid(row=2, column=0, pady=(20, 0), sticky="ew")
        
        function_text = """Polar equation:
r = θ × sin(n × θ)

Where:
• r is the radius
• θ is the angle
• n is the number of petals

As θ increases, the pattern expands outward,
creating a spiraling petal effect."""
        
        function_label = ttk.Label(function_frame, text=function_text, justify="left")
        function_label.grid(row=0, column=0, sticky="w")
        
        # Instructions
        instructions_frame = ttk.LabelFrame(control_frame, text="Instructions", padding=10)
        instructions_frame.grid(row=3, column=0, pady=(20, 0), sticky="ew")
        
        instructions_text = """• Enter a whole number of petals (1-20)
• Hold Ctrl + Mouse Scroll to zoom in/out
• Right-click and drag to pan the view
• Use toolbar buttons for additional controls
• Double-click on the plot to reset the view"""
        
        instructions_label = ttk.Label(instructions_frame, text=instructions_text, justify="left")
        instructions_label.grid(row=0, column=0, sticky="w")
        
        # Reset Button
        reset_button = ttk.Button(control_frame, text="Reset View", command=self.reset_view)
        reset_button.grid(row=4, column=0, pady=(20, 0), sticky="ew")

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

    def update_plot(self):
        # Clear the previous plot
        self.ax.clear()
        
        # Calculate the curve
        theta = np.linspace(0, self.max_theta, self.n_points)
        r = theta * np.sin(self.n_petals * theta)
        
        # Convert to Cartesian coordinates
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        
        # Plot the curve
        self.ax.plot(x, y, color='darkviolet', linewidth=1.5)
        
        # Set up the axis
        self.ax.set_title(f"Flower Petal Pattern (n={self.n_petals})", fontsize=14)
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