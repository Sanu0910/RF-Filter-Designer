import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Entry, Button, StringVar, OptionMenu

# Filter design function
def design_filter(filter_type, order, cutoff, f_type, fs=1e9):
    nyquist = fs / 2
    normalized_cutoff = np.array(cutoff) / nyquist
    
    if filter_type == "butterworth":
        b, a = signal.butter(order, normalized_cutoff, btype=f_type)
    elif filter_type == "chebyshev1":
        b, a = signal.cheby1(order, 0.5, normalized_cutoff, btype=f_type)
    elif filter_type == "chebyshev2":
        b, a = signal.cheby2(order, 20, normalized_cutoff, btype=f_type)
    elif filter_type == "elliptic":
        b, a = signal.ellip(order, 0.5, 20, normalized_cutoff, btype=f_type)
    else:
        raise ValueError("Invalid filter type")
    
    return b, a

# Plot function
def plot_response(b, a, fs):
    w, h = signal.freqz(b, a, worN=2000)
    freq = (w / np.pi) * (fs / 2)
    
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.plot(freq, 20 * np.log10(abs(h)))
    plt.title("Magnitude Response")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude (dB)")
    plt.grid()
    
    plt.subplot(1, 2, 2)
    plt.plot(freq, np.angle(h, deg=True))
    plt.title("Phase Response")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Phase (Degrees)")
    plt.grid()
    
    plt.show()

# GUI Setup
def run_gui():
    root = Tk()
    root.title("RF Filter Designer")
    
    Label(root, text="Filter Type").grid(row=0, column=0)
    Label(root, text="Order").grid(row=1, column=0)
    Label(root, text="Cutoff Frequency (Hz)").grid(row=2, column=0)
    Label(root, text="Filter Mode").grid(row=3, column=0)
    
    filter_types = ["butterworth", "chebyshev1", "chebyshev2", "elliptic"]
    filter_modes = ["lowpass", "highpass", "bandpass", "bandstop"]
    
    f_type_var = StringVar(root)
    f_type_var.set(filter_types[0])
    mode_var = StringVar(root)
    mode_var.set(filter_modes[0])
    
    type_menu = OptionMenu(root, f_type_var, *filter_types)
    type_menu.grid(row=0, column=1)
    
    order_entry = Entry(root)
    order_entry.grid(row=1, column=1)
    
    cutoff_entry = Entry(root)
    cutoff_entry.grid(row=2, column=1)
    
    mode_menu = OptionMenu(root, mode_var, *filter_modes)
    mode_menu.grid(row=3, column=1)
    
    def on_submit():
        filter_type = f_type_var.get()
        order = int(order_entry.get())
        cutoff = list(map(float, cutoff_entry.get().split(',')))
        mode = mode_var.get()
        
        b, a = design_filter(filter_type, order, cutoff, mode)
        plot_response(b, a, fs=1e9)
    
    Button(root, text="Design Filter", command=on_submit).grid(row=4, columnspan=2)
    
    root.mainloop()

if __name__ == "__main__":
    run_gui()
