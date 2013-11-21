"""
Configuration file for ``atrain_match``. Most configuration options and
constants used in ``atrain_match`` are set in this file. However, there may
still be some modules which have internal constants defined.

"""

import os
#Set to true if you always want an avhrr orbit that starts before the cross
ALWAYS_USE_AVHRR_ORBIT_THAT_STARTS_BEFORE_CROSS = False

#Choose one to validate
PPS_VALIDATION = False
print "PPS_VALIDATION", PPS_VALIDATION
CCI_CLOUD_VALIDATION = True 



COMPILE_RESULTS_SEPARATELY_FOR_SINGLE_LAYERS_ETC = True
OPTICAL_DETECTION_LIMIT = 0.3
ALSO_USE_5KM_FILES = True #5km data is needed to split result on optical depth of top layer.


#When using 1km data, use the 5km data to filterout clouds to thin for VIIRS/AVHRR to see.
#PARAMETERS FOR CHOOSING HOW TO FILTER DATA 1km RESOLUTION:
#If USE_5KM_FILES_TO_FILTER_CALIPSO_DATA is True, we take the cloud top to
# be OPTICAL_LIMIT_CLOUD_TOP down in the cloud. For clouds thinner than
# OPTICAL_LIMIT_CLOUD_TOP we use the cloud base as cloud top.
USE_5KM_FILES_TO_FILTER_CALIPSO_DATA = True
OPTICAL_LIMIT_CLOUD_TOP = 0.6
if USE_5KM_FILES_TO_FILTER_CALIPSO_DATA:
    ALSO_USE_5KM_FILES = True
 
EXCLUDE_CALIPSO_PIXEL_IF_TOTAL_OPTICAL_THICKNESS_TO_LOW = False
EXCLUDE_ALL_MULTILAYER = False
EXCLUDE_MULTILAYER_IF_TOO_THIN_TOP_LAYER = False
EXCLUDE_GEOMETRICALLY_THICK = False

H4H5_EXECUTABLE = os.environ.get('H4H5_EXECUTABLE','/local_disk/opt/h4h5tools-2.2.1-linux-x86_64-static/bin/h4toh5')
#H4H5_EXECUTABLE = '/software/apps/h4h5tools/2.2.1/i1214-hdf4-4.2.8-i1214-hdf5-1.8.9-i1214/bin/h4toh5'
PLOT_ONLY_PNG = True

#important for cph_validate.py
VAL_CPP = os.environ.get('VAL_CPP', True)
VALIDATE_FOR_CPP_PIXELS = True #means validating for cloudtype only for pixels where we also got cpp.cph values 

# Imager Instrument on which PPS has been run (currently you can only run the
# atrain match on either AVHRR data or VIIRS data, not both):
IMAGER_INSTRUMENT = os.environ.get('IMAGER_INSTRUMENT', 'viirs')

#: Resolution, in km, to use for data files. This setting is used throughout
#: ``atrain_match`` to specify file names, sub-directories, and data handling.
#: Currently, 1 or 5 is supported
RESOLUTION = int(os.environ.get('ATRAIN_RESOLUTION', 1))
if RESOLUTION == 1:
    AVHRR_SAT = 'NPP' #'pps'
    CALIPSO_CLOUD_FRACTION = False
    ALSO_USE_1KM_FILES = False
elif RESOLUTION == 5:
    AVHRR_SAT = 'NOAA18'
    # CALIPSO_CLOUD_FRACTION = True   Introduced when the idea was to use single_shot_cloud_cleared_fraction, now abandoned!
    CALIPSO_CLOUD_FRACTION = False  #Notice that both these parameters must equal, i.e. set to either True or False!!!/KG
    ALSO_USE_1KM_FILES = False

#: Base directory for validation results
#_validation_results_dir = os.environ['VALIDATION_RESULTS_DIR']    
_validation_results_dir = os.environ.get('VALIDATION_RESULTS_DIR', "/nobackup/smhid9/sm_kgkar/atrain_match_2013")
#Not really used????/KG

#: Don't know how this directory is used...
MAIN_RUNDIR = os.getcwd()

