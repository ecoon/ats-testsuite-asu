import os,sys
import numpy as np
sys.path.append(os.path.join(os.environ['AMANZI_SRC_DIR'],'tools','amanzi_xml'))
sys.path.append(os.path.join(os.environ['ATS_SRC_DIR'],'tools','ats_xml'))

import amanzi_xml.common.parameter_list as plist
import amanzi_xml.amanzi.functions as afuncs
import amanzi_xml.amanzi.evaluators.base as aevals
import amanzi_xml.amanzi.regions as aregions
import ats_xml.models.wrm as wrm

soils = []
for i in range(1,5):
    for j in range(1,5):
        soils.append("soil %d layer %d"%(i,j))

porosities = [0.34,0.34,0.56,0.56,  # soil class 1
              0.32,0.36,0.43,0.43,  # soil class 2
              0.50,0.48,0.48,0.48,  # soil class 3
              0.62,0.60,0.60,0.60]  # soil class 4

hydraulic_conduct = np.array([2.488,]*4 +
                             [2.294,]*4 +
                             [0.618,]*4 +
                             [0.946,]*4) * 1.e-4
visc = 0.0017
dens = 997.0
g = 9.80665
permeabilities = hydraulic_conduct * visc / (dens * g)

res_wcs = np.array([0.008,0.022,0.26,0.26,
                    0.008,0.12,0.12,0.12,
                    0.12,0.16,0.18,0.18,
                    0.24,0.32,0.34,0.34])
res_sats = np.array([wc/phi for wc,phi in zip(res_wcs,porosities)])

vg_alphas = 6.e-4 * np.ones((16,)) # made up!
vg_ms = 0.2 * np.ones((16,)) # made up!
res_sats = .2*np.random.rand(16)

# create the regions
region_list = plist.ParameterList("regions")
for i,s in enumerate(soils):
    region_list.append(aregions.createRegionLabeledSet(s,"cell", str(i+1), "mesh.exo"))
print "Regions list:"
print "-------------"
region_list.indent(0)
print region_list
print ""
print ""

    
# create the porosity functions
poro_funcs = []
for s,poro in zip(soils, porosities):
    func = afuncs.createConstantFunction(poro)
    poro_funcs.append(afuncs.createFunctionSpec(s,s,"cell",func))
porosity_spec = aevals.createIndependentVariableEvaluator("base_porosity",
                                                          poro_funcs)
print "Porosity list:"
print "-------------"
porosity_spec.indent(0)
print porosity_spec
print ""
print ""


# create the permeability functions
perm_funcs = []
for s,perm in zip(soils, permeabilities):
    func = afuncs.createConstantFunction(perm)
    perm_funcs.append(afuncs.createFunctionSpec(s,s,"cell",func))
perm_spec = aevals.createIndependentVariableEvaluator("permeability",
                                                          perm_funcs)

print "Permeability list:"
print "-------------"
perm_spec.indent(0)
print perm_spec
print ""
print ""


# create the WRMs
wrm_list = plist.ParameterList("WRM parameters")
for s, alpha, m, sr in zip(soils, vg_alphas, vg_ms, res_sats):
    wrm_list.append(wrm.createWRMvanGenuchten(s,alpha=alpha, m=m, residual_saturation=sr,
                                   smoothing_interval=100.0))


print "WRM list:"
print "-------------"
wrm_list.indent(0)
print wrm_list
print ""
print ""
    



