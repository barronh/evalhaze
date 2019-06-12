import PseudoNetCDF as pnc
from readobs import obsdf, locs
import numpy as np
import pandas as pd
import os


monobskeys = ['FRH', 'FLRH', 'FSRH', 'FSSRH', 'SS_RAYLEIGH']
dayobskeys = ['GROUP']

camxinpath = 'derived/dailyavg.LST.Y_24.2016ff_cb6camx_16j.12US2.ncf'
cmaqinpath = 'derived/dailyavg.LST.Y_24.2016ff_cb6r3_ae6nvpoa_16j.v521.12US2.ncf'

cmaqf = pnc.pncopen(cmaqinpath, format='ioapi').copy()
camxf = pnc.pncopen(camxinpath, format='ioapi').copy()
