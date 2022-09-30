import numpy as np

def min_max(data):
    """
    Normalize the data to the range [0, 1].
    """
    return (data - np.min(data)) / (np.max(data) - np.min(data)).tolist()
