CMAQVARS=PM25_TOT,PM25_SO4,PM25_NO3,PM25_OC,PM25_OM,PM25_CL,PMC_CL,PM25_EC,PM25_SOIL,PMC_TOT

CMAQIN=$(sort $(wildcard ${DAILYROOT}/${DAILYTMPL}.??.ncf))

CMAQOUT=$(notdir $(CMAQIN))

all: $(CMAQOUT)

$(CMAQOUT): %.ncf: ${DAILYROOT}/%.ncf
	ncks -7 --deflate 1 -v TFLAG,$(CMAQVARS) -d VAR,10 $< $@
	ncatted -a NVARS,global,o,i,9 $@
