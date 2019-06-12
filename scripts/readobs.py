import pandas as pd
import os

yyyy = int(os.environ['YYYY'])
obspath = os.environ['OBSPATH']
'obs/ClassIareas_NEWIMPROVEALG_2000to2017_2019_feb11_IMPAIRMENT.csv'
"""
Day
_ID, _TYPE, LAT, LONG, DATE, FRH, FSRH, FLRH, FSSRH, SS_RAYLEIGH, SEA_SALT, PM25, CRUSTAL, AMM_NO3, OMC, EC, PM10, CM, AMM_SO4, LARGE_OMC, SMALL_OMC, LARGE_AMM_SO4, SMALL_AMM_SO4, LARGE_AMM_NO3, SMALL_AMM_NO3, E_AMM_SO4, E_AMM_NO3, E_OMC, E_EC, E_CRUSTAL, E_CM, E_SEA_SALT, TBEXT, DV, GOOD_YEAR, GROUP, POSSIBLE_NDAYS, NDAYS, COMPLETE_QUARTER, SF, SO4F
"""

obspath = 'obs/ClassIareas_NEWIMPROVEALG_2000to2017_2019_feb11_IMPAIRMENT.csv'
def cleannames(key):
    tmp = key.strip()
    if tmp == 'LONG':
        tmp = 'longitude'
    elif tmp == 'LAT':
        tmp = 'latitude'
    elif tmp == '_ID':
        tmp = 'site_id'

    return tmp
allobsdf = pd.read_csv(obspath, skiprows=1)
allobsdf.rename(columns=cleannames, inplace=True)
allobsdf['datetime'] = pd.to_datetime(allobsdf['DATE'], format='%Y%m%d')
allobsdf['month'] = allobsdf.datetime.dt.month.astype('int32')

obsdf = allobsdf[allobsdf.datetime.dt.year == yyyy].copy()

locs = obsdf.filter(['site_id', 'longitude', 'latitude']).groupby('site_id').last().sort_values(by='site_id')
