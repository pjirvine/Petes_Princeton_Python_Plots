"""
Functions for Plot Notebook
"""

"""
Import needed modules
"""

import numpy as np
import pandas as pd
import copy
import sys
import cf
import itertools
import os.path

from netCDF4 import Dataset
from mpl_toolkits.basemap import Basemap
from scipy.stats import ttest_ind_from_stats

"""
Define functions
"""

# This function retrieves the desired netcdf file.
def get_2d_geomip(var, exp, stat, model='NorESM1-M', run='r1i1p1', time='11-50', seas='ann',
                    lon_lat=False, lat_name='lat', lon_name='lon'):

    """
    Returns array of netcdf file along with latitude and longitude if option selected.
    (data.array [, lat.array, lon.array])
    """
    # Define nc_file format
    nc_file_base = "{var}_{model}_{exp}_{run}_{time}_{seas}_{stat}.nc"
    nc_file = nc_file_base.format(var=var, model=model, exp=exp, run=run, time=time, seas=seas, stat=stat)

    file_loc = "data/" + nc_file

    if os.path.isfile(file_loc):
        f = cf.read(file_loc)
        if lon_lat:
            return (f.array.squeeze(), f.dim(lat_name).array, f.dim(lon_name).array)
        else:
            return f.array.squeeze()
    else:
        return None
    
  