#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: markjhku
"""



class Mirror():
    
    """
        Class for mirror object. To instantiate, supply a `move_mirror_function`.
        `move_mirror_function` may be None for simulation mode
        
        The property `position` allows for moving to a new position and
        obtaining the position that was last set
        
        The property `move_mirror_function` points to the current
        `move_mirror_function` associated with the given Mirror object
    """
    def __init__(self, move_mirror_function = None):
       self._position = 0
  
       self._move_mirror_function = move_mirror_function

    def move_mirror_to_position(self,position: float | None = None):
        """
            moves mirror to position
            position: float can be between -1 to 1  
        """

        if position is not None:
            if abs(position) > 1:
                m = "position must be between -1 and 1"
                raise ValueError(m)
                
            if self._move_mirror_function is not None:
                self._move_mirror_function(position)

            self._position = position
                
    @property
    def position(self):

        return self._position
    
    @position.setter
    def position(self, value: float):
        self.move_mirror_to_position(position=value)
        self._position = value


    @property
    def move_mirror_function(self):
        
        return self._move_mirror_function
    
    @move_mirror_function.setter
    def move_mirror_function(self, move_mirror_function):
        self._move_mirror_function = move_mirror_function      
        
        if move_mirror_function is None:
            self.simulation = True
        
        