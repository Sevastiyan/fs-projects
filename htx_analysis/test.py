import os

from utils.data_loader import load_combined_file, convert_signal
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import re
from datetime import datetime, timedelta
from scipy.signal import find_peaks

root_folder = "./htx_analysis"
subjects = ["P1"]
dates_to_include = [
    "2024-04-02",
]


def main():
    files = {}
    for subject in subjects:
        root = f"{root_folder}/data/{subject}"
        dates = os.listdir(root)
        for day in dates:
            if day not in dates_to_include:
                continue
            files[day] = []
            for file in os.listdir(f"{root}/{day}"):
                files[day].append(os.path.join(root, day, file))

    df_left, df_right = load_combined_file(files["2024-04-02"][0], filter=True, cutoff=2)
    my_date = df_left["ms"].iloc[-1]
    # convert my_date variable to iso 8601 format
    print(my_date)
    date_object = datetime.strptime(my_date, "%Y-%m-%d %H:%M:%S.%f")
    date_utc = date_object - timedelta(hours=8)
    print(date_utc)
    date_string = date_utc.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    print(date_string)
    print(my_date)
    print(df_left.columns)
    x = convert_signal(df_left, "acc_total")
    print(df_left.head())


if __name__ == "__main__":
    main()
