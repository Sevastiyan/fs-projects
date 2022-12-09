import customtkinter
import tkinter
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

from utils.data_loader import load_data, convert_signal
from utils.slice import slice_data
import os 

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green


def slider_callback(value):
    progressbar_1.set(value)


def move_slice(new_val):
    left_border.set_xdata(new_val)
    right_border.set_xdata(new_val + 200)

    ax2.set_xlim(new_val-20, new_val + 220)
    slider_callback(new_val)

    canvas.draw() #! required to update canvas and attached toolbar


def save_data_callback():
    x = int(slider_1.get())
    data_slice = signal[x:x+200]
    if len(data_slice) < 200: # Padding
        data_slice = np.resize(data_slice, (200))

    print(data_slice.shape) 
    results.append(data_slice)
    app.destroy()


def quit():
    save_file(results, 'incidents')



def save_file(data, filename):
    path = 'data/processed/'
    if not os.path.isdir(path):
        os.makedirs(path)

    with open(f"{path}/{filename}.txt", "w") as f: #! Careful with Append
        np.savetxt(f, data, fmt="%s", delimiter=" ")

    
# ----- Data Load -----
root = 'data/incidents/'
file_list = []
filenames = []
for file in os.listdir(root):
    if file in ['processed']: # Skip folders
        continue
    file_list.append(os.path.join(root, file))#.replace("\\","/")
    filenames.append(file)

    # for p, s, f in os.walk(os.path.join(root, subdir)):
    #     for filename in f: 
    #         file_list.append(os.path.join(root, subdir, filename).replace("\\","/"))
    #         filenames.append(filename)
            
print(file_list)
data = load_data(file_list)
results = []


# ----- Application UI ------
for i in range(len(data[:])): 
    print(f'--- Data {filenames[i]} ----- ')
    sample = data[i]
    signal = convert_signal(sample, type='acc_total')
    signal = signal.to_numpy()
    print(signal.shape)

    # sliced = slice_data(signal, [50, 250])
    # print(sliced)

    # --- Create Figure ---
    fig, (ax1, ax2) = plt.subplots(2)
    t = [x for x in range(signal.shape[0])] #np.arange(0, 30, .01)

    line, = ax1.plot(t, signal)
    print(max(line.get_data()[1]))

    borders = [len(t)/2, len(t)/2 + 200]
    left_border = ax1.axvline(borders[0], color='r')
    right_border = ax1.axvline(borders[1], color='r')

    line2, = ax2.plot(t, signal)
    ax2.set_xlabel("time [s]")
    ax1.set_ylabel("f(t)")

    # --- Main App ---
    app = customtkinter.CTk()
    app.geometry("600x800")
    app.title(f"CustomTkinter {filenames[i]}.py")

    canvas = FigureCanvasTkAgg(fig, master=app) 
    canvas.draw()
    canvas.mpl_connect("key_press_event", key_press_handler)
    button_skip = customtkinter.CTkButton(master=app, text="Skip", command=app.destroy)
    button_skip.pack(side=tkinter.BOTTOM)

    # Packing order is important. Widgets are processed sequentially and if there
    # is no space left, because the window is too small, they are not displayed.
    # The canvas is rather flexible in its size, so we pack it last which makes
    # sure the UI controls are displayed as long as possible.

    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)

    frame_1 = customtkinter.CTkFrame(master=app)
    frame_1.pack(pady=20, padx=60, fill="both", expand=True)

    label_1 = customtkinter.CTkLabel(master=frame_1, justify=tkinter.LEFT)
    label_1.pack(pady=12, padx=10)

    progressbar_1 = customtkinter.CTkProgressBar(master=frame_1)
    progressbar_1.pack(pady=12, padx=10)

    slider_1 = customtkinter.CTkSlider(master=frame_1, command=move_slice, from_=t[0], to=t[-1])
    slider_1.pack(pady=12, padx=10)
    slider_1.set(len(t)/2)

    button_save_slice = customtkinter.CTkButton(master=frame_1, text="Save", command=save_data_callback)
    button_save_slice.pack(side=tkinter.BOTTOM)

    app.mainloop()

save_file(results, 'incidents')
