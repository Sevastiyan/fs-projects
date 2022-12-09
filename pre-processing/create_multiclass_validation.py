# Move borders in plot_data function if required, requires 10 seconds of data 
import numpy as np
from utils.data_loader import convert_signal, load_data
from utils.slice import slice_data
import glob, os

def main():
    root = 'data/classification/validation/2022-10-21'
    print(os.listdir())
    file_list = {}
    for subdir in os.listdir(root):
        file_list[subdir] = []
        for p, s, f in os.walk(os.path.join(root, subdir)):
            for filename in f: 
                file_list[subdir].append(os.path.join(root, subdir, filename))

    for label in file_list.keys():
        if label in ['Slip', 'Trip']:
            print(label, 'has', len(file_list[label]), 'files')
            data = load_data(file_list[label])
            incidents(data, label)
        if label in ['No Incident']:
            print(label, 'has', len(file_list[label]), 'files')
            data = load_data(file_list[label])
            no_incidents(data, label)


def incidents(data, label):
    START = 60
    END = 70
    STEP = 10

    acc_results = []
    gyro_results = []

    for sample in data: 
        acc_signal = convert_signal(sample, type='acc_total').to_numpy()
        gyro_signal = convert_signal(sample, type='gyro_total').to_numpy()
        for i in range(START, END, STEP): # overlap samples
            x_acc = acc_signal[i : i+200]
            x_gyro = gyro_signal[i : i+200]
            if len(x_acc) < 200:
                x_acc = np.resize(x_acc, (200)) 
            if len(x_gyro) < 200:
                x_gyro = np.resize(x_gyro, (200)) 

            acc_results.append(x_acc.tolist())
            gyro_results.append(x_gyro.tolist())


    path = 'data/processed/validation_set/'

    save_file(np.asarray(acc_results), f'{path}/{label}', 'incidents_acc')
    save_file(np.asarray(gyro_results), f'{path}/{label}', 'incidents_gyro')


def no_incidents(data, label):
    START = 100
    END = 200
    STEP = 100
    
    acc_results = []
    gyro_results = []

    for sample in data: 
        acc_signal = convert_signal(sample, type='acc_total').to_numpy()
        gyro_signal = convert_signal(sample, type='gyro_total').to_numpy()
        for i in range(START, END, STEP): # overlap samples
            x_acc = acc_signal[i : i+200]
            x_gyro = gyro_signal[i : i+200]
            if len(x_acc) < 200:
                x_acc = np.resize(x_acc, (200)) 
            if len(x_gyro) < 200:
                x_gyro = np.resize(x_gyro, (200)) 

            acc_results.append(x_acc.tolist())
            gyro_results.append(x_gyro.tolist())

    path = 'data/processed/validation_set/'
    save_file(np.asarray(acc_results), f'{path}/{label}', 'no_incidents_acc')
    save_file(np.asarray(gyro_results), f'{path}/{label}', 'no_incidents_gyro')


def save_file(data, path, filename):
    if not os.path.isdir(path):
        os.makedirs(path)

    with open(f"{path}/{filename}.txt", "w") as f:
        np.savetxt(f, data, fmt="%s", delimiter=" ")


if __name__ == "__main__":
    # base()
    main()
