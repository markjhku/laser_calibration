#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  6 22:16:42 2025

@author: markjhku
"""

from laser_calibration.ion_response_simulation import GaussianIonResponseSimulation
from laser_calibration.laser_calibration_system import LaserCalibrationSystem

from laser_calibration.grid_sweep_optimize import grid_sweep_optimize

if __name__ == "__main__":
    
    sim = GaussianIonResponseSimulation(photon_number=100,x_center=0.1,y_center=0.2,x_width=0.3,y_width=0.4)
    
    
    syst = LaserCalibrationSystem(ion_response_function=sim.measure_ion_response)
    syst.simulation = True
    syst.add_mirror("x", None)
    syst.add_mirror("y", None)    
    syst.simulation_mirror_set = ["x","y"]
    grid_sweep_optimize(laser_syst = syst)
