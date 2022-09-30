import os
import matplotlib.pyplot as plt
from utils.normalisation import min_max

def plot_data(data, borders, subdir, title=None, save=False):
    acc, acc_sliced = data

    # plot the sine wave in a subplot with the original and sliced sine wave
    # ggplot style
    plt.figure(figsize=[7,5])
    plt.style.use('seaborn-muted')
    # --------------------------------------------------
    plt.subplot(2, 1, 1).set_title(title)
    plt.plot(min_max(acc))
    # plt.plot(min_max(gyro))
    # add a vertical line corresponding to the slice
    plt.xticks([], [])
    plt.axvline(borders[0], color='r')
    plt.axvline(borders[1], color='r')
    plt.ylabel('Amplitude')
    # --------------------------------------------------
    plt.subplot(2, 1, 2).set_title(title + ' sliced')
    plt.plot(min_max(acc_sliced))
    # plt.plot(min_max(gyro_sliced))
    plt.xlabel('Time')
    plt.ylabel('Amplitude')

    path = os.path.join(os.getcwd(), 'graphs', subdir)

    if not os.path.exists(path):
        os.makedirs(path)

    if save:
        # make sure that the save directory exists
        plt.savefig(path + '\\' +  title + '.png')
    else: 
        plt.show()