
"""Read all matched data and make tables
"""
import os
from glob import glob
import numpy as np
from scipy import ndimage
from matchobject_io import (readCaliopAvhrrMatchObj,
                            CalipsoAvhrrTrackObject)

def get_clear_cloudy_vectors(caObj, use):#, both_have_ct):
    nlay =np.where(caObj.calipso.all_arrays['number_layers_found']>0,1,0)
    meancl=ndimage.filters.uniform_filter1d(nlay*1.0, size=3)
    isCalipsoCloudy = np.logical_and(
        nlay > 0, 
        caObj.calipso.all_arrays['cloud_fraction']>0.5)
    isCalipsoCloudy = np.logical_and(
        isCalipsoCloudy, 
        caObj.calipso.all_arrays['total_optical_depth_5km']>0.15)
    isCalipsoClear = np.logical_and(nlay == 0, meancl<0.01)
    isCalipsoClear = np.logical_and(
        isCalipsoClear, 
        caObj.calipso.all_arrays['total_optical_depth_5km']<0)
    isCloudyPPSorMAIA = np.logical_and(caObj.avhrr.all_arrays['cloudtype']>4,
                                       caObj.avhrr.all_arrays['cloudtype']<21) 
    isClearPPSorMAIA = np.logical_and(caObj.avhrr.all_arrays['cloudtype']>0,
                                      caObj.avhrr.all_arrays['cloudtype']<5)
    nodata = np.sum(caObj.avhrr.all_arrays['cloudtype'][use]>200)
    use = np.logical_and(use, np.logical_or(isCloudyPPSorMAIA, isClearPPSorMAIA))
    use = np.logical_and(use, np.logical_or(isCalipsoCloudy, isCalipsoClear))
    #use = np.logical_and(use, both_have_ct)
    #print isCalipsoCloudy[use].all()
    #print np.sum(isCalipsoCloudy[use])
    #print np.sum(np.logical_and(isCalipsoCloudy[use], 
    #                            isCloudyPPSorMAIA[use]))

    N_clouds = 1.0*np.sum(isCalipsoCloudy[use])
    N_clear = 1.0*np.sum(isCalipsoClear[use])
    N_detected_clouds= 1.0*np.sum(
        np.logical_and(isCalipsoCloudy[use], 
                       isCloudyPPSorMAIA[use]))
    N_undetected_clouds = 1.0*np.sum(
        np.logical_and(isCalipsoCloudy[use], 
                       isClearPPSorMAIA[use]))
    N_detected_clear = 1.0*np.sum(
        np.logical_and(isCalipsoClear[use], 
                       isClearPPSorMAIA[use]))
    N_false_clouds = 1.0*np.sum(
        np.logical_and(isCalipsoClear[use], 
                       isCloudyPPSorMAIA[use]))

    PODcloudy = np.divide(N_detected_clouds,N_clouds)
    FARcloudy = np.divide(N_false_clouds,np.sum(isCloudyPPSorMAIA[use]))
    PODclear = np.divide(N_detected_clear,N_clear)
    FARclear = np.divide(N_undetected_clouds,np.sum(isClearPPSorMAIA[use]))
    Kuipers_devider = (N_clouds*N_clear)
    Kuipers = np.divide((N_detected_clouds*N_detected_clear - 
                   N_false_clouds*N_undetected_clouds),Kuipers_devider)
    Num = np.sum(use)
    Hitrate = np.divide(N_detected_clouds + N_detected_clear,N_clouds+N_clear)
    #part_nodata = nodata*1.0/(nodata+Num)
    max_time_diff = np.max(caObj.diff_sec_1970[use])
    #print "N: %d POD-cloudy: %3.2f FAR-cloudy: %3.2f POD-clear %3.2f Max-time-diff %ds"%(# Part-CT-nodata: %3.2f"%(Num, PODcloudy, FARcloudy , PODclear, max_time_diff)#, part_nodata)
    print "%d"%(Num), "%3.2f"%(PODcloudy), "%3.2f"%(FARcloudy) , "%3.2f"%(PODclear), "%3.2f"%(FARclear),  "%3.3f"%(Hitrate), "%3.3f"%(Kuipers), "%d"%(max_time_diff)           

