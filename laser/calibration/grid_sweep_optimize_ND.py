#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: markjhku
"""

import numpy as np
from laser_calibration.laser_calibration_system import LaserCalibrationSystem
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt

import itertools

def grid_sweep_optimize_ND(laser_syst: LaserCalibrationSystem, optimize_over_axes: str | list[str] | None = None, sweep_range: list | tuple | None = None, step: list[float] | tuple[float] | float = 0.1, plot: bool = True):
    """
        function to perform grid sweep over up to 2 dimensions, and then
        perform Gaussian fit to find the optimal operating point.
        
        Arguments:
        laser_syst: a LaserCalibrationSystem instance
        
        Optional arguments:
        optimize_over_axes: str | list[str] | None. Specify which mirror
        axes to optmize over (if None, all is assumed)
        plot: bool, defaulted to True. Whether to display the final plot.
    """
    
    if optimize_over_axes is None:
        optimize_over_axes = laser_syst.get_all_mirror_names()
    elif isinstance(optimize_over_axes, str):
        optimize_over_axes = [optimize_over_axes]
    
    dimension = len(optimize_over_axes)
    
    if isinstance(step,float):
        step = [step]*dimension
        
    if sweep_range is None:
        sweep_range = [[-1,1]]*dimension
        
    
    meshgrid_arg = [np.arange(sweep_range[index][0],sweep_range[index][1],step[index]) for index in range(dimension)] 
    independent_variables_grid = np.meshgrid(*meshgrid_arg, indexing="ij")
    independent_variables_ravel = list(itertools.product(*meshgrid_arg))
    all_mirror_names = laser_syst.get_all_mirror_names()
    response = np.array([laser_syst.move_mirrors_and_measure(**dict(zip(all_mirror_names,val))) for val in independent_variables_ravel])
    
    amplitude_guess = np.max(response)
    p0 = [amplitude_guess]
    for index in range(dimension):
        x = np.ravel(independent_variables_grid[index])
        center_guess = np.sum(x*response)/np.sum(response)
        width_guess = np.sum((x-center_guess)**2*response)/np.sum(response)*np.sqrt(2)
        p0.append(center_guess)
        p0.append(width_guess)        
    
    try:
        popt, pcov = curve_fit(gaussian_ND,independent_variables_grid,response,p0)
    except:
        print("Fit failed; exiting calibration")
        return    
    

    if any(np.isnan(popt)):
        print("Fit obtained NaN values; exiting calibration")
        return
    


    move_mirrors_args = {}
    [move_mirrors_args.update({optimize_over_axes[index]:popt[index*2+1]}) for index in range(len(optimize_over_axes)) ]
    laser_syst.batch_move_mirrors(**move_mirrors_args)
    

    for mirror in optimize_over_axes:
        print("\33[0;49;33mMirror "+mirror + " moved to:\33[0;49;38m "+str(move_mirrors_args[mirror]))
    
    return move_mirrors_args



def gaussian_ND(*args):
    """
        r = args[0]
        A = args[1]
        r1 = args[2]
        w1 = args[3]
        r2 = args[4]
        w2 = args[5]
        ...
        A.np.exp(-(r[0]-r1)**2/w1**2-(r[1]-r2)**2/w2**2...)
    """
    r = args[0]
    dim = len(r)
    arg = np.array([(r[index]-args[index*2+2])/args[index*2+3] for index in range(dim)])
    G= args[1]*np.exp(-np.sum(arg**2,0))

    return np.ravel(G)
    