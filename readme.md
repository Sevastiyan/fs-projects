# Data Analysis Scripts

This repository contains small apps that can:

1. [Extract data from database]()
2. [Pre-process data]()
3. [Center Of Pressure]()
4. [Displacement Metrics]()
5. [Training Neural Networks for STF]()

## Extracting data from database:

The databse itself is part of **Back4App** which handles the backend of the applicaitons which record data.

First, navigate to the core of the database, where all the raw files for all sessions is currently recorded. 

Second we have to select the files we want to download and analyse. 
Use the Filter option and search for these parameters:
  - `sessio_number`
  - `rawDataLeft`
  - `rawDataRight`
  - `created`

Once that is done we will use the inbuilt export feature which will download a **CSV** file which contains the selected data files and the relevant data that was selected 

After the file has been obtained open the file `/Extract data from databse/extract_data.ipynb` and run the notebook, by following the instructions.


```
make_json('Recent json file/RawDataFiles.csv', 'result.json')
data = read_json('result.json')

urls = []
for d in data.values():
    urls.append(d['rawDataLeft']['url']) 
    urls.append(d['rawDataRight']['url'])

download_path = 'download/'
download_files(urls, download_path)
rename_files('download')
```

This is the main code of the notebook. It performs a couple of tasks:
- Creates a `json` file (_a dictionary in python terms_) using the `make_json(file_to_read, file_to_make)` for easy handling.
- Extract the urls from each data object 
  - The json file is essentially a dictionary object with metadata.
  - The metadata is used to download the raw data.
- Then using the obtained urls we can download the raw data.
- Last piece is to rename the files in the correct format.

All of the data will be saved in the passed folder `download` will include the files from the server.

    For the purposes of Training a neural network for STF its advisable to put the data into the respective label folders.


## Pre Processing:

There are three different ways to pre-process the data.

The recommended way to pre-process the data is using the newer Slicer UI, which will slice the data with the containing features (e.g. an incident) and save it in the correct labeled folder.

First place the data in the data folder. 

--- 
### Using the Slicer UI

    Currently please perform this task only for one incident type so that the end result will hold only one type of incidents. This will guarantee homogenous data for the STF training.

Open the folder with VSCode and first install the necessary dependencies using `pip` by running the following commands in the terminal:

_This can be skipped if the environment has all the dependencies_ 
```
pip3 install matplotlib numpy customtkinter
```

Then open the file data_slicer.py and run the applicaiton from the `Play` button on top.

The script will load all the data files from the data folder and display the first data loaded on the graph. 

The graph is divided into two sections. The top one displays the full session recording, and the second represents a slice of 200 indexes (_this number can be changed for different use cases_). The slice is indicated on the main graph with two vertical red lines, which indicate the starting point and the end point of the slice. Dragging the slice using the slider bellow the graph. 

Once the selection is made click `Save` and the data will be memorised and extracted. After that the next data in the list of files will be shown. Perform this task for every subsequent session.

    TODO: add photos detailing the process

The end result will be inside `/data/processed/<training set>/` which contains all of the selections. 


---
