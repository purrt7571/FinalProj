import numpy as np
import tkinter as tk
import tkinter.ttk as ttk
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
root.minsize(1500, 900)

# Frame/Container for buttons/labels/textboxes/checkboxes
control_frame = tk.Frame(root)
control_frame.pack(side='left', fill='y', expand=True)

# TreeView for Vector Values
tree = ttk.Treeview(root, columns=("c1", "c2", "c3"), show="headings")
tree.pack(side='left', fill='both', expand=True)
tree.column("# 1", width=50)
tree.column("# 2", width=50)
tree.column("# 3", width=50)
tree.heading("# 1", text="Name")
tree.heading("# 2", text="X")
tree.heading("# 3", text="Y")


# Frame/Container for Graph
canvas_frame = tk.Frame(root)
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
