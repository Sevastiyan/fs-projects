from cmath import pi
import pandas as pd
import numpy as np
from scipy.signal import butter, filtfilt


def load_combined_file(file, filter=False, regressions=None, frequency=20, cutoff=1.8, order=4):
    left_data, right_data = read_combined_file(file)

    xLeft = pd.DataFrame()
    xRight = pd.DataFrame()
    if filter:
        print("Filtering data")
        for col in left_data.columns:
            if col in [
                "ms",
                "acc_x",
                "acc_y",
                "acc_z",
                "gyro_x",
                "gyro_y",
                "gyro_z",
                "Session_no",
                "Timestamp",
                "battery",
            ]:  # Don't filter
                xLeft[col] = left_data[col]
                xRight[col] = right_data[col]
                continue
            xLeft[col] = butter_lowpass_filter(left_data[col], cutoff=cutoff, fs=frequency, order=order)
            xRight[col] = butter_lowpass_filter(right_data[col], cutoff=cutoff, fs=frequency, order=order)
            # Substitute negative signals with 0 in raw columns
        raw_columns = [col for col in xLeft.columns if col.startswith("raw_")]
        xLeft[raw_columns] = xLeft[raw_columns].clip(lower=1)
        xRight[raw_columns] = xRight[raw_columns].clip(lower=1)
    else:
        xLeft = left_data
        xRight = right_data

    return xLeft, xRight


def load_file(file, filter=False, regressions=None, cutoff=1.8):
    # Read the data -------------------------------------------------------
    raw_data = read_data(file)

    x = pd.DataFrame()  # Buffer for filtered data
    # Filter the data -----------------------------------------------------
    if filter:  # If the filter is not used
        print("Filtering data")
        for col in raw_data.columns:
            if col in [
                "acc_x",
                "acc_y",
                "acc_z",
                "gyro_x",
                "gyro_y",
                "gyro_z",
                "Session_no",
                "Timestamp",
                "battery",
            ]:  # Don't filter
                x[col] = raw_data[col]
                continue
            x[col] = butter_lowpass_filter(raw_data[col], cutoff=cutoff, fs=20)
            # Substitute negative signals with 0 in raw columns
            raw_columns = [col for col in x.columns if col.startswith("raw_")]
            x[raw_columns] = x[raw_columns].clip(lower=1)
    else:
        x = raw_data

    # convert to pressure -------------------------------------------------
    if regressions:
        print("Converting to pressure:")
        print("Right" if "Right" in file else "Left")

        if "Left" in file:
            print("left insole")
            x = convert_to_pressure(x, regressions[0])
        elif "Right" in file:
            print("right insole")
            x = convert_to_pressure(x, regressions[1])
    # ---------------------------------------------------------------------

    return x


def load_data(files, filter=False, regressions=None):
    """Loads data from ./data folder
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
    """
    # files = os.listdir(path)  # List of files in the data path folder
    data = []
    sessions = []
    for file in files:
        # Read the data -------------------------------------------------------
        raw_data = read_data(file)
        x = pd.DataFrame()  # Buffer for filtered data
        # Filter the data -----------------------------------------------------
        if filter:  # If the filter is not used
            print("Filtering data")
            for col in raw_data.columns:
                if col in [
                    "acc_x",
                    "acc_y",
                    "acc_z",
                    "gyro_x",
                    "gyro_y",
                    "gyro_z",
                    "Session_no",
                    "Timestamp",
                    "battery",
                ]:  # Don't filter
                    x[col] = raw_data[col]
                    continue
                x[col] = butter_lowpass_filter(raw_data[col], cutoff=1.8, fs=20)
        else:
            x = raw_data

        # convert to pressure -------------------------------------------------
        if regressions:
            print("Converting to pressure:")
            print("Right" if "Right" in file else "Left")

            if "Left" in file:
                print("left insole")
                x = convert_to_pressure(x, regressions[0])
            if "Right" in file:
                print("right insole")
                x = convert_to_pressure(x, regressions[1])
        # ---------------------------------------------------------------------

        data.append(x)  # Add the data to the buffer list

    return data


def read_combined_file(filename):
    """Find data files from the os data path and read the data

    Args:
        param path: A string with the path to the data files

    Returns:
    DataFrame with the data
    """
    # print("reading data file", filename)

    df = filename  # pd.read_csv(filename, sep=",")
    print(f"{len(df.columns)} columns found")
    left_columns = [col for col in df.columns if "left" in col or "ms" in col]
    right_columns = [col for col in df.columns if "right" in col or "ms" in col]

    df_left = df[left_columns]
    df_left.columns = [col.replace("_left", "") for col in df_left.columns]
    df_right = df[right_columns]
    df_right.columns = [col.replace("_right", "") for col in df_right.columns]

    return df_left, df_right


