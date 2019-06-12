import PseudoNetCDF as pnc
from readobs import locs
import os

dailytmpl = os.environ['DAILYTMPL']
gdnam = os.environ['GDNAM']
gdf = pnc.pncopen('GRIDDESC', format='griddesc', GDNAM=gdnam)

# Edit
extractopts = dict(
    cmaq = dict(
        tmpl = 'cache/' + dailytmpl + '.{:02d}.ncf',
        outpath = 'extr/' + dailytmpl + '.ncf'
    )
)

# For testing speed
# locs = locs.head().copy()
# nmonths = 2
nmonths = 12
i, j = gdf.ll2ij(locs['longitude'].values, locs['latitude'].values)
ic, jc = gdf.ll2ij(locs['longitude'].values, locs['latitude'].values, clean='clip')
locs['i'] = i
locs['j'] = j
locs['ic'] = ic
locs['jc'] = jc
mask = (jc != j) | (ic != i)

def getsites(path):
    """
    path : path to ioapi file
    returns i, j locations
    """
    keepvars = [
        'PM25_TOT', 'PM25_SO4', 'PM25_NO3', 'PM25_OC', 'PM25_OM', 'PM25_CL',
        'PMC_CL', 'PM25_EC', 'PM25_SOIL', 'PMC_TOT'
    ]
    print(path, flush=True)
    inf = pnc.pncopen(path, format='ioapi')
    varf = inf.subsetVariables(keepvars)
    sitef = inf.slice(ROW=jc, COL=ic, newdims=('site',))
    ntimes = len(sitef.dimensions['TSTEP'])
    dims = sitef.variables[keepvars[0]].dimensions
    mymask = mask[None, None, :].repeat(ntimes, 0)
    
    outf = sitef.mask(
        mymask,
        dims=dims
    )
    return outf

def getyear(tmpl):
    modfs = [getsites(tmpl.format(month)) for month in range(1, nmonths + 1)]
    modf = modfs[0].stack(modfs[1:], 'TSTEP')
    modf.createDimension('str16', 16)
    site = modf.createVariable('site_id', 'c', ('site', 'str16'))
    site.units = 'none'
    site.long_name = 'site_id'
    site.var_desc = 'site_id'
    sitev = locs.index.values.astype('S16').view('S1').reshape(-1, 16)
    site[:, :] = sitev
    lat = modf.createVariable('latitude', 'f', ('site',))
    lat.units = 'degrees_north'
    lat.var_desc = 'latitude'
    lat.long_name = 'latitude'
    lat[:]  = locs.latitude.values
    lon = modf.createVariable('longitude', 'f', ('site',))
    lon.units = 'degrees_east'
    lon.var_desc = 'longitude'
    lon.long_name = 'longitude'
    lon[:]  = locs.longitude.values
    del modfs
    return modf

def process(tmpl, outpath):
    modf = getyear(tmpl)
    modf.save(outpath, complevel=1, verbose=0)

for key, opts in extractopts.items():
    print(key)
    process(**opts)

os.system('date > extr/updated')
