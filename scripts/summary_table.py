import PseudoNetCDF as pnc
from readobs import obsdf, locs
import numpy as np
import pandas as pd
import os


dailytmpl = os.environ['DAILYTMPL']
shortname = os.environ['SHORTNAME']
monobskeys = ['FRH', 'FLRH', 'FSRH', 'FSSRH', 'SS_RAYLEIGH']
dayobskeys = ['GROUP']

cmaqinpath = 'derived/' + dailytmpl + '.ncf'
cmaqf = pnc.pncopen(cmaqinpath, format='ioapi').copy()
dims = cmaqf.variables['GROUP'].dimensions
cmaqg = cmaqf.variables['GROUP'][:]
q90 = (cmaqg != 90).filled(True)
q10 = (cmaqg != 10).filled(True)
qother = (~(q90 | q10)) | cmaqg.mask
cmaqif = cmaqf.mask(q90, dims=dims).apply(TSTEP='mean')
cmaqcf = cmaqf.mask(q10, dims=dims).apply(TSTEP='mean')
cmaqof = cmaqf.mask(qother, dims=dims).apply(TSTEP='mean')
impdf = obsdf.query('GROUP == 90').groupby(['site_id']).mean()
clrdf = obsdf.query('GROUP == 10').groupby(['site_id']).mean()
othdf = obsdf.query('(GROUP != 10) & (GROUP != 90)').groupby(['site_id']).mean()
compkeys = 'SEA_SALT AMM_SO4 AMM_NO3 OMC EC CRUSTAL CM'.split()
extkeys = 'SS_RAYLEIGH E_SEA_SALT E_AMM_SO4 E_AMM_NO3 E_OMC E_EC E_CRUSTAL E_CM'.split()
keys = ['longitude', 'latitude'] + compkeys + extkeys
siteids = np.char.decode(cmaqif.variables['site_id'][:].view('S16')).astype(str)[:, 0]
dfs = []

def getdf(qf, mydf):
    qv = [np.float32(qf.variables[k][:].filled(np.nan).ravel()[0]) for k in keys]
    ov = [np.float32(mydf[k]) for k in keys]
    df = pd.DataFrame(
        [ov, qv],
        columns=keys,
        index=['Obs', shortname]
    )
    return df

for si, siteid in enumerate(siteids):
    print(siteid) 
    mydf = impdf.loc[siteid]
    qf = cmaqif.slice(site=si)
    idf = getdf(qf, mydf)
    mydf = othdf.loc[siteid]
    qf = cmaqof.slice(site=si)
    odf = getdf(qf, mydf)
    mydf = clrdf.loc[siteid]
    qf = cmaqcf.slice(site=si)
    cdf = getdf(qf, mydf)
    df = pd.concat([idf, odf, cdf], keys=['Most Impaired', 'Other', 'Clearest'])
    dfs.append(df)

masterdf = pd.concat(dfs, keys=siteids.tolist())
masterdf.to_csv('tables/summary.csv', index_label=['site_id', 'metric', 'source'])
