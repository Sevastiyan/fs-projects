import os
import utils.cop as cop
from utils.data_loader import load_data

print('hello world')

path = f"./data"
root = './data'
file_list = []
for file in os.listdir(root):
    file_list.append(os.path.join(root, file))

print(file_list)

data = load_data(file_list)

data_left = data[0]
data_right =  data[0]

# c = cop.CenterOfPressure([data_left, data_right])
# print('left: ', c.get_cop_foot('left'))
# print('right: ', c.get_cop_foot('right'))