def print_common_stats(caObjMAIA, caObjPPS, y_month, satellite, dnt='all'):
    pps_sec_1970 = caObjPPS.calipso.all_arrays['sec_1970']
    maia_sec_1970 = caObjMAIA.calipso.all_arrays['sec_1970']
    pps_lat = caObjPPS.calipso.all_arrays['latitude']
    maia_lat = caObjMAIA.calipso.all_arrays['latitude']
    min_time_pps =  np.min(pps_sec_1970)
    max_time_pps =  np.max(pps_sec_1970)
    min_time_maia =  np.min(maia_sec_1970) 
    max_time_maia =  np.max(maia_sec_1970)
    min_lat_pps =  np.min(pps_lat)
    max_lat_pps =  np.max(pps_lat)
    min_lat_maia =  np.min(maia_lat) 
    max_lat_maia =  np.max(maia_lat)
    

        

    maia_profile_id = caObjMAIA.calipso.profile_id
    pps_profile_id = caObjPPS.calipso.profile_id

    #maia_ct = caObjMAIA.avhrr.all_arrays['cloudtype']
    pps_bt11 = caObjPPS.avhrr.all_arrays['bt11micron']
    pps_profile_id[pps_bt11<0]=-9
    pps_profile_id[caObjPPS.avhrr.all_arrays['cloudtype']<1]=-9
    pps_profile_id[caObjPPS.avhrr.all_arrays['cloudtype']>20]=-9
    maia_profile_id[caObjMAIA.avhrr.all_arrays['cloudtype']<1]=-9
    maia_profile_id[caObjMAIA.avhrr.all_arrays['cloudtype']>20]=-9
    #profile_id_in_both = np.intersect1d(maia_profile_id,pps_profile_id) 

    use_pps = pps_sec_1970>0
    use_maia = maia_sec_1970>0
    use_pps[pps_sec_1970<min_time_maia] = False
    use_pps[pps_sec_1970<min_time_maia] = False
    use_pps[caObjPPS.diff_sec_1970>600] = False
    use_maia[caObjMAIA.diff_sec_1970>600] = False
    use_maia[maia_sec_1970<min_time_pps] = False
    use_maia[maia_sec_1970>max_time_pps] = False
    use_pps[pps_lat<min_lat_maia] = False
    use_pps[pps_lat>max_lat_maia] = False
    use_maia[maia_lat<min_lat_pps] = False
    use_maia[maia_lat>max_lat_pps] = False
    use_maia[maia_profile_id<0] = False
    use_pps[pps_profile_id<0] = False

    sunz = caObjPPS.avhrr.all_arrays['sunz']*100
    #print sunz
    if dnt=='day and twilight':
        use_pps[sunz>=95.0]=False
    elif dnt=='twilight':
        use_pps[sunz>=95.0]=False
        use_pps[sunz<=80.0]=False
    elif dnt=='day':
        use_pps[sunz>80.0]=False
    elif dnt=='night':
        use_pps[sunz<95.0]=False

    use_maia_same_profile = np.array([p_id in pps_profile_id[use_pps] for p_id in maia_profile_id])
    use_pps_same_profile =  np.array([p_id in maia_profile_id[use_maia] for p_id in pps_profile_id])
    use_maia =  np.logical_and(use_maia, use_maia_same_profile)
    use_pps =   np.logical_and(use_pps, use_pps_same_profile)
    #print np.sum(use_maia), np.sum(use_pps)


    #both_have_ct = np.logical_and(caObjMAIA.avhrr.all_arrays['cloudtype']<20,
    #                              caObjPPS.avhrr.all_arrays['cloudtype']<200)

    if np.sum(use_maia)>50 and np.sum(use_pps)>50:
        print "MAIA",y_month, satellite, '-','-',
        get_clear_cloudy_vectors(caObjMAIA, use_maia)
        print "PPS",y_month, satellite, int(min(sunz[use_pps])),int(max(sunz[use_pps])),
        get_clear_cloudy_vectors(caObjPPS, use_pps)#, both_have_ct)


MAIA_ROOT_DIR = ("/home/a001865/VALIDATIONS/MAIA/Reshaped_Files/"
                 "*/1km/")
PPS_ROOT_DIR = ("/home/a001865/VALIDATIONS/PPS/Reshaped_Files/"
                "*/1km/")

print "Algorithm time satellite min-sunz, max-sunz, N PODcloudy FARcloudy PODclear FARclear Hitrate Kuipers Max-time-diff"
for y_month in ['2012/06','2012/07','2012/08','2012/10','2015/1201','2015/1207', '2015/07']:
    maia_files = glob(MAIA_ROOT_DIR + "%s/*/*h5"%(y_month))
    pps_files = glob(PPS_ROOT_DIR + "%s/*/*h5"%(y_month))
    caObjMAIA = CalipsoAvhrrTrackObject()
    caObjPPS = CalipsoAvhrrTrackObject()
    for filename in maia_files:
        caObjMAIA +=  readCaliopAvhrrMatchObj(filename)  
    for filename in pps_files:
        caObjPPS +=  readCaliopAvhrrMatchObj(filename) 
    satellite = 'Suomi-NPP'


    if y_month in ['2015/1201','2015/1207']:
        satellite = 'Metop-B'
        for dnt in ['day and twilight', 'night']:
            #print "Year, month, satellite %s %s %s"%(y_month, satellite, dnt)
            print_common_stats(caObjMAIA, caObjPPS,y_month, satellite, dnt=dnt)
    elif y_month in ['2015/07']:
        for dnt in ['day', 'twilight', 'night']:
            print_common_stats(caObjMAIA, caObjPPS,y_month, satellite, dnt=dnt)           
    else: 
        #for dnt in ['day and twilight', 'night']:
        #print "Year, month, satellite %s %s"%(y_month, satellite)
        print_common_stats(caObjMAIA, caObjPPS, y_month, satellite,)
