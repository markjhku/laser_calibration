#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  6 22:16:42 2025

@author: markjhku
"""

from laser_calibration.ion_response_simulation import GaussianIonResponseSimulation
from laser_calibration.laser_calibration_system import LaserCalibrationSystem

from laser_calibration.generic_optimize import generic_optimize

if __name__ == "__main__":
    
    sim = GaussianIonResponseSimulation(photon_number=100,x_center=-0.235,y_center=0,x_width=0.3,y_width=100,use_poisson_distribution=False)
    
    
    syst = LaserCalibrationSystem(ion_response_function=lambda x: sim.measure_ion_response(x,y=0))
    syst.simulation = True
    syst.add_mirror("x", None)
    syst.simulation_mirror_set = ["x"]
    generic_optimize(syst)
