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


# -------------- root variables for folders and file location - -------------- #
root_folder = "./MCI analysis"
subjects = ["mci015"]

left_data_list = []
right_data_list = []


# ----------------------------------- Main ----------------------------------- #
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


def start_analysis(data, date):
    time = {}
    filt_signal = {}
    acc = {}
    mask = {}
    total_time = {}
    gait_speed = {
        "left": [],
        "right": [],
    }

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
        time[side] = [x * 0.05 for x in range(len(left_data))]
        total_time[side] = len(left_data) * 0.05
        filt_signal[side] = convert_signal(left_data, "pressure")
        acc[side] = convert_signal(left_data, "acc_total")
        mask[side] = generate_mask(acc[side])

        side = "right"
        time[side] = [x * 0.05 for x in range(len(right_data))]
        total_time[side] = len(right_data) * 0.05
        filt_signal[side] = convert_signal(right_data, "pressure")
        acc[side] = convert_signal(right_data, "acc_total")
        mask[side] = generate_mask(acc[side])

        activity_input_left = left_data[mask["left"]].reset_index()
        activity_input_right = right_data[mask["right"]].reset_index()

        # ---------------------- Check if the activity is enough --------------------- #
        if len(activity_input_left) * 0.05 / 60 < 0.8 or len(activity_input_right) * 0.05 / 60 < 0.8:  #! Check if this works
            print("length of data", len(mask["left"]), len(mask["right"]))
            left_data_list.append(generate_dummy(file_left, date.split(" ")[0], session))
            right_data_list.append(generate_dummy(file_right, date.split(" ")[0], session))
            continue

        # ------------------------------- Peak Finding ------------------------------- #

        filt_c = Cop.CenterOfPressure([activity_input_left, activity_input_right])

        cop = {}
        peaks = {}

        prom = 4
        dist = 14

        side = "left"
        cop[side] = filt_c.get_cop_foot(side)
        time[side] = [x * 0.05 for x in range(len(cop[side][0]))]

        xl = cop[side][1]
        xl = butter_lowpass_filter(xl, cutoff=2, fs=20, order=3)
        peaks[side] = {}
        peaks[side]["positive"], _ = find_peaks(xl, prominence=prom, distance=dist)
        peaks[side]["negative"], _ = find_peaks(-xl, prominence=prom, distance=dist)

        side = "right"
        cop[side] = filt_c.get_cop_foot(side)
        time[side] = [x * 0.05 for x in range(len(cop[side][0]))]

        xr = cop[side][1]
        xr = butter_lowpass_filter(xr, cutoff=2, fs=20, order=3)

        peaks[side] = {}
        peaks[side]["positive"], _ = find_peaks(xr, prominence=prom, distance=dist)
        peaks[side]["negative"], _ = find_peaks(-xr, prominence=prom, distance=dist)

        # fig, axs = plt.subplots(2, 1, figsize=(10, 7))

        # # First subplot
        # # axs[0].plot(convert_signal(nf_right, 'pressure'), label='pressure')
        # axs[0].plot(filt_signal[side], label="filtered pressure")  # Adjust x and y accordingly
        # # add the peaks (positive and negative)
        # axs[0].set_xlabel("Time")
        # axs[0].set_ylabel("Pressure")
        # axs[0].grid(True)
        # axs[0].set_title("Pressure Graph")
        # axs[0].legend(loc="upper right")

        # # Second subplot
        # axs[1].plot(cop[side][1], label="COP")  # Adjust x and y accordingly
        # axs[1].plot(xr, label="filter COP")  # Adjust x and y accordingly
        # # add the peaks (positive and negative)
        # axs[1].plot(peaks[side]["positive"], xr[peaks[side]["positive"]], "o", linewidth=3, label="toe lift")
        # axs[1].plot(peaks[side]["negative"], xr[peaks[side]["negative"]], "o", linewidth=3, label="heel strike")
        # axs[1].set_xlabel("Time")
        # axs[1].set_ylabel("COP position [mm]")
        # axs[1].grid(True)
        # axs[1].set_title("COP Graph")
        # axs[1].legend(loc="upper right")

        # plt.tight_layout()
        # plt.show()

        # ---------------------------------- Results --------------------------------- #

        side = "left"
        l_timings, l_pairs = gait_timings(peaks[side]["positive"], peaks[side]["negative"])
        l_velocity = find_cop_velocity(xl, l_timings["step"], l_pairs["step"])
        gait_speed[side] = calculate_gait_speed(l_timings, l_pairs, acc[side][mask[side]].reset_index().iloc[:, 1])
        # Create dictionaries for left and right sides
        cadence = len(peaks[side]["positive"]) / (len(activity_input_left) * 0.05 / 60) * 2  # ? *2 for both feet
        left_data = {
            # 'File': file_left,
            "Date": date.split(" ")[0],
            "Session": session,
            "Total_Time": total_time[side] / 60,
            "Total_Activity_Time_minutes": len(activity_input_left) * 0.05 / 60,
            "Avg_Step_Time": np.mean(l_timings["step"]),
            "Avg_Swing_Time": np.mean(l_timings["swing"]),
            "Avg_Stride_Time": np.mean(l_timings["stride"]),
            "Total_Steps": len(peaks[side]["positive"]),
            "Avg_Cadence": cadence,
            "Step_Time_Variability": np.std(l_timings["step"]) / np.mean(l_timings["step"]),
            "Stride_Time_Variability": np.std(l_timings["stride"]) / np.mean(l_timings["stride"]),
            "Median_COP_Speed": np.median(l_velocity) * 2 / 100,
            "Avg_COP_Speed": np.mean(l_velocity) / 100,
            "Avg_Gait_Speed": np.median(gait_speed[side]),
        }

        side = "right"
        r_timings, r_pairs = gait_timings(peaks[side]["positive"], peaks[side]["negative"])
        gait_speed[side] = calculate_gait_speed(r_timings, r_pairs, acc[side][mask[side]].reset_index().iloc[:, 1])
        r_velocity = find_cop_velocity(xr, r_timings["step"], r_pairs["step"])
        cadence = len(peaks[side]["positive"]) / (len(activity_input_right) * 0.05 / 60) * 2  # ? *2 for both feet

        right_data = {
            # 'File': file_right,
            "Date": date.split(" ")[0],
            "Session": session,
            "Total_Time": total_time[side] / 60,
            "Total_Activity_Time_minutes": len(activity_input_right) * 0.05 / 60,
            "Avg_Step_Time": np.mean(r_timings["step"]),
            "Avg_Swing_Time": np.mean(r_timings["swing"]),
            "Avg_Stride_Time": np.mean(r_timings["stride"]),
            "Total_Steps": len(peaks[side]["positive"]) * 2,
            "Avg_Cadence": cadence,
            "Step_Time_Variability": np.std(r_timings["step"]),
            "Stride_Time_Variability": np.std(r_timings["stride"]),
            "Median_COP_Speed": np.median(r_velocity) * 2 / 100,  #! Median vs mean | Also Keep in mind the 2.5 multiplier
            "Avg_COP_Speed": np.mean(r_velocity) / 100,
            "Avg_Gait_Speed": np.median(gait_speed[side]),
        }

        # step_rhythm, stride_rhythm = find_rhythm(l_timings, r_timings)

        # left_data["Step_Rhythm"] = step_rhythm
        # left_data["Stride_Rhythm"] = stride_rhythm

        # right_data["Step_Rhythm"] = step_rhythm
        # right_data["Stride_Rhythm"] = stride_rhythm

        # Append dictionaries to the respective lists
        left_data_list.append(left_data)
        right_data_list.append(right_data)

    return


