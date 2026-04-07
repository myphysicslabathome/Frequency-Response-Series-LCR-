''' Program for the frequency response of series LCR Circuit
    This simulation will give the frequency response curve and the extraced parameters for a given set of L, C and R
    Date: 07_04_2026 by Dr. Ujjwal Ghanta
'''


import tkinter as tk
from tkinter import ttk
import numpy as np
import math
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

# ======================================================
# GUI INITIALIZATION
# ======================================================
root = tk.Tk()
root.title("Series LCR Frequency Response – Virtual Instrument")
root.geometry("1300x720")
root.minsize(1150, 650)

# ======================================================
# PROFESSIONAL LIGHT THEME (FIXED)
# ======================================================
style = ttk.Style()
style.theme_use("clam")

style.configure(".", background="#f4f6f8", foreground="#1f2933")
style.configure("TFrame", background="#f4f6f8")
style.configure("TLabelframe", background="#f4f6f8")
style.configure("TLabelframe.Label",
                background="#f4f6f8",
                foreground="#1f2933",
                font=("Segoe UI", 10, "bold"))
style.configure("TLabel", background="#f4f6f8", foreground="#1f2933")
style.configure("TEntry", padding=5)
style.configure("TButton",
                background="#2563eb",
                foreground="white",
                font=("Segoe UI", 10, "bold"),
                padding=(10, 6))
style.map("TButton", background=[("active", "#1d4ed8")])
style.configure("Instrument.TLabel",
                background="#eef2f7",
                foreground="#111827",
                font=("Consolas", 10),
                padding=6,
                relief="solid")

# ======================================================
# SCROLLABLE LEFT PANEL
# ======================================================
left_container = ttk.Frame(root)
left_container.pack(side=tk.LEFT, fill=tk.Y)

canvas_left = tk.Canvas(left_container, width=360, highlightthickness=0)
scrollbar = ttk.Scrollbar(left_container, orient="vertical",
                          command=canvas_left.yview)
left = ttk.Frame(canvas_left)

left.bind("<Configure>",
          lambda e: canvas_left.configure(scrollregion=canvas_left.bbox("all")))

canvas_left.create_window((0, 0), window=left, anchor="nw")
canvas_left.configure(yscrollcommand=scrollbar.set)

