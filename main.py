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


class BaseWindow(tk.Toplevel):

    """
    Base window for each case with a control panel, table, resultant, and graphing plane.
    """

    def __init__(self, master: tk.Tk, min_width: int = 1500, min_height: int = 900) -> None:

        super().__init__(master=master)
        self.title("VectorSim")
        self.minsize(min_width, min_height)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=3)
        self.grid_rowconfigure(0, weight=1)

        self.vector_vars: dict[str, tk.StringVar] = {"name": tk.StringVar(self), "req1": tk.StringVar(self), "req2": tk.StringVar(self)}
        self.coordinate: tk.IntVar = tk.IntVar(self, value=0)
        self.vector_dict: dict[str, np.ndarray] = {}
        self.quiver_dict: dict[str, Quiver] = {}
        self.resultant_vct: np.ndarray = np.array([0, 0])
        self.resultant_vars: dict[str, tk.StringVar] = {"x": tk.StringVar(self, "0.0000"), "y": tk.StringVar(self, "0.0000"), "r": tk.StringVar(self, "0.0000"), "theta": tk.StringVar(self, "0.0000")}

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

        self.name_entry = ttk.Entry(self.vector_frame, textvariable=self.vector_vars["name"])
        self.name_entry.grid(column=1, row=0, columnspan=3, sticky="new", padx=10)
        self.req1_entry = ttk.Entry(self.vector_frame, textvariable=self.vector_vars["req1"])
        self.req1_entry.grid(column=1, row=1, sticky="ew", padx=10, pady=10)
        self.req2_entry = ttk.Entry(self.vector_frame, textvariable=self.vector_vars["req2"])
        self.req2_entry.grid(column=3, row=1, sticky="ew", padx=10, pady=10)

        ttk.Radiobutton(self.vector_frame, text="X and Y components", variable=self.coordinate, value=0).grid(column=0, row=2, columnspan=2, sticky="ew", padx=10, pady=10)
        ttk.Radiobutton(self.vector_frame, text="Magnitude and Direction", variable=self.coordinate, value=1).grid(column=2, row=2, columnspan=2, sticky="ew", padx=10, pady=10)
        self.add_vector_button = ttk.Button(self.vector_frame, text="Add vector")
        self.add_vector_button.grid(column=0, row=3, columnspan=4, sticky="ew", padx=10, pady=5)
        self.remove_vector_button = ttk.Button(self.vector_frame, text="Remove vector")
        self.remove_vector_button.grid(column=0, row=4, columnspan=4, sticky="ew", padx=10, pady=5)
        self.clear_all_button = ttk.Button(self.vector_frame, text="Clear all vectors")
        self.clear_all_button.grid(column=0, row=5, columnspan=4, sticky="ew", padx=10, pady=(5, 10))

        self.tree = ttk.Treeview(master=self, columns=("name", "x", "y", "rm", "r_theta"), show="headings")
        self.tree.grid(column=1, row=0, sticky="nsew")
        self.tree.column("name", width=50)
        self.tree.column("x", width=70)
        self.tree.column("y", width=70)
        self.tree.column("rm", width=70)
        self.tree.column("r_theta", width=70)
        self.tree.heading("name", text="Name")
        self.tree.heading("x", text="X")
        self.tree.heading("y", text="Y")
        self.tree.heading("rm", text="R")
        self.tree.heading("r_theta", text="\u03B8")

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
        ttk.Label(self.resultant_canvas, textvariable=self.resultant_vars["x"]).grid(column=1, row=0, sticky="nsw", pady=10)
        ttk.Label(self.resultant_canvas, textvariable=self.resultant_vars["y"]).grid(column=3, row=0, sticky="nsw", pady=10)
        ttk.Label(self.resultant_canvas, textvariable=self.resultant_vars["r"]).grid(column=5, row=0, sticky="nsw", pady=10)
        ttk.Label(self.resultant_canvas, textvariable=self.resultant_vars["theta"]).grid(column=7, row=0, sticky="nsw", pady=10)

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

        if len(selected):

            for name in selected:
                self.vector_dict.pop(name)
                self.quiver_dict.pop(name).remove()
                self.tree.delete(name)

            self.get_resultant()
            self.rescale_graph()

        else:

            showerror("Error", "No vector selected on the table!")

        return

    def get_resultant(self) -> None:
        """
        Get the resultant of the vectors listed on the table
        """
        self.resultant_vct = sum(self.vector_dict.values()) if len(self.vector_dict) else np.array([0, 0])  # type: ignore
        self.resultant_vars["x"].set(value=f"{self.resultant_vct[0]: .4f}")  # type: ignore
        self.resultant_vars["y"].set(value=f"{self.resultant_vct[1]: .4f}")  # type: ignore
        self.resultant_vars["r"].set(value=f"{np.hypot(*self.resultant_vct): .4f}")
        self.resultant_vars["theta"].set(value=f"{np.rad2deg(np.arctan2(self.resultant_vct[1], self.resultant_vct[0])): .4f}")  # type: ignore
        self.resultant_plot.remove()
        self.resultant_plot = self.plot.quiver(*self.resultant_vct, color="black", scale=1, scale_units="xy", angles="xy")  # type: ignore
        return

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


