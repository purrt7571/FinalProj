import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Close matplotlib figure then close program
def on_close() -> None:
    plt.close(fig)
    root.destroy()
    return


# Initialize dict[np.array] for vectors
vct: dict[np.array] = {}

# Tk main window
root = tk.Tk()
root.title("Vector Addition")

# Frame/Container for Graph
canvas_frame = tk.Frame(root, background="green")
canvas_frame.pack(side="right", fill="both", expand=True)

# Setup Graph elements
fig = plt.figure()
plot = fig.add_subplot()
canvas = FigureCanvasTkAgg(figure=fig, master=canvas_frame)
canvas.get_tk_widget().pack(side='top', fill='both', expand=True)
toolbar = NavigationToolbar2Tk(canvas = canvas, window = canvas_frame, pack_toolbar = False)
toolbar.pack(side='bottom', fill='x')

# Set closing sequence
root.protocol("WM_DELETE_WINDOW", on_close)

# Run GUI
root.mainloop()