#: Base directory for validation results
#MAIN_DIR = os.environ.get('VALIDATION_RESULTS_DIR', "/nobackup/smhid9/sm_erjoh/atrain_match")
MAIN_DIR = os.environ.get('VALIDATION_RESULTS_DIR', "/nobackup/smhid9/sm_kgkar/atrain_match_2013")
#: Base directory where matchup files are stored. (TODO: Are these still used?)
#SUB_DIR = "%s/Matchups" %MAIN_DIR
#SUB_DIR = "%s/Matchups_prob" %MAIN_DIR #Used for reprocessed dataset for probmask studies

#: Base directory for files containing matched data from PPS and Calipso/Cloudsat
RESHAPE_DIR = "%s/Reshaped_Files" %MAIN_DIR
#RESHAPE_DIR = "%s/Reshaped_Files_prob" %MAIN_DIR #Used for reprocessed dataset for probmask studies

#: TODO: How is this directory used?
#DATA_DIR = "%s/Data" %MAIN_DIR

#: Base directory for plots
PLOT_DIR = "%s/Plot" %MAIN_DIR

#: Base directory for statistics results
#RESULT_DIR = "%s/Results_prob" %MAIN_DIR
RESULT_DIR = "Results" 


# Region configuaration file with area definitons
AREA_CONFIG_FILE = os.environ.get('AREA_CONFIG_FILE', './areas.def')

#_satellite_data_dir = '/data/arkiv/proj/safworks/data'
_satellite_data_dir = '/nobackup/smhid9/sm_kgkar/atrain_match_2013/testdata'

#: Base dir for PPS data
# PPS_DATA_DIR = os.environ.get('PPS_DATA_DIR', _satellite_data_dir + '/pps')
#PPS_DATA_DIR = "%s/%s" % (SAT_DIR, AVHRR_SAT)
#PPS_DATA_DIR = "%s/%s_probmask" % (SAT_DIR, AVHRR_SAT) # Just to select reprocessed dataset for probmask

#: Base dir for Cloudsat data
CLOUDSAT_DIR = os.environ.get('CLOUDSAT_DIR', _satellite_data_dir + '/cloudsat')

#: Cloudsat data type (currently 'GEOPROF' and 'CWC-RVOD' are supported)
#CLOUDSAT_TYPE = 'CWC-RVOD'
CLOUDSAT_TYPE = 'GEOPROF'

#: Base dir for Calipso data
CALIPSO_DIR = os.environ.get('CALIPSO_DIR', _satellite_data_dir + '/calipso')



#: Constant: Approximate duration of a satellite orbit in seconds
SAT_ORBIT_DURATION = 110*60 #Not to large
# If to large, cloudsat_calipso_avhrr_match.py takes wrong swath
# sometimes when swaths are close in time



#: Allowed time deviation in seconds between AVHRR and CALIPSO/CloudSat matchup

sec_timeThr = 60*20



#: Recommended cloud threshold for the CloudSat cloud mask. In 5km data this
#: threshold has already been applied, so there is no reason to change it for
#: this data set.
CLOUDSAT_CLOUDY_THR = 30.0 

#: MAXHEIGHT is used in the plotting. 
#: If None the maxheight is calculated from the highest cloud
#MAXHEIGHT = None
MAXHEIGHT = None

#: Range of allowed (AVHRR) satellite azimuth angles, in degrees
AZIMUTH_RANGE = (0., 360.)

#: TODO: No description...
EMISS_MIN_HEIGHT = 2000.0

#: A value of 0.2-0.3 in cloud emissivity seems reasonable
EMISS_LIMIT = 0.2


