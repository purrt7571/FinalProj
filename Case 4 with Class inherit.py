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

        # Variables for the Given Vectors
        self.name_var: tk.StringVar = tk.StringVar(self)
        self.req1_var: tk.StringVar = tk.StringVar(self)
        self.req2_var: tk.StringVar = tk.StringVar(self)
        self.coordinate: tk.IntVar = tk.IntVar(self, value=0)
        self.vector_dict: dict[str, np.ndarray] = {}
        self.quiver_dict: dict[str, Quiver] = {}

        # Variables for the Resultant Vector        
        self.resultant_vct: np.ndarray = np.array([0,0])
        self.resultant_xvar: tk.StringVar = tk.StringVar(self, "0.0000")
        self.resultant_yvar: tk.StringVar = tk.StringVar(self, "0.0000")
        self.resultant_rvar: tk.StringVar = tk.StringVar(self, "0.0000")
        self.resultant_thetavar: tk.StringVar = tk.StringVar(self, "0.0000")

        # Control Panel
        self.control_panel = tk.Frame(self)
        self.control_panel.grid(column=0, row=0, rowspan=2, sticky="nsew")
        self.control_panel.grid_columnconfigure(0, weight=1)
        
        # Given Vector Widget
        self.vector_frame = ttk.Labelframe(self.control_panel, text="Given Vector (Given)")
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

class Case_1(BaseWindow):
    def __init__(self, master: tk.Tk, minwidth: int = 1500, minheight: int = 900) -> None:
        super().__init__(master, minwidth, minheight)
        ttk.Button(self.vector_frame, text="Add Vector", command=self.add_vector).grid(column=0, row=3, columnspan=4, sticky="ew", pady=(5,10), padx=10)


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

        self.name_entry.delete(0, "end")
        self.req1_entry.delete(0, "end")
        self.req2_entry.delete(0, "end")

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
    
