# Python program to read json file
import csv
import json
import os

# Request url info
import requests


def main():
    print("Script Start")
    print("------------")
    subject = "mci003"
    root_file = f"2024-02-23 {subject}"
    root_folder = "./Extract data from database"
    date = root_file.split(" ")[0]

    print("Creating JSON file...")
    json_file = make_json(
        f"{root_folder}/csv/{subject}/{root_file}.csv",
        f"{root_folder}/json/{subject}",
        root_file,
    )
    data = read_json(json_file)

    urls = []
    for d in data.values():
        urls.append(d["rawDataLeft"]["url"])
        urls.append(d["rawDataRight"]["url"])

    download_path = f"COP analysis/data/{subject}/{date}/"  #! Downloads the data to COP analysis folder Depending on environment use abspath to navigate
    print("Downloading files to:", os.path.abspath(download_path))
    download_files(urls, download_path)
    rename_files(download_path)


def download_files(url_list, download_path):
    """
    Download files into provided pathway given a list of url

    @Params:
    url_list (list) - List of url to download from
    download_path (str) - path to download the files into

    Does not have return values
    """

    # Save text from url as a .txt
    print("Downloading Files...")
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    for url in url_list:
        f = requests.get(url)

        # filename gotten by splitting url and removing the unique ID of each dataset
        filename = url.split("/")[-1][33:-4] + ".txt"
        print("Filename: ", filename)

        # Save files as txt
        with open(download_path + filename, "w+") as text_file:
            text_file.write(f.text)

    return


def make_json(csvFilePath: str, jsonFilePath: str, filename: str) -> str:
    # create a dictionary
    data = {}
    # Open a csv reader called DictReader
    if not os.path.isdir(jsonFilePath):
        os.makedirs(jsonFilePath)

    with open(csvFilePath, encoding="utf-8") as csvf:
        csvReader = csv.DictReader(csvf)
        # Convert each row into a dictionary
        # and add it to data
        for rows in csvReader:
            # Assuming a column named 'No' to
            # be the primary key
            key = rows["sessionNumber"]
            data[key] = rows
            data[key]["rawDataLeft"] = json.loads(rows["rawDataLeft"])
            data[key]["rawDataRight"] = json.loads(rows["rawDataRight"])
    # Open a json writer, and use the json.dumps()
    # function to dump data

    with open(f"{jsonFilePath}/{filename}.json", "w", encoding="utf-8") as jsonf:
        jsonf.write(json.dumps(data, indent=4))

    return f"{jsonFilePath}/{filename}.json"


def read_json(jsonFilePath):
    with open(jsonFilePath, "r") as read_it:
        data = json.load(read_it)

    return data


def rename_files(path):
    print("Renaming Files in: ", path)
    files = os.listdir(path)  # List of files in the data path folder
    for file in files:
        filename = file.split(".txt")[0]
        str_list = filename.split("_")
        new_filename = str_list[2] + "_" + str_list[3] + "_" + str_list[1] + "_" + str_list[0] + ".txt"
        os.rename(os.path.join(path, file), os.path.join(path, new_filename))


if __name__ == "__main__":
    main()