#: Processing modes which can be handled
#  OBS: I removed the 'EMISSFILT'-cases!The reason is to avoid the need to use any NWP-data
#       (in this case surface temperature). Besides - we can now use optical thickness filtering
#       which is much more reliable as concerns removal of contributions from thin clouds. /KG 120925
# TODO: Split into latitude dependent area, snow-ice-land-sea area and day-night-twilight
ALLOWED_MODES = ['BASIC',
                 'BASIC_DAY',
                 'BASIC_NIGHT',
                 'BASIC_TWILIGHT', 
#                 'EMISSFILT',       # Filter out cases with the thinnest topmost CALIPSO layers
#                 'EMISSFILT_DAY',
#                 'EMISSFILT_NIGHT',
#                 'EMISSFILT_TWILIGHT',    
                 'ICE_COVER_SEA',   # Restrict to ice cover over sea using NSIDC and IGBP data
                 'ICE_COVER_SEA_DAY',    
                 'ICE_COVER_SEA_NIGHT',    
                 'ICE_COVER_SEA_TWILIGHT',    
                 'ICE_FREE_SEA',    # Restrict to ice-free sea using NSIDC and IGBP data
                 'ICE_FREE_SEA_DAY',     
                 'ICE_FREE_SEA_NIGHT',     
                 'ICE_FREE_SEA_TWILIGHT',  
                 'SNOW_COVER_LAND', # Restrict to snow over land using NSIDC and IGBP data
                 'SNOW_COVER_LAND_DAY',
                 'SNOW_COVER_LAND_NIGHT', 
                 'SNOW_COVER_LAND_TWILIGHT',
                 'SNOW_FREE_LAND',  # Restrict to snow-free land using NSIDC and IGBP data
                 'SNOW_FREE_LAND_DAY',
                 'SNOW_FREE_LAND_NIGHT',
                 'SNOW_FREE_LAND_TWILIGHT',
                 'COASTAL_ZONE',    # Restrict to coastal regions using NSIDC data (mixed microwave region)
                 'COASTAL_ZONE_DAY',
                 'COASTAL_ZONE_NIGHT',
                 'COASTAL_ZONE_TWILIGHT',
                 'TROPIC_ZONE',     # Restrict to tropical regions lat <= +- 10
                 'TROPIC_ZONE_DAY',
                 'TROPIC_ZONE_NIGHT',
                 'TROPIC_ZONE_TWILIGHT',
                 'TROPIC_ZONE_SNOW_FREE_LAND',      # Restrict to tropical regions  +-10 < lat <= +-45
                 'TROPIC_ZONE_SNOW_FREE_LAND_DAY',
                 'TROPIC_ZONE_SNOW_FREE_LAND_NIGHT',
                 'TROPIC_ZONE_SNOW_FREE_LAND_TWILIGHT',
                 'TROPIC_ZONE_ICE_FREE_SEA',        # Restrict to tropical regions  +-10 < lat <= +-45
                 'TROPIC_ZONE_ICE_FREE_SEA_DAY',
                 'TROPIC_ZONE_ICE_FREE_SEA_NIGHT',
                 'TROPIC_ZONE_ICE_FREE_SEA_TWILIGHT',
                 'SUB_TROPIC_ZONE',     # Restrict to sub tropical regions +-10 < lat <= +-45
                 'SUB_TROPIC_ZONE_DAY',
                 'SUB_TROPIC_ZONE_NIGHT',
                 'SUB_TROPIC_ZONE_TWILIGHT',
                 'SUB_TROPIC_ZONE_SNOW_FREE_LAND',      # Restrict to tropical regions  +-10 < lat <= +-45
                 'SUB_TROPIC_ZONE_SNOW_FREE_LAND_DAY',
                 'SUB_TROPIC_ZONE_SNOW_FREE_LAND_NIGHT',
                 'SUB_TROPIC_ZONE_SNOW_FREE_LAND_TWILIGHT',
                 'SUB_TROPIC_ZONE_ICE_FREE_SEA',        # Restrict to tropical regions  +-10 < lat <= +-45
                 'SUB_TROPIC_ZONE_ICE_FREE_SEA_DAY',
                 'SUB_TROPIC_ZONE_ICE_FREE_SEA_NIGHT',
                 'SUB_TROPIC_ZONE_ICE_FREE_SEA_TWILIGHT',
                 'HIGH-LATITUDES',     # Restrict to tropical regions  +-45 < lat <= +-75
                 'HIGH-LATITUDES_DAY',
                 'HIGH-LATITUDES_NIGHT',
                 'HIGH-LATITUDES_TWILIGHT',
                 'HIGH-LATITUDES_SNOW_FREE_LAND',      # Restrict to tropical regions  +-45 < lat <= +-75
                 'HIGH-LATITUDES_SNOW_FREE_LAND_DAY',
                 'HIGH-LATITUDES_SNOW_FREE_LAND_NIGHT',
                 'HIGH-LATITUDES_SNOW_FREE_LAND_TWILIGHT',
                 'HIGH-LATITUDES_ICE_FREE_SEA',        # Restrict to tropical regions  +-45 < lat <= +-75
                 'HIGH-LATITUDES_ICE_FREE_SEA_DAY', 
                 'HIGH-LATITUDES_ICE_FREE_SEA_NIGHT',
                 'HIGH-LATITUDES_ICE_FREE_SEA_TWILIGHT',
                 'HIGH-LATITUDES_SNOW_COVER_LAND',      # Restrict to tropical regions  +-45 < lat <= +-75
                 'HIGH-LATITUDES_SNOW_COVER_LAND_DAY',
                 'HIGH-LATITUDES_SNOW_COVER_LAND_NIGHT',
                 'HIGH-LATITUDES_SNOW_COVER_LAND_TWILIGHT',
                 'HIGH-LATITUDES_ICE_COVER_SEA',        # Restrict to tropical regions  +-45 < lat <= +-75
                 'HIGH-LATITUDES_ICE_COVER_SEA_DAY',
                 'HIGH-LATITUDES_ICE_COVER_SEA_NIGHT',
                 'HIGH-LATITUDES_ICE_COVER_SEA_TWILIGHT',
                 'POLAR',     # Restrict to tropical regions  +-75
                 'POLAR_DAY',
                 'POLAR_NIGHT',
                 'POLAR_TWILIGHT', 
                 'POLAR_SNOW_FREE_LAND',      # Restrict to tropical regions  +-75
                 'POLAR_SNOW_FREE_LAND_DAY',
                 'POLAR_SNOW_FREE_LAND_NIGHT',
                 'POLAR_SNOW_FREE_LAND_TWILIGHT',
                 'POLAR_ICE_FREE_SEA',        # Restrict to tropical regions  +-75
                 'POLAR_ICE_FREE_SEA_DAY', 
                 'POLAR_ICE_FREE_SEA_NIGHT',
                 'POLAR_ICE_FREE_SEA_TWILIGHT',
                 'POLAR_SNOW_COVER_LAND',      # Restrict to tropical regions  +-75
                 'POLAR_SNOW_COVER_LAND_DAY',
                 'POLAR_SNOW_COVER_LAND_NIGHT',
                 'POLAR_SNOW_COVER_LAND_TWILIGHT',
                 'POLAR_ICE_COVER_SEA',        # Restrict to tropical regions  +-75
                 'POLAR_ICE_COVER_SEA_DAY',
                 'POLAR_ICE_COVER_SEA_NIGHT',
                 'POLAR_ICE_COVER_SEA_TWILIGHT']
