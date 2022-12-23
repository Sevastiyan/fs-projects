# Data Analysis Scripts

This repository contains small apps that can:

1. [Extract data from database]()
2. ~~[Pre-process data]()~~ replaced by [Slicer UI]()
3. [Center Of Pressure]()
4. [Displacement Metrics]()
5. [Training Neural Networks for STF]()

## Dependencies:

First navigate to the root folder of this repository with the command line/terminal/VSCode. Install the necessary dependencies using `pip` by running the following commands in the terminal:

_This can be skipped if the environment has all the dependencies already._ 
```
pip3 install -r requirements.txt
pip3 install --upgrade  # optional
```

The `requirements.txt` file has all the dependecnies for the projects to run on any computer running with the python 3.6^ environment. Please make sure that the python is handling the current project either by **Anaconda** or python 3.6+ and above.

---

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


## Using the Slicer UI
    Please perform this task only for one incident type so that the data is homogenously classified in folders.

navigate with the terminal to `C:<User>/<project folder>/Slicer UI` with the command line.
```
cd "Slicer UI"
```

Open the file `data_slicer.py` with VSCode. At the bottom there is a function called `main()`. Here you can set the name of the folder that should indicate which data you want to load and slice using the UI. Write the correct path e.g. `data/incidents/Trip`. Make sure that there is data within the folder selected.

To run the applicaiton from the `Play` button at top right, or write the following command in the terminal:
```
python app.py
```
 The script will load all the data files from the data folder and display the first sample loaded on the graph.

![Alt text](Slicer%20UI/resources/Screenshot%202022-12-20%20113213.png)

The graph is divided into two sections. The top one displays the full session recording, and the second represents a slice of 200 indexes (_this number can be changed for different use cases_). The slice is indicated on the main graph with two vertical red lines, which indicate the starting point and the end point of the slice. Dragging the slice using the slider bellow the graph. 

There are four control buttons on the right:
- **Slice** - Slices the sample within the current borders
- **Skip** - Skips this current sample 
- **Save** - Saves the data so far (can be saved at the end)
- **Quit** - Quit the application after saving one last time

Once the selection is made click `Slice` and the slice will be extracted and memorised. After that the next sample from the files will be loaded. Perform this task for every subsequent sample. 

If for any reason the data is not useful, you can click `Skip`.

The progress bar on the left indicates how many files are left in the batch loaded. Full bar means that the last one has been loaded.

When done click `Save` or `Quit`. The end result will be inside `/data/processed/<training set>/` which contains all of the selections in a compiled format that is ready for training. 

---

# Deprecated: 

## Pre Processing:

There are three different ways to pre-process the data.

The recommended way to pre-process the data is using the newer Slicer UI, which will slice the data with the containing features (e.g. an incident) and save it in the correct labeled folder.

First place the data in the data folder. 