class Case_2(BaseWindow):

    def __init__(self, master: tk.Tk, minwidth: int=1500, minheight: int=900) -> None:

        super().__init__(master, minwidth, minheight)
        self.sum_given_vct: np.ndarray = []

        # Variables for the Resultant Vector                                #Inadd
        self.resultant_name_var: tk.StringVar = tk.StringVar(self)          #Inadd
        self.resultant_req1_var: tk.StringVar = tk.StringVar(self)          #Inadd
        self.resultant_req2_var: tk.StringVar = tk.StringVar(self)          #Inadd
        self.resultant_coordinate: tk.IntVar = tk.IntVar(self, value = 0)   #Inadd

        # Variables for the Missing Vector                                  
        self.missing_xvar: tk.StringVar = tk.StringVar(self, "0.0000")      #Inadd
        self.missing_yvar: tk.StringVar = tk.StringVar(self, "0.0000")      #Inadd
        self.missing_vct_var: tk.StringVar = tk.StringVar(self, "0.0000")   #Inadd
        self.missing_thetavar: tk.StringVar = tk.StringVar(self, "0.0000")  #Inadd
        self.missing_vct: np.ndarray = []                                   #Inadd
        self.missing_vct_plot: Quiver = self.plot.quiver(0, 0, color="black", scale=1, scale_units="xy", angles="xy")

        # Given Vector Widget
        self.vector_frame.grid_rowconfigure(0, weight=0)              #Inadd & Rename
        self.vector_frame.grid_rowconfigure(1, weight=0)              #Inadd & Rename
        self.vector_frame.grid_rowconfigure(2, weight=0)              #Inadd & Rename
        self.vector_frame.grid_rowconfigure(3, weight=0)              #Inadd & Rename
        self.vector_frame.grid_rowconfigure(4, weight=0)              #Inadd & Rename
        self.vector_frame.grid_rowconfigure(5, weight=0)              #Inadd & Rename

        ttk.Button(self.vector_frame, text="Add Vector", command=self.add_given_vector).grid(column=0, row=3, columnspan=4, sticky="ew", pady=(10,5), padx=10)
        ttk.Button(self.vector_frame, text = "Remove Selected Vectors", command = self.remove_selected_given).grid(column = 0, row = 4, columnspan=4, sticky="ew", padx=10, pady = 5)
        ttk.Button(self.vector_frame, text = "Remove All Vectors", command = self.remove_all_given).grid(column = 0, row = 5, columnspan=4, sticky="ew", padx=10, pady = 5)

        # Resultant Vector Widget
        self.resultant_vector_frame = ttk.Labelframe(self.control_panel, text = "Resultant Vector (Black)")
        self.resultant_vector_frame.grid(column = 0, row = 1, sticky = "new", padx = 10, pady = 10)
        self.resultant_vector_frame.grid_columnconfigure(0,weight=1)
        self.resultant_vector_frame.grid_columnconfigure(1,weight=3)
        self.resultant_vector_frame.grid_columnconfigure(2,weight=1)
        self.resultant_vector_frame.grid_columnconfigure(3,weight=3)
        self.resultant_vector_frame.grid_rowconfigure(0, weight=0)
        self.resultant_vector_frame.grid_rowconfigure(1, weight=0)
        self.resultant_vector_frame.grid_rowconfigure(2, weight=0)
        self.resultant_vector_frame.grid_rowconfigure(3, weight=0)

        ttk.Label(self.resultant_vector_frame, text = "Vector name: ").grid(column = 0, row = 0, sticky = "nw", padx = 10)
        ttk.Label(self.resultant_vector_frame, text="X / R : ").grid(column=0, row=1, sticky="ew", padx=10)
        ttk.Label(self.resultant_vector_frame, text="Y / \u03B8 : ").grid(column=2, row=1, sticky="ew", padx=10)

        self.resultant_name_entry = ttk.Entry(self.resultant_vector_frame, textvariable = self.resultant_name_var)
        self.resultant_name_entry.grid(column = 1, row = 0, columnspan = 3, sticky = "new", padx = 10)
        self.resultant_req1_entry = ttk.Entry(self.resultant_vector_frame, textvariable = self.resultant_req1_var)
        self.resultant_req1_entry.grid(column = 1, row = 1, sticky = "ew", padx = 10, pady = 10)
        self.resultant_req2_entry = ttk.Entry(self.resultant_vector_frame, textvariable = self.resultant_req2_var)
        self.resultant_req2_entry.grid(column = 3, row = 1, sticky = "ew", padx = 10, pady = 10)

        ttk.Radiobutton(self.resultant_vector_frame, text = "X and Y components", variable = self.resultant_coordinate, value = 0).grid(column = 0, row = 2, columnspan = 2, sticky = "ew", padx = 10, pady = 10)
        ttk.Radiobutton(self.resultant_vector_frame, text = "Magnitude and Direction", variable = self.resultant_coordinate, value = 1).grid(column = 2, row = 2, columnspan = 2, sticky = "ew", padx = 10, pady = 10)
        ttk.Button(self.resultant_vector_frame, text = "Add Vector", command=self.add_resultant_vector).grid(column=0, row=3, columnspan=4, sticky="ew", pady=(5,10), padx=10)

        # Missing Vector Widget
        self.missing_vector_frame = ttk.Labelframe(self.control_panel, text = "Missing Vector (Red)")
        self.missing_vector_frame.grid(column = 0, row = 2, sticky = "new", padx = 10, pady = 10)
        self.missing_vector_frame.grid_columnconfigure(0,weight=1)
        self.missing_vector_frame.grid_columnconfigure(1,weight=3)
        self.missing_vector_frame.grid_columnconfigure(2,weight=1)
        self.missing_vector_frame.grid_columnconfigure(3,weight=3)
        self.missing_vector_frame.grid_rowconfigure(0, weight=0)
        self.missing_vector_frame.grid_rowconfigure(1, weight=0)
        self.missing_vector_frame.grid_rowconfigure(2, weight=0)
        self.missing_vector_frame.grid_rowconfigure(3, weight=0)

        ttk.Label(self.missing_vector_frame, text = "X-Component = ").grid(column = 0, row = 0, sticky = "nw", padx = 10)
        ttk.Label(self.missing_vector_frame, textvariable = self.missing_xvar).grid(column = 1, row = 0, sticky = "nw", padx = 10)
        ttk.Label(self.missing_vector_frame, text = "Y-Component = ").grid(column = 0, row = 1, sticky = "nw", padx = 10)
        ttk.Label(self.missing_vector_frame, textvariable = self.missing_yvar).grid(column = 1, row = 1, sticky = "nw", padx = 10)
        ttk.Label(self.missing_vector_frame, text = "Magnitude = ").grid(column = 2, row = 0, sticky = "nw", padx = 10)
        ttk.Label(self.missing_vector_frame, textvariable = self.missing_vct_var).grid(column = 3, row = 0, sticky = "nw", padx = 10)
        ttk.Label(self.missing_vector_frame, text = "Direction (\u03B8) = ").grid(column = 2, row = 1, sticky = "nw", padx = 10)
        ttk.Label(self.missing_vector_frame, textvariable = self.missing_thetavar).grid(column = 3, row = 1, sticky = "nw", padx = 10)

    def add_given_vector(self) -> None:
        """
        Add a given vector to the table with a unique name and plot the vector into the plane.
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
        self.sum_given_vct = sum(self.vector_dict.values()) if len(self.vector_dict) else np.array([0,0])
        self.quiver_dict[vector_name] = self.plot.quiver(x, y, alpha = 0.5, color = "g", scale = 1, scale_units = "xy", angles = "xy") # Need to change
        self.tree.insert("", "end", vector_name, values = (vector_name, "%.6f" % x, "%.6f" % y, "%.6f" % r, "%.6f" % theta))

        self.name_entry.delete(0, "end")
        self.req1_entry.delete(0, "end")
        self.req2_entry.delete(0, "end")

        self.get_missing_vct()
        self.rescale_graph()
        return

    def remove_selected_given(self) -> None:
        selected_vector = self.tree.selection()
        for select in selected_vector:
            self.vector_dict.pop(select)
            self.quiver_dict[select].remove()
            self.quiver_dict.pop(select)
            self.tree.delete(select)

        if self.vector_dict:
            pass
        else:
            self.reset()

        self.get_missing_vct()
        self.rescale_graph()
        return

    def remove_all_given(self) -> None:
        selected_vector = self.tree.get_children()
        for select in selected_vector:
            self.vector_dict.pop(select)
            self.quiver_dict[select].remove()
            self.quiver_dict.pop(select)
            self.tree.delete(select)

        self.reset()
        self.rescale_graph()
        return
     
    def reset(self) -> None:
        if self.resultant_plot != {}:
            self.resultant_plot.remove()
            self.missing_vct_plot.remove()
        else:
            pass
        self.sum_given_vct, self.resultant_vct, self.missing_vct = [], [], []
        self.vector_dict, self.quiver_dict, self.resultant_plot, self.missing_vct_plot = {}, {}, {}, {}

        self.resultant_name_entry = ttk.Entry(self.resultant_vector_frame, textvariable = self.resultant_name_var)
        self.resultant_name_entry.grid(column = 1, row = 0, columnspan = 3, sticky = "new", padx = 10)
        self.resultant_req1_entry = ttk.Entry(self.resultant_vector_frame, textvariable = self.resultant_req1_var)
        self.resultant_req1_entry.grid(column = 1, row = 1, sticky = "ew", padx = 10, pady = 10)
        self.resultant_req2_entry = ttk.Entry(self.resultant_vector_frame, textvariable = self.resultant_req2_var)
        self.resultant_req2_entry.grid(column = 3, row = 1, sticky = "ew", padx = 10, pady = 10)
        ttk.Button(self.resultant_vector_frame, text = "Add Vector", command = self.add_resultant_vector).grid(column=0, row=3, columnspan=4, sticky="ew", pady=(5,10), padx=10)

        self.name_entry.delete(0, "end")
        self.req1_entry.delete(0, "end")
        self.req2_entry.delete(0, "end")
        self.resultant_name_entry.delete(0, "end")
        self.resultant_req1_entry.delete(0, "end")
        self.resultant_req2_entry.delete(0, "end")

        self.resultant_xvar.set(value = "0.0000")
        self.resultant_yvar.set(value = "0.0000")
        self.resultant_rvar.set(value = "0.0000")
        self.resultant_thetavar.set(value = "0.0000")
        self.missing_xvar.set(value = "0.0000")
        self.missing_yvar.set(value = "0.0000")
        self.missing_vct_var.set(value = "0.0000")
        self.missing_thetavar.set(value = "0.0000")

        return

    def add_resultant_vector(self) -> None:
        """
        Add a resultant vector to the table with a unique name and plot the vector into the plane.
        """
        resultant_vector_name = self.resultant_name_var.get()

        if resultant_vector_name == "":

            showerror("Error", "Vector name is empty!")
            self.resultant_name_entry.focus_set()
            return
        
        elif self.resultant_coordinate.get():

            try:
                r = float(self.resultant_req1_var.get())
            except ValueError:
                showerror("Error", "Value must be a valid decimal number!")
                self.resultant_req1_entry.focus_set()
                return
            
            try:
                theta = float(self.resultant_req2_var.get())
            except ValueError:
                showerror("Error", "Value must be a valid decimal number!")
                self.resultant_req2_entry.focus_set()
                return
            
            x = r * np.cos(np.radians(theta))
            y = r * np.sin(np.radians(theta))

        else:

            try:
                x = float(self.resultant_req1_var.get())
            except ValueError as e:
                showerror("Error", "Value must be a valid decimal number!")
                self.resultant_req1_entry.focus_set()
                return
            
            try:
                y = float(self.resultant_req2_var.get())
            except ValueError as e:
                showerror("Error", "Value must be a valid decimal number!")
                self.resultant_req2_entry.focus_set()
                return

            r = np.hypot(x,y)
            theta = np.rad2deg(np.arctan2(y, x))
        
        self.resultant_vct = np.array([x,y])
        self.resultant_xvar.set(value = "%.4f" % self.resultant_vct[0]) # type: ignore
        self.resultant_yvar.set(value = "%.4f" % self.resultant_vct[1]) # type: ignore
        self.resultant_rvar.set(value = "%.4f" % np.hypot(self.resultant_vct[0], self.resultant_vct[1]))
        self.resultant_thetavar.set(value = "%.4f" % np.rad2deg(np.arctan2(self.resultant_vct[1], self.resultant_vct[0])))
        self.check_existing_resultantplot()

        self.resultant_name_entry = ttk.Label(self.resultant_vector_frame, textvariable = self.resultant_name_var)
        self.resultant_name_entry.grid(column = 1, row = 0, columnspan = 3, sticky = "new", padx = 10)
        self.resultant_req1_entry = ttk.Label(self.resultant_vector_frame, textvariable = self.resultant_req1_var)
        self.resultant_req1_entry.grid(column = 1, row = 1, sticky = "ew", padx = 10, pady = 10)
        self.resultant_req2_entry = ttk.Label(self.resultant_vector_frame, textvariable = self.resultant_req2_var)
        self.resultant_req2_entry.grid(column = 3, row = 1, sticky = "ew", padx = 10, pady = 10)
        ttk.Button(self.resultant_vector_frame, text = "Edit Vector", command = self.edit_resultant_vector).grid(column=0, row=3, columnspan=4, sticky="ew", pady=(5,10), padx=10)

        self.get_missing_vct()
        self.rescale_graph()

        return
        
    def edit_resultant_vector(self) -> None:
            self.resultant_name_entry = ttk.Entry(self.resultant_vector_frame, textvariable = self.resultant_name_var)
            self.resultant_name_entry.grid(column = 1, row = 0, columnspan = 3, sticky = "new", padx = 10)
            self.resultant_req1_entry = ttk.Entry(self.resultant_vector_frame, textvariable = self.resultant_req1_var)
            self.resultant_req1_entry.grid(column = 1, row = 1, sticky = "ew", padx = 10, pady = 10)
            self.resultant_req2_entry = ttk.Entry(self.resultant_vector_frame, textvariable = self.resultant_req2_var)
            self.resultant_req2_entry.grid(column = 3, row = 1, sticky = "ew", padx = 10, pady = 10)
            ttk.Button(self.resultant_vector_frame, text = "Save", command = self.add_resultant_vector).grid(column=0, row=3, columnspan=4, sticky="ew", pady=(5,10), padx=10)

            self.check_existing_resultantplot()
            self.get_missing_vct()
            self.rescale_graph()

    def get_missing_vct(self) -> None:
        if np.any(self.resultant_vct) == True:
            if len(self.vector_dict) != 0:
                missing_x = self.resultant_vct[0] - self.sum_given_vct[0]
                missing_y = self.resultant_vct[1] - self.sum_given_vct[1]
                self.missing_xvar.set(value = "%.4f" % missing_x) # type: ignore
                self.missing_yvar.set(value = "%.4f" % missing_y) # type: ignore
                self.missing_vct_var.set(value = "%.4f" % np.hypot(missing_x, missing_y))
                self.missing_thetavar.set(value = "%.4f" % np.rad2deg(np.arctan2(missing_y, missing_x)))
                self.missing_vct = np.array([missing_x,missing_y])
                
                self.check_existing_missing_vctplot()
        else:
            return

    def check_existing_resultantplot(self) -> None:
        if self.resultant_plot != {}:
            self.resultant_plot.remove()
            self.resultant_plot = self.plot.quiver(*self.resultant_vct, color = "black", scale = 1, scale_units = "xy", angles = "xy") # type: ignore
        else:
            self.resultant_plot = self.plot.quiver(*self.resultant_vct, color = "black", scale = 1, scale_units = "xy", angles = "xy") # type: ignore
        return

    def check_existing_missing_vctplot(self) -> None:
        if self.missing_vct_plot != {}:
            self.missing_vct_plot.remove()
            self.missing_vct_plot = self.plot.quiver(*self.missing_vct, color = "r", scale = 1, scale_units = "xy", angles = "xy") # type: ignore
        else:
            self.missing_vct_plot = self.plot.quiver(*self.missing_vct, color = "r", scale = 1, scale_units = "xy", angles = "xy") # type: ignore
        return

    def rescale_graph(self) -> None:

        if np.any(self.resultant_vct) == False and self.vector_dict == {}:
            self.vector_dict = {"null": np.array([0,0])}
            x = [i[0] for i in self.vector_dict.values()]
            y = [i[1] for i in self.vector_dict.values()] 

        elif np.any(self.resultant_vct) == False and self.vector_dict != {}:
            x = [i[0] for i in self.vector_dict.values()] + [self.sum_given_vct[0]] 
            y = [i[1] for i in self.vector_dict.values()] + [self.sum_given_vct[1]]

        else:
            if self.vector_dict:
                x = [i[0] for i in self.vector_dict.values()] + [self.sum_given_vct[0]] + [self.resultant_vct[0]] + [self.missing_vct[0]]
                y = [i[1] for i in self.vector_dict.values()] + [self.sum_given_vct[1]] + [self.resultant_vct[1]] + [self.missing_vct[1]] 

            else:
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


root = HdpiTk()
root.title("VectorSim")
root.minsize(300, 100)
root.grid_columnconfigure(0, weight=1)

ttk.Button(root, text="Case 1", command=lambda: Case_1(root)).grid(column=0, row=0, sticky="nsew", padx=10, pady=(10, 0))
ttk.Button(root, text="Case 2", command=lambda: Case_2(root)).grid(column=0, row=1, sticky="nsew", padx=10)
ttk.Button(root, text="Case 3").grid(column=0, row=2, sticky="nsew", padx=10)

root.mainloop()