canvas_left.pack(side=tk.LEFT, fill=tk.Y, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas_left.bind_all("<MouseWheel>",
                     lambda e: canvas_left.yview_scroll(
                         int(-1*(e.delta/120)), "units"))

# ======================================================
# RIGHT PANEL (GRAPH)
# ======================================================
right = ttk.Frame(root)
right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# ======================================================
# INPUT PARAMETERS
# ======================================================
inp = ttk.LabelFrame(left, text="Circuit Parameters", padding=10)
inp.pack(fill=tk.X, pady=5)

labels = ["L (mH)", "C (µF)", "Series R (Ω)", "Test R (Ω)",
          "Vp (V)", "f start (Hz)", "f end (Hz)"]

entries = []
for i, txt in enumerate(labels):
    ttk.Label(inp, text=txt).grid(row=i, column=0, sticky="w", pady=3)
    e = ttk.Entry(inp, width=14)
    e.grid(row=i, column=1, pady=3)
    entries.append(e)

(ent_L, ent_C, ent_R, ent_Rtest,
 ent_Vp, ent_fstart, ent_fend) = entries

ent_L.insert(0, "10")
ent_C.insert(0, "0.01")
ent_R.insert(0, "100")
ent_Rtest.insert(0, "56")
ent_Vp.insert(0, "1")
ent_fstart.insert(0, "1000")
ent_fend.insert(0, "100000")

# ======================================================
# PLOT OPTIONS
# ======================================================
scale_var = tk.StringVar(value="log")

ttk.Label(inp, text="Plot Scale").grid(row=7, column=0, sticky="w")
ttk.Radiobutton(inp, text="Log", variable=scale_var,
                value="log").grid(row=7, column=1, sticky="w")
ttk.Radiobutton(inp, text="Linear", variable=scale_var,
                value="linear").grid(row=8, column=1, sticky="w")

ttk.Button(inp, text="Add Plot",
           command=lambda: calculate_and_plot()).grid(row=9, column=0, pady=8)
ttk.Button(inp, text="Clear Graph",
           command=lambda: clear_plot()).grid(row=9, column=1, pady=8)

# ======================================================
# ANALYSIS & CURSOR
# ======================================================
res = ttk.LabelFrame(left, text="Automatic Analysis", padding=10)
res.pack(fill=tk.X, pady=5)

result_text = tk.StringVar()
ttk.Label(res, textvariable=result_text,
          style="Instrument.TLabel",
          justify="left").pack(fill=tk.X)

cursor_frame = ttk.LabelFrame(left, text="Cursor Readout", padding=10)
cursor_frame.pack(fill=tk.X, pady=5)

cursor_var = tk.StringVar(value="Move mouse over graph")
ttk.Label(cursor_frame, textvariable=cursor_var,
          style="Instrument.TLabel").pack(fill=tk.X)

# ======================================================
# AXIS SCALING
# ======================================================
axis_frame = ttk.LabelFrame(left, text="Axis Scaling", padding=10)
axis_frame.pack(fill=tk.X, pady=5)

xscale_var = tk.StringVar(value="auto")
yscale_var = tk.StringVar(value="auto")

ttk.Label(axis_frame, text="X-axis").grid(row=0, column=0, sticky="w")
ttk.Radiobutton(axis_frame, text="Auto", variable=xscale_var,
                value="auto", command=lambda: apply_axis_limits()).grid(row=0, column=1)
ttk.Radiobutton(axis_frame, text="Manual", variable=xscale_var,
                value="manual").grid(row=0, column=2)

ent_xmin = ttk.Entry(axis_frame, width=8)
ent_xmax = ttk.Entry(axis_frame, width=8)
ent_xmin.insert(0, "1000")
ent_xmax.insert(0, "100000")
ent_xmin.grid(row=1, column=1)
ent_xmax.grid(row=1, column=2)
ttk.Label(axis_frame, text="Min / Max (Hz)").grid(row=1, column=0, sticky="w")

ttk.Label(axis_frame, text="Y-axis").grid(row=2, column=0, sticky="w")
ttk.Radiobutton(axis_frame, text="Auto", variable=yscale_var,
                value="auto", command=lambda: apply_axis_limits()).grid(row=2, column=1)
ttk.Radiobutton(axis_frame, text="Manual", variable=yscale_var,
                value="manual").grid(row=2, column=2)

ent_ymin = ttk.Entry(axis_frame, width=8)
ent_ymax = ttk.Entry(axis_frame, width=8)
ent_ymin.insert(0, "0")
ent_ymax.insert(0, "20")
ent_ymin.grid(row=3, column=1)
ent_ymax.grid(row=3, column=2)
ttk.Label(axis_frame, text="Min / Max (mA)").grid(row=3, column=0, sticky="w")

ttk.Button(axis_frame, text="Apply Axis Limits",
           command=lambda: apply_axis_limits()).grid(row=4, column=0,
                                                     columnspan=3, pady=6)

# ======================================================
# PLOT SETUP
# ======================================================
fig = Figure(figsize=(7, 6), dpi=100)
ax = fig.add_subplot(111)

def style_axes():
    ax.set_title("Series LCR Frequency Response")
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Current (mA)")
    ax.grid(True, which="both", linestyle="--", alpha=0.6)

style_axes()

canvas = FigureCanvasTkAgg(fig, master=right)
canvas.draw()
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

toolbar = NavigationToolbar2Tk(canvas, right)
toolbar.update()

# ======================================================
# FUNCTIONS
# ======================================================
def on_mouse_move(event):
    if event.inaxes:
        cursor_var.set(
            f"Cursor → f = {event.xdata:.1f} Hz , I = {event.ydata:.3f} mA")

def extract_Q(f, I):
    Imax = np.max(I)
    Ihp = Imax / math.sqrt(2)
    idx = np.where(I >= Ihp)[0]
    if len(idx) < 2:
        return None
    fL, fH = f[idx[0]], f[idx[-1]]
    f0 = f[np.argmax(I)]
    return f0, fL, fH, f0 / (fH - fL)

def apply_axis_limits():
    try:
        if xscale_var.get() == "manual":
            ax.set_xlim(float(ent_xmin.get()), float(ent_xmax.get()))
        else:
            ax.autoscale(axis="x")
        if yscale_var.get() == "manual":
            ax.set_ylim(float(ent_ymin.get()), float(ent_ymax.get()))
        else:
            ax.autoscale(axis="y")
        canvas.draw()
    except:
        pass

def calculate_and_plot():
    L = float(ent_L.get()) * 1e-3
    C = float(ent_C.get()) * 1e-6
    #R = float(ent_R.get()) + float(ent_Rtest.get())
    Rb = float(ent_R.get())
    Rt = float(ent_Rtest.get())
    R = Rb + Rt
    
    Vp = float(ent_Vp.get())
    f = np.logspace(np.log10(float(ent_fstart.get())),
                    np.log10(float(ent_fend.get())), 2000)
    w = 2*np.pi*f
    I = (Vp / np.sqrt(R**2 + (w*L - 1/(w*C))**2))*1000

    if scale_var.get() == "log":
        ax.semilogx(f, I, linewidth=2, label=f"R = {Rb:.0f}Ω + {Rt:.0f}Ω")
    else:
        ax.plot(f, I, linewidth=2, label=f"R = {Rb:.0f}Ω + {Rt:.0f}Ω")

    q = extract_Q(f, I)
    if q:
        f0, fL, fH, Q = q
        result_text.set(f"f₀ = {f0/1000:.3f} kHz\nQ = {Q:.2f}\nfL = {fL/1000:.3f} kHz\nfH = {fH/1000:.3f} kHz")
         
    ax.legend()
    apply_axis_limits()
    canvas.draw()

def clear_plot():
    ax.clear()
    style_axes()
    ax.autoscale()
    result_text.set("")
    canvas.draw()

canvas.mpl_connect("motion_notify_event", on_mouse_move)

# ======================================================
root.mainloop()


