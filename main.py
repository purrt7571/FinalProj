"""
VectorSim - Python Program for simulating vectors and computing for unknown variables
"""
import numpy as np
import tkinter as tk
from tkinter import ttk
from hdpitkinter import HdpiTk
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk  # type: ignore
from matplotlib.quiver import Quiver
from tkinter.messagebox import showerror
import warnings

warnings.simplefilter("error", category=RuntimeWarning)
class BaseWindow(tk.Toplevel):

    """
    Base window for each case with a control panel, table, resultant, and graphing plane.
    """

    def __init__(self, master: tk.Tk, min_width: int = 900, min_height: int = 700) -> None:

        super().__init__(master=master)
        self.title("VectorSim")
        self.minsize(min_width, min_height)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=3)
        self.grid_rowconfigure(0, weight=1)

        self.vector_str_vars: dict[str, tk.StringVar] = {
            "name": tk.StringVar(self),
            "req1": tk.StringVar(self),
            "req2": tk.StringVar(self)
        }
        self.coordinate: tk.IntVar = tk.IntVar(self, value=0)
        self.vector_dict: dict[str, np.ndarray] = {}
        self.quiver_dict: dict[str, Quiver] = {}
        self.resultant_vct: np.ndarray = np.array([0, 0])
        self.resultant_str_vars: dict[str, tk.StringVar] = {
            "x": tk.StringVar(self, "0.0000"),
            "y": tk.StringVar(self, "0.0000"),
            "r": tk.StringVar(self, "0.0000"),
            "theta": tk.StringVar(self, "0.0000")
        }

        self.control_panel = tk.Frame(self)
        self.control_panel.grid(column=0, row=0, rowspan=2, sticky="nsew")
        self.control_panel.grid_columnconfigure(0, weight=1)

        self.vector_frame = ttk.Labelframe(self.control_panel, text="Given Vector (Green)")
        self.vector_frame.grid(column=0, row=0, sticky="new", padx=10, pady=10)
        self.vector_frame.grid_columnconfigure(0, weight=1)
        self.vector_frame.grid_columnconfigure(1, weight=3)
        self.vector_frame.grid_columnconfigure(2, weight=1)
        self.vector_frame.grid_columnconfigure(3, weight=3)

        ttk.Label(self.vector_frame, text="Vector name: ").grid(column=0, row=0, sticky="nw", padx=10)
        ttk.Label(self.vector_frame, text="X / R : ").grid(column=0, row=1, sticky="ew", padx=10)
        ttk.Label(self.vector_frame, text="Y / \u03B8 : ").grid(column=2, row=1, sticky="ew", padx=10)

        self.name_entry = ttk.Entry(self.vector_frame, textvariable=self.vector_str_vars["name"])
        self.name_entry.grid(column=1, row=0, columnspan=3, sticky="new", padx=10)
        self.req1_entry = ttk.Entry(self.vector_frame, textvariable=self.vector_str_vars["req1"])
        self.req1_entry.grid(column=1, row=1, sticky="ew", padx=10, pady=10)
        self.req2_entry = ttk.Entry(self.vector_frame, textvariable=self.vector_str_vars["req2"])
        self.req2_entry.grid(column=3, row=1, sticky="ew", padx=10, pady=10)

        ttk.Radiobutton(self.vector_frame, text="X and Y components", variable=self.coordinate, value=0).grid(column=0, row=2, columnspan=2, sticky="ew", padx=10, pady=10)
        ttk.Radiobutton(self.vector_frame, text="Magnitude and Direction", variable=self.coordinate, value=1).grid(column=2, row=2, columnspan=2, sticky="ew", padx=10, pady=10)
        self.add_vector_button = ttk.Button(self.vector_frame, text="Add vector")
        self.add_vector_button.grid(column=0, row=3, columnspan=4, sticky="ew", padx=10, pady=5)
        self.remove_vector_button = ttk.Button(self.vector_frame, text="Remove vector")
        self.remove_vector_button.grid(column=0, row=4, columnspan=4, sticky="ew", padx=10, pady=5)
        self.clear_all_button = ttk.Button(self.vector_frame, text="Clear all vectors")
        self.clear_all_button.grid(column=0, row=5, columnspan=4, sticky="ew", padx=10, pady=(5, 10))

        self.tree = ttk.Treeview(master=self, columns=("name", "x", "y", "rm", "r_theta"), show="tree headings")
        self.tree.grid(column=1, row=0, sticky="nsew")
        self.tree.column("#0", width=70, anchor="w")
        self.tree.column("name", width=50, anchor="w")
        self.tree.column("x", width=70, anchor="e")
        self.tree.column("y", width=70, anchor="e")
        self.tree.column("rm", width=70, anchor="e")
        self.tree.column("r_theta", width=70, anchor="e")
        self.tree.heading("name", text="Name")
        self.tree.heading("x", text="X")
        self.tree.heading("y", text="Y")
        self.tree.heading("rm", text="R")
        self.tree.heading("r_theta", text="\u03B8")

        self.tree_entries = {
            "given": self.tree.insert("", "end", text="Given"),
            "missing": self.tree.insert("", "end", text="Missing")
            }

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

        ttk.Label(self.resultant_canvas, text="X=").grid(column=0, row=0, sticky="nsw", pady=10)
        ttk.Label(self.resultant_canvas, text="Y=").grid(column=2, row=0, sticky="nsw", pady=10)
        ttk.Label(self.resultant_canvas, text="R=").grid(column=4, row=0, sticky="nsw", pady=10)
        ttk.Label(self.resultant_canvas, text="\u03B8=").grid(column=6, row=0, sticky="nsw", pady=10)
        ttk.Label(self.resultant_canvas, textvariable=self.resultant_str_vars["x"]).grid(column=1, row=0, sticky="nsw", pady=10)
        ttk.Label(self.resultant_canvas, textvariable=self.resultant_str_vars["y"]).grid(column=3, row=0, sticky="nsw", pady=10)
        ttk.Label(self.resultant_canvas, textvariable=self.resultant_str_vars["r"]).grid(column=5, row=0, sticky="nsw", pady=10)
        ttk.Label(self.resultant_canvas, textvariable=self.resultant_str_vars["theta"]).grid(column=7, row=0, sticky="nsw", pady=10)

        self.fig = Figure()
        self.plot: Axes = self.fig.subplots()
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

    def remove_vector(self) -> None:
        """
        Remove the selected vector from the list.
        """
        selected = self.tree.selection()

        if len(selected) == 0:

            showerror("Error", "No vector selected on the table!")

        elif selected[0] in self.tree_entries.values():

            showerror("Error", "Cannot remove top category")

        else:

            for name in selected:
                self.vector_dict.pop(name)
                self.quiver_dict.pop(name).remove()
                self.tree.delete(name)

            self.get_resultant()
            self.rescale_graph()

        return

    def get_resultant(self) -> tuple[float, float, float, float]:
        """
        Get the resultant of the vectors listed on the table
        """
        self.resultant_vct = sum(self.vector_dict.values()) if len(self.vector_dict) else np.array([0, 0])  # type: ignore
        x: float = self.resultant_vct[0]
        y: float = self.resultant_vct[1]
        r: float = np.hypot(*self.resultant_vct)
        theta: float = np.rad2deg(np.arctan2(self.resultant_vct[1], self.resultant_vct[0]))
        self.resultant_str_vars["x"].set(value=f"{x: .4f}")  # type: ignore
        self.resultant_str_vars["y"].set(value=f"{y: .4f}")  # type: ignore
        self.resultant_str_vars["r"].set(value=f"{r: .4f}")
        self.resultant_str_vars["theta"].set(value=f"{theta: .4f}")  # type: ignore
        self.resultant_plot.remove()
        self.resultant_plot = self.plot.quiver(*self.resultant_vct, color="black", scale=1, scale_units="xy", angles="xy")  # type: ignore
        return x, y, r, theta

    def rescale_graph(self) -> None:
        """
        Rescales the canvas to fit all vectors on the screen.
        """
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
        """
        Closes the vector canvas and program window.
        """
        self.canvas.callbacks.process('close_event')
        self.master.focus_set()
        self.destroy()
        return
    

