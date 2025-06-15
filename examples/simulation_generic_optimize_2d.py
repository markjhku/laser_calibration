#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: markjhku

This example demonstrates using generic_optimize routine for calibration.
"""

from laser_calibration.ion_response_simulation import GaussianIonResponseSimulation
from laser_calibration.laser_calibration_system import LaserCalibrationSystem

from laser_calibration.generic_optimize import generic_optimize

if __name__ == "__main__":
    # simulated response to be used
    # note that `use_poisson_distribution` is set to False; this is because
    # generic_optimize is not robust against noise
    sim = GaussianIonResponseSimulation(photon_number=100,x_center=-0.325,y_center=.523,x_width=0.3,y_width=0.2,use_poisson_distribution=False)
    
    # instantiate a LaserCalibrationSystem class    
    syst = LaserCalibrationSystem(ion_response_function=lambda x,y: sim.measure_ion_response(x,y))
    
    # add mirrors to the LaserCalibrationSystem object
    syst.add_mirror("x", None)
    syst.add_mirror("y", None)    

    # the following two lines are needed for simulation mode    
    syst.simulation = True
    syst.simulation_mirror_set = ["x","y"]
    
    # perform optimization of ion response to calibrate the system
    generic_optimize(syst)
