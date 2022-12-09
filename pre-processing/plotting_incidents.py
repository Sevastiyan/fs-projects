import numpy as np
from utils.data_loader import convert_signal, load_data
from utils.plots import plot_data
from utils.slice import slice_data
import glob, os

def plot_incidents():
    root = 'data/validation/2022-10-21/'
    file_list = []
    filenames = []
    for subdir in os.listdir(root):
        print(subdir)
        if subdir in ['Slip', 'Trip']:
            for p, s, f in os.walk(os.path.join(root, subdir)):
                for filename in f: 
                    file_list.append(os.path.join(root, subdir, filename).replace("\\","/"))
                    filenames.append(filename)
                
    data = load_data(file_list)
    for i in range(len(data)): 
        sample = data[i]
        signal = convert_signal(sample, type='acc_total')
        signal = signal.to_numpy()

        sliced = slice_data(signal, [50, 250])

        plot_data([signal, sliced], [50, 250], subdir='2022-10-21', title=filenames[i], save=True)


if __name__ == "__main__":
    plot_incidents()