#latitude_filter = ['TROPICAL', 'SUB-TROPIC-ZONE', 'HIGH-LATITUDES', 'POLAR']
#land_filter = ['SNOW-COVER-LAND', 'SNOW-FREE-LAND', 'ICE-FREE-SEA', 'ICE-COVER-SEA']
#day_night_filter = ['DAY', 'NIGHT', 'TWILIGHT']
#modes = set()
#modes.add('BASIC') # no filtering
#for lat in latitude_filter:
#    modes.add(lat)
#    for land in land_filter:
#        modes.add('_'.join([lat, land]))
#        modes.add(land)
#        for day in day_night_filter:
#            modes.add('_'.join([lat, land, day]))
#            modes.add('_'.join([lat, day]))
#            modes.add(day)
    


#: Threshold for optical thickness. If optical thickness is below this value it will be filtered out.
#MIN_OPTICAL_DEPTH = 0.35 # Original formulation - only allowing one value
#MIN_OPTICAL_DEPTH = [0.35] # New formulation - allowing a set of values
MIN_OPTICAL_DEPTH = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00]


print "RESOLUTION=", RESOLUTION
if RESOLUTION == 1:
    if IMAGER_INSTRUMENT == 'viirs':
        # VIIRS scan period is 1.7864 - see
        # D34862-07-01_C_CDFCB-X_Volume_VII-Part_1_ECR1017D_PR.pdf
        # Adam, 2012-10-21
        DSEC_PER_AVHRR_SCALINE = 1.7864 / 16.
        #DSEC_PER_AVHRR_SCALINE = 60 / 40. # ??? AD, 2012-Oct
        SWATHWD=3200
    else:
        DSEC_PER_AVHRR_SCALINE = 1.0/6. # Full scan period, i.e. the time
                                        # interval between two consecutive
                                        # lines (sec)
        SWATHWD=2048
    AREA = "arctic_europe_1km"
