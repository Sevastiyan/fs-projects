import requests
from pymongo import MongoClient
import os
import numpy as np

subject = "htx01"  # ? Change this to the subject. Can be added in the filename at modify_filename(file_name)
username = "htx@flexosense.com"
date = "2024-04-12"
root_destination = f"./Extract data from database/data/download"  #! Check the local root destination
base_url = "https://parsefiles.back4app.com/iNiIcVqwVFMgMxU4JpX9aJP4MMGaVaHFut1va4UR/"


def main():
    # Connect to the MongoDB database
    client = MongoClient("mongodb://admin:2AKPzI4SHhrEShmgVJ6pQfMX@MongoS3601A.back4app.com:27017/331f348adcc74d2c8a4f8e47b651b747")
    db = client.get_default_database()
    # Specify the collection
    collection = db["RawDataFiles"]

    # Query documents from the collection
    documents = collection.find({"username": username})

    # Filter documents based on _created_at
    filtered_documents = [doc for doc in documents if str(doc["_created_at"]).startswith(date)]

    # Create the download destination folder if it doesn't exist
    if not os.path.exists(root_destination):
        os.makedirs(root_destination)

    for document in filtered_documents:
        print("--------------------------------------")
        print("ID:", document["_id"])
        print("Username:", document["username"])
        print("Created At:", document["_created_at"])
        print("RawDataLeft URL:", document["rawDataLeft"])
        print("RawDataRight URL:", document["rawDataRight"])

        download_file(document["rawDataLeft"])
        download_file(document["rawDataRight"])


def download_file(file):
    """
    Download a file from the given URL and save it to the destination path.
    """
    response = requests.get(base_url + file)
    if response.status_code == 200:
        # Get the filename from the URL and modify it
        new_filename = modify_filename(file)
        print("modified Filename:", new_filename)

        # Save the file with the modified filename
        with open(os.path.join(root_destination, new_filename), "w+") as text_file:
            text_file.write(response.text)
        print(f"File downloaded successfully: {new_filename}")
    else:
        print(f"Failed to download file from URL: {base_url + file}")


def modify_filename(file_name):
    """
    Modify the filename extracted from the URL.
    """
    # Split the URL by "/" and get the last part (filename)
    filename = file_name.split("/")[-1]
    # Extract session number and date
    parts = filename.split("_")
    session_number = parts[3]
    date = parts[-1].split(".")[0]
    # Rearrange the filename
    new_filename = f"{session_number}_{date}_rawDataLeft.txt"
    return new_filename


if "__main__" == __name__:
    main()