class ResultantWindow(BaseWindow):

    """Window Class made for getting the resultant of the given vectors"""
    def __init__(self, master: tk.Tk, min_width: int = 900, min_height: int = 700) -> None:
        super().__init__(master, min_width, min_height)

        self.resultant_frame = ttk.LabelFrame(self.control_panel, text="Resultant (Black)")
        self.resultant_frame.grid(column=0, row=2, sticky="new", padx=10, pady=10)
        self.resultant_frame.grid_columnconfigure(0, weight=1)
        self.resultant_frame.grid_columnconfigure(1, weight=1)
        self.resultant_frame.grid_columnconfigure(2, weight=1)
        self.resultant_frame.grid_columnconfigure(3, weight=1)
        self.resultant_frame.grid_rowconfigure(0, weight=1)
        self.resultant_frame.grid_rowconfigure(1, weight=1)

        self.result_str_vars: dict[str, tk.StringVar] = {
            "x": tk.StringVar(self, "0.000000"),
            "y": tk.StringVar(self, "0.000000"),
            "r": tk.StringVar(self, "0.000000"),
            "theta": tk.StringVar(self, "0.000000")
        }

        ttk.Label(self.resultant_frame, text="X = ").grid(column=0, row=0, sticky="w", padx=20, pady=5)
        ttk.Label(self.resultant_frame, textvariable=self.result_str_vars["x"]).grid(column=1, row=0, sticky="e", padx=20, pady=5)
        ttk.Label(self.resultant_frame, text="R = ").grid(column=2, row=0, sticky="w", padx=20, pady=5)
        ttk.Label(self.resultant_frame, textvariable=self.result_str_vars["r"]).grid(column=3, row=0, sticky="e", padx=20, pady=5)
        ttk.Label(self.resultant_frame, text="Y = ").grid(column=0, row=1, sticky="w", padx=20, pady=5)
        ttk.Label(self.resultant_frame, textvariable=self.result_str_vars["y"]).grid(column=1, row=1, sticky="e", padx=20, pady=5)
        ttk.Label(self.resultant_frame, text="\u03B8 = ").grid(column=2, row=1, sticky="w", padx=20, pady=5)
        ttk.Label(self.resultant_frame, textvariable=self.result_str_vars["theta"]).grid(column=3, row=1, sticky="e", padx=20, pady=5)

        self.add_vector_button.configure(command=self.add_vector)
        self.remove_vector_button.configure(command=self.rm_vector)
        return
    
    def add_vector(self) -> None:
        """
        Add a vector to the table with a unique name and plot the vector into the plane.
        """
        vector_name = self.vector_str_vars["name"].get()

        if vector_name == "":

            showerror("Error", "Vector name is empty!")
            self.name_entry.focus_set()
            return

        elif vector_name in self.vector_dict:

            showerror("Error", f"Vector \"{vector_name}\" already exists!")
            self.name_entry.focus_set()
            return

        elif vector_name in self.tree_entries.values():

            showerror("Error", f"{self.tree_entries['given']}, {self.tree_entries['missing']}, and {self.tree_entries['other']} are currently reserved for the main categories.")
            self.name_entry.focus_set()
            return

        elif self.coordinate.get():

            try:
                r = float(self.vector_str_vars["req1"].get())
            except ValueError:
                showerror("Error", "Value must be a valid decimal number!")
                self.req1_entry.focus_set()
                return

            try:
                theta = float(self.vector_str_vars["req2"].get())
            except ValueError:
                showerror("Error", "Value must be a valid decimal number!")
                self.req2_entry.focus_set()
                return

            x = r * np.cos(np.radians(theta))
            y = r * np.sin(np.radians(theta))

        else:

            try:
                x = float(self.vector_str_vars["req1"].get())
            except ValueError:
                showerror("Error", "Value must be a valid decimal number!")
                self.req1_entry.focus_set()
                return

            try:
                y = float(self.vector_str_vars["req2"].get())
            except ValueError:
                showerror("Error", "Value must be a valid decimal number!")
                self.req2_entry.focus_set()
                return

            r = np.hypot(x, y)
            theta_rad = np.arctan2(y, x)
            theta = np.rad2deg(theta_rad)

        self.vector_dict[vector_name] = np.array([x, y])
        self.quiver_dict[vector_name] = self.plot.quiver(x, y, alpha=0.5, color="g", scale=1, scale_units="xy", angles="xy")
        self.tree.insert(self.tree_entries["given"], "end", vector_name, values=(vector_name, f"{x: .6f}", f"{y: .6f}", f"{r: .6f}", f"{theta: .6f}"))
        self.tree.item(self.tree_entries["given"], open=True)

        # noinspection SpellCheckingInspection
        rx, ry, rm, rtheta = self.get_resultant()  # type: ignore

        self.result_str_vars["x"].set(f"{rx: .6f}")  # type: ignore
        self.result_str_vars["y"].set(f"{ry: .6f}")  # type: ignore
        self.result_str_vars["r"].set(f"{rm: .6f}")
        self.result_str_vars["theta"].set(f"{rtheta: .6f}")  # type: ignore

        self.rescale_graph()

        return

    # noinspection SpellCheckingInspection
    def rm_vector(self) -> None:
        
        self.remove_vector()
        rx, ry, rm, rtheta = self.get_resultant()  # type: ignore

        self.result_str_vars["x"].set(f"{rx: .6f}")  # type: ignore
        self.result_str_vars["y"].set(f"{ry: .6f}")  # type: ignore
        self.result_str_vars["r"].set(f"{rm: .6f}")
        self.result_str_vars["theta"].set(f"{rtheta: .6f}")  # type: ignore

        self.rescale_graph()
        return



