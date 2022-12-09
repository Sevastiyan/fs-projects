import numpy as np
# slice the sine wave from 25% to 75%
def slice_data (data, bounds):
    # a = int(len(data) * 0.25)
    # b = int(len(data) * 0.75)
    # Modify the borders in slice_data TODO Perhaps take it out of the function?
    a = bounds[0]
    b = bounds[1]
    y_sliced = data[a:b]
    return y_sliced

def unison_shuffled_copies(a, b):
    assert len(a) == len(b)
    p = np.random.permutation(len(a))
    return a[p], b[p]
