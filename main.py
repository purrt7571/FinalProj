import numpy as np
import tkinter as tk
import tkinter.ttk as ttk
from hdpitkinter import HdpiTk
from matplotlib.figure import Figure
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter.messagebox import showerror

class ConfirmationPrompt(tk.Toplevel):

    def __init__(self, master: tk.Tk, msg: str, useTextbox: bool = False, confirmButtonText: str = "OK", cancelButtonText: str = "Cancel"):

        super().__init__(master = master)
        self.title("Confirm")
        self.geometry("300x100")
        self.grid_columnconfigure(0, weight = 2)
        self.grid_columnconfigure(1, weight = 0)
        self.grid_columnconfigure(2, weight = 0)
        self.prompt_status = tk.IntVar(self)
        ttk.Label(self, text = msg).grid(column = 0, row = 0, columnspan = 3, sticky = "w", padx = 10, pady = (10,5))

        if useTextbox:
            prompt_namevar = tk.StringVar(self)
            ttk.Entry(self, textvariable = prompt_namevar).grid(column = 0, row = 1, columnspan = 3, sticky = "ew", padx = 10, pady = (0,5))

        ttk.Button(self, text = confirmButtonText, command = self.confirm).grid(column = 1, row = 2, sticky = "e", pady = 10)
        ttk.Button(self, text = cancelButtonText, command = self.cancel).grid(column = 2, row = 2, sticky = "e", padx = 5, pady = 10)

    def confirm(self):
        pass

    def cancel(self):
        pass

    def close(self):
        self.destroy()

class BaseWindow(tk.Toplevel):
    
    def __init__(self, master: tk.Tk, minwidth: int = 1500, minheight: int = 900) -> None:
        super().__init__(master = master)
        self.title("VectorSim")
        self.minsize(minwidth, minheight)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=3)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)

        self.resultant_vct: np.ndarray = np.array([0,0])
        self.resultant_xvar: tk.StringVar = tk.StringVar(self, "0.0000")
        self.resultant_yvar: tk.StringVar = tk.StringVar(self, "0.0000")
        self.resultant_rvar: tk.StringVar = tk.StringVar(self, "0.0000")
        self.resultant_thetavar: tk.StringVar = tk.StringVar(self, "0.0000")
        self.resultant_plot: None = None

        self.Base_Widgets()
        self.protocol("WM_DELETE_WINDOW", self.close)
        return
    
    def Base_Widgets(self) -> None:
        self.control_panel = tk.Frame(self)
        self.control_panel.grid(column = 0, row = 0, rowspan = 2, sticky = "nsew")
        self.control_panel.grid_columnconfigure(0, weight = 1)

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
        return
    
    def close(self) -> None:
        self.canvas.close_event()
        self.destroy()
        return

def build_case1():
    global root, active_windows
    active_windows["win1"] = BaseWindow(root)

root = HdpiTk()
root.grid_columnconfigure(0, weight = 1)

active_windows: dict[str, tk.Toplevel] = {}

prompt_askName = ConfirmationPrompt(root, "Enter window name:", useTextbox = True)
prompt_askName.withdraw()

""" prompt_namewindow = tk.Toplevel(root)
prompt_namewindow.grid_columnconfigure(0, weight=1)
prompt_namevar = tk.StringVar(prompt_namewindow)
ttk.Label(prompt_namewindow, text="Enter the window name: ").grid(column = 0, row = 0, padx = 10, pady = (10,3))
prompt_nameentry = ttk.Entry(prompt_namewindow, textvariable = prompt_namevar)
prompt_nameentry.grid(column = 0, row = 1, sticky = "ew", padx = 10, pady = (0,10)) """

case1_button = ttk.Button(root, text = "Case 1", command = build_case1)
case1_button.grid(column = 0, row = 0, sticky = "nsew")

root.mainloop()