import PseudoNetCDF as pnc
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse
import os


gdnam = os.environ['GDNAM']
plt.rcParams["figure.subplot.left"] = 0.05
plt.rcParams["figure.subplot.bottom"] = 0.05
plt.rcParams["figure.subplot.right"] = 0.95
plt.rcParams["figure.subplot.top"] = 0.98

compkeys = 'SEA_SALT AMM_SO4 AMM_NO3 OMC EC CRUSTAL CM'.split()
extkeys = ['SS_RAYLEIGH'] + ['E_' + k for k in compkeys]
parser = argparse.ArgumentParser()
parser.add_argument(
    '-s', '--modsources', type=lambda x: x.split(','),
    default=None,
    help='Defaults to all sources'
)
parser.add_argument(
    '-m', '--metrics', type=lambda x: x.split(','),
    default=None,
    help='Defaults to all sources'
)
parser.add_argument('-c', '--compkeys', default=tuple(compkeys))
parser.add_argument(
    'inpath',
    help=(
        'Path to summary file, which must have site_id, metric, source ' +
        'and compkeys and sitekeys'
    )
)

args = parser.parse_args()

gf = pnc.pncopen('GRIDDESC', format='griddesc', GDNAM=gdnam)
m = gf.getMap()

data = pd.read_csv(args.inpath, index_col=['site_id', 'metric', 'source'])
if args.metrics is None:
    args.metrics = data.index.levels[1].unique()

if args.modsources is None:
    args.modsources = [k for k in data.index.levels[2].unique() if k != 'Obs']

fig = plt.figure(figsize=(8, 4))
m.drawcoastlines()
m.drawcountries()
m.drawstates()
ax = None
cax = None


def qscatter(mm, ax, x, y, c, s, m, norm, cmap):
    mask = c.mask
    c = np.ma.masked_where(mask, c).compressed()
    x = np.ma.masked_where(mask, x).compressed()
    y = np.ma.masked_where(mask, y).compressed()
    p = mm.scatter(x, y, c=c, marker=m, s=s, ax=ax, norm=norm, cmap=cmap)
    return p


stats = dict(
    nmb = '(mod / obs - 1) * 100',
    mb = '(mod - obs)',
    mod = 'mod',
    obs = 'obs',
)

for metric in args.metrics:
    for modsource in args.modsources:
        obs = data.xs('Obs', level=2).xs(metric, level=1)
        mod = data.xs(modsource, level=2).xs(metric, level=1)

        for statkey, statexpr in stats.items():
            stat = eval(statexpr).copy()
            stat.latitude = mod.latitude
            stat.longitude = mod.longitude

            x, y = m(stat.longitude.values, stat.latitude.values)

            for spckey in args.compkeys:
                figpath = 'figs/spatial/{}_{}_{}_IMPROVE_{}_{}_map.png'.format(
                    modsource, gdnam, spckey, metric, statkey 
                ).replace(' ', '_')
                c = np.ma.masked_invalid(stat[spckey].values)
                o = np.ma.masked_invalid(obs[spckey].values)
                ovmin = o.min()
                ovmax = o.max()
                vmin = c.min()
                vmax = c.max()
                if '-' in statexpr:
                    v = np.ma.abs(c).max()
                    if '100' in statexpr:
                        v = np.maximum(v, 110)
                    edges = np.linspace(-v, v, 12)
                    norm = plt.matplotlib.colors.BoundaryNorm(edges, 256)
                    cmap = 'bwr'
                else:
                    norm = plt.Normalize(vmin=0, vmax=ovmax)
                    cmap = None

                if '100' in statexpr:
                    label = '{} {} {} ({:.0f}, {:.0f}%)'.format(modsource, spckey, statkey, vmin, vmax)
                else:
                    label = (
                        '{} {} {} ({:.2g}, {:.2g}'.format(
                            modsource, spckey, statkey, vmin, vmax
                        ) +
                        ' $\mu$g/m$^{3}$)'
                    )

                ismax = (c == vmax).filled(False)
                ismin = (c == vmin).filled(False)
                outliers = (plt.rcParams['lines.markersize']+2)**2
                normals = (plt.rcParams['lines.markersize'])**2
                nc = np.ma.masked_where(~ismin, c)
                xc = np.ma.masked_where(~ismax, c)
                mc = np.ma.masked_where((ismin | ismax), c)
                p = qscatter(m, ax, x, y, mc, s=normals, m='o', norm=norm, cmap=cmap)
                pn = qscatter(m, ax, x, y, nc, s=outliers, m='v', norm=norm, cmap=cmap)
                px = qscatter(m, ax, x, y, xc, s=outliers, m='^', norm=norm, cmap=cmap)
                ax = p.axes
                ax.set_facecolor('gainsboro')
                cb = ax.figure.colorbar(p, cax=cax, orientation='vertical', label=label)
                cax = cb.ax
                ax.figure.savefig(figpath)
                print(figpath)
                del ax.collections[-3:]

os.system('date > figs/spatial/updated')
