import os
import numpy as np
import pandas as pd
from utils.plots import plot_data
from utils.data_loader import load_data, convert_signal

def main():
    root = 'data/clean_data'
    file_list = []
    for subdir in os.listdir(root):
        if subdir == "Base Case Walking":
            continue

        for p, s, f in os.walk(os.path.join(root, subdir)):
            for filename in f: 
                file_list.append(os.path.join(root, subdir, filename))

    data = load_data(file_list)
    
    x = convert_signal(data[120], type='acc_total')
    x = np.asarray(x)

    plot_data([x, x[150:350]], borders=[150,350], title='Trip Accelerometer', save=True)

def base(): 
    root = 'data/clean_data'
    file_list = []
    for subdir in os.listdir(root):
        if subdir == "Base Case Walking":
            for p, s, f in os.walk(os.path.join(root, subdir)):
                for filename in f: 
                    file_list.append(os.path.join(root, subdir, filename))
        else: 
            continue

    data = load_data(file_list)
    
    x = convert_signal(data[11], type='acc_total')
    x = np.asarray(x)

    plot_data([x, x[400:600]], borders=[400,600], title='Walking Accelerometer', save=True)


if __name__ == "__main__":
    # base()
    main()
