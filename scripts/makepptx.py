from imgpptx import ImgPres
from glob import glob
from datetime import datetime


comppaths = sorted(glob('figs/comp/*.png'))
extpaths = sorted(glob('figs/ext/*.png'))

prs = ImgPres('pptx/RegionalHaze_tmp.pptx')

prs.add_titlepage('Regional Haze Evaluation from 2016ff 12km', 'Barron H. Henderson\n{}\nDraft'.format(datetime.now()), layout=0)

for comppath, extpath in zip(comppaths, extpaths):
    title = comppath.split('_')[-2]
    prs.add_rowbycol(
        [comppath, extpath],
        [], # ['BASE', 'NAT', 'ROW', 'USA'],
        title=title, titleside='left',
        rows=1, cols=2, vspace=0.02, hspace=-0.1, adjust='height'
    )

prs.save('pptx/RegionalHaze.pptx')
