import customtkinter
import tkinter
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

from utils.data_loader import load_data, convert_signal
from utils.slice import slice_data
import os

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green


class App(customtkinter.CTk):
    def __init__(self, data):  # Add the data source
        super().__init__()

        self.geometry("700x700")
        self.title("CustomTkinter")
        self.index = 0
        self.data = data
        self.results = []
        self.create_widgets()

    def create_widgets(self):
        self.fig, (self.ax1, self.ax2) = plt.subplots(2)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.mpl_connect("key_press_event", key_press_handler)
        self.canvas.get_tk_widget().grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 0), sticky="nsew")

        self.frame_1 = customtkinter.CTkFrame(master=self)
        self.frame_1.grid(row=1, column=0, rowspan=3, padx=20, pady=20, sticky="ew")

        self.button_slice = customtkinter.CTkButton(master=self, text="Slice", fg_color="green", command=self.save_slice)
        self.button_slice.grid(row=1, column=1, padx=20, pady=5, sticky="ew")

        self.button_skip = customtkinter.CTkButton(master=self, text="Skip", fg_color="orange", command=self.update_figure)
        self.button_skip.grid(row=2, column=1, padx=20, pady=5, sticky="ew")

        self.button_save = customtkinter.CTkButton(master=self, text="Save", command=self.save_file)
        self.button_save.grid(row=3, column=1, padx=20, pady=5, sticky="ew")

        self.button_quit = customtkinter.CTkButton(master=self, text="Quit", fg_color="gray", command=self.quit)
        self.button_quit.grid(row=4, column=1, padx=20, pady=5, sticky="ew")

        # self.label_1 = customtkinter.CTkLabel(master=self, justify=tkinter.LEFT)
        # self.label_1.pack(pady=12, padx=10)

        self.progressbar_1 = customtkinter.CTkProgressBar(master=self.frame_1)
        self.progressbar_1.pack(pady=12, padx=10)
        self.progressbar_1.set(0.20)
        self.update_figure()  # has progress dependency.

        self.slider_1 = customtkinter.CTkSlider(
            master=self.frame_1, command=self.move_slice, from_=self.t[0], to=self.t[-1]  # has t dependency from update_figure
        )
        self.slider_1.pack(pady=12, padx=10)
        self.slider_1.set(len(self.t) / 2)

    def update_figure(self):
        self.ax1.clear()
        self.ax2.clear()
        self.signal = self.get_signal()
        self.t = [x for x in range(self.signal.shape[0])]
        (self.line,) = self.ax1.plot(self.t, self.signal)
        borders = (len(self.t) / 2, len(self.t) / 2 + 200)
        self.left_border = self.ax1.axvline(borders[0], color='r')
        self.right_border = self.ax1.axvline(borders[1], color='r')
        (self.line2,) = self.ax2.plot(self.t, self.signal)
        self.ax2.set_xlabel("time [s]")
        self.ax1.set_ylabel("f(t)")
        print(max(self.line.get_data()[1]))
        self.update_progress()
        self.canvas.draw()

    def get_signal(self):
        sample = self.data[self.index]
        signal = convert_signal(sample, type='acc_total')
        signal = signal.to_numpy()
        print(f'index {self.index}, shape {signal.shape}')
        self.index += 1

        return signal

    def move_slice(self, new_val):
        self.left_border.set_xdata(new_val)
        self.right_border.set_xdata(new_val + 200)
        self.ax2.set_xlim(new_val - 20, new_val + 220)
        self.canvas.draw()

    def update_progress(self):
        length = len(self.data)
        progress = self.index / length
        print(progress)
        self.progressbar_1.set(progress)

    def save_slice(self):
        x = int(self.slider_1.get())
        data_slice = self.signal[x:x+200]
        if len(data_slice) < 200: # Padding
            data_slice = np.resize(data_slice, (200))

        print(data_slice.shape) 
        self.results.append(data_slice)
        self.update_figure()

    def save_file(self):
        path = 'data/processed/'
        if not os.path.isdir(path):
            os.makedirs(path)

        with open(f"{path}/incidents.txt", "w") as f: #! Careful with Append
            np.savetxt(f, self.results, fmt="%s", delimiter=" ")

    def quit(self):
        self.save_file()
        self.destroy()


def main():
    # ----- Data Load -----
    root = 'data/incidents/'
    file_list = []
    filenames = []
    for file in os.listdir(root):
        if file in ['processed']:  # Skip folders
            continue
        file_list.append(os.path.join(root, file))  # .replace("\\","/")
        filenames.append(file)

        # for p, s, f in os.walk(os.path.join(root, subdir)):
        #     for filename in f:
        #         file_list.append(os.path.join(root, subdir, filename).replace("\\","/"))
        #         filenames.append(filename)

    print(file_list)
    data = load_data(file_list)

    app = App(data)
    app.mainloop()


if __name__ == "__main__":
    main()
