import os
import utils.cop as Cop
from utils.data_loader import load_file, convert_signal
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import re
from scipy.signal import find_peaks


# -------------- root variables for folders and file location - -------------- #
root_folder = "./COP analysis"
subjects = ["htx02"]


left_data_list = []
right_data_list = []


# ----------------------------------- Main ----------------------------------- #
def main():
    for subject in subjects:
        left_data_list.clear()
        right_data_list.clear()
        files = {}
        root = f"{root_folder}/data/{subject}"
        dates = os.listdir(root)

        for day in dates:
            if day.endswith(".zip"):
                continue
            if day.startswith("2024-04-02"):
                files[day] = []
                for file in os.listdir(f"{root}/{day}"):
                    files[day].append(os.path.join(root, day, file))

        for date in files.keys():
            print(f"--- Starting analysis for {date} ---")
            start_analysis(files[date], date, 0.01)

        # Create pandas DataFrames for left and right sides
        left_df = pd.DataFrame(left_data_list)
        right_df = pd.DataFrame(right_data_list)
        print(left_df.head(15))

        right_df.to_csv(f"{subject}_right_aws.csv")
        left_df.to_csv(f"{subject}_left_aws.csv")


def start_analysis(data, date, freq):
    time = {}
    filt_signal = {}
    acc = {}
    mask = {}

    for file_set in range(0, len(data), 2):
        # Data load
        file_left = data[file_set]
        file_right = data[file_set + 1]
        match = re.search(r"S(\d+)_", file_left)
        session = match.group(1)
        left_data = load_file(file_left, filter=True, cutoff=2)
        right_data = load_file(file_right, filter=True, cutoff=2)

        # ---------------------------- Pre-processing Data --------------------------- #
        side = "left"
        time[side] = [x * freq for x in range(len(left_data))]
        filt_signal[side] = convert_signal(left_data, "pressure")
        acc[side] = convert_signal(left_data, "acc_total")
        mask[side] = generate_mask(acc[side], freq)

        side = "right"
        time[side] = [x * freq for x in range(len(right_data))]
        filt_signal[side] = convert_signal(right_data, "pressure")
        acc[side] = convert_signal(right_data, "acc_total")
        mask[side] = generate_mask(acc[side], freq)

        activity_input_left = left_data[mask["left"]].reset_index()
        activity_input_right = right_data[mask["right"]].reset_index()

        # ---------------------- Check if the activity is enough --------------------- #
        if len(activity_input_left) * freq / 60 < 0.1 or len(activity_input_right) * freq / 60 < 0.1:  #! Check if this works
            print("length of data", int(len(mask["left"]) * freq / 60 < 2), int(len(mask["right"]) * freq / 60 < 2), "< 2 minutes")
            left_data_list.append(generate_dummy(file_left, date.split(" ")[0], session))
            right_data_list.append(generate_dummy(file_right, date.split(" ")[0], session))

            continue

        # ------------------------------- Peak Finding ------------------------------- #
        filt_c = Cop.CenterOfPressure([activity_input_left, activity_input_right])

        cop = {}
        peaks = {}

        prom = 10
        dist = 12

        # -------------------------------------- Left Side ------------------------------------- #
        side = "left"
        cop[side] = filt_c.get_cop_foot(side)
        time[side] = [x * freq for x in range(len(cop[side][0]))]

        xl = cop[side][1]
        peaks[side] = {}
        peaks[side]["positive"], _ = find_peaks(xl, prominence=prom, distance=dist)
        peaks[side]["negative"], _ = find_peaks(-xl, prominence=prom, distance=dist)

        l_timings, l_pairs = gait_timings(peaks[side]["positive"], peaks[side]["negative"], freq)
        l_velocity = find_cop_velocity(xl, l_timings["step"], l_pairs["step"])

        # Create dictionaries for left and right sides
        cadence = len(peaks[side]["positive"]) / (len(activity_input_left) * freq / 60) * 2  # ? *2 for both feet
        left_data = {
            # 'File': file_left,
            "session": session,
            "activity_time": len(activity_input_left) * freq / 60,
            "step_time": np.mean(l_timings["step"]),
            "swing_time": np.mean(l_timings["swing"]),
            "stride_time": np.mean(l_timings["stride"]),
            "total_steps": len(peaks[side]["positive"]),
            "cadence": cadence,
            "step_variability": np.std(l_timings["step"]),
            "stride_variability": np.std(l_timings["stride"]),
            "cop_speed": np.median(l_velocity) * 2 / 100,
            # "Avg_COP_Speed": np.mean(l_velocity) / 100,
        }

        # ------------------------------------- Right Side ------------------------------------- #
        side = "right"
        cop[side] = filt_c.get_cop_foot(side)
        time[side] = [x * freq for x in range(len(cop[side][0]))]

        xr = cop[side][1]
        peaks[side] = {}
        peaks[side]["positive"], _ = find_peaks(xr, prominence=prom, distance=dist)
        peaks[side]["negative"], _ = find_peaks(-xr, prominence=prom, distance=dist)

        r_timings, r_pairs = gait_timings(peaks[side]["positive"], peaks[side]["negative"], freq)
        r_velocity = find_cop_velocity(xr, r_timings["step"], r_pairs["step"])

        cadence = len(peaks[side]["positive"]) / (len(activity_input_right) * freq / 60) * 2  # ? *2 for both feet
        right_data = {
            # 'File': file_right,
            "session": session,
            "activity_time": len(activity_input_right) * freq / 60,
            "step_time": np.mean(r_timings["step"]),
            "swing_time": np.mean(r_timings["swing"]),
            "stride_time": np.mean(r_timings["stride"]),
            "total_steps": len(peaks[side]["positive"]) * 2,
            "cadence": cadence,
            "step_variability": np.std(r_timings["step"]),
            "stride_variability": np.std(r_timings["stride"]),
            "cop_speed": np.median(r_velocity) * 2 / 100,
            # "Avg_COP_Speed": np.mean(r_velocity) / 100,
        }

        # Append dictionaries to the respective lists
        left_data_list.append(left_data)
        right_data_list.append(right_data)

    return


# ---------------------------------------------------------------------------- #
#                               HELPING FUNCTIONS                              #
# ---------------------------------------------------------------------------- #


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


if __name__ == "__main__":
    main()
