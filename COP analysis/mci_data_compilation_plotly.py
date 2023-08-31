from utils.data_loader import load_file, convert_signal
from plotly.subplots import make_subplots
from scipy.signal import find_peaks
import os
import utils.cop as Cop
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

root_folder = './COP analysis'
subject = 'mci002'
prom = 10
dist = 18

files = {}
subplot_titles = []
root = f'{root_folder}/data/{subject}'
for d in os.listdir(root):
    files[d] = []
    for file in os.listdir(f'{root}/{d}'):
        files[d].append(os.path.join(root, d, file))


def main():
    keys = list(files.keys())
    for date in keys:
        data = files[date]
        time = {}
        raw_signal = {}
        filt_signal = {}
        acc = {}
        mask = {}

        row = 1
        row_cop = 1
        fig = make_subplots(
            rows=len(data),
            cols=2,
            # subplot_titles=subplot_titles
        )

        fig_cop = make_subplots(
            rows=int(len(data) / 2),
            cols=2,
        )
        for i in range(0, len(data) - 1, 2):
            print('Starting Plot for', data[i])

            # --------------------------------- Data Load -------------------------------- #
            raw_left = load_file(data[i], filter=False)
            raw_right = load_file(data[i + 1], filter=False)
            filter_left = load_file(data[i], filter=True, cutoff=2)
            filter_right = load_file(data[i + 1], filter=True, cutoff=2)

            # --------------------------------- Left Side -------------------------------- #
            side = 'left'
            time[side] = [x * 0.05 for x in range(len(raw_left))]
            raw_signal[side] = convert_signal(raw_left, 'pressure')
            filt_signal[side] = convert_signal(filter_left, 'pressure')
            acc[side] = convert_signal(filter_left, 'acc_total')
            mask[side] = generate_mask(acc[side])

            fig.add_trace(
                go.Scatter(
                    x=time[side],
                    y=raw_signal[side],
                    name=f'{side} signal',
                    marker=dict(color='royalblue'),
                ),
                row=row,
                col=1,
            )
            fig.add_trace(
                go.Scatter(
                    x=time[side],
                    y=filt_signal[side],
                    name=f"{side} filter",
                    marker=dict(color='orange'),
                ),
                row=row,
                col=1,
            )
            fig.add_trace(
                go.Scatter(
                    x=time[side],
                    y=acc[side],
                    name=f"{side} acc",
                    marker=dict(color='royalblue'),
                ),
                row=row + 1,
                col=1,
            )
            fig.add_trace(
                go.Scatter(
                    x=time[side],
                    y=mask[side] * 40,
                    name=f"{side} mask",
                    marker=dict(color='green'),
                ),
                row=row + 1,
                col=1,
            )

            # -------------------------------- Right Side -------------------------------- #
            side = 'right'
            time[side] = [x * 0.05 for x in range(len(raw_right))]
            raw_signal[side] = convert_signal(raw_right, 'pressure')
            filt_signal[side] = convert_signal(filter_right, 'pressure')
            acc[side] = convert_signal(filter_right, 'acc_total')
            mask[side] = generate_mask(acc[side])

            fig.add_trace(
                go.Scatter(
                    x=time[side],
                    y=raw_signal[side],
                    name=f'{side} signal',
                    marker=dict(color='royalblue'),
                ),
                row=row,
                col=2,
            )
            fig.add_trace(
                go.Scatter(
                    x=time[side],
                    y=filt_signal[side],
                    name=f"{side} filter",
                    marker=dict(color='orange'),
                ),
                row=row,
                col=2,
            )
            fig.add_trace(
                go.Scatter(
                    x=time[side],
                    y=acc[side],
                    name=f"{side} acc",
                    marker=dict(color='royalblue'),
                ),
                row=row + 1,
                col=2,
            )
            fig.add_trace(
                go.Scatter(
                    x=time[side],
                    y=mask[side] * 40,
                    name=f"{side} mask",
                    marker=dict(color='green'),
                ),
                row=row + 1,
                col=2,
            )

            # ------------------------------- Figure Format ------------------------------ #
            fig.update_xaxes(title_text="Time [s]", row=row, col=1)
            fig.update_xaxes(title_text="Time [s]", row=row, col=2)
            fig.update_xaxes(title_text="Time [s]", row=row + 1, col=1)
            fig.update_xaxes(title_text="Time [s]", row=row + 1, col=2)
            fig.update_yaxes(title_text="Pressure", range=[-10, 200], row=row, col=1)
            fig.update_yaxes(title_text="Pressure", range=[-10, 200], row=row, col=2)
            fig.update_yaxes(
                title_text="Acceleration", range=[-5, 50], row=row + 1, col=1
            )
            fig.update_yaxes(
                title_text="Acceleration", range=[-5, 50], row=row + 1, col=2
            )

            # ------------------------------------ COP ----------------------------------- #
            print('Calculating COP...')
            input_left = filter_left[mask['left']].reset_index()
            input_right = filter_right[mask['right']].reset_index()
            c = Cop.CenterOfPressure([input_left, input_right])

            cop = {}
            peaks = {}

            side = "left"
            cop[side] = c.get_cop_foot(side)
            time[side] = [x * 0.05 for x in range(len(cop[side][0]))]

            xl = cop[side][1]
            peaks[side] = {}
            peaks[side]["positive"], _ = find_peaks(xl, prominence=prom, distance=dist)
            peaks[side]["negative"], _ = find_peaks(-xl, prominence=prom, distance=dist)

            fig_cop.add_trace(
                go.Scatter(
                    x=np.arange(xl.shape[0]),
                    y=xl,
                    name='COP',
                    marker=dict(color='blue'),
                ),
                row=row_cop,
                col=1,
            )
            fig_cop.add_trace(
                go.Scatter(
                    x=peaks[side]['positive'],
                    y=xl[peaks[side]['positive']],
                    name='Toe Off',
                    mode="markers",
                    marker=dict(color='red'),
                ),
                row=row_cop,
                col=1,
            )
            fig_cop.add_trace(
                go.Scatter(
                    x=peaks[side]['negative'],
                    y=xl[peaks[side]['negative']],
                    name='Heel Strike',
                    mode="markers",
                    marker=dict(color='green'),
                ),
                row=row_cop,
                col=1,
            )

            side = "right"
            cop[side] = c.get_cop_foot(side)
            time[side] = [x * 0.05 for x in range(len(cop[side][0]))]

            xr = cop[side][1]
            peaks[side] = {}
            peaks[side]["positive"], _ = find_peaks(xr, prominence=prom, distance=dist)
            peaks[side]["negative"], _ = find_peaks(-xr, prominence=prom, distance=dist)

            fig_cop.add_trace(
                go.Scatter(
                    x=np.arange(xr.shape[0]),
                    y=xr,
                    name='COP',
                    marker=dict(color='blue'),
                ),
                row=row_cop,
                col=2,
            )
            fig_cop.add_trace(
                go.Scatter(
                    x=peaks[side]['positive'],
                    y=xr[peaks[side]['positive']],
                    name='Toe Off',
                    mode="markers",
                    marker=dict(color='red'),
                ),
                row=row_cop,
                col=2,
            )
            fig_cop.add_trace(
                go.Scatter(
                    x=peaks[side]['negative'],
                    y=xr[peaks[side]['negative']],
                    name='Heel Strike',
                    mode="markers",
                    marker=dict(color='green'),
                ),
                row=row_cop,
                col=2,
            )

            row_cop = row_cop + 1
            row = row + 2

        # Save Plots
        print('-------------- Saving Figures -------------')
        plots_path = f'{root_folder}/plots/{subject}/{date}'
        if not os.path.isdir(plots_path):
            os.makedirs(plots_path)

        fig.update_layout(title=f'{subject}: {date}')
        fig_cop.update_layout(title=f'{subject}: {date}')
        fig.update_layout(
            title=date, height=row * 300, showlegend=True, yaxis_range=[-100, 100]
        )
        fig_cop.update_layout(
            title=date, height=row * 300, showlegend=True, yaxis_range=[-100, 100]
        )
        # fig.show()
        fig.write_html(f'{plots_path}/activity.html')
        fig_cop.write_html(f'{plots_path}/center_of_pressure.html')


def generate_mask(signal, threshold=5):
    print('Generating Mask...')
    freq = 0.05
    seconds = 3
    window = int(seconds / freq)
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

    return np.array([True if x < window else False for x in count])


if __name__ == "__main__":
    main()
