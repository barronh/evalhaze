import pandas as pd
import matplotlib.pyplot as plt
import json
import os
import argparse


shortname = os.environ['SHORTNAME']
gdnam = os.environ['GDNAM']

compkeys = 'SEA_SALT AMM_SO4 AMM_NO3 OMC EC CRUSTAL CM'.split()
extkeys = ['SS_RAYLEIGH'] + ['E_' + k for k in compkeys]
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--sources', default=None, type=lambda x: x.split(','))
parser.add_argument('-m', '--metrics', default=None, type=lambda x: x.split(','))
parser.add_argument('-c', '--compkeys', default=tuple(compkeys))
parser.add_argument('-e', '--extkeys', default=tuple(extkeys))
parser.add_argument(
    'inpath',
    help=(
        'Path to summary file, which must have site_id, metric, source ' +
        'and compkeys and sitekeys'
    )
)

args = parser.parse_args()

data = pd.read_csv(args.inpath)

cfg = json.load(open('scripts/composition_config.json', 'r'))
coloropts = cfg['colors']

compkeys = args.compkeys
extkeys = args.extkeys

compcolors = [coloropts[k] for k in compkeys]
extcolors = [coloropts[k] for k in extkeys]

plt.rcParams['legend.handletextpad'] = .2
plt.rcParams['legend.handlelength'] = .75
plt.rcParams['legend.columnspacing'] = 1

gridspec_kw = dict(
    left=0.125, bottom=.275, right=0.9, top=0.9, wspace=0, hspace=0
)
if args.metrics is None:
    metrics = list(data.metric.unique())
else:
    metrics = args.metrics

if args.sources is None:
    sources = list(data.source.unique())
else:
    sources = args.sources

print(metrics)
print(sources)
siteids = data.site_id.unique()

data = data.query(
    'source in {}'.format(sources)
).set_index(
    ['site_id', 'metric', 'source']
)

fig, axx = plt.subplots(
    1, len(metrics), sharey='row', gridspec_kw=gridspec_kw
)


for siteid in siteids:
    figpath = 'figs/comp/{}_{}_VISIBILITYCONC_IMPROVE_{}_bar.png'.format(shortname, gdnam, siteid).replace(' ', '_')
    print(figpath)
    ax = axx[0]
    for axi, lkey in enumerate(metrics):
        sdf = data.xs((siteid, lkey)).copy()
        sdf.index.set_names([lkey], inplace=True)
        sdf.filter(compkeys).plot(kind='bar', stacked=True, color=compcolors, legend=False, ax=axx[axi])
    ax.set_ylabel('micrograms/m$^3$')
    patches = [
        plt.Rectangle(
            (0, 0), 1, 1,
            color=cfg['colors'][k],
            label=k.replace('_', '')
        )
        for k in compkeys
    ]
    labels = [p.get_label() for p in patches]
    plt.legend(
        patches, labels,
        loc='upper center', bbox_to_anchor=(.5, .99), ncol=len(compkeys),
        bbox_transform=ax.figure.transFigure
    )
    text = axx[-1].text(0.02, 0.90, siteid, size=18, transform=axx[-1].transAxes)
    ax.figure.savefig(figpath)
    for tax in axx:
        tax.cla()
    figpath = 'figs/ext/{}_{}_VISIBILITYEXT_IMPROVE_{}_bar.png'.format(shortname, gdnam, siteid).replace(' ', '_')
    print(figpath)
    for axi, lkey in enumerate(metrics):
        sdf = data.xs((siteid, lkey)).copy()
        sdf.index.set_names([lkey], inplace=True)
        sdf.filter(extkeys).plot(kind='bar', stacked=True, color=extcolors, legend=False, ax=axx[axi])
    patches = [
        plt.Rectangle(
            (0, 0), 1, 1,
            color=cfg['colors'][k],
            label=k.replace('SS_', 'S_')[2:].replace('_', ''))
        for k in extkeys
    ]
    labels = [p.get_label() for p in patches]
    plt.legend(
        patches, labels,
        loc='upper center', bbox_to_anchor=(.5, .99), ncol=len(extkeys),
        bbox_transform=ax.figure.transFigure
    )
    ax.set_ylabel('Mm$^{-1}$')
    text = axx[-1].text(0.02, 0.90, siteid, size=18, transform=axx[-1].transAxes)
    ax.figure.savefig(figpath)
    for tax in axx:
        tax.cla()
"""

Where:

PROJECT = CAMx_2016ff_12US2 or CMAQ_2016ff_12US2.  If putting both models on one plot use CMAQ_CAMx_2016ff_12US2

POLLUTANT = ?  I think we can define that here.  Perhaps visibility or extinction

NETWORK = IMPROVE or CSN

PLOTTYPE = ?  Again you could decide how to refer to these plots
"""
os.system('date > figs/ext/updated')
os.system('date > figs/comp/updated')