class OneMissingVector(BaseWindow):

    """
    Window Class for finding one vector with missing angle and magnitude.
    """
    def __init__(self, master: tk.Tk, min_width: int = 1500, min_height: int = 900) -> None:

        super().__init__(master, min_width, min_height)

        self.missing_vector_frame = ttk.LabelFrame(master=self.control_panel, text="One Missing Vector (Red)")
        self.missing_vector_frame.grid(column=0, row=2, sticky="new", padx=10, pady=10)
        self.missing_vector_frame.grid_columnconfigure(0, weight=1)
        self.missing_vector_frame.grid_columnconfigure(1, weight=3)
        self.missing_vector_frame.grid_columnconfigure(2, weight=1)
        self.missing_vector_frame.grid_columnconfigure(3, weight=3)

        self.expected_resultant_vars: dict[str, tk.StringVar] = {"name": tk.StringVar(self), "req1": tk.StringVar(self), "req2": tk.StringVar(self)}
        self.expected_resultant_coordinate: tk.IntVar = tk.IntVar(self, value=0)
        self.missing_vector_vars: dict[str, tk.StringVar] = {"x": tk.StringVar(self), "y": tk.StringVar(self), "r": tk.StringVar(self), "theta": tk.StringVar(self)}
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
        vector_name = self.vector_vars["name"].get()

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
                r = float(self.vector_vars["req1"].get())
            except ValueError:
                showerror("Error", "Value must be a valid decimal number!")
                self.req1_entry.focus_set()
                return

            try:
                theta = float(self.vector_vars["req2"].get())
            except ValueError:
                showerror("Error", "Value must be a valid decimal number!")
                self.req2_entry.focus_set()
                return

            x = r * np.cos(np.radians(theta))
            y = r * np.sin(np.radians(theta))

        else:

            try:
                x = float(self.vector_vars["req1"].get())
            except ValueError:
                showerror("Error", "Value must be a valid decimal number!")
                self.req1_entry.focus_set()
                return

            try:
                y = float(self.vector_vars["req2"].get())
            except ValueError:
                showerror("Error", "Value must be a valid decimal number!")
                self.req2_entry.focus_set()
                return

            r = np.hypot(x, y)
            theta_rad = np.arctan2(y, x)
            theta = np.rad2deg(theta_rad)

        self.vector_dict[vector_name] = np.array([x, y])
        self.quiver_dict[vector_name] = self.plot.quiver(x, y, alpha=0.5, color="g", scale=1, scale_units="xy", angles="xy")
        self.tree.insert("", "end", vector_name, values=(vector_name, f"{x: .6f}", f"{y: .6f}", f"{r: .6f}", f"{theta: .6f}"))

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
        self.tree.delete(*self.tree.get_children())
        self.expected_resultant: np.ndarray = np.array([0, 0])
        for i in self.vector_vars.values():
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

        missing_vector: np.ndarray = self.expected_resultant - sum(self.vector_dict.values())
        x, y = missing_vector[0], missing_vector[1]
        magnitude = np.hypot(x, y)
        direction = np.rad2deg(np.arctan2(y, x))
        self.vector_dict[vector_name] = missing_vector
        self.quiver_dict[vector_name] = self.plot.quiver(x, y, alpha=0.5, color="r", scale=1, scale_units="xy", angles="xy")
        self.tree.insert("", "end", vector_name, values=(vector_name, f"{x: .6f}", f"{y: .6f}", f"{magnitude: .6f}", f"{direction: .6f}"))
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
            self.tree.insert("", "end", vector_name, values=(vector_name, 0, 0, 0, 0))
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

    def __init__(self, master: tk.Tk, min_width: int = 1500, min_height: int = 900) -> None:

        super().__init__(master, min_width, min_height)

        self.vector1_name_var = tk.StringVar(self)
        self.vector2_name_var = tk.StringVar(self)
        self.vector1_angle_var = tk.StringVar(self)
        self.vector2_angle_var = tk.StringVar(self)
        self.resultant_req1_var = tk.StringVar(self)
        self.resultant_req2_var = tk.StringVar(self)
        self.missing_coordinate = tk.IntVar(self, value=0)

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

        self.vector1_name_entry = ttk.Entry(self.missing_magnitudes_frame, textvariable=self.vector1_name_var)
        self.vector1_name_entry.grid(column=1, row=1, sticky="new", padx=10, pady=(3, 0))
        self.vector1_angle_entry = ttk.Entry(self.missing_magnitudes_frame, textvariable=self.vector1_angle_var)
        self.vector1_angle_entry.grid(column=3, row=1, sticky="new", padx=10, pady=(3, 13))
        self.vector2_name_entry = ttk.Entry(self.missing_magnitudes_frame, textvariable=self.vector2_name_var)
        self.vector2_name_entry.grid(column=1, row=3, sticky="new", padx=10)
        self.vector2_angle_entry = ttk.Entry(self.missing_magnitudes_frame, textvariable=self.vector2_angle_var)
        self.vector2_angle_entry.grid(column=3, row=3, sticky="new", padx=10, pady=(3, 13))
        self.resultant_req1_entry = ttk.Entry(self.missing_magnitudes_frame, textvariable=self.resultant_req1_var)
        self.resultant_req1_entry.grid(column=1, row=5, sticky="new", padx=10)
        self.resultant_req2_entry = ttk.Entry(self.missing_magnitudes_frame, textvariable=self.resultant_req2_var)
        self.resultant_req2_entry.grid(column=3, row=5, sticky="new", padx=10, pady=(3, 13))

        ttk.Radiobutton(self.missing_magnitudes_frame, text="X and Y components", variable=self.missing_coordinate, value=0).grid(column=0, row=6, columnspan=2, sticky="ew", padx=10, pady=10)
        ttk.Radiobutton(self.missing_magnitudes_frame, text="Magnitude and Direction", variable=self.missing_coordinate, value=1).grid(column=2, row=6, columnspan=2, sticky="ew", padx=10, pady=10)
        ttk.Button(self.missing_magnitudes_frame, text="Find Missing Magnitudes", command=self.find_two_missing_magnitudes).grid(column=0, row=7, columnspan=4, sticky="ew", padx=10, pady=10)

        self.add_vector_button.configure(command=self.add_vector)
        return

    def add_vector(self) -> None:
        """
        Add a vector to the table with a unique name and plot the vector into the plane.
        """
        vector_name = self.vector_vars["name"].get()

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
                r = float(self.vector_vars["req1"].get())
            except ValueError:
                showerror("Error", "Value must be a valid decimal number!")
                self.req1_entry.focus_set()
                return

            try:
                theta = float(self.vector_vars["req2"].get())
            except ValueError:
                showerror("Error", "Value must be a valid decimal number!")
                self.req2_entry.focus_set()
                return

            x = r * np.cos(np.radians(theta))
            y = r * np.sin(np.radians(theta))

        else:

            try:
                x = float(self.vector_vars["req1"].get())
            except ValueError:
                showerror("Error", "Value must be a valid decimal number!")
                self.req1_entry.focus_set()
                return

            try:
                y = float(self.vector_vars["req2"].get())
            except ValueError:
                showerror("Error", "Value must be a valid decimal number!")
                self.req2_entry.focus_set()
                return

            r = np.hypot(x, y)
            theta_rad = np.arctan2(y, x)
            theta = np.rad2deg(theta_rad)

        self.vector_dict[vector_name] = np.array([x, y])
        self.quiver_dict[vector_name] = self.plot.quiver(x, y, alpha=0.5, color="g", scale=1, scale_units="xy", angles="xy")
        self.tree.insert("", "end", vector_name, values=(vector_name, f"{x: .6f}", f"{y: .6f}", f"{r: .6f}", f"{theta: .6f}"))

        self.get_resultant()
        self.rescale_graph()

        return

    def find_two_missing_magnitudes(self) -> None:

        vector1_name = self.vector1_name_var.get()
        vector2_name = self.vector2_name_var.get()
        angle_array = np.array([0, 0])
        sum_vectors = sum(self.vector_dict.values()) if len(self.vector_dict) else np.array([0, 0])

        if vector1_name == "":

            showerror("Error", "Vector name is empty!")
            self.vector1_name_entry.focus_set()
            return

        elif vector1_name in self.quiver_dict:

            showerror("Error", f"Vector \"{vector1_name}\" already exists!")
            self.vector1_name_entry.focus_set()
            return

        elif vector2_name == "":

            showerror("Error", "Vector name is empty!")
            self.vector2_name_entry.focus_set()
            return

        elif vector2_name in self.quiver_dict:

            showerror("Error", f"Vector \"{vector2_name}\" already exists!")
            self.vector2_name_entry.focus_set()
            return

        elif vector1_name == vector2_name:

            showerror("Error", "Vector names must be different!")
            self.vector1_angle_entry.focus_set()
            return

        elif self.missing_coordinate.get():

            try:
                angle_array[0] = float(self.vector1_angle_var.get())
            except ValueError:
                showerror("Error", "Value must be a valid decimal number!")
                self.vector1_angle_entry.focus_set()
                return

            try:
                angle_array[1] = float(self.vector2_angle_var.get())
            except ValueError:
                showerror("Error", "Value must be a valid decimal number!")
                self.vector2_angle_entry.focus_set()
                return

            try:
                resultant_magnitude = float(self.resultant_req1_var.get())
            except ValueError:
                showerror("Error", "Value must be a valid decimal number!")
                self.resultant_req1_entry.focus_set()
                return

            try:
                resultant_angle = float(self.resultant_req2_var.get())
            except ValueError:
                showerror("Error", "Value must be a valid decimal number!")
                self.resultant_req2_entry.focus_set()
                return

            inverted_matrix = np.linalg.inv(np.array([np.cos(np.radians(angle_array)), np.sin(np.radians(angle_array))]))
            magnitudes = np.dot(inverted_matrix, np.array([resultant_magnitude * np.cos(np.radians(resultant_angle)), resultant_magnitude * np.sin(np.radians(resultant_angle))]) - sum_vectors)

            x = magnitudes * np.cos(np.radians(angle_array))
            y = magnitudes * np.sin(np.radians(angle_array))

        else:

            try:
                angle_array[0] = float(self.vector1_angle_var.get())
            except ValueError:
                showerror("Error", "Value must be a valid decimal number!")
                self.vector1_angle_entry.focus_set()
                return

            try:
                angle_array[1] = float(self.vector2_angle_var.get())
            except ValueError:
                showerror("Error", "Value must be a valid decimal number!")
                self.vector2_angle_entry.focus_set()
                return

            try:
                resultant_x = float(self.resultant_req1_var.get())
            except ValueError:
                showerror("Error", "Value must be a valid decimal number!")
                self.resultant_req1_entry.focus_set()
                return

            try:
                resultant_y = float(self.resultant_req2_var.get())
            except ValueError:
                showerror("Error", "Value must be a valid decimal number!")
                self.resultant_req2_entry.focus_set()
                return

            inverted_matrix = np.linalg.inv(np.array([np.cos(np.radians(angle_array)), np.sin(np.radians(angle_array))]))
            magnitudes = np.dot(inverted_matrix, np.array([resultant_x, resultant_y]) - sum_vectors)

            x = magnitudes * np.cos(np.radians(angle_array))
            y = magnitudes * np.sin(np.radians(angle_array))

        self.vector_dict[vector1_name] = np.array([x[0], y[0]])
        self.vector_dict[vector2_name] = np.array([x[1], y[1]])
        self.quiver_dict[vector1_name] = self.plot.quiver(x[0], y[0], alpha=0.5, color="b", scale=1, scale_units="xy", angles="xy")
        self.quiver_dict[vector2_name] = self.plot.quiver(x[1], y[1], alpha=0.5, color="b", scale=1, scale_units="xy", angles="xy")
        self.tree.insert("", "end", values=(vector1_name, "%.6f" % x[0], "%.6f" % y[0], "%.6f" % magnitudes[0], "%.6f" % angle_array[0]))
        self.tree.insert("", "end", values=(vector2_name, "%.6f" % x[1], "%.6f" % y[1], "%.6f" % magnitudes[1], "%.6f" % angle_array[1]))

        self.get_resultant()
        self.rescale_graph()
        return


def main():

    root = HdpiTk()
    root.title("VectorSim")
    root.minsize(300, 100)
    root.grid_columnconfigure(0, weight=1)

    ttk.Button(root, text="Case 1", command=lambda: OneMissingVector(root)).grid(column=0, row=0, sticky="nsew", padx=10, pady=(10, 0))
    ttk.Button(root, text="Case 2", command=lambda: TwoMissingMagnitudes(root)).grid(column=0, row=1, sticky="nsew", padx=10)
    ttk.Button(root, text="Case 3").grid(column=0, row=2, sticky="nsew", padx=10)

    root.mainloop()
    return


if __name__ == "__main__":
    main()
