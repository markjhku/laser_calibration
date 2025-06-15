#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: markjhku
"""
from laser_calibration.mirror import Mirror


class LaserCalibrationSystem():
    
    """
        This provides a class for laser calibration system which combines
        mirrors and ion response measurement. Currently, up to two spatial 
        dimensions is supported.
        
        To instantiate, one has to supply `ion_response_function`, which is a 1D
        or 2D function that corresponds to the average-photon distribution 
        function at x and y.
        
        The following are the key methods:
            
        The `add_mirror` method allows one to add mirror to be associated
        with the laser calibration system.
        
        The `get_all_mirror_names` function gets all the names of the currently
        associated mirrors
        
        The `move_mirrors_and_measure` method move mirrors to specified 
        positions and perform measurement
        
        To use simulation mode, see, for examples such as
        `simulation_laser_calibration_system_1d.py`
    """
    def __init__(self, ion_response_function):

       self._ion_response_function = ion_response_function
       self._simulation = False
       self._mirror_set = {}
       self._simulation_mirror_set = []

    
    def add_mirror(self, mirror_name: str, mirror_object):
        
        """
            add a mirror to be associated with the laser calibraiton system.
            
            mirror_name: str, name of the mirror
            mirror_object: either a Mirror instance, a mirror control
            function handle, or None (for simulation purpose)
                
        """
        if mirror_name in self._mirror_set:
            m = "supplied mirror_name is already in the mirror set"
            raise ValueError(m)
        
        # if mirror_object is not a Mirror instance, it is assumed to be a 
        # mirror movement function. In this case, instantiate a Mirror instance
        
        if not isinstance(mirror_object, Mirror):
            mirror_object = Mirror(mirror_object)
        
        self._mirror_set[mirror_name] = mirror_object

    def get_all_mirror_names(self):
        """
            get all currently associated mirror names
                
        """
        
        return list(self._mirror_set.keys())

    def get_mirror_position(self, mirror_name: str):
        """
            Get position of a single mirror
            
            mirror_name: str, name of mirror whose position is to be returned

        """
        if mirror_name not in self._mirror_set:
            m = "mirror_name is not in the mirror set"
            raise ValueError(m)
        
        return self._mirror_set[mirror_name].position
    
    def move_mirror(self, mirror_name: str, position: float):
        """
            Move a single mirror

            mirror_name: str, name of mirror to be moved
            position: float, position to be moved to
        """
        if mirror_name not in self._mirror_set:
            m = "mirror_name is not in the mirror set"
            raise ValueError(m)
        
        self._mirror_set[mirror_name].position = position
    
    def batch_move_mirrors(self,**kwargs):
        """
            Batch move mirrors. Takes keyword arguments in the form of
            mirror_name = position.
            
        """        
        [self.move_mirror(mirror_name = key, position = value) for key, value in kwargs.items()]
        
    @property
    def simulation(self):
        return self._simulation
    
    @simulation.setter
    def simulation(self, is_simulation: bool):
        if not is_simulation and self._move_mirror_function is None:
            m = "if move_mirror_function is None, simulation has to True"
            raise AssertionError(m)
                    
        self._simulation = is_simulation        


    @property
    def simulation_mirror_set(self):
        return self._simulation_mirror_set
    
    @simulation_mirror_set.setter
    def simulation_mirror_set(self, mirror_set: list):

        if any(mirror not in self._mirror_set for mirror in mirror_set):
            m = "mirror_set must be a subset of all mirrors"
            raise ValueError(m)
            
        self._simulation_mirror_set = mirror_set               
        
    @property
    def ion_response_function(self):
        return self._ion_response_function
    
    @ion_response_function.setter
    def ion_response_function(self, ion_response_function):
        self._ion_response_function = ion_response_function
            
    def measure_ion_response(self):
        if self.simulation:
            
            args = [self.get_mirror_position(mirror) for mirror in self.simulation_mirror_set]
            return self._ion_response_function(*args)
        else:
            return self._ion_response_function()


    def move_mirrors_and_measure(self,**kwargs):
        """
            Batch move mirrors and perform measurement. 
            Takes keyword arguments in the form of mirror_name = position.
            
        """        
        self.batch_move_mirrors(**kwargs)
        return self.measure_ion_response()
