import customtkinter
import tkinter
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

from utils.data_loader import load_data, load_file, convert_signal
from utils.slice import slice_data
import os

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green


class App(customtkinter.CTk):
    def __init__(self, folder):  # Add the data source
        super().__init__()

        self.geometry("700x800")
        self.title("CustomTkinter")
        self.index = 0
        self.root_folder = folder
        self.files_list = []
        self.file_names = []
        self.results = {'acc': [], 'gyro': []}
        self.create_widgets()
        self.load_data()

    def load_data(self):
        for file in os.listdir(self.root_folder):
            if file in ['processed', '2022-12-06']:  # Skip folders
                continue
            self.files_list.append(os.path.join(self.root_folder, file))  # .replace("\\","/")
            self.filenames.append(file)

        print(self.file_list)

    def read_data(self, file_name):

        pass

    def create_widgets(self):
        self.fig, (self.ax1, self.ax2) = plt.subplots(2)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.mpl_connect("key_press_event", key_press_handler)
        self.canvas.get_tk_widget().grid(row=0, column=0, columnspan=3, padx=20, pady=(20, 0), sticky="nsew")

        self.control_frame = customtkinter.CTkFrame(master=self)
        self.control_frame.grid(row=1, column=0, rowspan=4, padx=20, pady=(20, 0), sticky="ew")

        self.folder_frame = customtkinter.CTkFrame(master=self)
        self.folder_frame.grid(row=5, column=0, rowspan=2, padx=20, pady=(20, 0), sticky="ew")

        self.button_slice = customtkinter.CTkButton(master=self, text="Slice", fg_color="green", command=self.slice_data)
        self.button_slice.grid(row=1, column=2, padx=20, pady=5, sticky="ew")

        self.button_skip = customtkinter.CTkButton(master=self, text="Skip", fg_color="orange", command=self.update_figure)
        self.button_skip.grid(row=2, column=2, padx=20, pady=5, sticky="ew")

        self.button_save = customtkinter.CTkButton(master=self, text="Save", command=self.save_file)
        self.button_save.grid(row=3, column=2, padx=20, pady=5, sticky="ew")

        self.button_quit = customtkinter.CTkButton(master=self, text="Quit", fg_color="gray", command=self.quit)
        self.button_quit.grid(row=4, column=2, padx=20, pady=5, sticky="ew")

        # Navigation ------------------------------
        self.text_var = tkinter.StringVar(value=f'Progress: ')
        self.label_1 = customtkinter.CTkLabel(master=self.control_frame, textvariable=self.text_var)
        self.label_1.pack(pady=12, padx=10)

        self.progressbar_1 = customtkinter.CTkProgressBar(master=self.control_frame)
        self.progressbar_1.pack(pady=12, padx=10)

        self.slider_1 = customtkinter.CTkSlider(
            master=self.control_frame,
            command=self.move_slice,
            from_=0,
            to=1,
        )
        self.slider_1.pack(pady=12, padx=10)
        self.slider_1.set(0.5)

        # Folders ----------------------------------
        self.folder_label = customtkinter.CTkLabel(master=self.folder_frame, text='Folder: Not in Use at the moment')
        self.folder_label.pack(pady=12, padx=10)

        self.folders = os.listdir('data/')
        self.combobox = customtkinter.CTkComboBox(master=self.folder_frame, values=self.folders)
        self.combobox.pack(pady=12, padx=10)

        self.update_figure()  # has progress dependency.

    def update_figure(self):
        print('------------------')
        self.ax1.clear()
        self.ax2.clear()
        self.acc_signal, self.gyro_signal = self.get_signal(self.index)
        self.t = range(self.acc_signal.shape[0])
        (self.line,) = self.ax1.plot(self.t, self.acc_signal)
        # borders = (len(self.t) / 2, len(self.t) / 2 + 200)
        print('slice before save', self.slider_1.get() * len(self.t))
        borders = (self.slider_1.get() * len(self.t), self.slider_1.get() * len(self.t) + 200)

        self.left_border = self.ax1.axvline(borders[0], color='r')
        self.right_border = self.ax1.axvline(borders[1], color='r')
        (self.line2,) = self.ax2.plot(self.t, self.acc_signal)
        self.ax2.set_xlabel("time [s]")
        self.ax1.set_ylabel("f(t)")
        print('Max value: ', max(self.line.get_data()[1]))
        self.update_progress()
        self.canvas.draw()

    def get_signal(self, index):
        sample = self.data[index]
        acc = convert_signal(sample, type='acc_total')
        gyro = convert_signal(sample, type='gyro_total')
        acc = acc.to_numpy()
        gyro = gyro.to_numpy()
        print(f'index: {index}')
        print(f'Acc shape {acc.shape}', f' Gyro shape {gyro.shape}')

        return acc, gyro

    def move_slice(self, new_val):
        x = int(len(self.t) * new_val)  # convert from fraction to data where t is x axis and new_val is
        self.left_border.set_xdata(x)
        self.right_border.set_xdata(x + 200)
        self.ax2.set_xlim(x - 20, x + 220)
        self.canvas.draw()

    def update_progress(self):
        self.index += 1  # ! Important to keep track of the current index of the file list
        length = len(self.data)
        progress = self.index / length
        self.progressbar_1.set(progress)
        self.text_var.set(value=f'Progress: {self.index}/{length}')
        print('Progress: ', self.index, '/', length)

    def slice_data(self):
        x = int(self.slider_1.get() * len(self.t))  # convert from fraction to data where
        print('Slice after save', x)
        acc_slice = self.acc_signal[x : x + 200]
        if len(acc_slice) < 200:  # Padding
            acc_slice = np.resize(acc_slice, (200))
        self.results['acc'].append(acc_slice)

        gyro_slice = self.gyro_signal[x : x + 200]
        if len(gyro_slice) < 200:  # Padding
            gyro_slice = np.resize(gyro_slice, (200))
        self.results['gyro'].append(gyro_slice)

        print('Slice Shape: ', acc_slice.shape)
        self.update_figure()
        # self.slider_1.set(0.5) # len(self.t) / 2)

    def save_file(self):
        path = 'data/processed/cop'
        if not os.path.isdir(path):
            os.makedirs(path)

        with open(f"{path}/incidents_acc.txt", "w") as f:  #! Careful with Append
            np.savetxt(f, self.results['acc'], fmt="%s", delimiter=" ")
        with open(f"{path}/incidents_gyro.txt", "w") as f:  #! Careful with Append
            np.savetxt(f, self.results['gyro'], fmt="%s", delimiter=" ")
        print('Data Saved')

    def quit(self):
        self.save_file()
        self.destroy()


def main():
    # ----- Data Load -----
    root = 'data/2022-10/Slip'
    file_list = []
    filenames = []

    for file in os.listdir(root):
        if file in ['processed', '2022-12-06']:  # Skip folders
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
