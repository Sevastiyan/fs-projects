# Move borders in plot_data function if required, requires 10 seconds of data 
import numpy as np
from utils.data_loader import convert_signal, load_data
from utils.slice import slice_data
import glob, os

def incidents():
    path = f"./data/processed/May/"
    root = 'data/raw/May/cleaned_data'
    file_list = []
    for subdir in os.listdir(root):
        if subdir in ['Base Case', 'Base Case Walking']:
            continue

        for p, s, f in os.walk(os.path.join(root, subdir)):
            for filename in f: 
                file_list.append(os.path.join(root, subdir, filename))

    data = load_data(file_list)

    acc_results = []
    for sample in data: 
        signal = convert_signal(sample, type='acc_total')
        signal = signal.to_numpy()
        for i in range(40, 50, 10): # overlap samples for incidents data (1 seconds)
            x = signal[i : i+200]
            if len(x) < 200:
                x = np.resize(x, (200)) 

            acc_results.append(x.tolist())

    gyro_results = []
    for sample in data: 
        signal = convert_signal(sample, type='gyro_total')
        signal = signal.to_numpy()
        for i in range(40, 50, 10): # overlap samples for incidents data (40 to 50 in 10i)
            x = signal[i : i+200]
            if len(x) < 200:
                x = np.resize(x, (200)) 

            gyro_results.append(x.tolist())
        
    save_file(np.asarray(acc_results), path, 'incidents_acc')
    save_file(np.asarray(gyro_results), path, 'incidents_gyro')


def no_incidents():
    root = 'data/raw/May/'
    file_list = []
    for subdir in os.listdir(root):
        if subdir == "Base Case Walking":
            for p, s, f in os.walk(os.path.join(root, subdir)):
                for filename in f: 
                    file_list.append(os.path.join(root, subdir, filename))
        else: 
            continue

    data = load_data(file_list)

    acc_results = []
    for sample in data:
        x = convert_signal(sample, type='gyro_total')
        for i in range(0, len(x)-200, 200): # 100 because we can overlap samples for no incidents data
            acc_results.append(x[i:i+200])

    gyro_results = []
    for sample in data:
        x = convert_signal(sample, type='acc_total')
        for i in range(0, len(x)-200, 200): # 100 because we can overlap samples for no incidents data
            gyro_results.append(x[i:i+200])

    save_file(np.asarray(acc_results), 'no_incidents_acc')
    save_file(np.asarray(gyro_results), 'no_incidents_gyro')



def save_file(data, path, filename):
    if not os.path.isdir(path):
        os.makedirs(path)

    with open(f"{path}/{filename}.txt", "a") as f:
        np.savetxt(f, data, fmt="%s", delimiter=" ")


def keith_incidents():
    root = 'data/raw/Keith/'
    file_list = []
    for subdir in os.listdir(root):
        if subdir == "Base Case Walking":
            continue

        for p, s, f in os.walk(os.path.join(root, subdir)):
            for filename in f: 
                file_list.append(os.path.join(root, subdir, filename))

    data = load_data(file_list)

    acc_results = []
    for sample in data: 
        signal = convert_signal(sample, type='acc_total')
        signal = signal.to_numpy()
        
        x = signal[40 : 240]
        if len(x) < 200:
            x = np.resize(x, (200)) 

        acc_results.append(x.tolist())

    save_file(np.asarray(acc_results), 'keith_incidents_acc')


if __name__ == "__main__":
    incidents()