def read_data(filename):
    """Find data files from the os data path and read the data

    Args:
        param path: A string with the path to the data files

    Returns:
    DataFrame with the data
    """
    print("reading data file", filename)
    try:
        df = pd.read_csv(filename, sep=",", header=None)
        print(f"{len(df.columns)} columns found")
        if len(df.columns) > 24:
            print("File too large, use read_combined_file() instead")

        if len(df.columns) == 23:
            df.columns = [
                "time",
                "raw_1",
                "raw_2",
                "raw_3",
                "raw_4",
                "raw_5",
                "raw_6",
                "raw_7",
                "raw_8",
                "raw_9",
                "raw_10",
                "raw_11",
                "raw_12",
                "raw_13",
                "raw_14",
                "acc_x",
                "acc_y",
                "acc_z",
                "gyro_x",
                "gyro_y",
                "gyro_z",
                "Session_no",
                "Timestamp",
            ]
            df["time"] = np.arange(0, len(df["raw_1"])) / 20

        elif len(df.columns) == 24:
            df.columns = [
                "time",
                "raw_1",
                "raw_2",
                "raw_3",
                "raw_4",
                "raw_5",
                "raw_6",
                "raw_7",
                "raw_8",
                "raw_9",
                "raw_10",
                "raw_11",
                "raw_12",
                "raw_13",
                "raw_14",
                "acc_x",
                "acc_y",
                "acc_z",
                "gyro_x",
                "gyro_y",
                "gyro_z",
                "Session_no",
                "Timestamp",
                "battery",
            ]
            df["time"] = np.arange(0, len(df["raw_1"])) / 20
            df = df.drop(["battery"], axis=1)

        elif len(df.columns) == 17:
            df.columns = [
                "time",
                "raw_1",
                "raw_2",
                "raw_3",
                "raw_4",
                "raw_5",
                "raw_6",
                "raw_7",
                "raw_8",
                "raw_9",
                "raw_10",
                "raw_11",
                "raw_12",
                "raw_13",
                "raw_14",
                "acc_x",
                "acc_y",
            ]
            df.insert(17, "acc_z", 0)
            df.insert(18, "gyro_x", 0)
            df.insert(19, "gyro_y", 0)
            df.insert(20, "gyro_z", 0)
            df.insert(21, "Timestamp", 0)

        elif len(df.columns) == 21:
            df.columns = [
                "raw_1",
                "raw_2",
                "raw_3",
                "raw_4",
                "raw_5",
                "raw_6",
                "raw_7",
                "raw_8",
                "raw_9",
                "raw_10",
                "raw_11",
                "raw_12",
                "raw_13",
                "raw_14",
                "acc_x",
                "acc_y",
                "acc_z",
                "gyro_x",
                "gyro_y",
                "gyro_z",
                "Timestamp",
            ]
            df.insert(0, "time", (np.arange(0, len(df["raw_1"])) / 20))

        # Substitute negative signals with 0 in raw columns
        raw_columns = [col for col in df.columns if col.startswith("raw_")]
        df[raw_columns] = df[raw_columns].clip(lower=0)

        return df

    except:
        print("No data found")
        return pd.DataFrame()


def convert_to_pressure(data, regression_coefficients):
    """Convert the data to the pressure.

    Args:
        param data: DataFrame with the data
        param regression_coefficients: Coefficients of the pressure regression
    """
    pressure_data = (
        data[
            [
                "raw_1",
                "raw_2",
                "raw_3",
                "raw_4",
                "raw_5",
                "raw_6",
                "raw_7",
                "raw_8",
                "raw_9",
                "raw_10",
                "raw_11",
                "raw_12",
                "raw_13",
                "raw_14",
            ]
        ]
        * regression_coefficients
    )
    for col in data.columns:
        if col in [
            "time",
            "acc_x",
            "acc_y",
            "acc_z",
            "gyro_x",
            "gyro_y",
            "gyro_z",
            "Timestamp",
        ]:
            pressure_data[col] = data[col]

    return pressure_data


def convert_signal(data, type):
    if type == "acc":
        x = data[["acc_x", "acc_y", "acc_z"]]
        # data = data.iloc[:, 14:17]
        return x * 9.81 / 4096

    if type == "acc_total":
        x = data[["acc_x", "acc_y", "acc_z"]]
        x = np.sqrt((x["acc_x"] / 4096 * 9.81) ** 2 + (x["acc_y"] / 4096 * 9.81) ** 2 + (x["acc_z"] / 4096 * 9.81) ** 2) - 9.81
        return x

    if type == "gyro":
        x = data[["gyro_x", "gyro_y", "gyro_z"]]
        # data = data.iloc[:, 17:20]
        return x / 16.2

    if type == "gyro_total":
        x = data[["gyro_x", "gyro_y", "gyro_z"]]
        x = np.sqrt((x["gyro_x"] / 16.2) ** 2 + (x["gyro_y"] / 16.2) ** 2 + (x["gyro_z"] / 16.2) ** 2)
        return x

    if type == "pressure":
        x = data[
            [
                "raw_1",
                "raw_2",
                "raw_3",
                "raw_4",
                "raw_5",
                "raw_6",
                "raw_7",
                "raw_8",
                "raw_9",
                "raw_10",
                "raw_11",
                "raw_12",
                "raw_13",
                "raw_14",
            ]
        ]
        return x.mean(axis=1)


def get_overall_signal(data, signal):
    if signal == "acc":
        data["Total Acc"] = np.sqrt((np.square(data["acc_x"]) + np.square(data["acc_y"]) + np.square(data["acc_z"]))) - 9.81
        # data = data.iloc[:, 14:17]
        return data

    if signal == "gyro":
        data["Total Gyro"] = np.sqrt((np.square(data["gyro_x"]) + np.square(data["gyro_y"]) + np.square(data["gyro_z"])))
        # data = data.iloc[:, 17:20]
        return data


def butter_lowpass_filter(signal, cutoff=5, fs=20, order=4):
    """Return a low-pass filtered signal."""
    nyq = 0.5 * fs  # Nyquist frequency
    normal_cutoff = cutoff / nyq  # Normalize the cutoff
    b, a = butter(order, normal_cutoff, btype="low", analog=False)  # Filter coefficients
    y = filtfilt(b, a, signal)  # Filter the signal
    return y
