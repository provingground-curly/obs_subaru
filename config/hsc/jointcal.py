import os.path
from lsst.utils import getPackageDir

filterMapFile = os.path.join(getPackageDir("obs_subaru"), "config", "hsc", "filterMap.py")
config.photometryRefObjLoader.load(filterMapFile)
config.astrometryRefObjLoader.load(filterMapFile)
config.applyColorTerms = True

config.colorterms.load(os.path.join(getPackageDir("obs_subaru"), "config", "hsc", "colorterms.py"))

config.sourceSelector.name = 'science'
# Use only stars because aperture fluxes of galaxies are biased and depend on seeing
config.sourceSelector['science'].doUnresolved = True
# with dependable signal to noise ratio.
config.sourceSelector['science'].doSignalToNoise = True
# Min SNR must be > 0 because jointcal cannot handle negative fluxes,
# otherwise selection of 10 is arbitrary
config.sourceSelector['science'].signalToNoise.minimum = 10.
# Base SNR on CalibFlux because that is the flux jointcal that fits and must be positive
config.sourceSelector['science'].signalToNoise.fluxField = 'slot_CalibFlux_instFlux'
config.sourceSelector['science'].signalToNoise.errField = 'slot_CalibFlux_instFluxErr'
# Do not trust blended sources' aperture fluxes which also depend on seeing
config.sourceSelector['science'].doIsolated = True
# Do not trust either flux or centroid measurements with flags (chosen from the usual QA flags for stars)
config.sourceSelector['science'].doFlags = True
badFlags = ['base_PixelFlags_flag_edge', 'base_PixelFlags_flag_saturated',
            'base_PixelFlags_flag_interpolatedCenter', 'base_SdssCentroid_flag',
            'base_PsfFlux_flag', 'base_PixelFlags_flag_suspectCenter']
config.sourceSelector['science'].flags.bad = badFlags
