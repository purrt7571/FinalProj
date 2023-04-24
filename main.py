import numpy as np
import tkinter as tk
import tkinter.ttk as ttk
from hdpitkinter import HdpiTk
from matplotlib.figure import Figure
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.quiver import Quiver
from tkinter.messagebox import showerror

        
class BaseWindow(tk.Toplevel):
    """
    Base window for each case with a control panel, table, resultant, and graphing plane.
    """
    def __init__(self, master: tk.Tk, minwidth: int = 1500, minheight: int = 900) -> None:

        super().__init__(master=master)
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
        self.coordinate: tk.IntVar = tk.IntVar(self, value=0)
        self.vector_dict: dict[str, np.ndarray] = {}
        self.quiver_dict: dict[str, Quiver] = {}

        self.resultant_vct: np.ndarray = np.array([0,0])
        self.resultant_xvar: tk.StringVar = tk.StringVar(self, "0.0000")
        self.resultant_yvar: tk.StringVar = tk.StringVar(self, "0.0000")
        self.resultant_rvar: tk.StringVar = tk.StringVar(self, "0.0000")
        self.resultant_thetavar: tk.StringVar = tk.StringVar(self, "0.0000")

        self.control_panel = tk.Frame(self)
        self.control_panel.grid(column=0, row=0, rowspan=2, sticky="nsew")
        self.control_panel.grid_columnconfigure(0, weight=1)
        
        self.vector_frame = ttk.Labelframe(self.control_panel, text="Vector")
        self.vector_frame.grid(column=0, row=0, sticky="new", padx=10, pady=10)
        self.vector_frame.grid_columnconfigure(0,weight=1)
        self.vector_frame.grid_columnconfigure(1,weight=3)
        self.vector_frame.grid_columnconfigure(2,weight=1)
        self.vector_frame.grid_columnconfigure(3,weight=3)

        ttk.Label(self.vector_frame, text="Vector name: ").grid(column=0, row=0, sticky="nw", padx=10)
        ttk.Label(self.vector_frame, text="X / R : ").grid(column=0, row=1, sticky="ew", padx=10)
        ttk.Label(self.vector_frame, text="Y / \u03B8 : ").grid(column=2, row=1, sticky="ew", padx=10)

        self.name_entry = ttk.Entry(self.vector_frame, textvariable=self.name_var)
        self.name_entry.grid(column=1, row=0, columnspan=3, sticky="new", padx=10)
        self.req1_entry = ttk.Entry(self.vector_frame, textvariable=self.req1_var)
        self.req1_entry.grid(column=1, row=1, sticky="ew", padx=10, pady=10)
        self.req2_entry = ttk.Entry(self.vector_frame, textvariable=self.req2_var)
        self.req2_entry.grid(column=3, row=1, sticky="ew", padx=10, pady=10)

        ttk.Radiobutton(self.vector_frame, text="X and Y components", variable=self.coordinate, value=0).grid(column=0, row=2, columnspan=2, sticky="ew", padx=10, pady=10)
        ttk.Radiobutton(self.vector_frame, text="Magnitude and Direction", variable=self.coordinate, value=1).grid(column=2, row=2, columnspan=2, sticky="ew", padx=10, pady=10)
        ttk.Button(self.vector_frame, text="Add Vector", command=self.add_vector).grid(column=0, row=3, columnspan=4, sticky="ew", pady=(5,10), padx=10)

        self.tree = ttk.Treeview(master=self, columns=("name", "x", "y", "rm", "rtheta"), show="headings")
        self.tree.grid(column=1, row=0, sticky="nsew")
        self.tree.column("name", width=50)
        self.tree.column("x", width=70)
        self.tree.column("y", width=70)
        self.tree.column("rm", width=70)
        self.tree.column("rtheta", width=70)
        self.tree.heading("name", text="Name")
        self.tree.heading("x", text="X")
        self.tree.heading("y", text="Y")
        self.tree.heading("rm", text="R")
        self.tree.heading("rtheta", text="\u03B8")

        self.resultant_canvas = tk.Frame(self)
        self.resultant_canvas.grid(column=1, row=1, sticky="nsew", padx=10)
        self.resultant_canvas.grid_columnconfigure(0, weight=1)
        self.resultant_canvas.grid_columnconfigure(1, weight=3)
        self.resultant_canvas.grid_columnconfigure(2, weight=1)
        self.resultant_canvas.grid_columnconfigure(3, weight=3)
        self.resultant_canvas.grid_columnconfigure(4, weight=1)
        self.resultant_canvas.grid_columnconfigure(5, weight=3)
        self.resultant_canvas.grid_columnconfigure(6, weight=1)
        self.resultant_canvas.grid_columnconfigure(7, weight=3)
        self.resultant_canvas.grid_rowconfigure(0, weight=0)

        ttk.Label(self.resultant_canvas, text="X=").grid(column=0, row=0, sticky="nsw", pady=10)
        ttk.Label(self.resultant_canvas, text="Y=").grid(column=2, row=0, sticky="nsw", pady=10)
        ttk.Label(self.resultant_canvas, text="R=").grid(column=4, row=0, sticky="nsw", pady=10)
        ttk.Label(self.resultant_canvas, text="\u03B8=").grid(column=6, row=0, sticky="nsw", pady=10)
        ttk.Label(self.resultant_canvas, textvariable=self.resultant_xvar).grid(column=1, row=0, sticky="nsw", pady=10)
        ttk.Label(self.resultant_canvas, textvariable=self.resultant_yvar).grid(column=3, row=0, sticky="nsw", pady=10)
        ttk.Label(self.resultant_canvas, textvariable=self.resultant_rvar).grid(column=5, row=0, sticky="nsw", pady=10)
        ttk.Label(self.resultant_canvas, textvariable=self.resultant_thetavar).grid(column=7, row=0, sticky="nsw", pady=10)

        self.fig = Figure()
        self.plot = self.fig.subplots()
        self.plot.set_aspect("equal")
        self.plot.set_box_aspect(1.25)
        self.plot.grid()
        self.canvas = FigureCanvasTkAgg(figure=self.fig, master=self)
        self.canvas.get_tk_widget().grid(column=2, row=0, sticky="nsew")
        self.toolbar = NavigationToolbar2Tk(self.canvas, self, pack_toolbar=False)
        self.toolbar.grid(column=2, row=1, sticky="sew")

        self.resultant_plot: Quiver = self.plot.quiver(0, 0, color="black", scale=1, scale_units="xy", angles="xy")
        
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.rescale_graph()
        return
    
    def add_vector(self) -> None:
        """
        Add a vector to the table with a unique name and plot the vector into the plane.
        """
        vector_name = self.name_var.get()

        if vector_name == "":

            showerror("Error", "Vector name is empty!")
            self.name_entry.focus_set()
            return
        
        elif vector_name in self.quiver_dict:

            showerror("Error", f"Vector \"{vector_name}\" already exists!")
            self.name_entry.focus_set()
            return
        
        elif self.coordinate.get():

            try:
                r = float(self.req1_var.get())
            except ValueError:
                showerror("Error", "Value must be a valid decimal number!")
                self.req1_entry.focus_set()
                return
            
            try:
                theta = float(self.req2_var.get())
            except ValueError:
                showerror("Error", "Value must be a valid decimal number!")
                self.req2_entry.focus_set()
                return
            
            x = r * np.cos(np.radians(theta))
            y = r * np.sin(np.radians(theta))

        else:

            try:
                x = float(self.req1_var.get())
            except ValueError as e:
                showerror("Error", "Value must be a valid decimal number!")
                self.req1_entry.focus_set()
                return
            
            try:
                y = float(self.req2_var.get())
            except ValueError as e:
                showerror("Error", "Value must be a valid decimal number!")
                self.req2_entry.focus_set()
                return

            r = np.hypot(x,y)
            theta = np.rad2deg(np.arctan2(y, x))
        
        self.vector_dict[vector_name] = np.array([x, y])
        self.quiver_dict[vector_name] = self.plot.quiver(x, y, alpha=0.5, color="g", scale=1, scale_units="xy", angles="xy") # Need to change
        self.tree.insert("", "end", vector_name, values=(vector_name, "%.6f" % x, "%.6f" % y, "%.6f" % r, "%.6f" % theta))

        self.get_resultant()
        self.rescale_graph()
        return
    
    def get_resultant(self) -> None:

        self.resultant_vct = sum(self.vector_dict.values()) # type: ignore
        self.resultant_xvar.set(value="%.4f" % self.resultant_vct[0]) # type: ignore
        self.resultant_yvar.set(value="%.4f" % self.resultant_vct[1]) # type: ignore
        self.resultant_rvar.set(value="%.4f" % np.hypot(*self.resultant_vct))
        self.resultant_thetavar.set(value="%.4f" % np.rad2deg(np.arctan2(self.resultant_vct[1], self.resultant_vct[0]))) # type: ignore
        self.resultant_plot.remove()
        self.resultant_plot = self.plot.quiver(*self.resultant_vct, color="black", scale=1, scale_units="xy", angles="xy") # type: ignore
        return
    
    def rescale_graph(self) -> None:

        x = [i[0] for i in self.vector_dict.values()] + [self.resultant_vct[0]]
        y = [i[1] for i in self.vector_dict.values()] + [self.resultant_vct[1]]   

        x_min, x_max = np.floor(min(*x, 0)) - 1, np.ceil(max(*x, 0)) + 1
        y_min, y_max = np.floor(min(*y, 0)) - 1, np.ceil(max(*y, 0)) + 1
        x_mid = (x_min + x_max) / 2
        y_mid = (y_min + y_max) / 2
        x_range = x_max - x_min
        y_range = y_max - y_min

        if 1.25 * x_range > y_range:
            self.plot.set_xlim(x_mid - x_range / 2, x_mid + x_range / 2)
            self.plot.set_ylim(y_mid - x_range / 2 * 1.25, y_mid + x_range / 2 * 1.25)
        else:
            self.plot.set_xlim(x_mid - y_range / 2 / 1.25, x_mid + y_range / 2 / 1.25)
            self.plot.set_ylim(y_mid - y_range / 2, y_mid + y_range / 2)

        self.canvas.draw()
        return
        
    
    def close(self) -> None:

        self.canvas.callbacks.process('close_event')
        self.master.focus_set()
        self.destroy()
        return
    
