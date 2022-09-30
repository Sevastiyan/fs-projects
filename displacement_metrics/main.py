from json import load
import numpy as np
from utils.data_loader import load_data, convert_signal
import matplotlib.pyplot as plt
import os 

def main():
    path = f"./data"
    root = './data'
    file_list = []
    for file in os.listdir(root):
        file_list.append(os.path.join(root, file))

    print(file_list)

    data = load_data(file_list[0:1])

    acc_results = []
    for sample in data: 
        signal = convert_signal(sample, type='acc_total')
        signal = signal.to_numpy()
        acc_results.append(signal.tolist())

    gyro_results = []
    for sample in data: 
        signal = convert_signal(sample, type='gyro_total')
        signal = signal.to_numpy()
        gyro_results.append(signal.tolist())

    plot(gyro_results[0])


def plot(data):
    plt.figure(figsize=[7,5])
    plt.style.use('seaborn-muted')
    plt.plot(data)
    plt.show()

if __name__ == '__main__':
    main()