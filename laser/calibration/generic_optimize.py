#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: markjhku
"""

import numpy as np
from laser_calibration.laser_calibration_system import LaserCalibrationSystem
from scipy.optimize import minimize



def generic_optimize(laser_syst: LaserCalibrationSystem, optimize_over_axes: str | list[str] | None = None,samples: int = 1):
    """
        function to calibrate by using scipy's optimize.minimize function.
        
        Arguments:
        laser_syst: a LaserCalibrationSystem instance
        
        Optional arguments:
        optimize_over_axes: str | list[str] | None. Specify which mirror
        samples: how many samples of measurements to take at a given point
    """
    if optimize_over_axes is None:
        optimize_over_axes = laser_syst.get_all_mirror_names()
    elif isinstance(optimize_over_axes, str):
        optimize_over_axes = [optimize_over_axes]
    
    dimension = len(optimize_over_axes)
    
    
    
    
    if dimension == 1:
        func = lambda x: -1*np.mean( [laser_syst.move_mirrors_and_measure(**{optimize_over_axes[0]:x}) for sample_number in range(samples)])
        bounds = ((-1,1),)
        x0 = (.1,)
    elif dimension == 2:
        func = lambda r: -1*np.mean( [laser_syst.move_mirrors_and_measure(**{optimize_over_axes[0]:r[0],optimize_over_axes[1]:r[1]}) for sample_number in range(samples)])
        bounds = ((-1,1),(-1,1),)
        x0 = (.1,.1,)
    else:
        m = "optimization over more than 2 dimensions are not yet implemented"
        raise NotImplementedError(m)
        
    result = minimize(func,x0=x0,bounds=bounds)        

    
    move_mirrors_args = {}
    [move_mirrors_args.update({optimize_over_axes[index]:result.x[index]}) for index in range(len(optimize_over_axes)) ]
    laser_syst.batch_move_mirrors(**move_mirrors_args)
    
    
    print("Fit parameters: "+str(result))

    for mirror in optimize_over_axes:
        print("Mirror "+mirror + " moved to "+str(move_mirrors_args[mirror]))
        
    return move_mirrors_args