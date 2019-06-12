# IMPROVE Composition and Extinction Evaluation

Creating an evaluation of modeled visibility. Starting with composition,
but also considering the importance in visibility.

## To Reproduce

Execution requires nco and python with PseudoNetCDF, pandas and numpy.
The commands below load all necessary libraries and the final command
remakes all outputs.

```
module load netcdf-4.4.1/gcc-4.8.5
module load nco-4.6.6/gcc-4.8.5
source /work/ROMO/anaconda3/bin/activate dev
make
```

## Annotated Directory Structure

```
.
|-- README.md # this document
|-- Makefile  # driver that populates cache, extr, derived, tables, and figs
|-- NOTES.md  # notes
|-- GRIDDESC  # IOAPI GRIDDESC file
|-- scripts   # folder with scripts called by Makefile
|-- obs       # IMPROVE obs file from Brett Gantt (required as a prerequisite)
|   |-- ClassIareas_NEWIMPROVEALG_2000to2017_2019_feb11_IMPAIRMENT.csv
|-- cache     # folder with copies or links to CAMx/CMAQ daily combine files
|-- extr      # model values at obs locations
|-- derived   # model values at obs locations with derived species
|-- tables    # folder with tables of states from derived/obs
|-- figs      # folder with figures
|   |-- comp  # composition evaluation figures
|   `-- ext   # extinction evaluation figures
`-- pptx      # folder with powerpoint including all figures by site
```
