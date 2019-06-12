# IMPROVE Composition and Extinction Evaluation

Creating an evaluation of modeled visibility. Starting with composition,
but also considering the importance in visibility.

## Prerequisites

 - python >= 3.6
 - numpy >= 1.2.1
 - pandas
 - matplotlib
 - mpl_toolkits.basemap
 - PseudoNetCDF
 - imgpptx

## To Run

To use the system with your own data, run these commands on a linux system in bash:

1. `git clone /work/ROMO/regionalhaze/scratch/evalhaze evalmyhaze`
2. `cp /work/ROMO/regionalhaze/scratch/evalhaze/obs/*.csv evalmyhaze`
3. `cd evalmyhaze`
4. Copy obs file to obs/
5. Edit root Makefile (e.g., `vi Makefile`)
  a. `GDNAM` needs to be the grid your simulations is using (12US2, HEMIS, 12US1)
  b. `DAILYROOT` needs to be a folder with daily combine files stored as monthly files. 
  c. `DAILYTMPL` needs to be a file name root where the pattern `${DAILYTMPL}.??.ncf` matches files and `??` are months (01..12)
  d. `YYYY` needs to be the year (e.g., 2016) and the obs file only goes from 2005 to 2017.
  e. `SHORTNAME` needs to be the name of the simulation you want to see in figures.
  f. `OBSPATH` needs to be a path to observations as processed by EPA.
6. Type `make`
  a. First, the system will copy just the variables it needs to the cache folder (`cache/*.ncf`)
  b. Second, it will extract model data at the monitoring sites (`extr/*.ncf`) and pair with hygroscopicity data from the obs file.
  c. Third, it will derive the extinction variables (`derived/*.ncf`)
  d. Fourth, it will make bar plot figures (`comp/*.png` and `ext/*.png`) and maps (`spatial/*.png`)
  e. Fifth, as a convenience it will make a power point of the bar plots and another one of the maps.

## To Reproduce on atmos

Execution requires nco and python with PseudoNetCDF, pandas and numpy.
The commands below load all necessary libraries and the final command
remakes all outputs. Use bash for all commands

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
|-- obs       # IMPROVE obs file from EPA (required as a prerequisite)
|   `-- ClassIareas_NEWIMPROVEALG_2000to2017_2019_feb11_IMPAIRMENT.csv
|-- cache     # folder with copies or links to CAMx/CMAQ daily combine files
|-- extr      # model values at obs locations
|-- derived   # model values at obs locations with derived species
|-- tables    # folder with tables of states from derived/obs
|-- figs      # folder with figures
|   |-- comp  # composition evaluation figures
|   `-- ext   # extinction evaluation figures
`-- pptx      # folder with powerpoint including all figures by site
```
