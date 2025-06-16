#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: markjhku

Unit test using simulated Gaussian response
"""
import unittest
from laser_calibration.ion_response_simulation import GaussianIonResponseSimulation
from laser_calibration.laser_calibration_system import LaserCalibrationSystem

from laser_calibration.grid_sweep_optimize import grid_sweep_optimize

class LaserCalibrationTest(unittest.TestCase):
    
    def test_sim(self):
        # parameters:
        x_center = 0.1
        y_center = 0.2
        
        # simulated response to be used
        sim = GaussianIonResponseSimulation(
            photon_number=100,
            x_center=x_center,
            y_center=y_center,
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
        output = grid_sweep_optimize(laser_syst = syst,plot=False)
        
        # Check operating points are found within tolerance
        x_result_withitn_tolerance =  abs(output['x'] - x_center) < 0.05 
        y_result_withitn_tolerance = abs(output['y'] - y_center) < 0.05
        
        self.assertTrue(x_result_withitn_tolerance and y_result_withitn_tolerance)


if __name__ == "__main__":
    
    unittest.main()