#    AREA = "npole"
    #AREA = "arctic_super_5010"
#    AREA = "cea1km_test"
    #: CloudSat sampling frequency in km (or rather the most likely
    #: resolution difference between CALIPSO 1 km datasets and
    #: the CloudSat 2B-GEOPROF dataset). Nominally CloudSat sampling
    #: rate is said to be 1.1 km but it seems as the CALIPSO sampling
    #: rate is not exactly 1 km but slightly above - as based on the
    #: optimised matching of plots of the two datasets.
    # TODO: Try too remove this one. Should be much better if it could be \
    # calculated instead inside atrain_match sugestion: \
    # cloudsat_track_resolution = len(calipso.longitude) / len(cloudsat.longitude)
    CLOUDSAT_TRACK_RESOLUTION = 1.076
    if USE_5KM_FILES_TO_FILTER_CALIPSO_DATA:
        ALLOWED_MODES.append('OPTICAL_DEPTH')      # Filter out cases with the thinnest topmost CALIPSO layers. Define MIN_OPTICAL_DEPTH above
        ALLOWED_MODES.append('OPTICAL_DEPTH_DAY')
        ALLOWED_MODES.append('OPTICAL_DEPTH_NIGHT')
        ALLOWED_MODES.append('OPTICAL_DEPTH_TWILIGHT')
elif RESOLUTION == 5:
    DSEC_PER_AVHRR_SCALINE = 1.0/6. * 4 # A "work for the time being" solution.
    SWATHWD=409
    AREA = "cea5km_test"#"arctic_super_1002_5km"
    #: See :data:`CLOUDSAT_TRACK_RESOLUTION` in RESOLUTION = 1km
    CLOUDSAT_TRACK_RESOLUTION = 1.076#*5.0
    CLOUDSAT5KM_TRACK_RESOLUTION = CLOUDSAT_TRACK_RESOLUTION#*5.0


    ALLOWED_MODES.append('OPTICAL_DEPTH')      # Filter out cases with the thinnest topmost CALIPSO layers. Define MIN_OPTICAL_DEPTH above
    ALLOWED_MODES.append('OPTICAL_DEPTH_DAY')
    ALLOWED_MODES.append('OPTICAL_DEPTH_NIGHT')
    ALLOWED_MODES.append('OPTICAL_DEPTH_TWILIGHT')   #Let's run these cases separately but comment them all out if you always want to do filtering/KG
else:
    raise ValueError("RESOLUTION == %s not supported" % str(RESOLUTION))


#: TODO: No description
COMPRESS_LVL = 6

#: TODO: No description
NLINES=6000

#: TODO: No description
NODATA=-9

#: Processing modes for which plotting should also be performed
PLOT_MODES = ['BASIC']
#PLOT_MODES = ['No Plot']


