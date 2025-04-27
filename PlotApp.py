from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure


from tkinter import ttk


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
        self.create_control_panel()
        self.create_plot_panel()

        # Initialize the plot
        self.update_plot()

    def create_control_panel(self):
        """Create the left side control panel"""
        # This should be implemented by derived classes
        pass

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
        self.update_plot()