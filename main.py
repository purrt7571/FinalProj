import numpy as np
import tkinter as tk
import tkinter.ttk as ttk
import matplotlib.pyplot as plt
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter.messagebox import showerror

# Close matplotlib figure then close program
def on_close() -> None:
    plt.close(fig)
    root.destroy()
    return

def rescale_graph() -> None:
    global plot, canvas
    x = [i[0] for i in vct.values()] + [resultant[0]]
    y = [i[1] for i in vct.values()] + [resultant[1]]
    x_min, x_max = np.floor(min(*x, 0)) - 1, np.ceil(max(*x, 0)) + 1
    y_min, y_max = np.floor(min(*y, 0)) - 1, np.ceil(max(*y, 0)) + 1
    plot.set_xlim(x_min, x_max)
    plot.set_ylim(y_min, y_max)
    canvas.draw()
    return

def get_resultant() -> None:
    global resultant, resultant_x, resultant_y, resultant_Rm, result_Rtheta
    resultant = sum(vct.values())
    resultant_x.set(value="%.4f" % resultant[0])
    resultant_y.set(value="%.4f" % resultant[1])
    resultant_Rm_solve = np.round(np.hypot(resultant[0],resultant[1]), 6)
    resultant_Rtheta_solve = np.round(np.rad2deg(np.arctan2(resultant[1],resultant[0])), 6)
    resultant_Rm.set(value="%.4f" % resultant_Rm_solve)
    resultant_Rtheta.set(value="%.4f" % resultant_Rtheta_solve)
    return

def add_vector() -> None:
    global plot, vct_plt
    vector_name = vector_name_txtbox.get()
    if vector_name == "":
        showerror("Error", "Vector name is empty!")
        return
    elif vector_name in vct_plt:
        showerror("Error", f"Vector \"{vector_name}\" already exists!")
        return
    elif coordinate_choice.get():
        r = float(requirement1_txtbox.get())
        theta = float(requirement2_txtbox.get())
        x = r * np.cos(np.radians(theta))
        y = r * np.sin(np.radians(theta))
    else:
        x = float(requirement1_txtbox.get())
        y = float(requirement2_txtbox.get())
        r = np.hypot(x,y)
        theta = np.rad2deg(np.arctan2(y, x))
    vct[vector_name] = np.array([x,y])
    vct_plt[vector_name] = plot.quiver(0, 0, x, y, alpha=0.2, color='g', scale=1, scale_units='xy', angles='xy')
    tree.insert("", "end", vector_name, values=(vector_name, "%.6f" % x, "%.6f" % y, "%.6f" % r, "%.6f" % theta))
    get_resultant()
    rescale_graph()
    null_vectorname.set(value="")
    null_requirement1.set(value="")
    null_requirement2.set(value="")
    return


# Tk main window
root = tk.Tk()
root.title("Vector Addition")
root.minsize(1500, 900)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=0)
root.grid_columnconfigure(2, weight=3)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=0)

# Initialize dict[np.array] for vectors and resultant for sum
vct: dict[np.array] = {}
vct_plt: dict[plt.arrow] = {}
resultant = np.array([0,0])
resultant_x = tk.StringVar(value="0.0000")
resultant_y = tk.StringVar(value="0.0000")
resultant_Rm = tk.StringVar(value="0.0000")
resultant_Rtheta = tk.StringVar(value="0.0000")
null_vectorname = tk.StringVar(value="")
null_requirement1= tk.StringVar(value="")
null_requirement2= tk.StringVar(value="")

# Frame/Container for buttons/labels/textboxes/checkboxes
control_frame = ttk.Frame(root)
control_frame.grid(column=0, row=0, rowspan=2, sticky='nsew')
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

vector_name_label = ttk.Label(add_vector_frame, text="Vector name: ")
vector_name_label.grid(column=0, row=0, sticky="nw", padx=10)
vector_name_txtbox = ttk.Entry(add_vector_frame, textvariable=null_vectorname)
vector_name_txtbox.grid(column=1, row=0, columnspan=3, sticky="new", padx=10)

requirement1_label = ttk.Label(add_vector_frame, text="X / R : ")
requirement2_label = ttk.Label(add_vector_frame, text="Y / \u03B8 : ")
requirement1_label.grid(column=0, row=1, sticky="ew", padx=10)
requirement2_label.grid(column=2, row=1, sticky="ew", padx=10)
requirement1_txtbox = ttk.Entry(add_vector_frame, textvariable=null_requirement1)
requirement2_txtbox = ttk.Entry(add_vector_frame, textvariable=null_requirement2)
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
resultant_canvas = tk.Frame(root, background="white")
resultant_canvas.grid(column=1, row=1, sticky="nsew")
resultant_canvas.grid_columnconfigure(0,weight=1)
resultant_canvas.grid_columnconfigure(1,weight=3)
resultant_canvas.grid_columnconfigure(2,weight=1)
resultant_canvas.grid_columnconfigure(3,weight=3)
resultant_canvas.grid_rowconfigure(0, weight=0)
resultant_canvas.grid_rowconfigure(1, weight=0)

tree = ttk.Treeview(root, columns=("c1", "c2", "c3", "c4", "c5"), show="headings")
tree.grid(column=1, row=0, sticky="nsew")
tree.column("# 1", width=70)
tree.column("# 2", width=100, anchor="e")
tree.column("# 3", width=100, anchor="e")
tree.column("# 4", width=100, anchor="e")
tree.column("# 5", width=100, anchor="e")
tree.heading("# 1", text="Name")
tree.heading("# 2", text="X")
tree.heading("# 3", text="Y")
tree.heading("# 4", text="R")
tree.heading("# 5", text="\u03B8")

result_x_label = ttk.Label(resultant_canvas, text="X = ", background="white")
result_y_label = ttk.Label(resultant_canvas, text="Y = ", background="white")
result_Rm_label = ttk.Label(resultant_canvas, text="Rm = ", background="white")
result_Rtheta_label = ttk.Label(resultant_canvas, text="\u03B8 = ", background="white")
result_x_label.grid(column=0, row=0, sticky="nsw", padx=(10,0), pady=10)
result_y_label.grid(column=2, row=0, sticky="nsw", pady=10)
result_Rm_label.grid(column=0, row=1, sticky="nsw", padx=(10,0), pady=10)
result_Rtheta_label.grid(column=2, row=1, sticky="nsw", pady=10)

result_x = ttk.Label(resultant_canvas, textvariable=resultant_x, background="white")
result_y = ttk.Label(resultant_canvas, textvariable=resultant_y, background="white")
result_Rm = ttk.Label(resultant_canvas, textvariable=resultant_Rm, background="white")
result_Rtheta = ttk.Label(resultant_canvas, textvariable=resultant_Rtheta, background="white")
result_x.grid(column=1, row=0, sticky="nsw", pady=10)
result_y.grid(column=3, row=0, sticky="nsw", padx=(0,10), pady=10)
result_Rm.grid(column=1, row=1, sticky="nsw", pady=10)
result_Rtheta.grid(column=3, row=1, sticky="nsw", padx=(0,10), pady=10)

# Setup Graph elements
fig = plt.figure()
plot = plt.subplot()
plot.grid()
fig.add_subplot(plot)
canvas = FigureCanvasTkAgg(figure=fig, master=root)
canvas.get_tk_widget().grid(column=2, row=0, sticky='nsew')
toolbar = NavigationToolbar2Tk(canvas=canvas, window=root, pack_toolbar=False)
toolbar.grid(column=2, row=1, sticky='sew')

# Set closing sequence
root.protocol("WM_DELETE_WINDOW", on_close)

# Run GUI
root.mainloop()