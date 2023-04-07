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
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=0)
root.grid_columnconfigure(2, weight=1)
root.grid_rowconfigure(0, weight=1)

# Frame/Container for buttons/labels/textboxes/checkboxes
control_frame = tk.Frame(root, background="red")
control_frame.grid(column=0, row=0, sticky='nsew')

# Display vector values
tree = ttk.Treeview(root, columns=("c1", "c2", "c3"), show="headings")
tree.grid(column=1, row=0, sticky="nsw")
tree.column("# 1", width=70)
tree.column("# 2", width=100)
tree.column("# 3", width=100)
tree.heading("# 1", text="Name")
tree.heading("# 2", text="X")
tree.heading("# 3", text="Y")

# Frame/Container for Graph
canvas_frame = tk.Frame(root, background="blue")
canvas_frame.grid(column=2, row=0, sticky="nsew")
canvas_frame.grid_rowconfigure(0, weight=1)
canvas_frame.grid_rowconfigure(1, weight=0)
canvas_frame.grid_columnconfigure(0, weight=1)

# Setup Graph elements
fig = plt.figure()
plot = fig.add_subplot()
canvas = FigureCanvasTkAgg(figure=fig, master=canvas_frame)
canvas.get_tk_widget().grid(column=0, row=0, sticky='nsew')
toolbar = NavigationToolbar2Tk(canvas = canvas, window = canvas_frame, pack_toolbar = False)
toolbar.grid(column=0, row=1, sticky='sew')

# Set closing sequence
root.protocol("WM_DELETE_WINDOW", on_close)

# Run GUI
root.mainloop()
