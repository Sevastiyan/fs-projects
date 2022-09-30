import os

def rename(path):
    print(path)
    files = os.listdir(path)  # List of files in the data path folder
    for file in files:
        filename = file.split(".txt")[0]
        str_list = filename.split("_")
        new_filename = str_list[2] + "_" + str_list[3] + "_" + str_list[1] + "_" + str_list[0] + ".txt"
        os.rename(os.path.join(path, file), os.path.join(path, new_filename))


if __name__ == '__main__':
    rename()