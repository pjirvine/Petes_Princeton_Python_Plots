"""
Functions for Plot Notebook
"""

"""
Import needed modules
"""

import numpy as np
import sys
import cf
import os.path

from netCDF4 import Dataset
from mpl_toolkits.basemap import Basemap
from scipy.stats import ttest_ind_from_stats

"""
Define functions
"""

# This function retrieves the desired netcdf file.
def get_2d_geomip(var, exp, stat, var_internal, model='NorESM1-M', run='r1i1p1', time='11-50', seas='ann',
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
        f = Dataset(file_loc)
        if lon_lat: # Return variable array, latitude array, longitude array
            return (f.variables[var_internal][:].squeeze(), f.variables[lat_name][:], f.variables[lat_name][:])
        else:
            return f.variables[var_internal][:].squeeze()
    else:
        return None
    
def ttest_sub(mean_1, std_1, nyears_1, mean_2, std_2, nyears_2, equal_var=True):

    """
    Sub-routine to call ttest_ind_from_stats from scipy
    Checks that shapes match and turns integer years into correct format
    returns pvalue.
    """

    # check shapes match
    if (mean_1.shape, mean_1.shape, std_1.shape) != (std_1.shape, mean_2.shape, std_2.shape):
        return "array shapes don't match"

    # Convert nobs type
    nyears_1 = int(nyears_1)
    nyears_2 = int(nyears_2)

    # Create arrays like others for nobs
    nobs1_arr = (nyears_1-1) * np.ones_like(mean_1)
    nobs2_arr = (nyears_2-1) * np.ones_like(mean_1)

    """
    # ttest_ind_from_stats
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_ind_from_stats.html
    """

    ttest_out = ttest_ind_from_stats(mean_1, std_1, nobs1_arr, mean_2, std_2, nobs2_arr)

    # An array of p-values matching the shape of the input arrays
    pvalue_out = ttest_out[1]

    return pvalue_out