import ppshdf_cloudproducts
import ppshdf_helpers
from epshdf import (SafRegion, 
                    CloudType, 
                    SunSatAngleData)
import os
import netCDF4	
import numpy as np
import pps_io
import calendar
import datetime
from pps_error_messages import write_log
import time
import h5py
#from mpop.satin.nwcsaf_pps import NwcSafPpsChannel

#SPARC_resultdir = "/nobackup/smhid9/sm_kgkar/probmask_develop/prob_SPARC/data/

def sparc_read_prob(filename,prob_threshold,prob_result_dir,ctype_PPS):

    """Read cloudtype and flag info from filename
    """
    ctype = CloudType()
    ctype.region = SafRegion()
    #ctype.region.xsize=10
    #ctype.region.ysize=10
    ctype.des = "This is a faked SPARC cloudtype"
    ctype.cloudtype_des = "This is the cloudtype description"
    ctype.qualityflag_des = "This is the qualityflag description"
    ctype.phaseflag_des = "This is the phaseflag description"
    ctype.sec_1970 = "???"
    ctype.satellite_id = "????"

    ctype.cloudtype_lut.append("This is the first cloudtype lut")
    ctype.cloudtype_lut.append("This is the second cloudtype lut")
    ctype.qualityflag_lut.append("This is the first qualityflag lut")
    ctype.qualityflag_lut.append("This is the second qualityflag lut")
    ctype.phaseflag_lut.append("This is the first phaseflag lut")
    ctype.phaseflag_lut.append("This is the second phaseflag lut")

    #pps 1: cloudfree land 2:cloudfree sea
    #cci lsflag 0:sea 1:land
    write_log("WARNING", "Making skeleton cloudtype quality flag using "
              "sun zenith angels. "
              "This is ok for now, but will have to change "
              "when cloudtype flags are changed in pps v 2014!")
    #ctype.qualityflag = cci_nc.variables['lsflag'][::] 
    #ctype.qualityflag = ctype.qualityflag +128
    #Setting NWP_data_present when got day if we set nothing day pixels
    #over sea will have flag value == 0 and not be included.

    ctype.qualityflag = ctype_PPS.qualityflag #Just copying existing flags
##     ctype.qualityflag = np.where(
##         np.logical_and(
##             np.greater(avhrrAngObj.sunz.data,80),
##             np.less(avhrrAngObj.sunz.data,95)),
##         #np.equal(cci_nc.variables['illum'][::],2),#Twilight
##         ctype.qualityflag+8,#Twilight
##         ctype.qualityflag)
##     ctype.qualityflag = np.where(
##             np.greater_equal(avhrrAngObj.sunz.data,95),
##             #np.equal(cci_nc.variables['illum'][::],3),#Night
##             ctype.qualityflag+4,#Night
##             ctype.qualityflag)

    # Now open and read cloud probabilities

    sl_ = os.path.basename(filename).split('_avhrr')

    probname = "%s%s__cloudprob_SPARC.h5" % (prob_result_dir,sl_[0])
    print probname

    #noaa18_20091215_2318_99999_satproj_00000_13127__cloudprob_SPARC.h5

    h5file = h5py.File(probname,'r')
    dataset =h5file["/cloud_probability"]
    cloudprob = dataset.value
    h5file.close()
        
    #if cloud_prob higher than prob_threshold set ctype to 9: Medium level cumiliform cloud, otherwise 1 (clear Land)
    ctype.cloudtype = np.where(cloudprob>prob_threshold,9,1)
    ctype.phaseflag = None
    return ctype


if __name__ == "__main__":
    filename="20080613002200-ESACCI-L2_CLOUD-CLD_PRODUCTS-AVHRRGAC-NOAA18-fv1.0.nc"
    PPS_OBJECTS = cci_read_ctth(filename)
    print PPS_OBJECTS
