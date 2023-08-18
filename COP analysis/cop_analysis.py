import os
import utils.cop as cop
from utils.data_loader import load_file, convert_signal
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np



# root variables for folders and file location ----------------------------------
root_folder = './COP analysis'
date = '2023-07-22'
subject = 'mci004'
plots_path = './plots'


def main():
    print('Script Start')
    print('------------')

    
    # Fetch Data ---------------------------------------------------------------------
    # root = f'{root_folder}/data/{date} OneMinTests'
    # file_list = []
    # for file in os.listdir(root):
    #     file_list.append(os.path.join(root, file)) 
    
    # Fetch all data for individual subjects: ---------------------------------------
    files = {}
    root = f'{root_folder}/data/{subject}'
    for d in os.listdir(root):
        files[d] = []
        for file in os.listdir(f'{root}/{d}'):
            files[d].append(os.path.join(root, d, file))
    
    plots_path = f'{root_folder}/plots/{subject}/{date}'
    if not os.path.isdir(plots_path):
        os.makedirs(plots_path)
    
    
    time, raw_signal, filt_signal, mask = load_data(files[date])
    
    # Center Of Pressure -----------------------------------------------------------
    c = cop.CenterOfPressure(
        [
            raw_signal['left'][mask['left']].reset_index(), 
            raw_signal['right'][mask['right']].reset_index()
        ]
    )
    
    filt_c = cop.CenterOfPressure(
        [
            filt_signal['left'][mask['left']].reset_index(),                
            filt_signal['right'][mask['right']].reset_index()
        ]
    )

    left_cop = c.get_cop_foot('left')
    right_cop = c.get_cop_foot('right')

    filt_l_cop = filt_c.get_cop_foot('left')
    filt_r_cop = filt_c.get_cop_foot('right')
    
    # Plots ------------------------------------------------------------------------
    plot_pressure_and_differential(time, raw_signal, filt_signal, mask, plots_path)
    plot_cop(left_cop, right_cop, filt_l_cop, filt_r_cop, plots_path)
    
    return
    
    for key in files.keys():
        print(key)
        load_data(files[key])
        

def load_data(data):
    file_set = 0 * 2
    time = {}
    raw_signal = {}
    filt_signal = {}
    mask = {}

    # Data load
    raw_left = load_file(data[file_set], filter=False)
    raw_right = load_file(data[file_set + 1], filter=False)
    filter_left = load_file(data[file_set], filter=True, cutoff=1.5)
    filter_right = load_file(data[file_set + 1], filter=True, cutoff=1.5)

    # Creating Placeholders
    side = 'left'
    time[side] = [x * 0.05 for x in range(len(raw_left))]
    raw_signal[side] = convert_signal(raw_left, 'pressure')
    filt_signal[side] = convert_signal(filter_left, 'pressure')
    mask[side] = generate_mask(filt_signal[side])

    side = 'right'
    time[side] = [x * 0.05 for x in range(len(raw_right))]
    raw_signal[side] = convert_signal(raw_right, 'pressure')
    filt_signal[side] = convert_signal(filter_right, 'pressure')
    mask[side] = generate_mask(filt_signal[side])


    # Acceleration
    left_acc = convert_signal(filter_left, 'acc_total')
    right_acc = convert_signal(filter_right, 'acc_total')
    
    return (time, raw_signal, filt_signal, mask)


def plot_pressure_and_differential(time, raw_signal, filter_signal, mask, plots_path):
    left_line = [1 for x in time['left']]
    right_line = [1 for x in time['right']]
    
    
    plt.figure(figsize=(15,6))

    # Left Side ---------------------------------------------------------------
    side = 'left' 
    plt.subplot(2,2,1)
    plt.title('Left Foot')
    plt.plot(time[side], raw_signal[side], label='left data')
    plt.plot(time[side], filter_signal[side], label='left filter')
    plt.ylabel('Raw Input')
    plt.grid(True)
    plt.axis('tight')
    plt.legend(loc='upper left')

    plt.subplot(2,2,3)
    plt.plot(time[side], filter_signal[side].diff(), label='left diff')
    plt.plot(time[side], mask[side], label='left mask')
    plt.plot(time[side], left_line, '-.')
    plt.ylabel('Raw Input')
    plt.xlabel('Time[s]')
    plt.grid(True)
    plt.axis('tight')
    plt.legend(loc='upper left')
    
    # Right Side ---------------------------------------------------------------
    side = 'right'
    plt.subplot(2,2,2)
    plt.title('Right Foot')
    plt.plot(time[side], raw_signal[side], label='right data')
    plt.plot(time[side], filter_signal[side], label='right filter')
    plt.grid(True)
    plt.axis('tight')
    plt.legend(loc='upper left')


    plt.subplot(2,2,4)
    plt.plot(time[side], filter_signal[side].diff(), label='right diff')
    plt.plot(time[side], mask[side], label='right mask')
    plt.plot(time[side], right_line, '-.', label='Threshold')
    plt.xlabel('Time[s]')    
    plt.grid(True)
    plt.axis('tight')
    plt.legend(loc='upper left')

    # plt.show()
    plt.savefig(f'{plots_path}/plot_pressure.png')
    
    
def plot_cop(left_cop, right_cop, filt_l_cop, filt_r_cop, plots_path):
    left_time = [x * 0.05 for x in range(len(left_cop[0]))]
    right_time = [x * 0.05 for x in range(len(right_cop[0]))]
    plt.figure(figsize=(15,4))
    plt.subplot(1,2,1)
    plt.title('COP_AP - Left Foot')
    plt.plot(left_time, left_cop[1])
    plt.plot(left_time, filt_l_cop[1])
    plt.ylabel('Position Y [cm]')
    plt.xlabel('Time[s]')
    plt.subplot(1,2,2)
    plt.title('COP_AP - Right Foot')
    plt.plot(right_time, right_cop[1])
    plt.plot(right_time, filt_r_cop[1])
    plt.xlabel('Time[s]')
    
    plt.savefig(f'{plots_path}/COP.png')


def generate_mask(signal, threshold=1):
    print('Generating Mask...')
    freq = 0.05
    seconds = 3
    window = int(seconds / freq)
    active = False
    c = window + 1 # to start with no activity
    count = []

    diff = signal.diff()

    for i, x in enumerate(diff):
        if i <= window:
            c += 1
            count.append(c)
            continue
        
        if x > threshold:
            active = True
            c = 0

        if active and c < window:
            c += 1
            count.append(c)
            continue 
        
        if c > window:
            active = not active

        c += 1    
        count.append(c)
        
    return np.array([True if x < window else False for x in count])


if __name__ == '__main__':
    main()

