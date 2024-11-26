import requests
from pymongo import MongoClient
import os
from datetime import datetime
import plotly_analysis

SUBJECT = "bendy"                # Change this to the subject
GLOBAL_DATE = "2024-08-26"      # Change this for the date

def main():


    # Save destination
    root_destination = f"./Extract data from database/data/{SUBJECT}/{GLOBAL_DATE}"


    # ---------------------------------------------------------------------------- #
    #                            REST OF CODE                                      #
    # ---------------------------------------------------------------------------- #

    username = f"{SUBJECT}@flexosense.com"
    base_url = "https://parsefiles.back4app.com/oS1bmtzJUFyaiUD7kJEkxCmpVDem49v2y2SdAv6t/"

    # Connect to the MongoDB database
    client = MongoClient("mongodb://admin:RQIGi9Mwml2PpWJIrsihJK3h@MongoS3601A.back4app.com:27017/743527a2e1b041af98f33e75129dc57d")
    db = client.get_default_database()
    collection = db["RawDataFiles"]

    # Query documents from the collection
    documents = collection.find({"username": username})

    # Filter documents based on _created_at
    # filtered_documents = [doc for doc in documents if str(doc["_created_at"]).startswith(GLOBAL_DATE)]

    # Create the download destination folder if it doesn't exist
    if not os.path.exists(root_destination):
        os.makedirs(root_destination)

    for document in documents: #filtered_documents:
        print("--------------------------------------")
        # print("ID:", document["_id"])
        # print("Username:", document["username"])
        print("Created At:", document["_created_at"])
        # print("RawDataLeft URL:", document["rawDataLeft"])
        # print("RawDataRight URL:", document["rawDataRight"])

        download_file(document["rawDataLeft"], "Left", root_destination, base_url, SUBJECT)
        download_file(document["rawDataRight"], "Right", root_destination, base_url, SUBJECT)

def download_file(file, side, root_destination, base_url, subject):
    """
    Download a file from the given URL and save it to the destination path if it doesn't exist.
    """
    new_filename = modify_filename(file, side, subject)
    full_path = os.path.join(root_destination, new_filename)

    # Check if file already exists
    if os.path.exists(full_path):
        print(f"File {new_filename} already exists. Skipping download.")
        return

    response = requests.get(base_url + file)
    if response.status_code == 200:
        print("Downloading:", new_filename)

        with open(full_path, "w+") as text_file:
            text_file.write(response.text)
        print(f"File downloaded successfully: {new_filename}")
    else:
        print(f"Failed to download file from URL: {base_url + file}")

def modify_filename(file_name, side, subject):
    """
    Modify the filename extracted from the URL.
    """
    filename = file_name.split("/")[-1]
    parts = filename.split("_")
    session_number = parts[3]
    date = parts[-1].split(".")[0]
    new_filename = f"{date}_{session_number}_rawData{side}_{subject}.txt"
    return new_filename

if "__main__" == __name__:
    main()
    # plotly_analysis.process_data(SUBJECT, [GLOBAL_DATE])