class OneMissingVector(BaseWindow):

    """
    Window Class for finding one vector with missing angle and magnitude.
    """
    def __init__(self, master: tk.Tk, min_width: int = 900, min_height: int = 700) -> None:

        super().__init__(master, min_width, min_height)

        self.missing_vector_frame = ttk.LabelFrame(master=self.control_panel, text="One Missing Vector (Red)")
        self.missing_vector_frame.grid(column=0, row=2, sticky="new", padx=10, pady=10)
        self.missing_vector_frame.grid_columnconfigure(0, weight=1)
        self.missing_vector_frame.grid_columnconfigure(1, weight=3)
        self.missing_vector_frame.grid_columnconfigure(2, weight=1)
        self.missing_vector_frame.grid_columnconfigure(3, weight=3)

        self.expected_resultant_vars: dict[str, tk.StringVar] = {
            "name": tk.StringVar(self),
            "req1": tk.StringVar(self),
            "req2": tk.StringVar(self)
        }
        self.expected_resultant_coordinate: tk.IntVar = tk.IntVar(self, value=0)
        self.missing_vector_vars: dict[str, tk.StringVar] = {
            "x": tk.StringVar(self),
            "y": tk.StringVar(self),
            "r": tk.StringVar(self),
            "theta": tk.StringVar(self)
        }
        self.auto_update: tk.IntVar = tk.IntVar(self, value=0)
        self.expected_resultant: np.ndarray = np.array([0, 0])

        ttk.Label(self.missing_vector_frame, text="Vector name: ").grid(column=0, row=0, sticky="nw", padx=10)
        ttk.Label(self.missing_vector_frame, text="X / R : ").grid(column=0, row=2, sticky="ew", padx=10)
        ttk.Label(self.missing_vector_frame, text="Y / \u03B8 : ").grid(column=2, row=2, sticky="ew", padx=10)
        ttk.Label(self.missing_vector_frame, text="Expected Resultant").grid(column=0, row=1, columnspan=4, sticky="nw", padx=10, pady=(10, 0))

        self.missing_name_entry = ttk.Entry(self.missing_vector_frame, textvariable=self.expected_resultant_vars["name"])
        self.missing_name_entry.grid(column=1, row=0, columnspan=3, sticky="new", padx=10)
        self.missing_req1_entry = ttk.Entry(self.missing_vector_frame, textvariable=self.expected_resultant_vars["req1"])
        self.missing_req1_entry.grid(column=1, row=2, sticky="ew", padx=10, pady=10)
        self.missing_req2_entry = ttk.Entry(self.missing_vector_frame, textvariable=self.expected_resultant_vars["req2"])
        self.missing_req2_entry.grid(column=3, row=2, sticky="ew", padx=10, pady=10)

        self.cartesian = ttk.Radiobutton(self.missing_vector_frame, text="X and Y components", variable=self.expected_resultant_coordinate, value=0)
        self.cartesian.grid(column=0, row=3, columnspan=2, sticky="ew", padx=10, pady=10)
        self.polar = ttk.Radiobutton(self.missing_vector_frame, text="Magnitude and Direction", variable=self.expected_resultant_coordinate, value=1)
        self.polar.grid(column=2, row=3, columnspan=2, sticky="ew", padx=10, pady=10)
        ttk.Checkbutton(self.missing_vector_frame, text="Find and Auto-update missing vector", command=self.get_expected_resultant, variable=self.auto_update).grid(column=0, row=4, columnspan=4, sticky="ew", pady=(5, 10), padx=10)

        self.result_frame = ttk.LabelFrame(master=self.control_panel, text="Missing Vector (Red)")
        self.result_frame.grid(column=0, row=3, sticky="ew", padx=10, pady=10)
        self.result_frame.grid_columnconfigure(0, weight=2)
        self.result_frame.grid_columnconfigure(1, weight=3)
        self.result_frame.grid_columnconfigure(2, weight=2)
        self.result_frame.grid_columnconfigure(3, weight=3)

        ttk.Label(self.result_frame, text="X = ").grid(column=0, row=0, sticky="w", padx=20, pady=5)
        ttk.Label(self.result_frame, textvariable=self.missing_vector_vars["x"]).grid(column=1, row=0, sticky="e", padx=20, pady=5)
        ttk.Label(self.result_frame, text="R = ").grid(column=2, row=0, sticky="w", padx=20, pady=5)
        ttk.Label(self.result_frame, textvariable=self.missing_vector_vars["r"]).grid(column=3, row=0, sticky="e", padx=20, pady=5)
        ttk.Label(self.result_frame, text="Y = ").grid(column=0, row=1, sticky="w", padx=20, pady=5)
        ttk.Label(self.result_frame, textvariable=self.missing_vector_vars["y"]).grid(column=1, row=1, sticky="e", padx=20, pady=5)
        ttk.Label(self.result_frame, text="\u03B8 = ").grid(column=2, row=1, sticky="w", padx=20, pady=5)
        ttk.Label(self.result_frame, textvariable=self.missing_vector_vars["theta"]).grid(column=3, row=1, sticky="e", padx=20, pady=5)

        self.add_vector_button.configure(command=self.add_vector)
        self.remove_vector_button.configure(command=self.rm_vector)
        self.clear_all_button.configure(command=self.clear_all)
        return

    def add_vector(self) -> None:
        """
        Add a vector to the table with a unique name and plot the vector into the plane.
        """
        vector_name = self.vector_str_vars["name"].get()

        if vector_name == "":

            showerror("Error", "Vector name is empty!")
            self.name_entry.focus_set()
            return

        elif vector_name in self.vector_dict:

            showerror("Error", f"Vector \"{vector_name}\" already exists!")
            self.name_entry.focus_set()
            return

        elif vector_name in self.tree_entries.values():

            showerror("Error", f"{self.tree_entries['given']}, {self.tree_entries['missing']}, and {self.tree_entries['other']} are currently reserved for the main categories.")
            self.name_entry.focus_set()
            return

        elif self.coordinate.get():

            try:
                r = float(self.vector_str_vars["req1"].get())
            except ValueError:
                showerror("Error", "Value must be a valid decimal number!")
                self.req1_entry.focus_set()
                return

            try:
                theta = float(self.vector_str_vars["req2"].get())
            except ValueError:
                showerror("Error", "Value must be a valid decimal number!")
                self.req2_entry.focus_set()
                return

            x = r * np.cos(np.radians(theta))
            y = r * np.sin(np.radians(theta))

        else:

            try:
                x = float(self.vector_str_vars["req1"].get())
            except ValueError:
                showerror("Error", "Value must be a valid decimal number!")
                self.req1_entry.focus_set()
                return

            try:
                y = float(self.vector_str_vars["req2"].get())
            except ValueError:
                showerror("Error", "Value must be a valid decimal number!")
                self.req2_entry.focus_set()
                return

            r = np.hypot(x, y)
            theta_rad = np.arctan2(y, x)
            theta = np.rad2deg(theta_rad)

        self.vector_dict[vector_name] = np.array([x, y])
        self.quiver_dict[vector_name] = self.plot.quiver(x, y, alpha=0.5, color="g", scale=1, scale_units="xy", angles="xy")
        self.tree.insert(self.tree_entries["given"], "end", vector_name, values=(vector_name, f"{x: .6f}", f"{y: .6f}", f"{r: .6f}", f"{theta: .6f}"))
        self.tree.item(self.tree_entries["given"], open=True)

        if self.auto_update.get():
            self.find_missing_vector()

        self.get_resultant()
        self.rescale_graph()

        return

    def rm_vector(self) -> None:
        """
        Checks vector to be removed before removing from list and graph.
        """
        vector_name = self.expected_resultant_vars["name"].get()

        if vector_name in self.tree.selection() and self.auto_update.get():

            showerror("Error", f"Cannot remove \"{vector_name}\" vector while auto-updating! Please disable auto-update first.")
            return

        self.remove_vector()

        if self.auto_update.get():
            self.find_missing_vector()

        self.get_resultant()
        self.rescale_graph()
        return

    def clear_all(self) -> None:
        """
        Clear all vectors from screen and stop auto-update
        """
        self.auto_update.set(0)
        for i in self.quiver_dict.values():
            i.remove()
        self.quiver_dict.clear()
        self.vector_dict.clear()
        self.tree.delete(*self.tree.get_children(self.tree_entries["given"]))
        self.tree.delete(*self.tree.get_children(self.tree_entries["missing"]))
        self.expected_resultant: np.ndarray = np.array([0, 0])
        for i in self.vector_str_vars.values():
            i.set("")
        for i in self.expected_resultant_vars.values():
            i.set("")
        for i in self.missing_vector_vars.values():
            i.set("")
        self.coordinate.set(0)
        self.expected_resultant_coordinate.set(0)
        self.missing_name_entry.configure(state="enabled")
        self.missing_req1_entry.configure(state="enabled")
        self.missing_req2_entry.configure(state="enabled")
        self.cartesian.configure(state="enabled")
        self.polar.configure(state="enabled")

        self.get_resultant()
        self.rescale_graph()
        return

    def find_missing_vector(self) -> None:
        """
        Computes and plots the missing vector on the graph using the listed vectors.
        """
        vector_name = self.expected_resultant_vars["name"].get()

        self.vector_dict.pop(vector_name)
        self.quiver_dict[vector_name].remove()
        self.tree.delete(vector_name)

        missing_vector: np.ndarray = self.expected_resultant - (sum(self.vector_dict.values()) if len(self.vector_dict) else np.array([0, 0]))
        x, y = missing_vector[0], missing_vector[1]
        magnitude = np.hypot(x, y)
        direction = np.rad2deg(np.arctan2(y, x))
        self.vector_dict[vector_name] = missing_vector
        self.quiver_dict[vector_name] = self.plot.quiver(x, y, alpha=0.5, color="r", scale=1, scale_units="xy", angles="xy")
        self.tree.insert(self.tree_entries["missing"], "end", vector_name, values=(vector_name, f"{x: .6f}", f"{y: .6f}", f"{magnitude: .6f}", f"{direction: .6f}"))
        self.tree.item(self.tree_entries["missing"], open=True)
        self.missing_vector_vars["x"].set(f"{x: .6f}")
        self.missing_vector_vars["y"].set(f"{y: .6f}")
        self.missing_vector_vars["r"].set(f"{magnitude: .6f}")
        self.missing_vector_vars["theta"].set(f"{direction: .6f}")

        return

    def get_expected_resultant(self) -> None:

        vector_name = self.expected_resultant_vars["name"].get()

        if self.auto_update.get():

            if vector_name == "":

                showerror("Error", "Vector name is empty!")
                self.auto_update.set(0)
                self.missing_name_entry.focus_set()
                return

            elif vector_name in self.vector_dict:

                showerror("Error", f"Vector \"{vector_name}\" already exists!")
                self.auto_update.set(0)
                self.missing_name_entry.focus_set()
                return

            elif vector_name in self.tree_entries.values():

                showerror("Error",f"{self.tree_entries['given']}, {self.tree_entries['missing']}, and {self.tree_entries['other']} are currently reserved for the main categories.")
                self.auto_update.set(0)
                self.missing_name_entry.focus_set()
                return

            elif self.expected_resultant_coordinate.get():

                try:
                    r = float(self.expected_resultant_vars["req1"].get())
                except ValueError:
                    showerror("Error", "Value must be a valid decimal number!")
                    self.auto_update.set(0)
                    self.missing_req1_entry.focus_set()
                    return

                try:
                    theta = float(self.expected_resultant_vars["req2"].get())
                except ValueError:
                    showerror("Error", "Value must be a valid decimal number!")
                    self.auto_update.set(0)
                    self.missing_req2_entry.focus_set()
                    return

                x = r * np.cos(np.radians(theta))
                y = r * np.sin(np.radians(theta))

            else:

                try:
                    x = float(self.expected_resultant_vars["req1"].get())
                except ValueError:
                    showerror("Error", "Value must be a valid decimal number!")
                    self.auto_update.set(0)
                    self.missing_req1_entry.focus_set()
                    return

                try:
                    y = float(self.expected_resultant_vars["req2"].get())
                except ValueError:
                    showerror("Error", "Value must be a valid decimal number!")
                    self.auto_update.set(0)
                    self.missing_req2_entry.focus_set()
                    return

            self.missing_name_entry.configure(state="disabled")
            self.missing_req1_entry.configure(state="disabled")
            self.missing_req2_entry.configure(state="disabled")
            self.cartesian.configure(state="disabled")
            self.polar.configure(state="disabled")

            self.vector_dict[vector_name] = np.array([0, 0])
            self.quiver_dict[vector_name] = self.plot.quiver(0, 0)
            self.tree.insert(self.tree_entries["missing"], "end", vector_name, values=(vector_name, 0, 0, 0, 0))
            self.expected_resultant = np.array([x, y])

            self.find_missing_vector()
            self.get_resultant()
            self.rescale_graph()

        else:

            self.missing_name_entry.configure(state="enabled")
            self.missing_req1_entry.configure(state="enabled")
            self.missing_req2_entry.configure(state="enabled")
            self.cartesian.configure(state="enabled")
            self.polar.configure(state="enabled")

        return


