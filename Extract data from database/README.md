# MCI Analysis

This repository contains a Python script for analyzing Motor Control Index (MCI) data. The script downloads raw data from a MongoDB database, processes the data, and generates visualizations using Plotly.

## Table of Contents

- [MCI Analysis](#mci-analysis)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Modules](#modules)
  - [Functions](#functions)
    - [Main Script Functions](#main-script-functions)
    - [Plotly Analysis Functions](#plotly-analysis-functions)

## Installation

To run this project, you need to have Python 3.6 or higher installed. You also need to install the required packages. You can do this using pip:

```bash
pip install requests pymongo plotly numpy scipy
```

## Usage

1. Set the **SUBJECT** and **GLOBAL_DATE**: Modify the `SUBJECT` and `GLOBAL_DATE` variables in the main script to specify the subject and date you want to analyze.
2. Run the script: Execute the script using Python. This will download the necessary data files and generate the analysis plots.

```bash
python extract_directly_from_database.py
```

3. View the results: The generated plots will be saved in the `./plots/` directory under the respective subject and date.

## Modules
This project consists of the following main modules:

- **Main Script:** This script handles data collection from the MongoDB database and initiates the analysis process.
- **Plotly Analysis Module:** This module processes the downloaded data and generates visualizations using Plotly.


## Functions

### Main Script Functions

- `main():` Orchestrates the data collection and analysis process.
- `download_file(file, side, root_destination, base_url, subject):` Downloads a file from the specified URL and saves it to the destination path if it doesn't already exist.
- `modify_filename(file_name, side, subject):` Modifies the filename extracted from the URL for consistent naming.

### Plotly Analysis Functions

- `find_files(subject, dates):` Locates data files for a given subject and dates.
- `process_data(subject: str, dates: list[str]):` Processes data and generates activity and center of pressure plots.
- `generate_mask(signal, freq, threshold=7):` Generates a mask for activity detection based on the input signal.

- Global Variables:
  - `ROOT_FOLDER`: The root folder for the project.
  - `FREQ`: The sampling frequency for the data.
  - `PROMINENCE`: The threshold for detecting the center of pressure.
  - `DISTANCE`: The distance threshold for detecting the center of pressure.