class OneMissingVector(BaseWindow):

    def __init__(self, master: tk.Tk, minwidth: int=1500, minheight: int=900) -> None:

        super().__init__(master, minwidth, minheight)

        self.missing_vector_frame = ttk.LabelFrame(master=self.control_panel, text="Missing Vector")
        self.missing_vector_frame.grid(column=0, row=2, sticky="new", padx=10, pady=10)
        self.missing_vector_frame.grid_columnconfigure(0,weight=1)
        self.missing_vector_frame.grid_columnconfigure(1,weight=3)
        self.missing_vector_frame.grid_columnconfigure(2,weight=1)
        self.missing_vector_frame.grid_columnconfigure(3,weight=3)

        self.missing_name_var: tk.StringVar = tk.StringVar(self)
        self.missing_req1_var: tk.StringVar = tk.StringVar(self)
        self.missing_req2_var: tk.StringVar = tk.StringVar(self)
        self.missing_coordinate: tk.IntVar = tk.IntVar(self, value=0)

        ttk.Label(self.missing_vector_frame, text="Vector name: ").grid(column=0, row=0, sticky="nw", padx=10)
        ttk.Label(self.missing_vector_frame, text="X / R : ").grid(column=0, row=1, sticky="ew", padx=10)
        ttk.Label(self.missing_vector_frame, text="Y / \u03B8 : ").grid(column=2, row=1, sticky="ew", padx=10)

        self.missing_name_entry = ttk.Entry(self.missing_vector_frame, textvariable=self.missing_name_var)
        self.missing_name_entry.grid(column=1, row=0, columnspan=3, sticky="new", padx=10)
        self.missing_req1_entry = ttk.Entry(self.missing_vector_frame, textvariable=self.missing_req1_var)
        self.missing_req1_entry.grid(column=1, row=1, sticky="ew", padx=10, pady=10)
        self.missing_req2_entry = ttk.Entry(self.missing_vector_frame, textvariable=self.missing_req2_var)
        self.missing_req2_entry.grid(column=3, row=1, sticky="ew", padx=10, pady=10)

        ttk.Radiobutton(self.missing_vector_frame, text="X and Y components", variable=self.missing_coordinate, value=0).grid(column=0, row=2, columnspan=2, sticky="ew", padx=10, pady=10)
        ttk.Radiobutton(self.missing_vector_frame, text="Magnitude and Direction", variable=self.missing_coordinate, value=1).grid(column=2, row=2, columnspan=2, sticky="ew", padx=10, pady=10)
        ttk.Button(self.missing_vector_frame, text="Add Vector", command=self.find_one_missing_vector).grid(column=0, row=3, columnspan=4, sticky="ew", pady=(5,10), padx=10)

        return
    
    def find_one_missing_vector(self) -> None:

        vector_name = self.missing_name_var.get()
        sum_vectors = sum(self.vector_dict.values()) if len(self.vector_dict) else np.array([0, 0])

        if vector_name == "":

            showerror("Error", "Vector name is empty!")
            self.missing_name_entry.focus_set()
            return
        
        elif vector_name in self.quiver_dict:

            showerror("Error", f"Vector \"{vector_name}\" already exists!")
            self.missing_name_entry.focus_set()
            return
        
        elif self.missing_coordinate.get():

            try:
                r = float(self.missing_req1_var.get())
            except ValueError:
                showerror("Error", "Value must be a valid decimal number!")
                self.missing_req1_entry.focus_set()
                return
            
            try:
                theta = float(self.missing_req2_var.get())
            except ValueError:
                showerror("Error", "Value must be a valid decimal number!")
                self.missing_req2_entry.focus_set()
                return
            
            x = r * np.cos(np.radians(theta)) - sum_vectors[0] # type: ignore
            y = r * np.sin(np.radians(theta)) - sum_vectors[1] # type: ignore
            r = np.hypot(x, y)
            theta = np.rad2deg(np.arctan2(y, x))

        else:

            try:
                x = float(self.missing_req1_var.get()) - sum_vectors[0] # type: ignore
            except ValueError as e:
                showerror("Error", "Value must be a valid decimal number!")
                self.missing_req1_entry.focus_set()
                return
            
            try:
                y = float(self.missing_req2_var.get()) - sum_vectors[1] # type: ignore
            except ValueError as e:
                showerror("Error", "Value must be a valid decimal number!")
                self.missing_req2_entry.focus_set()
                return

            r = np.hypot(x,y)
            theta = np.rad2deg(np.arctan2(y, x))
        
        self.vector_dict[vector_name] = np.array([x, y])
        self.quiver_dict[vector_name] = self.plot.quiver(x, y, alpha=0.5, color="r", scale=1, scale_units="xy", angles="xy") # Need to change
        self.tree.insert("", "end", vector_name, values=(vector_name, "%.6f" % x, "%.6f" % y, "%.6f" % r, "%.6f" % theta))

        self.get_resultant()
        self.rescale_graph()
        return


root = HdpiTk()
root.title("VectorSim")
root.minsize(300, 100)
root.grid_columnconfigure(0, weight=1)

ttk.Button(root, text="Case 1", command=lambda: OneMissingVector(root)).grid(column=0, row=0, sticky="nsew", padx=10, pady=(10, 0))
ttk.Button(root, text="Case 2").grid(column=0, row=1, sticky="nsew", padx=10)
ttk.Button(root, text="Case 3").grid(column=0, row=2, sticky="nsew", padx=10)

root.mainloop()