class TwoMissingMagnitudes(BaseWindow):

    def __init__(self, master: tk.Tk, min_width: int = 900, min_height: int = 700) -> None:

        super().__init__(master, min_width, min_height)

        self.requirements_vars: dict[str, tk.StringVar] = {
            "v1_name": tk.StringVar(self),
            "v1_angle": tk.StringVar(self),
            "v2_name": tk.StringVar(self),
            "v2_angle": tk.StringVar(self),
            "result_req1": tk.StringVar(self),
            "result_req2": tk.StringVar(self)
        }
        self.missing_coordinate = tk.IntVar(self, value=0)
        self.angle_array = np.array([0, 0])
        self.auto_update = tk.IntVar(self, value=0)
        self.expected_resultant = np.array([0, 0])

        self.missing_magnitudes_frame = ttk.Labelframe(self.control_panel, text="Two Missing Magnitudes (Blue)")
        self.missing_magnitudes_frame.grid(column=0, row=2, sticky="new", padx=10, pady=10)
        self.missing_magnitudes_frame.grid_columnconfigure(0, weight=1)
        self.missing_magnitudes_frame.grid_columnconfigure(1, weight=3)
        self.missing_magnitudes_frame.grid_columnconfigure(2, weight=1)
        self.missing_magnitudes_frame.grid_columnconfigure(3, weight=3)

        ttk.Label(self.missing_magnitudes_frame, text="Vector 1").grid(column=0, row=0, columnspan=4, sticky="nw", padx=10, pady=(10, 0))
        ttk.Label(self.missing_magnitudes_frame, text="Name: ").grid(column=0, row=1, sticky="nw", padx=10, pady=(3, 0))
        ttk.Label(self.missing_magnitudes_frame, text="Angle: ").grid(column=2, row=1, sticky="nw", padx=10, pady=(3, 13))
        ttk.Label(self.missing_magnitudes_frame, text="Vector 2").grid(column=0, row=2, columnspan=4, sticky="nw", padx=10, pady=(5, 0))
        ttk.Label(self.missing_magnitudes_frame, text="Name: ").grid(column=0, row=3, sticky="nw", padx=10)
        ttk.Label(self.missing_magnitudes_frame, text="Angle: ").grid(column=2, row=3, sticky="nw", padx=10, pady=(3, 13))
        ttk.Label(self.missing_magnitudes_frame, text="Expected Resultant").grid(column=0, row=4, columnspan=4, sticky="nw", padx=10, pady=(5, 0))
        ttk.Label(self.missing_magnitudes_frame, text="X / Y: ").grid(column=0, row=5, sticky="nw", padx=10)
        ttk.Label(self.missing_magnitudes_frame, text="R / \u03B8: ").grid(column=2, row=5, sticky="nw", padx=10, pady=(3, 13))

        self.vector1_name_entry = ttk.Entry(self.missing_magnitudes_frame, textvariable=self.requirements_vars["v1_name"])
        self.vector1_name_entry.grid(column=1, row=1, sticky="new", padx=10, pady=(3, 0))
        self.vector1_angle_entry = ttk.Entry(self.missing_magnitudes_frame, textvariable=self.requirements_vars["v1_angle"])
        self.vector1_angle_entry.grid(column=3, row=1, sticky="new", padx=10, pady=(3, 13))
        self.vector2_name_entry = ttk.Entry(self.missing_magnitudes_frame, textvariable=self.requirements_vars["v2_name"])
        self.vector2_name_entry.grid(column=1, row=3, sticky="new", padx=10)
        self.vector2_angle_entry = ttk.Entry(self.missing_magnitudes_frame, textvariable=self.requirements_vars["v2_angle"])
        self.vector2_angle_entry.grid(column=3, row=3, sticky="new", padx=10, pady=(3, 13))
        self.resultant_req1_entry = ttk.Entry(self.missing_magnitudes_frame, textvariable=self.requirements_vars["result_req1"])
        self.resultant_req1_entry.grid(column=1, row=5, sticky="new", padx=10)
        self.resultant_req2_entry = ttk.Entry(self.missing_magnitudes_frame, textvariable=self.requirements_vars["result_req2"])
        self.resultant_req2_entry.grid(column=3, row=5, sticky="new", padx=10, pady=(3, 13))

        self.cartesian = ttk.Radiobutton(self.missing_magnitudes_frame, text="X and Y components", variable=self.missing_coordinate, value=0)
        self.cartesian.grid(column=0, row=6, columnspan=2, sticky="ew", padx=10, pady=10)
        self.polar = ttk.Radiobutton(self.missing_magnitudes_frame, text="Magnitude and Direction", variable=self.missing_coordinate, value=1)
        self.polar.grid(column=2, row=6, columnspan=2, sticky="ew", padx=10, pady=10)
        ttk.Checkbutton(self.missing_magnitudes_frame, text="Find Missing Magnitudes and auto-update", variable=self.auto_update, command=self.get_expected_resultant).grid(column=0, row=7, columnspan=4, sticky="ew", padx=10, pady=10)

        self.add_vector_button.configure(command=self.add_vector)
        self.remove_vector_button.configure(command=self.rm_vector)
        self.clear_all_button.configure(command=self.clear_all)
        return

    def add_vector(self) -> None:
        """
        Add a vector to the table with a unique name and plot the vector into the plane.
        """
        vector_name = self.vector_str_vars["name"].get()

        if vector_name == "":

            showerror("Error", "Vector name is empty!")
            self.name_entry.focus_set()
            return

        elif vector_name in self.vector_dict:

            showerror("Error", f"Vector \"{vector_name}\" already exists!")
            self.name_entry.focus_set()
            return

        elif self.coordinate.get():

            try:
                r = float(self.vector_str_vars["req1"].get())
            except ValueError:
                showerror("Error", "Value must be a valid decimal number!")
                self.req1_entry.focus_set()
                return

            try:
                theta = float(self.vector_str_vars["req2"].get())
            except ValueError:
                showerror("Error", "Value must be a valid decimal number!")
                self.req2_entry.focus_set()
                return

            x = r * np.cos(np.radians(theta))
            y = r * np.sin(np.radians(theta))

        else:

            try:
                x = float(self.vector_str_vars["req1"].get())
            except ValueError:
                showerror("Error", "Value must be a valid decimal number!")
                self.req1_entry.focus_set()
                return

            try:
                y = float(self.vector_str_vars["req2"].get())
            except ValueError:
                showerror("Error", "Value must be a valid decimal number!")
                self.req2_entry.focus_set()
                return

            r = np.hypot(x, y)
            theta_rad = np.arctan2(y, x)
            theta = np.rad2deg(theta_rad)

        self.vector_dict[vector_name] = np.array([x, y])
        self.quiver_dict[vector_name] = self.plot.quiver(x, y, alpha=0.5, color="g", scale=1, scale_units="xy", angles="xy")
        self.tree.insert(self.tree_entries["given"], "end", vector_name, values=(vector_name, f"{x: .6f}", f"{y: .6f}", f"{r: .6f}", f"{theta: .6f}"))
        self.tree.item(self.tree_entries["given"], open=True)

        if self.auto_update.get():
            self.find_missing_magnitudes()

        self.get_resultant()
        self.rescale_graph()

        return

    def rm_vector(self) -> None:
        """
        Checks vector to be removed before removing from list and graph
        """
        vector1_name = self.requirements_vars["v1_name"].get()
        vector2_name = self.requirements_vars["v2_name"].get()

        if self.auto_update.get() and vector1_name in self.tree.selection():

            showerror("Error", f"Cannot remove \"{vector1_name}\" vector while auto-updating! Please disable auto-update first.")
            return

        elif self.auto_update.get() and  vector2_name in self.tree.selection():
            showerror("Error", f"Cannot remove \"{vector2_name}\" vector while auto-updating! Please disable auto-update first.")
            return

        self.remove_vector()

        if self.auto_update.get():
            self.find_missing_magnitudes()

        self.get_resultant()
        self.rescale_graph()
        return

    def clear_all(self) -> None:

        self.auto_update.set(0)
        for i in self.quiver_dict.values():
            i.remove()
        self.quiver_dict.clear()
        self.vector_dict.clear()
        self.tree.delete(*self.tree.get_children(self.tree_entries["given"]))
        self.tree.delete(*self.tree.get_children(self.tree_entries["missing"]))
        self.expected_resultant: np.ndarray = np.array([0, 0])
        for i in self.vector_str_vars.values():
            i.set("")
        for i in self.requirements_vars.values():
            i.set("")
        self.coordinate.set(0)
        self.missing_coordinate.set(0)
        self.vector1_name_entry.configure(state="enabled")
        self.vector1_angle_entry.configure(state="enabled")
        self.vector2_name_entry.configure(state="enabled")
        self.vector2_angle_entry.configure(state="enabled")
        self.resultant_req1_entry.configure(state="enabled")
        self.resultant_req2_entry.configure(state="enabled")
        self.cartesian.configure(state="enabled")
        self.polar.configure(state="enabled")

        self.get_resultant()
        self.rescale_graph()
        return

    def find_missing_magnitudes(self) -> None:

        vector1_name = self.requirements_vars["v1_name"].get()
        vector2_name = self.requirements_vars["v2_name"].get()

        self.vector_dict.pop(vector1_name)
        self.vector_dict.pop(vector2_name)
        self.quiver_dict[vector1_name].remove()
        self.quiver_dict[vector2_name].remove()
        self.tree.delete(vector1_name)
        self.tree.delete(vector2_name)

        expected_sum: np.ndarray = self.expected_resultant - (sum(self.vector_dict.values()) if len(self.vector_dict) else np.array([0, 0]))
        angle_rad_array: np.ndarray = np.radians(self.angle_array)
        matrix = np.array([np.cos(angle_rad_array), np.sin(angle_rad_array)])
        inverted_matrix = np.linalg.inv(matrix)
        magnitude = np.dot(inverted_matrix, expected_sum)
        x = magnitude * np.cos(angle_rad_array)
        y = magnitude * np.sin(angle_rad_array)
        self.vector_dict[vector1_name] = np.array([x[0], y[0]])
        self.vector_dict[vector2_name] = np.array([x[1], y[1]])
        self.quiver_dict[vector1_name] = self.plot.quiver(x[0], y[0], alpha=0.5, color="b", scale=1, scale_units="xy", angles="xy")
        self.quiver_dict[vector2_name] = self.plot.quiver(x[1], y[1], alpha=0.5, color="orange", scale=1, scale_units="xy", angles="xy")
        self.tree.insert(self.tree_entries["missing"], "end", vector1_name, values=(vector1_name, f"{x[0]: .6f}", f"{y[0]: .6f}", f"{magnitude[0]: .6f}", f"{self.angle_array[0]: .6f}"))
        self.tree.insert(self.tree_entries["missing"], "end", vector2_name, values=(vector2_name, f"{x[1]: .6f}", f"{y[1]: .6f}", f"{magnitude[1]: .6f}", f"{self.angle_array[1]: .6f}"))
        self.tree.item(self.tree_entries["missing"], open=True)

        return

    def get_expected_resultant(self) -> None:

        vector1_name = self.requirements_vars["v1_name"].get()
        vector2_name = self.requirements_vars["v2_name"].get()

        if self.auto_update.get():

            if vector1_name == "":

                showerror("Error", "Vector name is empty!")
                self.auto_update.set(0)
                self.vector1_name_entry.focus_set()
                return

            elif vector1_name in self.quiver_dict:

                showerror("Error", f"Vector \"{vector1_name}\" already exists!")
                self.auto_update.set(0)
                self.vector1_name_entry.focus_set()
                return

            elif vector2_name == "":

                showerror("Error", "Vector name is empty!")
                self.auto_update.set(0)
                self.vector2_name_entry.focus_set()
                return

            elif vector2_name in self.quiver_dict:

                showerror("Error", f"Vector \"{vector2_name}\" already exists!")
                self.auto_update.set(0)
                self.vector2_name_entry.focus_set()
                return

            elif vector1_name == vector2_name:

                showerror("Error", "Vector names must be different!")
                self.auto_update.set(0)
                self.vector1_name_entry.focus_set()
                return

            elif self.requirements_vars["v1_angle"].get() == self.requirements_vars["v2_angle"].get():

                showerror("Error", "Angles must be different! Might result in infinitely solutions or no solution.")
                self.auto_update.set(0)
                self.vector2_angle_entry.focus_set()
                return

            try:
                self.angle_array[0] = float(self.requirements_vars["v1_angle"].get())
            except ValueError:
                showerror("Error", "Value must be a valid decimal number!")
                self.auto_update.set(0)
                self.vector1_angle_entry.focus_set()
                return

            try:
                self.angle_array[1] = float(self.requirements_vars["v2_angle"].get())
            except ValueError:
                showerror("Error", "Value must be a valid decimal number!")
                self.auto_update.set(0)
                self.vector2_angle_entry.focus_set()
                return

            if self.missing_coordinate.get():

                try:
                    resultant_magnitude = float(self.requirements_vars["result_req1"].get())
                except ValueError:
                    showerror("Error", "Value must be a valid decimal number!")
                    self.auto_update.set(0)
                    self.resultant_req1_entry.focus_set()
                    return

                try:
                    resultant_angle = float(self.requirements_vars["result_req2"].get())
                except ValueError:
                    showerror("Error", "Value must be a valid decimal number!")
                    self.auto_update.set(0)
                    self.resultant_req2_entry.focus_set()
                    return

                resultant_x = resultant_magnitude * np.cos(np.radians(resultant_angle))
                resultant_y = resultant_magnitude * np.sin(np.radians(resultant_angle))

            else:

                try:
                    resultant_x = float(self.requirements_vars["result_req1"].get())
                except ValueError:
                    showerror("Error", "Value must be a valid decimal number!")
                    self.auto_update.set(0)
                    self.resultant_req1_entry.focus_set()
                    return

                try:
                    resultant_y = float(self.requirements_vars["result_req2"].get())
                except ValueError:
                    showerror("Error", "Value must be a valid decimal number!")
                    self.auto_update.set(0)
                    self.resultant_req2_entry.focus_set()
                    return

            self.vector1_name_entry.configure(state="disabled")
            self.vector1_angle_entry.configure(state="disabled")
            self.vector2_name_entry.configure(state="disabled")
            self.vector2_angle_entry.configure(state="disabled")
            self.resultant_req1_entry.configure(state="disabled")
            self.resultant_req2_entry.configure(state="disabled")
            self.cartesian.configure(state="disabled")
            self.polar.configure(state="disabled")

            self.vector_dict[vector1_name] = np.array([0, 0])
            self.vector_dict[vector2_name] = np.array([0, 0])
            self.quiver_dict[vector1_name] = self.plot.quiver(0, 0)
            self.quiver_dict[vector2_name] = self.plot.quiver(0, 0)
            self.tree.insert(self.tree_entries["missing"], "end", vector1_name, values=(vector1_name, 0, 0, 0, 0))
            self.tree.insert(self.tree_entries["missing"], "end", vector2_name, values=(vector2_name, 0, 0, 0, 0))
            self.expected_resultant = np.array([resultant_x, resultant_y])

            self.find_missing_magnitudes()
            self.get_resultant()
            self.rescale_graph()

        else:

            self.vector1_name_entry.configure(state="enabled")
            self.vector1_angle_entry.configure(state="enabled")
            self.vector2_name_entry.configure(state="enabled")
            self.vector2_angle_entry.configure(state="enabled")
            self.resultant_req1_entry.configure(state="enabled")
            self.resultant_req2_entry.configure(state="enabled")
            self.cartesian.configure(state="enabled")
            self.polar.configure(state="enabled")

        return


