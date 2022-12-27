# Data Slicer

## TODO:

| Status | Task                                     | Description |
| ------ | ---------------------------------------- | ----------- |
| [X]    | Create the app with progressive change   |             |
| [X]    | Slice gyro and pressure data             |             |
| [ ]    | CoP Slicer Algorithm                     |             |
| [ ]    | Add Overlap option                       |             |
| [ ]    | Add photos detailing the process         |             |
| [ ]    | Add dependency file for easy pip install |             |


---

## Slicer UI
    Please perform this task only for one incident type so that the data is homogenously classified in folders.

navigate with the terminal to `<root project folder>/Slicer UI/` with the command line. Make sure that the terminal is in the root project folder, or start a terminal session on the `/Slicer UI/` Folder.

```
cd "Slicer UI"
```

Open the file `data_slicer.py` with VSCode. At the bottom there is a function called `main()`. Here you can set the name of the folder that should indicate which data you want to load and slice using the UI. Write the correct path e.g. `data/incidents/Trip`. Make sure that there is data within the folder selected.

To run the applicaiton from the `Play` button at top right. The script will load all the data files from the data folder and display the first sample loaded on the graph.

![Alt text](resources/Screenshot%202022-12-20%20113213.png)

The graph is divided into two sections. The top one displays the full session recording, and the second represents a slice of 200 indexes (_this number can be changed for different use cases_). The slice is indicated on the main graph with two vertical red lines, which indicate the starting point and the end point of the slice. Dragging the slice using the slider bellow the graph. 

There are four control buttons on the right:
- `Slice` - Slices the sample within the current borders
- `Skip` - Skips this current sample 
- `Save` - Saves the data so far (can be saved at the end)
- `Quit` - Quit the application after saving one last time

Once the selection is made click `Slice` and the slice will be extracted and memorised. After that the next sample from the files will be loaded. Perform this task for every subsequent sample. 

If for any reason the data is not useful, you can click `Skip`.

The progress bar on the left indicates how many files are left in the batch loaded. Full bar means that the last one has been loaded.

When done click `Save` or `Quit`. The end result will be inside `/data/processed/<training set>/` which contains all of the selections in a compiled format that is ready for training. 

