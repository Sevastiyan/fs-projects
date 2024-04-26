import os

from utils.data_loader import load_combined_file, convert_signal
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from scipy.signal import find_peaks
import shutil

root_folder = "./htx_analysis"
subjects = ["P1", "P2", "P3", "P4", "P5", "P6"]
dates_to_include = []


def main():
    for subject in subjects:
        root = f"{root_folder}/data/{subject}"
        dates = os.listdir(root)
        for day in dates:

            # Create new folder if it doesn't exist
            new_day_folder = f"{root_folder}/data/new_folder/{day}/{subject}"
            os.makedirs(new_day_folder, exist_ok=True)

            # Copy files to new folder
            for file in os.listdir(f"{root}/{day}"):
                source_file = os.path.join(root, day, file)
                destination_file = os.path.join(new_day_folder, file)
                shutil.copy(source_file, destination_file)


if __name__ == "__main__":
    main()
