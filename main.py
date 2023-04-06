import numpy as np
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Tk main window
root = tk.Tk()
root.title("Vector Addition")
frame = tk.Frame(root)
frame.grid(row=0,column=1)

# Setup Graph elements
fig = Figure()
subplt = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(figure = fig, master = frame)
canvas.get_tk_widget().grid(row=0, column=0)
toolbar = NavigationToolbar2Tk(canvas = canvas, window = frame, pack_toolbar = False)
toolbar.grid(row=1,column=0)


# Run GUI
root.mainloop()
