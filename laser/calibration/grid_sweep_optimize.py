#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: markjhku
"""

import numpy as np
from laser_calibration.laser_calibration_system import LaserCalibrationSystem
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt



def grid_sweep_optimize(laser_syst: LaserCalibrationSystem, optimize_over_axes: str | list[str] | None = None,  step: float = 0.1, plot: bool = True):
    """
        functino to perform grid sweep over up to 2 dimensions, and then
        perform Gaussian fit to find the optimal operating point.
        
        Arguments:
        laser_syst: a LaserCalibrationSystem instance
        
        Optional arguments:
        optimize_over_axes: str | list[str] | None. Specify which mirror
        axes to optmize over (if None, all is assumed)
        step: float, defaulted to 0.1. Step size of sweep
        plot: bool, defaulted to True. Whether to display the final plot.
    """
    
    if optimize_over_axes is None:
        optimize_over_axes = laser_syst.get_all_mirror_names()
    elif isinstance(optimize_over_axes, str):
        optimize_over_axes = [optimize_over_axes]
    
    dimension = len(optimize_over_axes)
    
    
    grid_values = np.arange(-1,1,step)
    
    if dimension == 1:
        model = gaussian_1d
           
        response = [laser_syst.move_mirrors_and_measure(x=x_val) for x_val in grid_values]
        response = np.array(response)
        independent_variables = grid_values
        
        amplitude_guess = np.max(response)
        x0_guess = independent_variables[np.argmax(response)]
        p0 = [amplitude_guess, x0_guess,.1]
        
    elif dimension == 2:
        model = gaussian_2d

        x,y = np.meshgrid(grid_values,grid_values,indexing='ij')
        independent_variables = (x,y)
        response = [[laser_syst.move_mirrors_and_measure(x=x_val,y=y_val) for y_val in grid_values] for x_val in grid_values]  
        response = np.array(response)
        
        index_x,index_y = np.unravel_index(np.argmax(response),shape=response.shape)
        amplitude_guess = np.max(response)
        x0_guess = grid_values[index_x]
        y0_guess = grid_values[index_y]        
        p0 = [amplitude_guess, x0_guess,.1,y0_guess,.1]
        
    else:
        m = "optimization over more than 2 dimensions are not yet implemented"
        raise NotImplementedError(m)
        
            
    response  = np.ravel(np.array(response ))
    popt, pcov = curve_fit(model,independent_variables,response,p0)
    
    if plot:
        if dimension == 1:
            
            plt.plot(grid_values,response,'o')
            x_fit = np.linspace(-1,1,101)
            plt.plot(x_fit,gaussian_1d(x_fit,*popt))
            plt.xlabel("x")
            plt.ylabel("Photon number")
            
            
        elif dimension == 2:
            response = response.reshape(x.shape)
            plt.pcolormesh(x,y,response)
            
            fit_model_z_values = gaussian_2d((x,y),*popt)
            fit_model_z_values = fit_model_z_values.reshape(x.shape)
            plt.contour(x,y,fit_model_z_values, cmap=plt.cm.copper)
            plt.pcolormesh(x,y,np.array(response))
            plt.xlabel("x")
            plt.ylabel("y")
            cbar = plt.colorbar()
            cbar.set_label("Photon number")


    move_mirrors_args = {}
    [move_mirrors_args.update({optimize_over_axes[index]:popt[index*2+1]}) for index in range(len(optimize_over_axes)) ]
    laser_syst.batch_move_mirrors(**move_mirrors_args)
    
    
    print("Fit parameters: "+str(popt))

    for mirror in optimize_over_axes:
        print("Mirror "+mirror + " moved to "+str(move_mirrors_args[mirror]))
    
    return move_mirrors_args
    
def gaussian_2d(x_y,A,x0,x_width,y0,y_width):
    x = x_y[0]
    y = x_y[1]    
    G= A*np.exp(-(x-x0)**2/(2*x_width**2) - (y-y0)**2/(2*y_width**2) )
    return np.ravel(G)

def gaussian_1d(x,A,x0,x_width):
 
    G= A*np.exp(-(x-x0)**2/(2*x_width**2))
    return np.ravel(G)