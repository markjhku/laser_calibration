#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: markjhku

This example demonstrates using grid_sweep_optimize_ND routine for 
N-dimensional calibration.
"""

from laser_calibration.ion_response_simulation import IonResponseSimulation
from laser_calibration.laser_calibration_system import LaserCalibrationSystem
import numpy as np
from laser_calibration.grid_sweep_optimize_ND import grid_sweep_optimize_ND

if __name__ == "__main__":
    # parameters
    photon_number = 100
    x1_center = 0.1
    x2_center = 0.2
    x1_width = 0.3
    x2_width = 0.4
    x3_center = -0.51
    x3_width = 0.21
    x4_center = -0.52
    x4_width = 0.12

    ########### 1 dimension case ###########
    
    print("1 dimension")
    # simulated response to be used
    
    photon_distribution = lambda x: photon_number*np.exp(-(x-x1_center)**2/x1_width**2)
    
    print(f"\33[0;49;36mlocation used in simulation:\33[0;49;38m ({x1_center})")
    sim = IonResponseSimulation(photon_distribution=photon_distribution)
    
    # instantiate a LaserCalibrationSystem class    
    syst = LaserCalibrationSystem(
        ion_response_function=sim.measure_ion_response
        )
    
    # add mirrors to the LaserCalibrationSystem object
    syst.add_mirror("x1", None)
    
    # the following two lines are needed for simulation mode
    syst.simulation = True
    syst.simulation_mirror_set = ["x1"]    
    
    # perform optimization of ion response to calibrate the system
    result = grid_sweep_optimize_ND(laser_syst = syst)
    x1_result = result['x1']

    print(f"\33[0;49;36Ion location found with deviation\33[0;49;38m ({x1_center-x1_result}) ")

    ########### 2 dimension case ###########    
    
    print("\n2 dimension")
    # simulated response to be used
    photon_distribution = lambda x,y: photon_number*np.exp(-(x-x1_center)**2/x1_width**2-(y-x2_center)**2/x2_width**2)
    
    print(f"\33[0;49;36mlocation used in simulation:\33[0;49;38m ({x1_center}, {x2_center})")
    sim = IonResponseSimulation(photon_distribution=photon_distribution)
    
    # instantiate a LaserCalibrationSystem class    
    syst = LaserCalibrationSystem(
        ion_response_function=sim.measure_ion_response
        )
    
    # add mirrors to the LaserCalibrationSystem object
    syst.add_mirror("x1", None)
    syst.add_mirror("x2", None) 

    
    # the following two lines are needed for simulation mode
    syst.simulation = True
    syst.simulation_mirror_set = ["x1","x2"]    
    
    # perform optimization of ion response to calibrate the system
    result = grid_sweep_optimize_ND(laser_syst = syst)
    x1_result = result['x1']
    x2_result = result['x2']    
    print(f"\33[0;49;36Ion location found with deviation\33[0;49;38m ({x1_center-x1_result}, {x2_center-x2_result}) ")
            
    ########### 3 dimension case ###########    
    
    print("\n3 dimension")
    # simulated response to be used
    photon_distribution = lambda x,y,z: photon_number*np.exp(-(x-x1_center)**2/x1_width**2-(y-x2_center)**2/x2_width**2-(z-x3_center)**2/x3_width**2)
    
    print(f"\33[0;49;36mlocation used in simulation:\33[0;49;38m ({x1_center}, {x2_center},{x3_center})")
    sim = IonResponseSimulation(photon_distribution=photon_distribution)
    
    # instantiate a LaserCalibrationSystem class    
    syst = LaserCalibrationSystem(
        ion_response_function=sim.measure_ion_response
        )
    
    # add mirrors to the LaserCalibrationSystem object
    syst.add_mirror("x1", None)
    syst.add_mirror("x2", None) 
    syst.add_mirror("x3", None)
    
    # the following two lines are needed for simulation mode
    syst.simulation = True
    syst.simulation_mirror_set = ["x1","x2","x3"]    
    
    # perform optimization of ion response to calibrate the system
    result = grid_sweep_optimize_ND(laser_syst = syst)
    x1_result = result['x1']
    x2_result = result['x2']    
    x3_result = result['x3']    
    print(f"\33[0;49;36Ion location found with deviation\33[0;49;38m ({x1_center-x1_result}, {x2_center-x2_result},{x3_center-x3_result}) ")
    
    ########### 4 dimension case ###########        
    print("\n4 dimension")
    # simulated response to be used
    photon_distribution = lambda x,y,z,t: photon_number*np.exp(-(x-x1_center)**2/x1_width**2-(y-x2_center)**2/x2_width**2-(z-x3_center)**2/x3_width**2-(t-x4_center)**2/x4_width**2)
    
    print(f"\33[0;49;36mlocation used in simulation:\33[0;49;38m ({x1_center}, {x2_center},{x3_center},{x4_center})")
    sim = IonResponseSimulation(photon_distribution=photon_distribution)
    
    # instantiate a LaserCalibrationSystem class    
    syst = LaserCalibrationSystem(
        ion_response_function=sim.measure_ion_response
        )
    
    # add mirrors to the LaserCalibrationSystem object
    syst.add_mirror("x1", None)
    syst.add_mirror("x2", None) 
    syst.add_mirror("x3", None)
    syst.add_mirror("x4", None)    
    
    # the following two lines are needed for simulation mode
    syst.simulation = True
    syst.simulation_mirror_set = ["x1","x2","x3","x4"]    
    
    # perform optimization of ion response to calibrate the system
    result = grid_sweep_optimize_ND(laser_syst = syst)
    x1_result = result['x1']
    x2_result = result['x2']    
    x3_result = result['x3']    
    x4_result = result['x4']        
    print(f"\33[0;49;36Ion location found with deviation\33[0;49;38m ({x1_center-x1_result}, {x2_center-x2_result},{x3_center-x3_result},{x4_center-x4_result}) ")
        