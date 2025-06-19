#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: markjhku
"""

from scipy.stats import poisson
import numpy as np


class IonResponseSimulation():
    """
        This provides a class for generating photon response based on a generic
        average-photon distribution. 
        
        To instantiate, one has to supply `photon_distribution`, which is an 
        N-dimensional function that corresponds to the average-photon 
        distribution function
        
        To obtain a measurement, one uses `measure_ion_response` function which
        is an N-dimensional function
        
        Options:        
        use_poisson_distribution: whether to generate photon number based on poisson distribution
        measurement_noise: instrument noise to the measurement
    """
        
    
    def __init__(self, photon_distribution, use_poisson_distribution: bool = True, measurement_noise: bool = 0):
        self._photon_distribution = photon_distribution
        self._use_poisson_distribution = use_poisson_distribution
        self._measurement_noise = measurement_noise



    def measure_ion_response(self,*args):
        """
            This generates ion response at a location x=args[0], y=args[1],...
            
            args: list or tuple of float
        """        
        
        
        photon_number = self._photon_distribution(*args)
        
        if self._use_poisson_distribution:
            photon_number = poisson.rvs(photon_number,size=1)[0]

        noise = int(np.random.normal(loc = 0, scale = self._measurement_noise))
        
        return photon_number + noise
    

class GaussianIonResponseSimulation(IonResponseSimulation):
    """
        This provides a class for generating photon response with Gaussian 
        distribution. To instantiate, provide the parameters associated
        with a 2D Gaussian distribution
        
        photon_number: float
        x_center: float
        y_center: float
        x_width: float
        y_width: float
        
        Options:        
        use_poisson_distribution: whether to generate photon number based on poisson distribution
        measurement_noise: instrument noise to the measurement

        
    """
    def __init__(self, photon_number: float, x_center: float, y_center: float, x_width: float, y_width: float, use_poisson_distribution: bool = True, measurement_noise: bool = 0):
        photon_distribution = lambda x,y: photon_number*np.exp(-(x-x_center)**2/x_width**2-(y-y_center)**2/y_width**2)
        super().__init__(photon_distribution = photon_distribution, use_poisson_distribution = use_poisson_distribution, measurement_noise = measurement_noise)