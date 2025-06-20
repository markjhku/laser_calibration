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
    
    photon_number = 100
    x_center = -.325
    x_width = 0.3
    
    # the parameters for y are just dummy parameters and can be anything
    y_center = 0 
    y_width = 100
    print(f"x location used in simulation: ({x_center})")
    sim = GaussianIonResponseSimulation(
        photon_number=photon_number,
        x_center=x_center,
        y_center=y_center,
        x_width=x_width,
        y_width=y_width,
        use_poisson_distribution=False
        )    
        
    # instantiate a LaserCalibrationSystem class
    # Note how we set up a strictly 1D system here
    syst = LaserCalibrationSystem(ion_response_function=lambda x: sim.measure_ion_response(x,0))

    # add mirrors to the LaserCalibrationSystem object
    syst.add_mirror("x", None)
    
    # the following two lines are needed for simulation mode    
    syst.simulation = True
    syst.simulation_mirror_set = ["x"]
    
    # perform optimization of ion response to calibrate the system
    generic_optimize(syst)
