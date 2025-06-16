#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: markjhku

This example demonstrates using grid_sweep_optimize routine for calibration.
"""

from laser_calibration.ion_response_simulation import GaussianIonResponseSimulation
from laser_calibration.laser_calibration_system import LaserCalibrationSystem

from laser_calibration.grid_sweep_optimize import grid_sweep_optimize
from matplotlib import pyplot as plt

if __name__ == "__main__":
    
    
    print("TEST WITH A STANDARD SET OF PARAMETERS")
    # simulated response to be used
    photon_number = 100
    x_center = 0.1
    y_center = 0.2
    x_width = 0.3
    y_width = 0.4
    
    print(f"\33[0;49;36mx and y location used in simulation:\33[0;49;38m ({x_center}, {y_center})")
    sim = GaussianIonResponseSimulation(
        photon_number=photon_number,
        x_center=x_center,
        y_center=y_center,
        x_width=x_width,
        y_width=y_width
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
    result = grid_sweep_optimize(laser_syst = syst)
    x_result = result['x']
    y_result = result['y']    
    print(f"\33[0;49;36Ion location found with deviation\33[0;49;38m ({x_center-x_result}, {y_center-y_result}) ")
    
    
    ###### The following demonstrate the performance in an extreme case of
    ###### low photon number and narrow width comparable to step size
    print("\n\nTEST WITH LOW PHOTON NUMBER AND NARROW WIDTH")
    # simulated response to be used
    photon_number = 10
    x_center = 0.6
    y_center = -0.45
    x_width = 0.1
    y_width = 0.1
    
    print(f"\33[0;49;36mx and y location used in simulation:\33[0;49;38m ({x_center}, {y_center})")
    sim = GaussianIonResponseSimulation(
        photon_number=photon_number,
        x_center=x_center,
        y_center=y_center,
        x_width=x_width,
        y_width=y_width
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
    result = grid_sweep_optimize(laser_syst = syst)
    x_result = result['x']
    y_result = result['y']    
    print(f"\33[0;49;36Ion location found with deviation\33[0;49;38m ({x_center-x_result}, {y_center-y_result}) ")
    
    ###### The following demonstrate the performance in an extreme case of
    ###### low photon number and narrow width much smaller than step size
    print("\n\nTEST WITH LOW PHOTON NUMBER AND VERY NARROW WIDTH")
    # simulated response to be used
    photon_number = 10
    x_center = 0.6
    y_center = -0.45
    x_width = 0.05
    y_width = 0.05
    
    print(f"\33[0;49;36mx and y location used in simulation:\33[0;49;38m ({x_center}, {y_center})")
    sim = GaussianIonResponseSimulation(
        photon_number=photon_number,
        x_center=x_center,
        y_center=y_center,
        x_width=x_width,
        y_width=y_width
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
    result = grid_sweep_optimize(laser_syst = syst)
    x_result = result['x']
    y_result = result['y']    
    print(f"\33[0;49;36Ion location found with deviation\33[0;49;38m ({x_center-x_result}, {y_center-y_result}) ")
    
    
    ###### Same parameter as before, but decrease step size
    print("\n\nAS ABOVE, BUT WITH SMALLER SWEEP STEP")
    # simulated response to be used
    photon_number = 10
    x_center = 0.6
    y_center = -0.45
    x_width = 0.05
    y_width = 0.05
    
    print(f"\33[0;49;36mx and y location used in simulation:\33[0;49;38m ({x_center}, {y_center})")
    sim = GaussianIonResponseSimulation(
        photon_number=photon_number,
        x_center=x_center,
        y_center=y_center,
        x_width=x_width,
        y_width=y_width
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
    result = grid_sweep_optimize(laser_syst = syst,step=0.02)
    x_result = result['x']
    y_result = result['y']    
    print(f"\33[0;49;36Ion location found with deviation ({x_center-x_result}, {y_center-y_result}) ")