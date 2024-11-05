import os
import utils.cop as Cop
from utils.data_loader import load_file, convert_signal
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import re
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
from utils.filters import butter_lowpass_filter


prom = 1.5
dist = 12
freq = 0.05
chunk_size = 100 * 30  # Size of each chunk in terms of rows
isoFormat = "%Y-%m-%d %H:%M:%S.%f"

# -------------- root variables for folders and file location - -------------- #
root_folder = "./MCI analysis"
subjects = ["mci015"]

left_data_list = []
right_data_list = []


def main():
    for subject in subjects:
        left_data_list.clear()
        right_data_list.clear()
        files = {}
        root = f"{root_folder}/data/mci_raw_data/{subject}"
        dates = os.listdir(root)

        for day in dates:
            if day.endswith(".zip"):
                continue
            files[day] = []
            for file in os.listdir(f"{root}/{day}"):
                files[day].append(os.path.join(root, day, file))

        for date in files.keys():
            print(f"--- Starting analysis for {date} ---")
            start_analysis(files[date], date)

        # Create pandas DataFrames for left and right sides
        left_df = pd.DataFrame(left_data_list)
        right_df = pd.DataFrame(right_data_list)
        print(left_df.head(15))

        right_df.to_csv(f"{root_folder}/data/compiled_data/{subject}_right_df.csv")
        left_df.to_csv(f"{root_folder}/data/compiled_data/{subject}_left_df.csv")


def start_analysis(data, date, freq=0.05):
    for file_set in range(0, len(data), 2):
        # Data load
        mask = {}
        acc = {}

        file_left = data[file_set]
        file_right = data[file_set + 1]
        match = re.search(r"S(\d+)_", file_left)
        session = match.group(1)

        l_data = load_file(file_left, filter=True, cutoff=2)
        acc["left"] = convert_signal(l_data, "acc_total")
        mask["left"] = generate_mask(acc["left"], freq)
        r_data = load_file(file_right, filter=True, cutoff=2)
        acc["right"] = convert_signal(r_data, "acc_total")
        mask["right"] = generate_mask(acc["right"], freq)

        left_data = l_data[mask["left"]].reset_index()
        right_data = r_data[mask["right"]].reset_index()

        cop = Cop.CenterOfPressure([left_data.reset_index(), right_data.reset_index()])

        if len(left_data) * 0.05 / 60 < 0.1 or len(right_data) * 0.05 / 60 < 0.1:  #! Check if this works
            print("length of data", len(mask["left"]), len(mask["right"]))
            left_data_list.append(generate_dummy(file_left, date.split(" ")[0], session))
            right_data_list.append(generate_dummy(file_right, date.split(" ")[0], session))
            continue

        left_result = process_side(left_data, cop, "left")
        right_result = process_side(right_data, cop, "right")

        print("Pairs Lengths: ", len(left_result["pairs"]["step"]), len(right_result["pairs"]["step"]))

        if len(left_result["pairs"]["step"]) >= 2 and len(right_result["pairs"]["step"]) >= 2:
            # Single / Double Support calculation
            lsm = step_mask(left_result["pairs"], len(data[0]))
            rsm = step_mask(right_result["pairs"], len(data[0]))

            lss = np.logical_and(lsm, np.logical_not(rsm)).astype(int)
            rss = np.logical_and(rsm, np.logical_not(lsm)).astype(int)
            double_support = np.logical_and(lsm, rsm).astype(int)

            left_support_len = len(left_result["pairs"]["step"])
            right_support_len = len(right_result["pairs"]["step"])

            left_result.update(
                {
                    "single_support": np.sum(lss) / left_support_len * freq,
                    "double_support": np.sum(double_support) / left_support_len * freq,
                }
            )

            right_result.update(
                {
                    "single_support": np.sum(rss) / right_support_len * freq,
                    "double_support": np.sum(double_support) / right_support_len * freq,
                }
            )
        else:
            # Set supports to 0 if pairs length is less than 2
            for result in [left_result, right_result]:
                result.update(
                    {
                        "double_support": 0,
                        "single_support": 0,
                        "pairs": {},
                    }
                )

        # average_result = {key: np.mean([left_result[key], right_result[key]]) for key in left_result if key != "pairs"}
        left_result["session"] = session
        right_result["session"] = session

        left_data_list.append(left_result)
        right_data_list.append(right_result)

    return left_data_list, right_data_list


# ---------------------------------------------------------------------------- #
#                               HELPING FUNCTIONS                              #
# ---------------------------------------------------------------------------- #


