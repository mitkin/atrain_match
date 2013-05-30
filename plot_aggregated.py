#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2013 Adam.Dybbroe

# Author(s):

#   Adam.Dybbroe <a000680@c14526.ad.smhi.se>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Read all matched data and make some plotting
"""

from glob import glob
import os.path
import numpy as np
from datetime import datetime, timedelta
from scipy import histogram

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')


ROOT_DIR = "/local_disk/laptop/NowcastingSaf/FA/cloud_week_2013may/atrain_matchdata"


files = glob(ROOT_DIR + "/2012/??/arctic_europe_1km/*h5")

from matchobject_io import (readCaliopAvhrrMatchObj,
                            CalipsoAvhrrTrackObject)

caObj = CalipsoAvhrrTrackObject()
for filename in files:
    print os.path.basename(filename)
    caObj = caObj + readCaliopAvhrrMatchObj(filename)


dtimes = np.array([ datetime.utcfromtimestamp(t) for t 
                    in caObj.avhrr.all_arrays['sec_1970']])

isCloud = caObj.calipso.all_arrays['number_of_layers_found'] > 0
r16 = caObj.avhrr.all_arrays['r16micron']
t37 = caObj.avhrr.all_arrays['bt37micron']
t86 = caObj.avhrr.all_arrays['bt86micron']
t11 = caObj.avhrr.all_arrays['bt11micron']
t12 = caObj.avhrr.all_arrays['bt12micron']
thr_t11t12 = caObj.avhrr.all_arrays['thr_t11t12']
thr_t11t12_inv = caObj.avhrr.all_arrays['thr_t11t12_inv']

# nsidc 
# 255 = Coast
# 1-100 = Sea ice concentration %
# 101 = Permamnent ice
# 0 = Ice free
isIce = np.logical_and(caObj.calipso.all_arrays['nsidc'] >= 15,
                       caObj.calipso.all_arrays['nsidc'] <= 100)
isWater = np.logical_and(np.equal(caObj.calipso.all_arrays['igbp'], 17), 
                         np.equal(isIce, False))
isClearWater = np.logical_and(isWater, np.equal(isCloud, False))
isClearIce = np.logical_and(isIce, np.equal(isCloud, False))

maskdata = np.logical_or(t11<=-9, t12<=-9)
maskdata = np.logical_or(t86<=-9, np.equal(maskdata, True))

t11t12 = np.ma.array(t11 - t12, mask=maskdata)
t86t12 = np.ma.array(t86 - t12, mask=maskdata)
#t11t12 = np.ma.array(t11 - t12 - (thr_t11t12 + thr_t11t12_inv)/2.0, mask=maskdata)


# Masking out what is not a cloud ==> gives all cloudy pixels
t11t12_cloud = np.ma.masked_where(isCloud==False, t11t12).compressed()
t86t12_cloud = np.ma.masked_where(isCloud==False, t86t12).compressed()
#t11t12_clear = np.ma.masked_where(isCloud==True, t11t12).compressed()
t11t12_clear_ice = np.ma.masked_where(isClearIce==False, t11t12).compressed()
t86t12_clear_ice = np.ma.masked_where(isClearIce==False, t86t12).compressed()
t11t12_clear_water = np.ma.masked_where(isClearWater==False, t11t12).compressed()
t86t12_clear_water = np.ma.masked_where(isClearWater==False, t86t12).compressed()


"""
fig = plt.figure(figsize=(7,7))
ax = fig.add_subplot(111)
ax.scatter(t11t12_cloud, t86t12_cloud, marker='o', 
           color='b', label='cloud')
ax.scatter(t11t12_clear_water, t86t12_clear_water, marker='o', 
           color='r', label='open water')
ax.set_xlim(-10,10)
ax.set_ylim(-10,10)
ax.legend()
fig.show()
"""

fig = plt.figure(figsize=(9,8))
ax = fig.add_subplot(311)

n, bins, patches = ax.hist(t11t12_cloud, 
                           100, range=[-8,8],
                           normed=1, facecolor='green', alpha=0.75,
                           label='cloudy')
ax.set_ylabel('Frequency')
ax.set_title('T11-T12: Cloudy and clear pixels according to Caliop')
ax.set_xlim(-5, 8)
ax.legend()

ax = fig.add_subplot(312)
n, bins, patches = ax.hist(t11t12_clear_water, 
                           100, range=[-8,8],
                           normed=1, facecolor='blue', alpha=0.75,
                           label='open water (ice conc < 15%')
ax.legend()
ax.set_ylabel('Frequency')
ax.set_xlim(-5, 8)

ax = fig.add_subplot(313)
n, bins, patches = ax.hist(t11t12_clear_ice, 
                           100, range=[-8,8],
                           normed=1, facecolor='red', alpha=0.75,
                           label='cloudfree sea ice')
ax.legend()
ax.set_ylabel('Frequency')
ax.set_xlim(-5, 8)
ax.set_xlabel('T11-T12 (K)')

plt.savefig('./t11t12.png')
