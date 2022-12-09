from cmath import pi
import os
from re import X
import pandas as pd
import numpy as np
from utils.filters import butter_lowpass_filter


def load_data(files, filter=False, regressions=None):
    '''Loads data from ./data folder
    Name the data in numerical order to get reading sequencing correct
    e.g. 
    1rawDataLeft_S5_20220401.txt
    2rawDataRight_S5_20220401.txt

    Args: 
        files: List of files to read
        filter: True will apply low pass filter to pressure readings
        regressions: Regressions for the the insoles

    Returns: 
        Dataset (by sessions, then L/R), Session number
        Dataset example: data[0][0] represents data of first session, Left foot
    '''
    # files = os.listdir(path)  # List of files in the data path folder
    data = []
    sessions = []
    for file in files:
        # Read the data -------------------------------------------------------
        raw_data = read_data(file)
        x = pd.DataFrame()  # Buffer for filtered data
        # Filter the data -----------------------------------------------------
        if filter:  # If the filter is not used
            for col in raw_data.columns:
                if col in ['time', 'Session_no', 'TIMESTAMP']:  # Don't filter
                    x[col] = raw_data[col]
                    continue
                x[col] = butter_lowpass_filter(raw_data[col], cutoff=3, fs=20)
        else:
            x = raw_data

        # convert to pressure -------------------------------------------------
        if regressions:
            if 'left' in file:
                x = convert_to_pressure(x, regressions[0])
            if 'right' in file:
                x = convert_to_pressure(x, regressions[1])

        # ---------------------------------------------------------------------
        data.append(x)                 # Add the data to the buffer list
    #     session = file.split('_')[-2:]
    #     sessions.append(session)

    # # Split the data into [(left, right)]
    # data_set = list(zip(data[::2], data[1::2]))
    # # Split the sessions into [(left, right)]
    # session_set = list(zip(sessions[::2], sessions[1::2]))
    
    return data #, session_set


def read_data(filename):
    """Find data files from the os data path and read the data

    Args:
        param path: A string with the path to the data files

    Returns:
        DataFrame with the data
    """
    try:
        df = pd.read_csv(filename,
                         sep=',',
                         header=None)
        if len(df.columns) == 23:
            df.columns = [
                'time', 'raw_1', 'raw_2', 'raw_3', 'raw_4', 'raw_5', 'raw_6',
                'raw_7', 'raw_8', 'raw_9', 'raw_10', 'raw_11', 'raw_12',
                'raw_13', 'raw_14', 'acc_x', 'acc_y', 'acc_z', 'gyro_x',
                'gyro_y', 'gyro_z', 'Session_no', 'Timestamp'
            ]
            df['time'] = (np.arange(0, len(df['raw_1'])) / 20)
            return df

        if len(df.columns) > 23:
            df.columns = [
                'time', 'raw_1', 'raw_2', 'raw_3', 'raw_4', 'raw_5', 'raw_6',
                'raw_7', 'raw_8', 'raw_9', 'raw_10', 'raw_11', 'raw_12',
                'raw_13', 'raw_14', 'acc_x', 'acc_y', 'acc_z', 'gyro_x',
                'gyro_y', 'gyro_z', 'Session_no', 'Timestamp', 'battery'
            ]
            df['time'] = (np.arange(0, len(df['raw_1'])) / 20)
            
            return df.drop(['battery'], axis=1)

        if len(df.columns) == 17:
            df.columns = [
                'time', 'raw_1', 'raw_2', 'raw_3', 'raw_4', 'raw_5', 'raw_6',
                'raw_7', 'raw_8', 'raw_9', 'raw_10', 'raw_11', 'raw_12',
                'raw_13', 'raw_14', 'acc_x', 'acc_y'
            ]
            df.insert(17, 'acc_z', 0)
            df.insert(18, 'gyro_x', 0)
            df.insert(19, 'gyro_y', 0)
            df.insert(20, 'gyro_z', 0)
            df.insert(21, 'Timestamp', 0)
            return df

        if len(df.columns) == 21:
            df.columns = [
                'raw_1', 'raw_2', 'raw_3', 'raw_4', 'raw_5', 'raw_6', 'raw_7',
                'raw_8', 'raw_9', 'raw_10', 'raw_11', 'raw_12', 'raw_13',
                'raw_14', 'acc_x', 'acc_y', 'acc_z', 'gyro_x', 'gyro_y',
                'gyro_z', 'Timestamp'
            ]
            df.insert(0, 'time', (np.arange(0, len(df['raw_1'])) / 20))
            return df

    except:
        print('No data found')
        return pd.DataFrame()

def convert_to_pressure(data, regression_coefficients):
    """Convert the data to the pressure.

    Args:
        param data: DataFrame with the data
        param regression_coefficients: Coefficients of the pressure regression
    """
    pressure_data = data.iloc[:, 1:15] * regression_coefficients
    for col in data.columns:
        if col in ['time', 'acc_x', 'acc_y', 'acc_z', 'gyro_x', 'gyro_y', 'gyro_z']:
            pressure_data[col] = data[col]
            continue
    return pressure_data

def convert_signal(data, type):
    if type == "acc":
        x = data[['acc_x', 'acc_y', 'acc_z']]
        # data = data.iloc[:, 14:17]
        return x * 9.81 / 4096

    if type == "acc_total":
        x = data[['acc_x', 'acc_y', 'acc_z']]
        x = np.sqrt((x['acc_x']/4096*9.81)**2 + (x['acc_y']/4096*9.81)**2 + (x['acc_z']/4096*9.81)**2) - 9.81
        return x

    if type == "gyro":
        x = data[['gyro_x', 'gyro_y', 'gyro_z']]
        # data = data.iloc[:, 17:20]
        return x / 16.2

    if type == "gyro_total":
        x = data[['gyro_x', 'gyro_y', 'gyro_z']]
        x = np.sqrt((x['gyro_x']/16.2)**2 + (x['gyro_y']/16.2)**2 + (x['gyro_z']/16.2)**2)
        return x

    if type == "pressure":
        data = data[['raw_1', 'raw_2', 'raw_3', 'raw_4', 'raw_5', 'raw_6',
                'raw_7', 'raw_8', 'raw_9', 'raw_10', 'raw_11', 'raw_12',
                'raw_13', 'raw_14']]
        return x.mean(axis=1)

def get_overall_signal(data, signal):
    if signal == "acc":
        data['Total Acc'] = np.sqrt((np.square(data['acc_x']) + np.square(data['acc_y']) + np.square(data['acc_z']))) - 9.81
        # data = data.iloc[:, 14:17]
        return data

    if signal == "gyro":
        data['Total Gyro'] = np.sqrt((np.square(data['gyro_x']) + np.square(data['gyro_y']) + np.square(data['gyro_z'])))
        # data = data.iloc[:, 17:20]
        return data 