def subdir(self, date, *args, **kwargs):
    """
    This method is used in all ``file_finders`` instances created in 
    :mod:`cloudsat_calipso_avhrr_match`, for finding the correct sub-directory.
    
    It is required to handle the listed arguments *self*, and *date*, as well as
    any other arguments (:emphasis:`*args`) or keyword arguments 
    (:emphasis:`**kwargs`) passed to it. It should return a string containing
    the sub-directory where the file can be found.
    
    Note that :func:`subdir` is used in several different ``file_finders``
    classes (sub-classes of :class:`file_finders.SatelliteDataFileFinder`).
    ``self.__class__`` can be used to check for a particular ``file_finders``
    class, e.g.::
    
        def subdir(self, date, *args, **kwargs):
            from file_finders import PpsFileFinder
            if self.__class__ is PpsFileFinder:
                return "some/subdir/specific/to/your/pps/files"
            else:
                # Just use default subdir for the instance's class
                return self.__class__.subdir(self, date, *args, **kwargs)
    
    """
    
    # If default subdirs should be used, the following line should be uncommented
    return self.__class__.subdir(self, date, *args, **kwargs)
    
    # Example of how to set non-default subdirs for PpsFileFinder instances:
    from file_finders import PpsFileFinder #@UnresolvedImport
    if self.__class__ is PpsFileFinder:
        ending = kwargs.get('ending', None)
        if ending is None:
            ending = self.ending

        _dir = "%dkm/%d/%02d" % (RESOLUTION, date.year, date.month)
        if 'avhrr' in ending or 'viirs' in ending:
            return os.path.join(_dir,"import/PPS_data")                
        if 'sunsatangles' in ending:
            return os.path.join(_dir, "import/ANC_data")
        if 'nwp' in ending:
            return os.path.join(_dir,"import/NWP_data")
            
        for export_ending in ['cloudmask', 'cloudtype', 'ctth', 'precip']:
            if export_ending in ending:
                return os.path.join(_dir, "export")
    else:
        return self.__class__.subdir(self, date, *args, **kwargs)

#========== Statistics setup ==========#
#: List of dictionaries containing *satname*, *year*, and *month*, for which
#: statistics should be summarized
#CASES = [{'satname': 'npp', 'year': 2012, 'month': 06}]
CASES = [{'satname': 'noaa18', 'year': 2006, 'month': 10},
         {'satname': 'noaa18', 'year': 2006, 'month': 11},
         {'satname': 'noaa18', 'year': 2006, 'month': 12},
         {'satname': 'noaa18', 'year': 2007, 'month': 1},
         {'satname': 'noaa18', 'year': 2007, 'month': 2},
         {'satname': 'noaa18', 'year': 2007, 'month': 3},
         {'satname': 'noaa18', 'year': 2007, 'month': 4},
         {'satname': 'noaa18', 'year': 2007, 'month': 5},
         {'satname': 'noaa18', 'year': 2007, 'month': 6},
         {'satname': 'noaa18', 'year': 2007, 'month': 7},
         {'satname': 'noaa18', 'year': 2007, 'month': 8},
         {'satname': 'noaa18', 'year': 2007, 'month': 9},
         {'satname': 'noaa18', 'year': 2007, 'month': 10},
         {'satname': 'noaa18', 'year': 2007, 'month': 11},
         {'satname': 'noaa18', 'year': 2007, 'month': 12},
         {'satname': 'noaa18', 'year': 2008, 'month': 1},
         {'satname': 'noaa18', 'year': 2008, 'month': 2},
         {'satname': 'noaa18', 'year': 2008, 'month': 3},
         {'satname': 'noaa18', 'year': 2008, 'month': 4},
         {'satname': 'noaa18', 'year': 2008, 'month': 5},
         {'satname': 'noaa18', 'year': 2008, 'month': 6},
         {'satname': 'noaa18', 'year': 2008, 'month': 7},
         {'satname': 'noaa18', 'year': 2008, 'month': 8},
         {'satname': 'noaa18', 'year': 2008, 'month': 9},
         {'satname': 'noaa18', 'year': 2008, 'month': 10},
         {'satname': 'noaa18', 'year': 2008, 'month': 11},
         {'satname': 'noaa18', 'year': 2008, 'month': 12},
         {'satname': 'noaa18', 'year': 2009, 'month': 1},
         {'satname': 'noaa18', 'year': 2009, 'month': 2},
         {'satname': 'noaa18', 'year': 2009, 'month': 3},
         {'satname': 'noaa18', 'year': 2009, 'month': 4},
         {'satname': 'noaa18', 'year': 2009, 'month': 5},
         {'satname': 'noaa18', 'year': 2009, 'month': 6},
         {'satname': 'noaa18', 'year': 2009, 'month': 7},
         {'satname': 'noaa18', 'year': 2009, 'month': 8},
         {'satname': 'noaa18', 'year': 2009, 'month': 9},
         {'satname': 'noaa18', 'year': 2009, 'month': 10},
         {'satname': 'noaa18', 'year': 2009, 'month': 11},
         {'satname': 'noaa18', 'year': 2009, 'month': 12}]

