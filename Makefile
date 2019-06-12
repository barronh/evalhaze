export DAILYROOT=/work/romo/users/shn/2016eval/PM_CMAQ/
export GDNAM=12US2
export YYYY=2016
export DAILYTMPL=dailyavg.LST.Y_24.2016ff_cb6r3_ae6nvpoa_16j.v521.12US2
export SHORTNAME=CMAQ 2016ff

all: cache/updated extr/updated derived/updated \
     tables/summary.csv \
     figs/comp/updated figs/spatial/updated \
     pptx/RegionalHaze.pptx pptx/RegionalHazeMaps.pptx

cache/updated:
	$(MAKE) -C cache

extr/updated: scripts/extrmod.py
	python $<

derived/updated: scripts/deriveext.py scripts/improve_composition.txt scripts/improve_extinction.txt extr/updated
	python $<

figs/comp/updated: tables/summary.csv
	python scripts/summary_figs.py \
		-s "Obs,${SHORTNAME}" \
		-m "Most Impaired,Clearest" \
		$<

figs/spatial/updated: tables/summary.csv scripts/spatial.py
	python scripts/spatial.py $<

tables/summary.csv: scripts/summary_table.py derived/updated
	python $<

pptx/RegionalHaze.pptx: scripts/makepptx.py figs/comp/updated
	python $<

pptx/RegionalHazeMaps.pptx: scripts/makemappptx.py figs/spatial/updated
	python $<

clean: cleandata cleanfigs cleanpptx

cleandata:
	rm -f cache/*.ncf cache/updated
	rm -f extr/*.ncf extr/updated
	rm -f derived/*.ncf derived/updated

cleanfigs:
	find figs -name \*.png -exec rm {} \;
	find figs -name updated -exec rm {} \;

cleanpptx:
	rm pptx/RegionalHaze.pptx
	rm pptx/RegionalHazeMaps.pptx
