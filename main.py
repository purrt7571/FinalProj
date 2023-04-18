import numpy as np
import tkinter as tk
import tkinter.ttk as ttk
from hdpitkinter import HdpiTk
from matplotlib.figure import Figure
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter.messagebox import showerror
from typing import Any

class BaseWindow(tk.Toplevel):
    """
    Base window for each case with a control panel, table, resultant, and graphing plane.
    """
    def __init__(self, master: tk.Tk, minwidth: int = 1500, minheight: int = 900) -> None:

        super().__init__(master = master)
        self.title("VectorSim")
        self.minsize(minwidth, minheight)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=3)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)

        self.name_var: tk.StringVar = tk.StringVar(self)
        self.req1_var: tk.StringVar = tk.StringVar(self)
        self.req2_var: tk.StringVar = tk.StringVar(self)
        self.coordinate: tk.IntVar = tk.IntVar(self, value = 0)
        self.vector_dict: dict[str, np.ndarray] = {}
        self.quiver_dict: dict[str, Any] = {}

        self.resultant_vct: np.ndarray = np.array([0,0])
        self.resultant_xvar: tk.StringVar = tk.StringVar(self, "0.0000")
        self.resultant_yvar: tk.StringVar = tk.StringVar(self, "0.0000")
        self.resultant_rvar: tk.StringVar = tk.StringVar(self, "0.0000")
        self.resultant_thetavar: tk.StringVar = tk.StringVar(self, "0.0000")
        self.resultant_plot: None = None

        self.control_panel = tk.Frame(self)
        self.control_panel.grid(column = 0, row = 0, rowspan = 2, sticky = "nsew")
        self.control_panel.grid_columnconfigure(0, weight = 1)
        
        self.vector_frame = ttk.Labelframe(self.control_panel, text = "Vector")
        self.vector_frame.grid(column = 0, row = 0, sticky = "new", padx = 10, pady = 10)
        self.vector_frame.grid_columnconfigure(0,weight=1)
        self.vector_frame.grid_columnconfigure(1,weight=3)
        self.vector_frame.grid_columnconfigure(2,weight=1)
        self.vector_frame.grid_columnconfigure(3,weight=3)
        self.vector_frame.grid_rowconfigure(0, weight=0)
        self.vector_frame.grid_rowconfigure(1, weight=0)
        self.vector_frame.grid_rowconfigure(2, weight=0)
        self.vector_frame.grid_rowconfigure(3, weight=0)

        ttk.Label(self.vector_frame, text = "Vector name: ").grid(column = 0, row = 0, sticky = "nw", padx = 10)
        ttk.Label(self.vector_frame, text="X / R : ").grid(column=0, row=1, sticky="ew", padx=10)
        ttk.Label(self.vector_frame, text="Y / \u03B8 : ").grid(column=2, row=1, sticky="ew", padx=10)
        ttk.Entry(self.vector_frame, textvariable = self.name_var).grid(column = 1, row = 0, columnspan = 3, sticky = "new", padx = 10)
        ttk.Entry(self.vector_frame, textvariable = self.req1_var).grid(column = 1, row = 1, sticky = "ew", padx = 10, pady = 10)
        ttk.Entry(self.vector_frame, textvariable = self.req2_var).grid(column = 3, row = 1, sticky = "ew", padx = 10, pady = 10)
        ttk.Radiobutton(self.vector_frame, text = "X and Y components", variable = self.coordinate, value = 0).grid(column = 0, row = 2, columnspan = 2, sticky = "ew", padx = 10, pady = 10)
        ttk.Radiobutton(self.vector_frame, text = "Magnitude and Direction", variable = self.coordinate, value = 1).grid(column = 2, row = 2, columnspan = 2, sticky = "ew", padx = 10, pady = 10)
        ttk.Button(self.vector_frame, text = "Add Vector", command = self.add_vector).grid(column=0, row=3, columnspan=4, sticky="ew", pady=(5,10), padx=10)

        self.tree = ttk.Treeview(master = self, columns = ("name", "x", "y", "rm", "rtheta"), show = "headings")
        self.tree.grid(column = 1, row = 0, sticky = "nsew")
        self.tree.column("name", width = 50)
        self.tree.column("x", width = 70)
        self.tree.column("y", width = 70)
        self.tree.column("rm", width = 70)
        self.tree.column("rtheta", width = 70)
        self.tree.heading("name", text = "Name")
        self.tree.heading("x", text = "X")
        self.tree.heading("y", text = "Y")
        self.tree.heading("rm", text = "R")
        self.tree.heading("rtheta", text = "\u03B8")

        self.resultant_canvas = tk.Frame(self)
        self.resultant_canvas.grid(column = 1, row = 1, sticky = "nsew", padx = 10)
        self.resultant_canvas.grid_columnconfigure(0, weight = 1)
        self.resultant_canvas.grid_columnconfigure(1, weight = 3)
        self.resultant_canvas.grid_columnconfigure(2, weight = 1)
        self.resultant_canvas.grid_columnconfigure(3, weight = 3)
        self.resultant_canvas.grid_columnconfigure(4, weight = 1)
        self.resultant_canvas.grid_columnconfigure(5, weight = 3)
        self.resultant_canvas.grid_columnconfigure(6, weight = 1)
        self.resultant_canvas.grid_columnconfigure(7, weight = 3)
        self.resultant_canvas.grid_rowconfigure(0, weight = 0)

        ttk.Label(self.resultant_canvas, text = "X = ").grid(column = 0, row = 0, sticky = "nsw", pady = 10)
        ttk.Label(self.resultant_canvas, text = "Y = ").grid(column = 2, row = 0, sticky = "nsw", pady = 10)
        ttk.Label(self.resultant_canvas, text = "R = ").grid(column = 4, row = 0, sticky = "nsw", pady = 10)
        ttk.Label(self.resultant_canvas, text = "\u03B8 = ").grid(column = 6, row = 0, sticky = "nsw", pady = 10)
        ttk.Label(self.resultant_canvas, textvariable = self.resultant_xvar).grid(column = 1, row = 0, sticky = "nsw", pady = 10)
        ttk.Label(self.resultant_canvas, textvariable = self.resultant_yvar).grid(column = 3, row = 0, sticky = "nsw", pady = 10)
        ttk.Label(self.resultant_canvas, textvariable = self.resultant_rvar).grid(column = 5, row = 0, sticky = "nsw", pady = 10)
        ttk.Label(self.resultant_canvas, textvariable = self.resultant_thetavar).grid(column = 7, row = 0, sticky = "nsw", pady = 10)

        self.fig = Figure(figsize = (4, 5))
        self.plot = self.fig.subplots()
        self.plot.grid()
        self.canvas = FigureCanvasTkAgg(figure = self.fig, master = self)
        self.canvas.get_tk_widget().grid(column = 2, row = 0, sticky = "nsew")
        self.toolbar = NavigationToolbar2Tk(self.canvas, self, pack_toolbar = False)
        self.toolbar.grid(column = 2, row = 1, sticky = "sew")
        
        self.protocol("WM_DELETE_WINDOW", self.close)
        return
    
    def add_vector(self) -> None:
        """
        Add a vector to the table with a unique name and plot the vector into the plane.
        """
        vector_name = self.name_var.get()

        if vector_name == "":
            showerror("Error", "Vector name is empty!")
            return
        elif vector_name in self.quiver_dict:
            showerror("Error", f"Vector \"{vector_name}\" already exists!")
            return
        elif self.coordinate.get():
            r = float(self.req1_var.get())
            theta = float(self.req2_var.get())
            x = r * np.cos(np.radians(theta))
            y = r * np.sin(np.radians(theta))
        else:
            x = float(self.req1_var.get())
            y = float(self.req2_var.get())
            r = np.hypot(x,y)
            theta = np.rad2deg(np.arctan2(y, x))
        
        self.vector_dict[vector_name] = np.array([x, y])
        self.quiver_dict[vector_name] = self.plot.quiver(x, y, alpha = 0.2, color = "g") # Need to change
        self.tree.insert("", "end", vector_name, values = (vector_name, "%.6f" % x, "%.6f" % y, "%.6f" % r, "%.6f" % theta))

        self.canvas.draw()
        return
    
    def close(self) -> None:

        self.canvas.close_event()
        self.destroy()
        return


root = HdpiTk()
root.title("VectorSim")
root.minsize(300, 100)
root.grid_columnconfigure(0, weight = 1)

ttk.Button(root, text = "Case 1", command = lambda: BaseWindow(root)).grid(column = 0, row = 0, sticky = "nsew", padx = 10, pady = (10, 0))
ttk.Button(root, text = "Case 2").grid(column = 0, row = 1, sticky = "nsew", padx = 10)
ttk.Button(root, text = "Case 3").grid(column = 0, row = 2, sticky = "nsew", padx = 10)

root.mainloop()