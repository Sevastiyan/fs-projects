TODO:

- [X] Sliced Old Slips 
- [X] Sliced Old Trips - Check the archive
  - Check in the Slicer UI `/data/processed`
  - 2022-10 - Training Data
  - 2022-12-06 - Validation Data 
- [ ] Put Data together in STF
- [ ] Treaining on 2022-10 Training Data
- [ ] Validation on 2022-12-06 Validation Data
- [ ] Confusion Matrix

# Usage

There are two projects that deal with classificaiton of STF incidents. 

- Binary Incident Detection
  - `binary_training.ipynb`
  - `binary_validation.ipynb`
- Multiclass Incident Classification
  - `multiclass_training.ipynb`
  - `multiclass_validaiton.ipynb`

Each is optimised to perform a training on a model stored in `models/`. `TS_CNN.py` is currently the most recent model, other models need to be updated and adjusted to be trained and do inference. Inside the file there are two architectures optimised to the current data supplied as input. 

## Data Perparation

After using the [Slicer UI](https://github.com/Sevastiyan/fs-projects/tree/main/Slicer%20UI) to create the processed training (*and/or validation*) data, copy the files to the `stf_main/data` folder. The data needs to be separated depending on the model that will be trained. Multiclass training needs to be separated into `multiclass/Slip`, `multiclass/Trip` folders. 

## Increasing the classes before training

If additional classes (in this case incidents), are going to be predicted, Please create a **new folder** and store the training data (extracted with [Slicer UI](https://github.com/Sevastiyan/fs-projects/tree/main/Slicer%20UI)) inside.

## Training
*Under Development*

## Validation
*Under Development*

## Saving and exporting the model and weights
*Under Development*
