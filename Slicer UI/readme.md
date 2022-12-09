# Data Slicer

## TODO:

| Status | Task                                     | Description |
| ------ | ---------------------------------------- | ----------- |
| [x]    | Create the app with progressive change   |             |
| [ ]    | Slice gyro and pressure data             |             |
| [ ]    | Add Overlap option                       |             |
| [ ]    | Add photos detailing the process         |             |
| [ ]    | Add dependency file for easy pip install |             |


---

## Using the Slicer UI

    Currently please perform this task only for one incident type so that the end result will hold only one type of incidents. This will guarantee homogenous data for the STF training.

Open the folder with VSCode and first install the necessary dependencies using `pip` by running the following commands in the terminal:

**Note**: _This can be skipped if the environment has all the dependencies_ 
```
pip3 install matplotlib numpy customtkinter
```

Then open the file data_slicer.py and run the applicaiton from the `Play` button on top.

The script will load all the data files from the data folder and display the first data loaded on the graph. 

The graph is divided into two sections. The top one displays the full session recording, and the second represents a slice of 200 indexes (_this number can be changed for different use cases_). The slice is indicated on the main graph with two vertical red lines, which indicate the starting point and the end point of the slice. Dragging the slice using the slider bellow the graph. 

Once the selection is made click `Save` and the data will be memorised and extracted. After that the next data in the list of files will be shown. Perform this task for every subsequent session.

    TODO: add photos detailing the process

The end result will be inside `/data/processed/<training set>/` which contains all of the selections. 


