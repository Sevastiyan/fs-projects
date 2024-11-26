import os
from typing import Dict, List, Tuple
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.signal import find_peaks
from utils.data_loader import load_file, convert_signal
from utils.filters import butter_lowpass_filter
import utils.cop as Cop
import matplotlib.pyplot as plt

# Global constants
FREQ = 0.01
PROMINENCE = 10
DISTANCE = 14
ROOT_FOLDER = "./Extract data from database"

def find_files(subject: str, dates: List[str]) -> Tuple[Dict, Dict, Dict]:
    files, subplot_titles, cop_subplot_titles = {}, {}, {}
    root = f"{ROOT_FOLDER}/data/{subject}"

    for d in os.listdir(root):
        if dates and d not in dates:
            continue
        files[d], subplot_titles[d], cop_subplot_titles[d] = [], [], []
        for file in os.listdir(f"{root}/{d}"):
            files[d].append(os.path.join(root, d, file))
            session_name = file.split('_')[0]
            cop_subplot_titles[d].append(f"{session_name} {'Left' if 'Left' in file else 'Right'}")
            act = "Activity and Mask" if len(cop_subplot_titles[d]) % 2 == 0 else "Pressure"
            subplot_titles[d].extend([f"{session_name} Left {act}", f"{session_name} Right {act}"])

    return files, subplot_titles, cop_subplot_titles

def process_side_data(data_file: str, side: str) -> Dict:
    raw_data = load_file(data_file, filter=False)
    filtered_data = load_file(data_file, filter=True, cutoff=2)

    time = [x * FREQ for x in range(len(raw_data))]
    raw_signal = convert_signal(raw_data, "pressure")
    filt_signal = convert_signal(filtered_data, "pressure")
    acc = convert_signal(filtered_data, "acc_total")
    mask = generate_mask(acc, FREQ)

    return {
        "time": time,
        "raw_signal": raw_signal,
        "filt_signal": filt_signal,
        "acc": acc,
        "mask": mask,
        "filtered_data": filtered_data
    }

def add_traces(fig: go.Figure, data: Dict, side: str, row: int, col: int):
    fig.add_trace(go.Scatter(x=data["time"], y=data["raw_signal"], name=f"{side} signal", marker=dict(color="royalblue")), row=row, col=col)
    fig.add_trace(go.Scatter(x=data["time"], y=data["filt_signal"], name=f"{side} filter", marker=dict(color="orange")), row=row, col=col)
    fig.add_trace(go.Scatter(x=data["time"], y=data["acc"], name=f"{side} acc", marker=dict(color="royalblue")), row=row+1, col=col)
    fig.add_trace(go.Scatter(x=data["time"], y=data["mask"] * 40, name=f"{side} mask", marker=dict(color="green")), row=row+1, col=col)

def process_cop(left_data: Dict, right_data: Dict) -> Dict:
    c = Cop.CenterOfPressure([left_data["filtered_data"][left_data["mask"]].reset_index(),
                              right_data["filtered_data"][right_data["mask"]].reset_index()])

    cop_data = {}
    for side in ["left", "right"]:
        cop = c.get_cop_foot(side)
        cop = butter_lowpass_filter(cop, cutoff=2, fs=100, order=4)
        x = cop[1]
        peaks = {
            "positive": find_peaks(x, prominence=PROMINENCE, distance=DISTANCE)[0],
            "negative": find_peaks(-x, prominence=PROMINENCE, distance=DISTANCE)[0]
        }
        cop_data[side] = {"cop": cop, "x": x, "peaks": peaks}

    return cop_data

def add_cop_traces(fig: go.Figure, cop_data: Dict, row: int, col: int):
    fig.add_trace(go.Scatter(x=np.arange(cop_data["x"].shape[0]), y=cop_data["x"], name="COP", marker=dict(color="blue")), row=row, col=col)
    fig.add_trace(go.Scatter(x=cop_data["peaks"]["positive"], y=cop_data["x"][cop_data["peaks"]["positive"]], name="Toe Off", mode="markers", marker=dict(color="red")), row=row, col=col)
    fig.add_trace(go.Scatter(x=cop_data["peaks"]["negative"], y=cop_data["x"][cop_data["peaks"]["negative"]], name="Heel Strike", mode="markers", marker=dict(color="green")), row=row, col=col)

def generate_mask(signal: np.ndarray, freq: float, threshold: float = 7) -> np.ndarray:
    window = int(3 / freq)
    active = False
    c = 100
    count = []

    for i, x in enumerate(signal):
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

    return np.array([x < window for x in count])

def process_data(subject: str, dates: List[str]):
    files, subplot_titles, cop_subplot_titles = find_files(subject, dates)

    for date in files.keys():
        fig = make_subplots(rows=len(files[date]), cols=2, subplot_titles=subplot_titles[date])
        fig_cop = make_subplots(rows=int(len(files[date]) / 2), cols=2, subplot_titles=cop_subplot_titles[date])

        row, row_cop = 1, 1
        for i in range(0, len(files[date]), 2):
            try:
                left_data = process_side_data(files[date][i], "left")
                right_data = process_side_data(files[date][i + 1], "right")

                add_traces(fig, left_data, "left", row, 1)
                add_traces(fig, right_data, "right", row, 2)

                cop_data = process_cop(left_data, right_data)
                add_cop_traces(fig_cop, cop_data["left"], row_cop, 1)

                # Matplotlib plot of cop
                plt.figure(figsize=(10, 5))
                plt.plot(cop_data["left"]["cop"][0], color="blue")
                plt.plot(cop_data["right"]["cop"][0], color="red")
                plt.show()

                add_cop_traces(fig_cop, cop_data["right"], row_cop, 2)

                row_cop += 1
                row += 2
            except Exception as e:
                print(f"Error processing {files[date][i]} or {files[date][i+1]}: {str(e)}")

        # Update layout and save figures
        plots_path = f"{ROOT_FOLDER}/plots/{subject}/{date}"
        os.makedirs(plots_path, exist_ok=True)

        for f, name in [(fig, "activity"), (fig_cop, "center_of_pressure")]:
            f.update_layout(title=f"{subject}: {date}", height=row * 300, showlegend=True, yaxis_range=[-100, 100])
            f.update_yaxes(range=[-100, 100])
            f.write_html(f"{plots_path}/{name}.html")

def main():
    subject = "htx4"
    dates_to_include = ["2024-08-20"]
    process_data(subject, dates_to_include)

if __name__ == "__main__":
    main()