def process_side(data, cop_data, side):
    cop = cop_data.get_cop_foot(side)
    x = cop[1]
    # x = butter_lowpass_filter(x, cutoff=2, fs=20, order=5)
    peaks_positive, _ = find_peaks(x, prominence=prom, distance=dist)
    peaks_negative, _ = find_peaks(-x, prominence=prom, distance=dist)

    # Check if there are at least two pairs
    # if len(peaks_positive) >= 2 and len(peaks_negative) >= 2:
    timings, pairs = gait_timings(peaks_positive, peaks_negative, freq)
    velocity = find_cop_velocity(x, timings["step"], pairs["step"])
    cadence = len(peaks_positive) * 2 / (len(data) * freq) * 60

    if len(peaks_positive) >= 2 and len(peaks_negative) >= 2:
        result = {
            "activity_time": int(len(data) * freq),
            "step_time": np.mean(timings["step"]),
            "swing_time": np.mean(timings["swing"]),
            "stride_time": np.mean(timings["stride"]),
            "total_steps": len(peaks_positive) * 2,
            "cadence": cadence,
            "step_variability": np.std(timings["step"]),
            "stride_variability": np.std(timings["stride"]),
            "cop_speed": np.median(velocity) * 2 / 100,
            "pairs": pairs,
        }
    else:
        # Handle case where there are not enough peaks
        result = {
            "activity_time": int(len(data) * freq),
            "step_time": 0,  # Provide default value
            "swing_time": 0,  # Provide default value
            "stride_time": 0,  # Provide default value
            "total_steps": len(peaks_positive) * 2,  # Provide default value
            "cadence": cadence,  # Provide default value
            "step_variability": 0,  # Provide default value
            "stride_variability": 0,  # Provide default value
            "cop_speed": 0,  # Provide default value
            "pairs": {"step": [], "swing": [], "stride": []},  # Provide default value
        }

    return result


# ---------------------------------------- Plots --------------------------------------- #

# fig, axs = plt.subplots(2, 1, figsize=(10, 7))

# # First subplot
# axs[0].plot(convert_signal(nf_data.reset_index(), 'pressure'), label='pressure')
# axs[0].plot(convert_signal(data.reset_index(), 'pressure'), label='filtered pressure')
# # add the peaks (positive and negative)
# axs[0].set_xlabel('Time')
# axs[0].set_ylabel('Pressure')
# axs[0].grid(True)
# axs[0].set_title(f'Pressure Graph {side}: {chunk_number} / {chunks_length} ')
# axs[0].legend(loc='upper right')

# axs[1].plot(cop[1], label='COP')  # Unfiltered COP
# axs[1].plot(x, label='filter COP')  # Adjust x and y accordingly
# # add the peaks (positive and negative)
# axs[1].plot(peaks_positive, x[peaks_positive], "o", linewidth=3, label='toe lift')
# axs[1].plot(peaks_negative, x[peaks_negative], "o", linewidth=3, label='heel strike')
# axs[1].set_xlabel('Time')
# axs[1].set_ylabel('COP position [mm]')
# axs[1].grid(True)
# axs[1].set_title('COP Graph')
# axs[1].legend(loc='upper right')

# plt.tight_layout()
# plt.show()

# return result


def calculate_gait_speed(timings, pairs, acc_data=[]):
    """
    Calculates the gait speed based on the step and stride times and the acceleration signal
    """
    step_time = timings["step"]
    stride_time = timings["stride"]
    step_idx = pairs["step"]
    stride_idx = pairs["stride"]

    if len(step_time) == 0 or len(stride_time) == 0 or len(step_idx) == 0 or len(stride_idx) == 0:
        return {
            "gait_speed": 0,
            "gait_speed_error": 0,
            "gait_speed_samples": 0,
        }

    acc_samples = len(acc_data[0])

    step_samples = step_idx[-1] - step_idx[0] + 1
    stride_samples = stride_idx[-1] - stride_idx[0] + 1

    gait_speed = 0
    gait_speed_error = 0
    gait_speed_samples = 0
    for i in range(len(step_idx)):
        if i + 1 < len(step_idx):
            step_start = step_idx[i]
            step_end = step_idx[i + 1]
            stride_start = stride_idx[i]
            stride_end = stride_idx[i + 1]
            step_mean = np.mean(acc_data[0][step_start:step_end])
            stride_mean = np.mean(acc_data[0][stride_start:stride_end])
            gs = np.abs(stride_mean - step_mean)
            gs_error = np.std(acc_data[0][step_start:step_end])
            gait_speed += gs
            gait_speed_error += gs_error
            gait_speed_samples += 1

    gait_speed /= gait_speed_samples
    gait_speed_error /= gait_speed_samples

    print("Gait Speed:", gait_speed, "Gait Speed Error:", gait_speed_error)

    return {
        "gait_speed": gait_speed,
        "gait_speed_error": gait_speed_error,
        "gait_speed_samples": gait_speed_samples,
    }


