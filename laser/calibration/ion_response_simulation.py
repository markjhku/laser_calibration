#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  6 16:34:20 2025

@author: markjhku
"""

from scipy.stats import poisson
import numpy as np


class IonResponseSimulation():
    """
        photon_distribution: function that generates average photon number at x and y
        use_poisson_distribution: whether to generate photon number based on poisson distribution
        measurement_noise: instrument noise to the measurement
    """
        
    
    def __init__(self, photon_distribution, use_poisson_distribution: bool = True, measurement_noise: bool = 0):
        self._photon_distribution = photon_distribution
        self._use_poisson_distribution = use_poisson_distribution
        self._measurement_noise = measurement_noise


    def measure_ion_response(self,x: float,y: float):
        
        
        
        photon_number = self._photon_distribution(x,y)
        
        if self._use_poisson_distribution:
            photon_number = poisson.rvs(photon_number,size=1)[0]

        noise = int(np.random.normal(loc = 0, scale = self._measurement_noise))
        
        return photon_number + noise

class GaussianIonResponseSimulation(IonResponseSimulation):
    def __init__(self, photon_number: float, x_center: float, y_center: float, x_width: float, y_width: float, use_poisson_distribution: bool = True, measurement_noise: bool = 0):
        photon_distribution = lambda x,y: photon_number*np.exp(-(x-x_center)**2/x_width**2-(y-y_center)**2/y_width**2)
        super().__init__(photon_distribution = photon_distribution, use_poisson_distribution = use_poisson_distribution, measurement_noise = measurement_noise)