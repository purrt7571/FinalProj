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

def add_vector():
    pass


# Initialize dict[np.array] for vectors and resultant for sum
vct: dict[np.array] = {}
resultant: np.array = np.array([0,0])

# Tk main window
root = tk.Tk()
root.title("Vector Addition")
root.minsize(1500, 900)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=0)
root.grid_columnconfigure(2, weight=3)
root.grid_rowconfigure(0, weight=1)

# Frame/Container for buttons/labels/textboxes/checkboxes
control_frame = tk.Frame(root)
control_frame.grid(column=0, row=0, sticky='nsew')
control_frame.grid_columnconfigure(0, weight=1)
control_frame.grid_columnconfigure(1, weight=0)
control_frame.grid_rowconfigure(0, weight=0)
control_frame.grid_rowconfigure(1, weight=0)

# Setup frame for adding vectors to plot
add_vector_frame = ttk.Labelframe(control_frame, text="Vector")
add_vector_frame.grid(column=0, row=0, sticky="new", padx=10, pady=10)
add_vector_frame.grid_columnconfigure(0,weight=1)
add_vector_frame.grid_columnconfigure(1,weight=3)
add_vector_frame.grid_columnconfigure(2,weight=1)
add_vector_frame.grid_columnconfigure(3,weight=3)
add_vector_frame.grid_rowconfigure(0, weight=0)
add_vector_frame.grid_rowconfigure(1, weight=0)
add_vector_frame.grid_rowconfigure(2, weight=0)
add_vector_frame.grid_rowconfigure(3, weight=0)

name_label = ttk.Label(add_vector_frame, text="Vector name: ")
name_label.grid(column=0, row=0, sticky="nw", padx=10)
name_txtbox = ttk.Entry(add_vector_frame)
name_txtbox.grid(column=1, row=0, columnspan=3, sticky="new", padx=10)

requirement1_label = ttk.Label(add_vector_frame, text="X / R : ")
requirement2_label = ttk.Label(add_vector_frame, text="Y / \u03B8 : ")
requirement1_label.grid(column=0, row=1, sticky="ew", padx=10)
requirement2_label.grid(column=2, row=1, sticky="ew", padx=10)
requirement1_txtbox = ttk.Entry(add_vector_frame)
requirement2_txtbox = ttk.Entry(add_vector_frame)
requirement1_txtbox.grid(column=1, row=1, sticky="ew", padx=10, pady=10)
requirement2_txtbox.grid(column=3, row=1, sticky="ew", padx=10, pady=10)

coordinate_choice = tk.IntVar(value=0)

cartesian_radio = ttk.Radiobutton(add_vector_frame, text="Cartesian", variable=coordinate_choice, value=0)
cartesian_radio.grid(column=0, row=2, columnspan=2, sticky="ew", padx=10, pady=10)
polar_radio = ttk.Radiobutton(add_vector_frame, text="Polar", variable=coordinate_choice, value=1)
polar_radio.grid(column=2, row=2, columnspan=2, sticky="ew", padx=10, pady=10)

add_vector_button = ttk.Button(add_vector_frame, text="Add Vector", command=add_vector)
add_vector_button.grid(column=0, row=3, columnspan=4, sticky="ew", pady=(5,10), padx=10)

scroll = tk.Scrollbar(control_frame, orient="vertical")
scroll.grid(column=1, row=0, rowspan=1, sticky="nse")

# Display vector values
tree = ttk.Treeview(root, columns=("c1", "c2", "c3"), show="headings")
tree.grid(column=1, row=0, sticky="nsw")
tree.column("# 1", width=70)
tree.column("# 2", width=100, anchor="e")
tree.column("# 3", width=100, anchor="e")
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