# TODO: Transfer to utils
def generate_mask(signal, freq, threshold=7, seconds=3):
    print("Generating Mask...")
    window = int(seconds / freq)
    active = False
    c = window + 1  # to start with no activity
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


def gait_timings(positive, negative, freq):
    pairs = {"step": [], "swing": [], "stride": []}
    timings = {"step": [], "swing": [], "stride": []}

    for n in negative:
        for p in positive:
            if n < p:
                time = abs(p - n)
                pairs["step"].append((n, p))
                timings["step"].append(time * freq)
                break

    for p in positive:
        for n in negative:
            if n > p:
                time = abs(n - p)
                pairs["swing"].append((p, n))
                timings["swing"].append(time * freq)
                break

    for i in range(len(negative) - 1):
        time = abs(negative[i] - negative[i + 1])
        pairs["stride"].append((negative[i], negative[i + 1]))
        timings["stride"].append(time * freq)

    return timings, pairs


def find_cop_velocity(data, time, peaks):
    velocity_array = []

    for i in range(len(time)):
        n, p = peaks[i]
        velocity_array.append((data[p] - data[n]) / time[i])
    return velocity_array


def calculate_gait_speed(timings, pairs, freq, acc_data=[]):
    gait_velocities = []
    print("gait Speed Data Input", len(timings), len(pairs))
    for i in range(len(pairs["stride"])):
        start_idx, end_idx = pairs["stride"][i]
        acc_window = acc_data[start_idx:end_idx]  # Extract acceleration data within the window

        time_steps = timings["stride"][i] / len(acc_window)  # Calculate time step

        # Numerical integration using trapezoidal rule
        velocity = abs(np.diff(acc_window))
        sum_velocity = np.cumsum(velocity)
        mean_velocity = np.mean(velocity)
        # integrated_velocity = np.trapz(acc_window, dx=0freq)
        integrated_velocity = np.trapz(acc_window, dx=freq)
        gait_velocities.append(integrated_velocity)

    print(len(gait_velocities))
    return gait_velocities


def get_cov(array):
    # cv =  lambda x: np.std(x) / np.mean(x)
    # var = np.apply_along_axis(cv, axis=0, arr=array)
    # idmax = np.argmax(var)
    return np.std(array) / np.mean(array)


def find_rhythm(l_timings, r_timings):
    step_time_acf = np.correlate(l_timings["step"], r_timings["step"], mode="full")  # acf - Auto Correlation Function
    stride_time_acf = np.correlate(l_timings["stride"], r_timings["stride"], mode="full")  # acf - Auto Correlation Function
    step_time_acf = step_time_acf / np.max(step_time_acf)
    stride_time_acf = stride_time_acf / np.max(stride_time_acf)
    step_time_rhythm = step_time_acf[len(step_time_acf) // 2]
    stride_time_rhythm = step_time_acf[len(step_time_acf) // 2]
    return step_time_rhythm, stride_time_rhythm


def generate_dummy(file, date, session):
    return {
        # 'File': file,
        "Session": session,
    }


def step_mask(side_pairs, chunk_length):
    mask_list = []
    for i in range(len(side_pairs["step"])):
        if i == 0:
            temp = [0] * side_pairs["step"][i][0]
            mask_list.extend(temp)
            temp = [1] * (side_pairs["step"][i][1] - side_pairs["step"][i][0])
            mask_list.extend(temp)
        elif i == len(side_pairs["step"]) - 1:
            temp = [0] * (side_pairs["step"][i][0] - side_pairs["step"][i - 1][1])
            mask_list.extend(temp)
            temp = [1] * (side_pairs["step"][i][1] - side_pairs["step"][i][0])
            mask_list.extend(temp)
            if len(mask_list) < chunk_length:
                temp = [0] * (chunk_length - len(mask_list))
                mask_list.extend(temp)
        else:
            temp = [0] * (side_pairs["step"][i][0] - side_pairs["step"][i - 1][1])
            mask_list.extend(temp)
            temp = [1] * (side_pairs["step"][i][1] - side_pairs["step"][i][0])
            mask_list.extend(temp)
    if len(mask_list) < chunk_length:  # Add this block to ensure full extension
        temp = [0] * (chunk_length - len(mask_list))
        mask_list.extend(temp)
    return mask_list


def generate_dummy(file, date, session):
    return {
        # 'File': file,
        "Date": date,
        "Session": session,
    }


if __name__ == "__main__":
    context = None
    event = {
        "subject": "P5",
        "date": "20240417",
        "frequency": 0.01,
        "fileKeys": "./data/S010_20240412_rawData_P9_rest2.csv",
    }

    main()