# ---------------------------------------------------------------------------- #
#                               HELPING FUNCTIONS                              #
# ---------------------------------------------------------------------------- #


def generate_mask(signal, threshold=7):
    print("Generating Mask...")
    freq = 0.05
    seconds = 2
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


def gait_timings(positive, negative):
    pairs = {"step": [], "swing": [], "stride": []}
    timings = {"step": [], "swing": [], "stride": []}

    for n in negative:
        for p in positive:
            if n < p:
                time = abs(p - n)
                pairs["step"].append((n, p))
                timings["step"].append(time * 0.05)
                break

    for p in positive:
        for n in negative:
            if n > p:
                time = abs(n - p)
                pairs["swing"].append((p, n))
                timings["swing"].append(time * 0.05)
                break

    for i in range(len(negative) - 1):
        time = abs(negative[i] - negative[i + 1])
        pairs["stride"].append((negative[i], negative[i + 1]))
        timings["stride"].append(time * 0.05)

    return timings, pairs


def find_cop_velocity(data, time, peaks):
    velocity_array = []

    for i in range(len(time)):
        n, p = peaks[i]
        velocity_array.append((data[p] - data[n]) / time[i])

    return velocity_array


def calculate_gait_speed(timings, pairs, acc_data=[]):
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
        # integrated_velocity = np.trapz(acc_window, dx=0.05)
        integrated_velocity = np.trapz(acc_window, dx=0.05)
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
        "Date": date,
        "Session": session,
    }


if __name__ == "__main__":
    main()
