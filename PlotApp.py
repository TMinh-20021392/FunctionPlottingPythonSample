from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from tkinter import ttk
import tkinter as tk


class PlotApp:
    """Base class for curve plotting applications"""
    def __init__(self, root, title="Curve Plotter"):
        self.root = root
        self.root.title(title)
        self.root.state('zoomed')  # Make window full-screen on Windows

        # Configure the main window layout
        self.root.columnconfigure(0, weight=1)  # Control panel
        self.root.columnconfigure(1, weight=4)  # Plot area
        self.root.rowconfigure(0, weight=1)

        # Create the plot figure
        self.fig = Figure(figsize=(10, 8), dpi=100)
        self.ax = self.fig.add_subplot(111)

        # Create the UI components
        self.create_scrollable_control_panel()
        self.create_plot_panel()

        # Initialize the plot
        self.update_plot()

    def create_scrollable_control_panel(self):
        """Create the left side scrollable control panel"""
        # Create the main control frame that will contain the canvas and scrollbar
        self.main_control_frame = ttk.Frame(self.root)
        self.main_control_frame.grid(row=0, column=0, sticky="nsew")
        self.main_control_frame.columnconfigure(0, weight=1)
        self.main_control_frame.rowconfigure(0, weight=1)
        
        # Create a canvas with scrollbar
        self.control_canvas = tk.Canvas(self.main_control_frame)
        self.control_canvas.grid(row=0, column=0, sticky="nsew")
        
        # Add scrollbar
        self.scrollbar = ttk.Scrollbar(self.main_control_frame, orient="vertical", command=self.control_canvas.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.control_canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Create frame for controls inside the canvas
        self.control_frame = ttk.Frame(self.control_canvas, padding="10")
        self.control_frame.columnconfigure(0, weight=1)
        
        # Create a window in the canvas to hold the control frame
        self.canvas_window = self.control_canvas.create_window((0, 0), window=self.control_frame, anchor="nw", width=self.control_canvas.winfo_reqwidth())
        
        # Configure the canvas to resize with the window and update scrollregion
        self.control_canvas.bind('<Configure>', self._configure_canvas)
        self.control_frame.bind('<Configure>', self._update_scrollregion)
        
        # Bind mousewheel for scrolling - improve to work on all elements
        self._bind_mousewheel_recursive(self.main_control_frame)
        
        # Now derived classes can add their controls to self.control_frame
        self.create_control_panel()
    
    def create_control_panel(self):
        """Create the controls inside the scrollable panel - to be implemented by derived classes"""
        pass

    def _configure_canvas(self, event):
        # Update the width of the canvas window when the canvas is resized
        if self.control_canvas.winfo_width() > 1:  # Check if width is valid
            self.control_canvas.itemconfig(self.canvas_window, width=self.control_canvas.winfo_width())
    
    def _update_scrollregion(self, event):
        # Update the scrollregion to encompass the inner frame
        self.control_canvas.configure(scrollregion=self.control_canvas.bbox("all"))
    
    def _bind_mousewheel_recursive(self, widget):
        """Recursively bind mousewheel events to all widgets in the control panel"""
        # Bind to this widget
        self._bind_mousewheel_to_widget(widget)
        
        # Recursively bind to all children
        for child in widget.winfo_children():
            self._bind_mousewheel_recursive(child)
    
    def _bind_mousewheel_to_widget(self, widget):
        """Bind mousewheel events to a specific widget"""
        widget.bind("<MouseWheel>", self._on_mousewheel)  # Windows and MacOS
        widget.bind("<Button-4>", self._on_mousewheel)    # Linux
        widget.bind("<Button-5>", self._on_mousewheel)    # Linux
    
    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        # Different delta calculation for different platforms
        if event.num == 5 or event.delta < 0:
            self.control_canvas.yview_scroll(1, "units")
        elif event.num == 4 or event.delta > 0:
            self.control_canvas.yview_scroll(-1, "units")

    def create_plot_panel(self):
        """Create the right side plot panel"""
        # Create frame for the plot
        plot_frame = ttk.Frame(self.root)
        plot_frame.grid(row=0, column=1, sticky="nsew")
        plot_frame.columnconfigure(0, weight=1)
        plot_frame.rowconfigure(0, weight=1)
        plot_frame.rowconfigure(1, weight=0)

        # Create matplotlib figure and canvas
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
        """Update the plot with current parameters"""
        # This should be implemented by derived classes
        pass

    def on_scroll(self, event):
        """Handle scroll events for zooming"""
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
        """Handle mouse button events"""
        if event.dblclick:
            self.reset_view()

    def reset_view(self):
        """Reset the view to default"""
        # Reset the view by updating the plot
        self.update_plot()
        
        # Reset the ax view limits to show the whole plot
        self.ax.relim()  # Recalculate limits
        self.ax.autoscale_view(True, True, True)  # Auto-scale the view
        self.canvas.draw()  # Redraw the canvas