import os
import utils.cop as Cop
from utils.data_loader import load_file, convert_signal
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.signal import find_peaks


# root variables for folders and file location ----------------------------------
root_folder = './COP analysis'
# date = '2023-07-10'
subject = 'mci007'
plots_path = './plots'

left_data_list = []
right_data_list = []

def main():
    files = {}
    root = f'{root_folder}/data/{subject}'
    dates = os.listdir(root)
    
    
    for day in dates:
        files[day] = []
        for file in os.listdir(f'{root}/{day}'):
            files[day].append(os.path.join(root, day, file))
    
    for date in files.keys():
        # for file_set in range(0, len(files[date]), 2):
            # file_left = files[date][file_set]
            # file_right = files[date][file_set + 1]
            # print(file_left, file_right)
        print(f'--- Starting analysis for {date} ---')
        start_analysis(files[date], date)
        
    # Create pandas DataFrames for left and right sides
    left_df = pd.DataFrame(left_data_list)
    right_df = pd.DataFrame(right_data_list)
    print(left_df.head(10))
        
    right_df.to_csv(f'{subject}_right_df.csv')
    left_df.to_csv(f'{subject}_left_df.csv')



def start_analysis(data, date):
    time = {}
    filt_signal = {}
    acc = {}
    mask = {}
    
    for file_set in range(0, len(data), 2):
        
        # Data load
        file_left = data[file_set]
        file_right = data[file_set + 1]
        
        
        left_data = load_file(file_left, filter=True, cutoff=2)      
        right_data = load_file(file_right, filter=True, cutoff=2)

        # Pre-processing Data ------------------------------------------------------------
        side = 'left'
        time[side] = [x * 0.05 for x in range(len(left_data))]        
        filt_signal[side] = convert_signal(left_data, 'pressure')
        acc[side] = convert_signal(left_data, 'acc_total')
        mask[side] = generate_mask(acc[side])
        
        side = 'right'
        time[side] = [x * 0.05 for x in range(len(right_data))]
        filt_signal[side] = convert_signal(right_data, 'pressure')
        acc[side] = convert_signal(right_data, 'acc_total')
        mask[side] = generate_mask(acc[side])

        activity_input_left = left_data[mask['left']].reset_index()
        
        # Check if the activity is enough ------------------------------------------------
        if len(activity_input_left) < 0.7 * 60 * 20: 
            left_data_list.append(generate_dummy(file_left, date.split(' ')[0]))
            right_data_list.append(generate_dummy(file_right, date.split(' ')[0]))

            continue
        
        # Peak Finding -------------------------------------------------------------------
        prom = 10
        dist = 18

        activity_input_right = right_data[mask['right']].reset_index()
        filt_c = Cop.CenterOfPressure([activity_input_left, activity_input_right])

        cop = {}
        peaks = {}

        side = 'left'
        cop[side] = filt_c.get_cop_foot(side)
        time[side] = [x * 0.05 for x in range(len(cop[side][0]))]

        xl = cop[side][1]
        peaks[side] = {}
        peaks[side]['positive'], _ = find_peaks(xl, prominence=prom, distance=dist)
        peaks[side]['negative'], _ = find_peaks(-xl, prominence=prom, distance=dist)


        side = 'right'
        cop[side] = filt_c.get_cop_foot(side)
        time[side] = [x * 0.05 for x in range(len(cop[side][0]))]

        xr = cop[side][1]
        peaks[side] = {}
        peaks[side]['positive'], _ = find_peaks(xr, prominence=prom, distance=dist)
        peaks[side]['negative'], _ = find_peaks(-xr, prominence=prom, distance=dist)

        # Results ------------------------------------------------------------------------
        side = 'left'
        l_timings, l_pairs = closest_peaks(peaks[side]['positive'], peaks[side]['negative'])
        l_velocity = find_cop_velocity(xl, l_timings['step'], l_pairs['step'])
        # Create dictionaries for left and right sides
        left_data = {
            'File': file_left,
            'Date': date.split(' ')[0],
            'Total_Activity_Time_minutes': len(activity_input_left) * 0.05 / 60,
            'Avg_Step_Time': np.mean(l_timings['step']),
            'Avg_Stride_Time': np.mean(l_timings['stride']),
            'Avg_Cycle_Time': np.mean(find_cycle_time(peaks[side]['negative'])),
            'Avg_COP_Velocity': np.mean(l_velocity),
            'COP_Variability': np.std(cop[side])
        }

        side = 'right'
        r_timings, r_pairs = closest_peaks(peaks[side]['positive'], peaks[side]['negative'])
        r_velocity = find_cop_velocity(xr, r_timings['step'], r_pairs['step'])
        right_data = {
            'File': file_right,
            'Date': date.split(' ')[0],
            'Total_Activity_Time_minutes': len(activity_input_right) * 0.05 / 60,
            'Avg_Step_Time': np.mean(r_timings['step']),
            'Avg_Stride_Time': np.mean(r_timings['stride']),
            'Avg_Cycle_Time': np.mean(find_cycle_time(peaks[side]['negative'])),
            'Avg_COP_Velocity': np.mean(r_velocity),
            'COP_Variability': np.std(cop[side])
        }
        
        # Append dictionaries to the respective lists
        left_data_list.append(left_data)
        right_data_list.append(right_data)

    return 


def generate_mask(signal, threshold=7):
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


def closest_peaks(positive, negative): 
    pairs = {
        'step': [],
        'stride': []
    }
    
    timings = {
        'step': [],
        'stride': []
    }
    
    for n in negative:
        for p in positive:
            if n < p:
                distance = abs(p - n)
                pairs['step'].append((p, n))
                timings['step'].append(distance*0.05)
                break
            
    for p in positive:
        for n in negative:
            if n > p:
                distance = abs(n - p)
                pairs['stride'].append((p, n))
                timings['stride'].append(distance*0.05)
                break
            
    return timings, pairs
            

def find_cycle_time(peaks):
    # Calculate distances between pairs of peaks
    time = []
    for i in range(len(peaks) - 1):
        distance = np.abs(peaks[i] - peaks[i + 1])
        time.append(distance*0.05)

    return time


def find_cop_velocity(data, time, peaks):
    velocity_array = []
    
    for i in range(len(time)):
        p, n = peaks[i]
        velocity_array.append((data[p] - data[n]) / time[i])
        
    return velocity_array


def generate_dummy(file, date): 
    return {
        'File': file,
        'Date': date,
        'Total_Activity_Time_minutes': 0,
        'Avg_Step_Time': 0,
        'Avg_Stride_Time': 0,
        'Avg_Cycle_Time': 0,
        'Avg_COP_Velocity': 0,
        'COP_Variability': 0
    }

if __name__ == '__main__':
    main()

