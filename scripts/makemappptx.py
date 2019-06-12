from imgpptx import ImgPres
from glob import glob
from datetime import datetime
import numpy as np

inpaths = sorted(glob('figs/spatial/*.png'))
for nmods in [1, 2]:
    try:
        mappaths = np.array(inpaths).reshape(nmods, -1, 3, 4)
    except Exception:
        pass

print('Using {} models'.format(mappaths.shape[0]))

# spc, mod, metric, stat
mappaths = mappaths.swapaxes(0, 1) # .swapaxes(1, 2)

prs = ImgPres('pptx/RegionalHaze_tmp.pptx')
prs.add_titlepage('Regional Haze Evaluation from 2016ff 12km', 'Barron H. Henderson\n{}\nDraft'.format(datetime.now()), layout=0)

for spcpaths in mappaths:
    for modpaths in spcpaths:
        for metpaths in modpaths:
            obspath = metpaths[3]
            modpath = metpaths[1]
            mbpath = metpaths[0]
            nmbpath = metpaths[2]
            title = obspath[13:25] + ' '.join(obspath[31:-12].split('_IMPROVE_'))
            print(title)
            prs.add_rowbycol(
                [obspath, modpath, mbpath, nmbpath],
                [], # ['BASE', 'NAT', 'ROW', 'USA'],
                title=title.replace('_', ' '), titleside='left',
                rows=2, cols=2, vspace=0.02, hspace=-0.1, adjust='width'
            )

prs.save('pptx/RegionalHazeMaps.pptx')