class TwoMissingDirections(BaseWindow):

    def __init__(self, master: tk.Tk, min_width: int = 900, min_height: int = 700) -> None:

        super().__init__(master, min_width, min_height)
        self.tree_entries["Other Angle"] = self.tree.insert("", "end", text = "Other \u03B8")

        self.requirements_vars: dict[str, tk.StringVar] = {
            "v1_name": tk.StringVar(self),
            "v1_magnitude": tk.StringVar(self),
            "v2_name": tk.StringVar(self),
            "v2_magnitude": tk.StringVar(self),
            "result_req1": tk.StringVar(self),
            "result_req2": tk.StringVar(self)
        }
        self.missing_coordinate = tk.IntVar(self, value=0)
        self.magnitude_array = np.array([0., 0.])
        self.auto_update = tk.IntVar(self, value=0)
        self.expected_resultant = np.array([])

        self.missing_angle_frame = ttk.Labelframe(self.control_panel, text="Two Missing Directions (Blue)")
        self.missing_angle_frame.grid(column=0, row=2, sticky="new", padx=10, pady=10)
        self.missing_angle_frame.grid_columnconfigure(0, weight=1)
        self.missing_angle_frame.grid_columnconfigure(1, weight=3)
        self.missing_angle_frame.grid_columnconfigure(2, weight=1)
        self.missing_angle_frame.grid_columnconfigure(3, weight=3)

        ttk.Label(self.missing_angle_frame, text="Vector 1").grid(column=0, row=0, columnspan=4, sticky="nw", padx=10, pady=(10, 0))
        ttk.Label(self.missing_angle_frame, text="Name: ").grid(column=0, row=1, sticky="nw", padx=10, pady=(3, 0))
        ttk.Label(self.missing_angle_frame, text="Magnitude: ").grid(column=2, row=1, sticky="nw", padx=10, pady=(3, 13))
        ttk.Label(self.missing_angle_frame, text="Vector 2").grid(column=0, row=2, columnspan=4, sticky="nw", padx=10, pady=(5, 0))
        ttk.Label(self.missing_angle_frame, text="Name: ").grid(column=0, row=3, sticky="nw", padx=10)
        ttk.Label(self.missing_angle_frame, text="Magnitude: ").grid(column=2, row=3, sticky="nw", padx=10, pady=(3, 13))
        ttk.Label(self.missing_angle_frame, text="Expected Resultant").grid(column=0, row=4, columnspan=4, sticky="nw", padx=10, pady=(5, 0))
        ttk.Label(self.missing_angle_frame, text="X / Y: ").grid(column=0, row=5, sticky="nw", padx=10)
        ttk.Label(self.missing_angle_frame, text="R / \u03B8: ").grid(column=2, row=5, sticky="nw", padx=10, pady=(3, 13))

        self.vector1_name_entry = ttk.Entry(self.missing_angle_frame, textvariable=self.requirements_vars["v1_name"])
        self.vector1_name_entry.grid(column=1, row=1, sticky="new", padx=10, pady=(3, 0))
        self.vector1_magnitude_entry = ttk.Entry(self.missing_angle_frame, textvariable=self.requirements_vars["v1_magnitude"])
        self.vector1_magnitude_entry.grid(column=3, row=1, sticky="new", padx=10, pady=(3, 13))
        self.vector2_name_entry = ttk.Entry(self.missing_angle_frame, textvariable=self.requirements_vars["v2_name"])
        self.vector2_name_entry.grid(column=1, row=3, sticky="new", padx=10)
        self.vector2_magnitude_entry = ttk.Entry(self.missing_angle_frame, textvariable=self.requirements_vars["v2_magnitude"])
        self.vector2_magnitude_entry.grid(column=3, row=3, sticky="new", padx=10, pady=(3, 13))
        self.resultant_req1_entry = ttk.Entry(self.missing_angle_frame, textvariable=self.requirements_vars["result_req1"])
        self.resultant_req1_entry.grid(column=1, row=5, sticky="new", padx=10)
        self.resultant_req2_entry = ttk.Entry(self.missing_angle_frame, textvariable=self.requirements_vars["result_req2"])
        self.resultant_req2_entry.grid(column=3, row=5, sticky="new", padx=10, pady=(3, 13))

        self.cartesian = ttk.Radiobutton(self.missing_angle_frame, text="X and Y components", variable=self.missing_coordinate, value=0)
        self.cartesian.grid(column=0, row=6, columnspan=2, sticky="ew", padx=10, pady=10)
        self.polar = ttk.Radiobutton(self.missing_angle_frame, text="Magnitude and Direction", variable=self.missing_coordinate, value=1)
        self.polar.grid(column=2, row=6, columnspan=2, sticky="ew", padx=10, pady=10)
        ttk.Checkbutton(self.missing_angle_frame, text="Find Missing Directions and auto-update", variable=self.auto_update, command= self.get_expected_resultant).grid(column=0, row=7, columnspan=4, sticky="ew", padx=10, pady=10)

        self.add_vector_button.configure(command=self.add_vector)
        self.remove_vector_button.configure(command=self.rm_vector)
        self.clear_all_button.configure(command=self.clear_all)
        return

    def add_vector(self) -> None:
        """
        Add a vector to the table with a unique name and plot the vector into the plane.
        """
        vector_name = self.vector_str_vars["name"].get()

        if vector_name == "":

            showerror("Error", "Vector name is empty!")
            self.name_entry.focus_set()
            return

        elif vector_name in self.vector_dict:

            showerror("Error", f"Vector \"{vector_name}\" already exists!")
            self.name_entry.focus_set()
            return

        elif self.coordinate.get():

            try:
                r = float(self.vector_str_vars["req1"].get())
            except ValueError:
                showerror("Error", "Value must be a valid decimal number!")
                self.req1_entry.focus_set()
                return

            try:
                theta = float(self.vector_str_vars["req2"].get())
            except ValueError:
                showerror("Error", "Value must be a valid decimal number!")
                self.req2_entry.focus_set()
                return

            x = r * np.cos(np.radians(theta))
            y = r * np.sin(np.radians(theta))

        else:

            try:
                x = float(self.vector_str_vars["req1"].get())
            except ValueError:
                showerror("Error", "Value must be a valid decimal number!")
                self.req1_entry.focus_set()
                return

            try:
                y = float(self.vector_str_vars["req2"].get())
            except ValueError:
                showerror("Error", "Value must be a valid decimal number!")
                self.req2_entry.focus_set()
                return

            r = np.hypot(x, y)
            theta_rad = np.arctan2(y, x)
            theta = np.rad2deg(theta_rad)

        self.vector_dict[vector_name] = np.array([x, y])
        self.quiver_dict[vector_name] = self.plot.quiver(x, y, alpha=0.5, color="g", scale=1, scale_units="xy", angles="xy")
        self.tree.insert(self.tree_entries["given"], "end", vector_name, values=(vector_name, f"{x: .6f}", f"{y: .6f}", f"{r: .6f}", f"{theta: .6f}"))
        self.tree.item(self.tree_entries["given"], open=True)

        if self.auto_update.get():
            self.find_missing_directions()

        self.get_resultant()
        self.rescale_graph()

        return

    def rm_vector(self) -> None:
        """
        Checks vector to be removed before removing from list and graph
        """
        vector1_name = self.requirements_vars["v1_name"].get()
        vector2_name = self.requirements_vars["v2_name"].get()

        if self.auto_update.get() and vector1_name in self.tree.selection():

            showerror("Error", f"Cannot remove \"{vector1_name}\" vector while auto-updating! Please disable auto-update first.")
            return

        elif self.auto_update.get() and  vector2_name in self.tree.selection():
            showerror("Error", f"Cannot remove \"{vector2_name}\" vector while auto-updating! Please disable auto-update first.")
            return
        
        elif self.auto_update.get() and  vector1_name + " 2" in self.tree.selection():
            showerror("Error", f"Cannot remove \"{vector2_name}\" vector while auto-updating! Please disable auto-update first.")
            return
        elif self.auto_update.get() and  vector2_name + " 2" in self.tree.selection():
            showerror("Error", f"Cannot remove \"{vector2_name}\" vector while auto-updating! Please disable auto-update first.")
            return
        


        self.remove_vector()

        if self.auto_update.get():
            self.find_missing_directions()

        self.get_resultant()
        self.rescale_graph()
        return

    def clear_all(self) -> None:

        self.auto_update.set(0)
        for i in self.quiver_dict.values():
            try:
                i.remove()
            except:
                pass
        self.quiver_dict.clear()
        self.vector_dict.clear()
        self.tree.delete(*self.tree.get_children(self.tree_entries["given"]))
        self.tree.delete(*self.tree.get_children(self.tree_entries["missing"]))
        self.tree.delete(*self.tree.get_children(self.tree_entries["Other Angle"]))
        self.expected_resultant: np.ndarray = np.array([0, 0])
        for i in self.vector_str_vars.values():
            i.set("")
        for i in self.requirements_vars.values():
            i.set("")
        self.coordinate.set(0)
        self.missing_coordinate.set(0)
        self.vector1_name_entry.configure(state="enabled")
        self.vector1_magnitude_entry.configure(state="enabled")
        self.vector2_name_entry.configure(state="enabled")
        self.vector2_magnitude_entry.configure(state="enabled")
        self.resultant_req1_entry.configure(state="enabled")
        self.resultant_req2_entry.configure(state="enabled")
        self.cartesian.configure(state="enabled")
        self.polar.configure(state="enabled")

        self.get_resultant()
        self.rescale_graph()
        return

    def find_missing_directions(self) -> None:

        vector1_name = self.requirements_vars["v1_name"].get()
        vector2_name = self.requirements_vars["v2_name"].get()

        try:
            self.vector_dict.pop(vector1_name)
            self.vector_dict.pop(vector2_name)
            self.quiver_dict[vector1_name].remove()
            self.quiver_dict[vector2_name].remove()
            self.tree.delete(vector1_name)
            self.tree.delete(vector2_name)
        except:
            pass

        if vector1_name + ' 2' in self.quiver_dict:
            self.quiver_dict[vector1_name + " 2"].remove()
            self.quiver_dict[vector2_name + " 2"].remove()
            self.tree.delete(vector1_name + " 2")
            self.tree.delete(vector2_name + " 2")

        expected_sum: np.ndarray = self.expected_resultant - (sum(self.vector_dict.values()) if len(self.vector_dict) else np.array([0, 0]))
        expected_sum_magnitude = np.hypot(expected_sum[0], expected_sum[1])
        expected_sum_angle = np.arctan2(expected_sum[1], expected_sum[0])


        try:
            angle2_1 = expected_sum_angle + np.arccos((expected_sum_magnitude**2 + self.magnitude_array[1]**2 - self.magnitude_array[0]**2)/(2*expected_sum_magnitude*self.magnitude_array[1]))
            angle2_2 = expected_sum_angle - np.arccos((expected_sum_magnitude**2 + self.magnitude_array[1]**2 - self.magnitude_array[0]**2)/(2*expected_sum_magnitude*self.magnitude_array[1]))
            angle1_1 = np.arccos((expected_sum_magnitude*np.cos(expected_sum_angle) - self.magnitude_array[1]*np.cos(angle2_1))/self.magnitude_array[0])
            angle1_2 = np.arccos((expected_sum_magnitude*np.cos(expected_sum_angle) - self.magnitude_array[1]*np.cos(angle2_2))/self.magnitude_array[0])

            x1: np.ndarray = np.array([self.magnitude_array[0]*np.cos(angle1_1), self.magnitude_array[1]*np.cos(angle2_1)])
            y1: np.ndarray = np.array([self.magnitude_array[0]*np.sin(angle1_1), self.magnitude_array[1]*np.sin(angle2_1)])
            x2: np.ndarray = np.array([self.magnitude_array[0]*np.cos(angle1_2), self.magnitude_array[1]*np.cos(angle2_2)])
            y2: np.ndarray = np.array([self.magnitude_array[0]*np.sin(angle1_2), self.magnitude_array[1]*np.sin(angle2_2)])
            angle1: np.ndarray = np.array([np.arctan2(y1[0], x1[0]), np.arctan2(y1[1], x1[1])])
            angle2: np.ndarray = np.array([np.arctan2(y2[0], x2[0]), np.arctan2(y2[1], x2[1])])

            self.check_sum1 = np.around(sum(self.vector_dict.values()) + np.array([x1[0], y1[0]]) + np.array([x1[1], y1[1]]), decimals =8)
            self.check_sum2 = np.around(sum(self.vector_dict.values()) + np.array([x2[0], y2[0]]) + np.array([x2[1], y2[1]]), decimals =8)

            if (self.check_sum1 == self.expected_resultant).all() and (self.check_sum2 != self.expected_resultant).all():
                self.vector_dict[vector1_name] = np.array([x1[0], y1[0]])
                self.vector_dict[vector2_name] = np.array([x1[1], y1[1]])
                self.quiver_dict[vector1_name] = self.plot.quiver(x1[0], y1[0], alpha=0.5, color="#008db9", scale=1, scale_units="xy", angles="xy")
                self.quiver_dict[vector2_name] = self.plot.quiver(x1[1], y1[1], alpha=0.5, color="#71daff", scale=1, scale_units="xy", angles="xy")
                self.tree.insert(self.tree_entries["missing"], "end", vector1_name, values=(vector1_name, f"{x1[0]: .6f}", f"{y1[0]: .6f}", f"{self.magnitude_array[0]: .6f}", f"{np.rad2deg(angle1[0]): .6f}"))
                self.tree.insert(self.tree_entries["missing"], "end", vector2_name, values=(vector2_name, f"{x1[1]: .6f}", f"{y1[1]: .6f}", f"{self.magnitude_array[1]: .6f}", f"{np.rad2deg(angle1[1]): .6f}"))
                self.tree.item(self.tree_entries["missing"], open=True)

            elif (self.check_sum2 == self.expected_resultant).all() and (self.check_sum1 != self.expected_resultant).all():
                self.vector_dict[vector1_name] = np.array([x2[0], y2[0]])
                self.vector_dict[vector2_name] = np.array([x2[1], y2[1]])
                self.quiver_dict[vector1_name] = self.plot.quiver(x2[0], y2[0], alpha=0.5, color="#cf4a49", scale=1, scale_units="xy", angles="xy")
                self.quiver_dict[vector2_name] = self.plot.quiver(x2[1], y2[1], alpha=0.5, color="#ff6666", scale=1, scale_units="xy", angles="xy")
                self.tree.insert(self.tree_entries["missing"], "end", vector1_name, values=(vector1_name, f"{x2[0]: .6f}", f"{y2[0]: .6f}", f"{self.magnitude_array[0]: .6f}", f"{np.rad2deg(angle2[0]): .6f}"))
                self.tree.insert(self.tree_entries["missing"], "end", vector2_name, values=(vector2_name, f"{x2[1]: .6f}", f"{y2[1]: .6f}", f"{self.magnitude_array[1]: .6f}", f"{np.rad2deg(angle2[1]): .6f}"))
                self.tree.item(self.tree_entries["missing"], open=True)

            elif (self.check_sum1 == self.expected_resultant).all() and (self.check_sum2 == self.expected_resultant).all():
                self.vector_dict[vector1_name] = np.array([x1[0], y1[0]])
                self.vector_dict[vector2_name] = np.array([x1[1], y1[1]])
                self.quiver_dict[vector1_name] = self.plot.quiver(x1[0], y1[0], alpha=0.5, color="#008db9", scale=1, scale_units="xy", angles="xy")
                self.quiver_dict[vector2_name] = self.plot.quiver(x1[1], y1[1], alpha=0.5, color="#71daff", scale=1, scale_units="xy", angles="xy")
                self.quiver_dict[vector1_name + " 2"] = self.plot.quiver(x2[0], y2[0], alpha=0.5, color="#cf4a49", scale=1, scale_units="xy", angles="xy")
                self.quiver_dict[vector2_name + " 2"] = self.plot.quiver(x2[1], y2[1], alpha=0.5, color="#ff6666", scale=1, scale_units="xy", angles="xy")
                self.tree.insert(self.tree_entries["missing"], "end", vector1_name, values=(vector1_name, f"{x1[0]: .6f}", f"{y1[0]: .6f}", f"{self.magnitude_array[0]: .6f}", f"{np.rad2deg(angle1[0]): .6f}"))
                self.tree.insert(self.tree_entries["missing"], "end", vector2_name, values=(vector2_name, f"{x1[1]: .6f}", f"{y1[1]: .6f}", f"{self.magnitude_array[1]: .6f}", f"{np.rad2deg(angle1[1]): .6f}"))
                self.tree.insert(self.tree_entries["Other Angle"], "end", vector1_name + " 2", values=(vector1_name, f"{x2[0]: .6f}", f"{y2[0]: .6f}", f"{self.magnitude_array[0]: .6f}", f"{np.rad2deg(angle2[0]): .6f}"))
                self.tree.insert(self.tree_entries["Other Angle"], "end", vector2_name + " 2", values=(vector2_name, f"{x2[1]: .6f}", f"{y2[1]: .6f}", f"{self.magnitude_array[1]: .6f}", f"{np.rad2deg(angle2[1]): .6f}"))
                self.tree.item(self.tree_entries["missing"], open=True)
                self.tree.item(self.tree_entries["Other Angle"], open=True)

        except RuntimeWarning:
            showerror("Error", "There is no valid solution!")
            self.is_noSolution = True

        return

    def get_expected_resultant(self) -> None:

        vector1_name = self.requirements_vars["v1_name"].get()
        vector2_name = self.requirements_vars["v2_name"].get()

        if self.auto_update.get():

            if vector1_name == "":

                showerror("Error", "Vector name is empty!")
                self.auto_update.set(0)
                self.vector1_name_entry.focus_set()
                return

            elif vector1_name in self.quiver_dict:

                showerror("Error", f"Vector \"{vector1_name}\" already exists!")
                self.auto_update.set(0)
                self.vector1_name_entry.focus_set()
                return

            elif vector2_name == "":

                showerror("Error", "Vector name is empty!")
                self.auto_update.set(0)
                self.vector2_name_entry.focus_set()
                return

            elif vector2_name in self.quiver_dict:

                showerror("Error", f"Vector \"{vector2_name}\" already exists!")
                self.auto_update.set(0)
                self.vector2_name_entry.focus_set()
                return

            elif vector1_name == vector2_name:

                showerror("Error", "Vector names must be different!")
                self.auto_update.set(0)
                self.vector1_name_entry.focus_set()
                return

            try:
                self.magnitude_array[0] = float(self.requirements_vars["v1_magnitude"].get())
            except ValueError:
                showerror("Error", "Value must be a valid decimal number!")
                self.auto_update.set(0)
                self.vector1_magnitude_entry.focus_set()
                return

            try:
                self.magnitude_array[1] = float(self.requirements_vars["v2_magnitude"].get())
            except ValueError:
                showerror("Error", "Value must be a valid decimal number!")
                self.auto_update.set(0)
                self.vector2_magnitude_entry.focus_set()
                return

            if self.missing_coordinate.get():

                try:
                    resultant_magnitude = float(self.requirements_vars["result_req1"].get())
                except ValueError:
                    showerror("Error", "Value must be a valid decimal number!")
                    self.auto_update.set(0)
                    self.resultant_req1_entry.focus_set()
                    return

                try:
                    resultant_angle = float(self.requirements_vars["result_req2"].get())
                except ValueError:
                    showerror("Error", "Value must be a valid decimal number!")
                    self.auto_update.set(0)
                    self.resultant_req2_entry.focus_set()
                    return

                resultant_x = resultant_magnitude * np.cos(np.radians(resultant_angle))
                resultant_y = resultant_magnitude * np.sin(np.radians(resultant_angle))

            else:

                try:
                    resultant_x = float(self.requirements_vars["result_req1"].get())
                except ValueError:
                    showerror("Error", "Value must be a valid decimal number!")
                    self.auto_update.set(0)
                    self.resultant_req1_entry.focus_set()
                    return

                try:
                    resultant_y = float(self.requirements_vars["result_req2"].get())
                except ValueError:
                    showerror("Error", "Value must be a valid decimal number!")
                    self.auto_update.set(0)
                    self.resultant_req2_entry.focus_set()
                    return

            self.vector1_name_entry.configure(state="disabled")
            self.vector1_magnitude_entry.configure(state="disabled")
            self.vector2_name_entry.configure(state="disabled")
            self.vector2_magnitude_entry.configure(state="disabled")
            self.resultant_req1_entry.configure(state="disabled")
            self.resultant_req2_entry.configure(state="disabled")
            self.cartesian.configure(state="disabled")
            self.polar.configure(state="disabled")

            self.vector_dict[vector1_name] = np.array([0, 0])
            self.vector_dict[vector2_name] = np.array([0, 0])
            self.quiver_dict[vector1_name] = self.plot.quiver(0, 0)
            self.quiver_dict[vector2_name] = self.plot.quiver(0, 0)
            self.tree.insert(self.tree_entries["missing"], "end", vector1_name, values=(vector1_name, 0, 0, 0, 0))
            self.tree.insert(self.tree_entries["missing"], "end", vector2_name, values=(vector2_name, 0, 0, 0, 0))
            self.expected_resultant = np.array([resultant_x, resultant_y])

            self.find_missing_directions()
            self.get_resultant()
            self.rescale_graph()

        else:

            self.vector1_name_entry.configure(state="enabled")
            self.vector1_magnitude_entry.configure(state="enabled")
            self.vector2_name_entry.configure(state="enabled")
            self.vector2_magnitude_entry.configure(state="enabled")
            self.resultant_req1_entry.configure(state="enabled")
            self.resultant_req2_entry.configure(state="enabled")
            self.cartesian.configure(state="enabled")
            self.polar.configure(state="enabled")

        return


def main():

    root = HdpiTk()
    root.title("VectorSim")
    root.minsize(300, 200)
    root.grid_columnconfigure(0, weight=1)

    ttk.Button(root, text="Resultant Vector", command=lambda: ResultantWindow(root)).grid(column=0, row=0, sticky="nsew", padx=10, pady=(10, 0))
    ttk.Button(root, text="One Missing Vector", command=lambda: OneMissingVector(root)).grid(column=0, row=1, sticky="nsew", padx=10)
    ttk.Button(root, text="Two Missing Magnitudes", command=lambda: TwoMissingMagnitudes(root)).grid(column=0, row=2, sticky="nsew", padx=10)
    ttk.Button(root, text="Two Missing Directions", command=lambda: TwoMissingDirections(root)).grid(column=0, row=3, sticky="nsew", padx=10)

    root.mainloop()
    return


if __name__ == "__main__":
    main()
