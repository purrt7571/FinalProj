import numpy as np
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Tk main window
root = tk.Tk()
root.title("Vector Addition")

# Setup Graph elements
fig = Figure()
canvas = FigureCanvasTkAgg(fig, root)
toolbar = NavigationToolbar2Tk(canvas, root)
