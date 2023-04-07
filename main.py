import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Tk main window
root = tk.Tk()
root.title("Vector Addition")

# Frame/Container for Graph
frame = tk.Frame(root, background="green")
frame.pack(side="right", fill="both")

# Setup Graph elements
fig = plt.figure()
subplt = fig.add_axes((0.1,0.1,0.8,0.8))
canvas = FigureCanvasTkAgg(figure=fig, master=frame)
canvas.get_tk_widget().pack(side='top', fill='both')
toolbar = NavigationToolbar2Tk(canvas = canvas, window = frame, pack_toolbar = False)
toolbar.pack(side='bottom', fill='x')

# Run GUI
root.mainloop()
