#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  6 22:16:42 2025

@author: markjhku
"""

from laser_calibration.ion_response_simulation import GaussianIonResponseSimulation
from matplotlib import pyplot as plt
import numpy as np

if __name__ == "__main__":
    
    sim = GaussianIonResponseSimulation(photon_number=1000,x_center=0.1,y_center=0.2,x_width=0.3,y_width=0.4)
    x_axis = np.linspace(-1,1,51)
    y_axis = np.linspace(-1,1,51)
    
    response = [[sim.measure_ion_response(x_val,y_val) for y_val in y_axis] for x_val in x_axis]
    
    x_grid,y_grid = np.meshgrid(x_axis,y_axis,indexing='ij')
    plt.pcolormesh(x_grid,y_grid,np.array(response))
    plt.xlabel("x")
    plt.ylabel("y")    