CASES = [{'satname': 'npp', 'year': 2012, 'month': 6},
         {'satname': 'npp', 'year': 2012, 'month': 7},
         {'satname': 'npp', 'year': 2012, 'month': 8},
         {'satname': 'npp', 'year': 2012, 'month': 9},
         {'satname': 'npp', 'year': 2012, 'month': 10}]

#: PPS area definition (from ``acpg/cfg/region_config.cfg``) for which
#: statistics should be summarized
MAP = [AREA]

#: Base directory for ``atrain_match`` output to use when summarizing statistics.
#: Should contain the ``Results`` directory
MAIN_DATADIR = MAIN_DIR

#: TODO: No description yet...
# Seems like this can't be set to True if we run without Calipso 5km data!
# ??? Adam 2012-10-14
if CALIPSO_CLOUD_FRACTION == True:
    #COMPILED_STATS_FILENAME = '%s/Results_prob/compiled_stats_CCF' %MAIN_DATADIR
    COMPILED_STATS_FILENAME = '%s/Results_cloudthreshold_0.3/compiled_stats_CCF' %MAIN_DATADIR
else:
    #COMPILED_STATS_FILENAME = '%s/Results_prob/compiled_stats' %MAIN_DATADIR
    COMPILED_STATS_FILENAME = '%s/Results_cloudthreshold_0.3/compiled_stats' %MAIN_DATADIR
    
#: Surfaces for which statistics should be summarized
SURFACES = ["ICE_COVER_SEA", "ICE_FREE_SEA", "SNOW_COVER_LAND", "SNOW_FREE_LAND", \
            "COASTAL_ZONE", "TROPIC_ZONE", "TROPIC_ZONE_SNOW_FREE_LAND", "TROPIC_ZONE_ICE_FREE_SEA", \
            "SUB_TROPIC_ZONE", "SUB_TROPIC_ZONE_SNOW_FREE_LAND", "SUB_TROPIC_ZONE_ICE_FREE_SEA", \
            "HIGH-LATITUDES", "HIGH-LATITUDES_SNOW_FREE_LAND", "HIGH-LATITUDES_ICE_FREE_SEA", \
            "HIGH-LATITUDES_SNOW_COVER_LAND", "HIGH-LATITUDES_ICE_COVER_SEA", \
            "POLAR", "POLAR_SNOW_FREE_LAND", "POLAR_ICE_FREE_SEA", \
            "POLAR_SNOW_COVER_LAND", "POLAR_ICE_COVER_SEA"]

#: Filter types for which statistics should be summerized
#FILTERTYPE = ['EMISSFILT']
FILTERTYPE = ['OPTICAL_DEPTH']
if RESOLUTION == 5:
    #FILTERTYPE.append('OPTICAL_DEPTH')
    FILTERTYPE = ['OPTICAL_DEPTH']
#: DAY NIGHT TWILIGHT FLAG that will be used
#DNT_FLAG = ['ALL']
DNT_FLAG = ['ALL', 'DAY', 'NIGHT', 'TWILIGHT']
    
# The following are used in the old-style script interface
SATELLITE = ['noaa18', 'noaa19']
STUDIED_YEAR = ["2009"]
STUDIED_MONTHS = ['01', '07']
OUTPUT_DIR = "%s/Ackumulering_stat/Results/%s" % (MAIN_DATADIR, SATELLITE[0])

