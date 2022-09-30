from turtle import position
import numpy as np

positions = {
    'left': { 
        'x': np.asarray([-149, -133, -115, -112, -96, -117, -101, -126, -146, -161, -140, -159, -158, -156]),
        'y': np.asarray([-95, -114, -92, -16, 50, 56, 97, 101, 87, 62, 55, 25, -10, -41])
    },
    'right': {
        'x': np.asarray([149, 133, 115, 112, 96, 117, 101, 126, 146, 161, 140, 159, 158, 156]),
        'y': np.asarray([-95, -114, -92, -16, 50, 56, 97, 101, 87, 62, 55, 25, -10, -41])
    }
}

drop = [[1,2,3,4,5,7,8,9],
        [5,6,7,2,1,3,9,10]]
idx = [[False if i+1 in drop[0] else True for i in range(14)],
        [False if i+1 in drop[1] else True for i in range(14)]]

# l = []
# for i in range(14):
#     if i in drop:
#         l.append(False)
#     else:
#         l.append(True)

positions = {
    'left': {
        'x': positions['left']['x'][idx[0]],
        'y': positions['left']['y'][idx[0]]},
    'right': { 
        'x': positions['right']['x'][idx[1]],
        'y': positions['right']['y'][idx[1]]
    }
}

print(positions)