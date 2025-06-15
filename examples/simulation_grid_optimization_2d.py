#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: markjhku

This example demonstrates using grid_sweep_optimize routine for calibration.
"""

from laser_calibration.ion_response_simulation import GaussianIonResponseSimulation
from laser_calibration.laser_calibration_system import LaserCalibrationSystem

from laser_calibration.grid_sweep_optimize import grid_sweep_optimize

if __name__ == "__main__":
    
    # simulated response to be used
    sim = GaussianIonResponseSimulation(
        photon_number=100,
        x_center=0.1,
        y_center=0.2,
        x_width=0.3,
        y_width=0.4
        )
    
    # instantiate a LaserCalibrationSystem class    
    syst = LaserCalibrationSystem(
        ion_response_function=sim.measure_ion_response
        )

    # add mirrors to the LaserCalibrationSystem object
    syst.add_mirror("x", None)
    syst.add_mirror("y", None)    
    
    # the following two lines are needed for simulation mode
    syst.simulation = True
    syst.simulation_mirror_set = ["x","y"]
    
    # perform optimization of ion response to calibrate the system
    grid_sweep_optimize(laser_syst = syst)

