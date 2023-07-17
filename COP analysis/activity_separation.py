import os
import utils.cop as cop
from utils.data_loader import load_data, load_file, convert_signal
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def main():
    print('Script Start')
    print('------------')

    root_folder = './COP analysis'
    root = f'{root_folder}/data/2023-06-30 OneMinTests/'
    file_list = []
    for file in os.listdir(root):
        file_list.append(os.path.join(root, file))
    
    file_set = 0 * 2

    data_left = load_file(file_list[file_set], filter=True, cutoff=2.5)
    left_filter_signal = convert_signal(data_left, 'pressure')

    data_right = load_file(file_list[file_set + 1], filter=True, cutoff=2.5)
    right_filter_signal = convert_signal(data_right, 'pressure')

    print('Generating Mask...')

def generate_mask(file): 

    pass



if __name__ == '__main__':
    main()

