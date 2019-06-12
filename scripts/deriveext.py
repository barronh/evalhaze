import PseudoNetCDF as pnc
from readobs import obsdf, locs
import numpy as np
import pandas as pd
import os


dailytmpl = os.environ['DAILYTMPL']
monobskeys = ['FRH', 'FLRH', 'FSRH', 'FSSRH', 'SS_RAYLEIGH']
dayobskeys = ['GROUP']

cmaqinpath = 'extr/' + dailytmpl + '.ncf'

cmaqoutpath = 'derived/' + dailytmpl + '.ncf'

cmaqf = pnc.pncopen(cmaqinpath, format='ioapi').copy()
keys = ['site_id', 'month']
metadf = obsdf.sort_values(by=keys).groupby(keys).first()

def addobsdata(modf):
    dims = ('TSTEP', 'LAY', 'site')
    times = modf.getTimes()
    months = np.array([t.month for t in times])
    sites = np.char.decode(modf.variables['site_id'][:].view('S16')[:, 0])
    for obskey in monobskeys:
        ovar = modf.createVariable(obskey, 'f', dims, missing_value=-999)
        ovar[:] = -999
        ovar.units = 'none'
        ovar.long_name = obskey
        ovar.var_desc = obskey
        for lk in sorted(np.unique(sites)):
            for mo in sorted(np.unique(months)):
                # missing months do not work
                if not (lk, mo) in metadf.index:
                    print('Skipping', lk, mo)
                    continue
                minedf = metadf.loc[lk, mo]
                # minedf = obsdf.query('(site_id == "%s") and (month == %d)' % (lk, mo)
                midx = np.where(months == mo)[0]
                sidx = np.where(sites == lk)[0] * np.ones_like(midx)
                ovar[midx, 0, sidx] = minedf[obskey]

    for obskey in dayobskeys:
        ovar = modf.createVariable(obskey, 'f', dims, missing_value=-999)
        ovar[:] = -999
        ovar.units = 'none'
        ovar.long_name = obskey
        ovar.var_desc = obskey
        for lk in sorted(np.unique(sites)):
            minedf = obsdf.query('site_id == "%s"' % lk).sort_values(by=['datetime'])
            ismine = np.where(np.in1d(pd.to_datetime(times), minedf.datetime.dt.values))[0]
            sidx = np.where(sites == lk)[0] * np.ones_like(ismine)
            ovar[ismine, 0, sidx] = minedf[obskey]

addobsdata(cmaqf)

compstr = open('scripts/improve_composition.txt', 'r').read()
bextstr = open('scripts/improve_extinction.txt', 'r').read()

cmaqf.eval(compstr, inplace=True).eval(bextstr, inplace=True)
cmaqf.save(cmaqoutpath)
os.system('date > derived/updated')
